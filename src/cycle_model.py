"""Model jednostopniowego obiegu pompy ciepła oparty na bibliotece TESPy i CoolProp."""

from dataclasses import dataclass
from typing import Dict, Any, Tuple
import logging
import pandas as pd
import CoolProp.CoolProp as CP
from tespy.networks import Network
from tespy.components import (
    CycleCloser,
    Compressor,
    SimpleHeatExchanger,
    Valve,
)
from tespy.connections import Connection

from src.utils import (
    c_to_k,
    pa_to_bar,
    validate_cycle_inputs,
)

# Wyciszenie nadmiarowych logów TESPy podczas symulacji i optymalizacji
logging.getLogger("tespy").setLevel(logging.ERROR)
logging.getLogger("TESPyLogger").setLevel(logging.ERROR)

# Cache sieci TESPy dla poszczególnych czynników chłodniczych (przyspiesza wielokrotne obliczenia SciPy i Streamlit)
_NETWORK_CACHE: Dict[str, Tuple[Network, Compressor, SimpleHeatExchanger, Valve, SimpleHeatExchanger, Connection, Connection, Connection, Connection]] = {}


def _get_or_create_network(
    fluid: str,
) -> Tuple[Network, Compressor, SimpleHeatExchanger, Valve, SimpleHeatExchanger, Connection, Connection, Connection, Connection]:
    """Zwraca zainicjalizowaną sieć TESPy dla danego czynnika lub tworzy nową."""
    if fluid in _NETWORK_CACHE:
        return _NETWORK_CACHE[fluid]

    nw = Network(iterinfo=False)
    nw.units.set_defaults(
        temperature="degC",
        pressure="bar",
        enthalpy="kJ/kg",
        mass_flow="kg/s",
        heat="W",
        power="W",
    )

    cc = CycleCloser("CycleCloser")
    comp = Compressor("Sprężarka")
    cond = SimpleHeatExchanger("Skraplacz")
    valve = Valve("Zawór dławiący")
    evap = SimpleHeatExchanger("Parownik")

    c0 = Connection(evap, "out1", cc, "in1", label="0_evap_to_cc")
    c1 = Connection(cc, "out1", comp, "in1", label="1_ssanie_sprezarki")
    c2 = Connection(comp, "out1", cond, "in1", label="2_tloczenie_sprezarki")
    c3 = Connection(cond, "out1", valve, "in1", label="3_za_skraplaczem")
    c4 = Connection(valve, "out1", evap, "in1", label="4_za_zaworem")

    nw.add_conns(c0, c1, c2, c3, c4)

    cond.set_attr(pr=1.0)
    evap.set_attr(pr=1.0)
    c1.set_attr(fluid={fluid: 1.0})

    _NETWORK_CACHE[fluid] = (nw, comp, cond, valve, evap, c1, c2, c3, c4)
    return _NETWORK_CACHE[fluid]


@dataclass
class CycleInput:
    """Parametry wejściowe jednostopniowego obiegu pompy ciepła."""

    fluid: str = "R290"
    t_evap_c: float = 0.0
    t_cond_c: float = 45.0
    superheat_k: float = 5.0
    subcooling_k: float = 5.0
    eta_s: float = 0.78
    q_cond_kw: float = 10.0


@dataclass
class CycleResult:
    """Wyniki obliczeń obiegu pompy ciepła."""

    cop_heating: float
    cop_cooling: float
    cop_carnot: float
    eta_exergetic: float
    q_cond_kw: float
    q_evap_kw: float
    p_comp_kw: float
    mass_flow_kg_s: float
    pressure_ratio: float
    p_evap_bar: float
    p_cond_bar: float
    v_dot_suction_m3_h: float
    energy_balance_error_w: float
    state_points_df: pd.DataFrame
    plot_data: Dict[str, Any]


class HeatPumpCycle:
    """Symulator jednostopniowego obiegu sprężarkowej pompy ciepła w TESPy."""

    def __init__(self, params: CycleInput) -> None:
        self.params = params
        validate_cycle_inputs(
            fluid=params.fluid,
            t_evap_c=params.t_evap_c,
            t_cond_c=params.t_cond_c,
            superheat_k=params.superheat_k,
            subcooling_k=params.subcooling_k,
            eta_s=params.eta_s,
            q_cond_kw=params.q_cond_kw,
        )

    def solve(self) -> CycleResult:
        """Buduje i rozwiązuje sieć termodynamiczną TESPy dla zadanych parametrów."""
        p = self.params
        fluid = p.fluid

        # 1. Wyznaczenie ciśnień nasycenia i stanów granicznych przy użyciu CoolProp
        t_evap_k = c_to_k(p.t_evap_c)
        t_cond_k = c_to_k(p.t_cond_c)

        p_evap_pa = CP.PropsSI("P", "T", t_evap_k, "Q", 1.0, fluid)
        p_cond_pa = CP.PropsSI("P", "T", t_cond_k, "Q", 0.0, fluid)

        p_evap_bar = pa_to_bar(p_evap_pa)
        p_cond_bar = pa_to_bar(p_cond_pa)

        # Stan 1: Wylot z parownika / wlot do sprężarki (para przegrzana lub nasycona x=1)
        t_1_c = p.t_evap_c + p.superheat_k
        t_1_k = c_to_k(t_1_c)
        if p.superheat_k > 1e-4:
            h_1_j_kg = CP.PropsSI("H", "P", p_evap_pa, "T", t_1_k, fluid)
        else:
            h_1_j_kg = CP.PropsSI("H", "P", p_evap_pa, "Q", 1.0, fluid)

        # Stan 3: Wylot ze skraplacza / wlot do zaworu dławiącego (ciecz dochłodzona lub nasycona x=0)
        t_3_c = p.t_cond_c - p.subcooling_k
        t_3_k = c_to_k(t_3_c)
        if p.subcooling_k > 1e-4:
            h_3_j_kg = CP.PropsSI("H", "P", p_cond_pa, "T", t_3_k, fluid)
        else:
            h_3_j_kg = CP.PropsSI("H", "P", p_cond_pa, "Q", 0.0, fluid)

        # 2. Pobranie lub utworzenie sieci TESPy i aktualizacja parametrów
        nw, comp, cond, valve, evap, c1, c2, c3, c4 = _get_or_create_network(fluid)

        cond.set_attr(Q=-p.q_cond_kw * 1e3)
        comp.set_attr(eta_s=p.eta_s)

        c1.set_attr(p=p_evap_bar, h=h_1_j_kg / 1e3)
        c2.set_attr(p=p_cond_bar)
        c3.set_attr(h=h_3_j_kg / 1e3)

        # 3. Rozwiązanie układu równań nieliniowych TESPy
        nw.solve(mode="design")

        if not nw.converged:
            # Jeśli sieć z cache nie zbiegła, zresetuj instancję sieci dla tego czynnika i spróbuj ponownie
            _NETWORK_CACHE.pop(fluid, None)
            nw, comp, cond, valve, evap, c1, c2, c3, c4 = _get_or_create_network(fluid)
            cond.set_attr(Q=-p.q_cond_kw * 1e3)
            comp.set_attr(eta_s=p.eta_s)
            c1.set_attr(p=p_evap_bar, h=h_1_j_kg / 1e3)
            c2.set_attr(p=p_cond_bar)
            c3.set_attr(h=h_3_j_kg / 1e3)
            nw.solve(mode="design")
            if not nw.converged:
                raise RuntimeError(
                    "Rozwiązanie sieci TESPy nie osiągnęło zbieżności dla zadanych parametrów."
                )

        # 4. Odczyt wyników z komponentów i połączeń
        q_cond_kw = abs(cond.Q.val) / 1e3
        q_evap_kw = evap.Q.val / 1e3
        p_comp_kw = comp.P.val / 1e3
        mass_flow = c1.m.val

        cop_heating = q_cond_kw / p_comp_kw
        cop_cooling = q_evap_kw / p_comp_kw
        cop_carnot = t_cond_k / (t_cond_k - t_evap_k)
        eta_exergetic = cop_heating / cop_carnot
        pressure_ratio = p_cond_bar / p_evap_bar

        # Bilans energii: |Q_cond| - (Q_evap + P_comp) [W]
        energy_balance_error_w = abs(cond.Q.val) - (evap.Q.val + comp.P.val)

        # Zestawienie stanów w 4 głównych węzłach obiegu
        connections = [
            ("1", "Wlot do sprężarki (para przegrzana)", c1),
            ("2", "Wylot ze sprężarki (para gorąca)", c2),
            ("3", "Wylot ze skraplacza (ciecz dochłodzona)", c3),
            ("4", "Wlot do parownika (mieszanina dwufazowa)", c4),
        ]

        rows = []
        for pt_id, desc, conn in connections:
            p_pa = conn.p.val * 1e5
            h_j_kg = conn.h.val * 1e3
            t_c = conn.T.val
            s_kj_kgk = CP.PropsSI("S", "P", p_pa, "H", h_j_kg, fluid) / 1e3
            rho_kg_m3 = CP.PropsSI("D", "P", p_pa, "H", h_j_kg, fluid)
            q_phase = CP.PropsSI("Q", "P", p_pa, "H", h_j_kg, fluid)
            vapor_quality = q_phase if 0.0 <= q_phase <= 1.0 else None

            rows.append(
                {
                    "Punkt": pt_id,
                    "Opis stanu": desc,
                    "p [bar]": round(conn.p.val, 3),
                    "T [°C]": round(t_c, 2),
                    "h [kJ/kg]": round(conn.h.val, 2),
                    "s [kJ/(kg·K)]": round(s_kj_kgk, 4),
                    "x [-]": round(vapor_quality, 3) if vapor_quality is not None else "Jednofazowy",
                    "ρ [kg/m³]": round(rho_kg_m3, 2),
                }
            )

        state_df = pd.DataFrame(rows)

        # Objętościowy strumień zasysania sprężarki [m³/h] w punkcie 1
        rho_1 = CP.PropsSI("D", "P", c1.p.val * 1e5, "H", c1.h.val * 1e3, fluid)
        v_dot_suction_m3_h = (mass_flow / rho_1) * 3600.0

        # Punkty pośrednie nasycenia dla dokładnego rysowania obiegu na wykresach T-s oraz log(p)-h:
        h_cond_vap = CP.PropsSI("H", "P", p_cond_pa, "Q", 1.0, fluid) / 1e3
        s_cond_vap = CP.PropsSI("S", "P", p_cond_pa, "Q", 1.0, fluid) / 1e3
        h_cond_liq = CP.PropsSI("H", "P", p_cond_pa, "Q", 0.0, fluid) / 1e3
        s_cond_liq = CP.PropsSI("S", "P", p_cond_pa, "Q", 0.0, fluid) / 1e3
        h_evap_vap = CP.PropsSI("H", "P", p_evap_pa, "Q", 1.0, fluid) / 1e3
        s_evap_vap = CP.PropsSI("S", "P", p_evap_pa, "Q", 1.0, fluid) / 1e3

        plot_data = {
            "fluid": fluid,
            "p_evap_bar": p_evap_bar,
            "p_cond_bar": p_cond_bar,
            "t_evap_c": p.t_evap_c,
            "t_cond_c": p.t_cond_c,
            "p_bar": [c1.p.val, c2.p.val, c3.p.val, c4.p.val],
            "T_c": [c1.T.val, c2.T.val, c3.T.val, c4.T.val],
            "h_kj_kg": [c1.h.val, c2.h.val, c3.h.val, c4.h.val],
            "s_kj_kgk": [
                CP.PropsSI("S", "P", c.p.val * 1e5, "H", c.h.val * 1e3, fluid) / 1e3
                for c in (c1, c2, c3, c4)
            ],
            "path_p_bar": [
                c1.p.val,
                c2.p.val,
                p_cond_bar,
                p_cond_bar,
                c3.p.val,
                c4.p.val,
                p_evap_bar,
                c1.p.val,
            ],
            "path_T_c": [
                c1.T.val,
                c2.T.val,
                p.t_cond_c,
                p.t_cond_c,
                c3.T.val,
                c4.T.val,
                p.t_evap_c,
                c1.T.val,
            ],
            "path_h_kj_kg": [
                c1.h.val,
                c2.h.val,
                h_cond_vap,
                h_cond_liq,
                c3.h.val,
                c4.h.val,
                h_evap_vap,
                c1.h.val,
            ],
            "path_s_kj_kgk": [
                CP.PropsSI("S", "P", c1.p.val * 1e5, "H", c1.h.val * 1e3, fluid) / 1e3,
                CP.PropsSI("S", "P", c2.p.val * 1e5, "H", c2.h.val * 1e3, fluid) / 1e3,
                s_cond_vap,
                s_cond_liq,
                CP.PropsSI("S", "P", c3.p.val * 1e5, "H", c3.h.val * 1e3, fluid) / 1e3,
                CP.PropsSI("S", "P", c4.p.val * 1e5, "H", c4.h.val * 1e3, fluid) / 1e3,
                s_evap_vap,
                CP.PropsSI("S", "P", c1.p.val * 1e5, "H", c1.h.val * 1e3, fluid) / 1e3,
            ],
        }

        return CycleResult(
            cop_heating=cop_heating,
            cop_cooling=cop_cooling,
            cop_carnot=cop_carnot,
            eta_exergetic=eta_exergetic,
            q_cond_kw=q_cond_kw,
            q_evap_kw=q_evap_kw,
            p_comp_kw=p_comp_kw,
            mass_flow_kg_s=mass_flow,
            pressure_ratio=pressure_ratio,
            p_evap_bar=p_evap_bar,
            p_cond_bar=p_cond_bar,
            v_dot_suction_m3_h=v_dot_suction_m3_h,
            energy_balance_error_w=energy_balance_error_w,
            state_points_df=state_df,
            plot_data=plot_data,
        )
