"""Funkcje pomocnicze, konwersje jednostek oraz baza czynników chłodniczych."""

from dataclasses import dataclass
from typing import Dict
import CoolProp.CoolProp as CP


@dataclass(frozen=True)
class RefrigerantInfo:
    """Metadane czynnika chłodniczego."""

    code: str
    name: str
    chemical_formula: str
    safety_group: str
    gwp: int
    description: str


REFRIGERANTS: Dict[str, RefrigerantInfo] = {
    "R290": RefrigerantInfo(
        code="R290",
        name="R290 (Propan)",
        chemical_formula="C3H8",
        safety_group="A3",
        gwp=3,
        description="Naturalny węglowodór o bardzo niskim GWP i doskonałych własnościach termodynamicznych.",
    ),
    "R32": RefrigerantInfo(
        code="R32",
        name="R32 (Difluorometan)",
        chemical_formula="CH2F2",
        safety_group="A2L",
        gwp=675,
        description="Popularny czynnik w nowoczesnych pompach ciepła powietrze-woda i klimatyzatorach.",
    ),
    "R134a": RefrigerantInfo(
        code="R134a",
        name="R134a (Tetrafluoroetan)",
        chemical_formula="CF3CH2F",
        safety_group="A1",
        gwp=1430,
        description="Klasyczny czynnik HFC stosowany w średnio- i wysokotemperaturowych układach.",
    ),
    "R410A": RefrigerantInfo(
        code="R410A",
        name="R410A (Mieszanina R32/R125)",
        chemical_formula="CH2F2 / CHF2CF3 (50/50%)",
        safety_group="A1",
        gwp=2088,
        description="Zeotropowa mieszanina o wysokim ciśnieniu roboczym, szeroko stosowana w starszych układach.",
    ),
    "R1234yf": RefrigerantInfo(
        code="R1234yf",
        name="R1234yf (Tetrafluoropropen)",
        chemical_formula="CF3CF=CH2",
        safety_group="A2L",
        gwp=4,
        description="Syntetyczny czynnik z grupy HFO o ultraniskim współczynniku GWP, zamiennik dla R134a.",
    ),
    "R600a": RefrigerantInfo(
        code="R600a",
        name="R600a (Izobutan)",
        chemical_formula="C4H10",
        safety_group="A3",
        gwp=3,
        description="Naturalny węglowodór o niskich ciśnieniach roboczych i wysokiej temperaturze krytycznej.",
    ),
    "R717": RefrigerantInfo(
        code="R717",
        name="R717 (Amoniak)",
        chemical_formula="NH3",
        safety_group="B2L",
        gwp=0,
        description="Przemysłowy czynnik naturalny o bardzo wysokim cieple parowania.",
    ),
}


def c_to_k(temp_c: float) -> float:
    """Konwertuje temperaturę z °C na K."""
    return temp_c + 273.15


def k_to_c(temp_k: float) -> float:
    """Konwertuje temperaturę z K na °C."""
    return temp_k - 273.15


def pa_to_bar(p_pa: float) -> float:
    """Konwertuje ciśnienie z Pa na bar."""
    return p_pa / 1e5


def bar_to_pa(p_bar: float) -> float:
    """Konwertuje ciśnienie z bar na Pa."""
    return p_bar * 1e5


def get_fluid_limits(fluid: str) -> Dict[str, float]:
    """Zwraca parametry punktu krytycznego i potrójnego dla wybranego czynnika."""
    t_crit_k = CP.PropsSI("Tcrit", fluid)
    p_crit_pa = CP.PropsSI("pcrit", fluid)
    t_min_k = CP.PropsSI("Tmin", fluid)
    return {
        "T_crit_C": k_to_c(t_crit_k),
        "p_crit_bar": pa_to_bar(p_crit_pa),
        "T_min_C": k_to_c(t_min_k),
    }


def validate_cycle_inputs(
    fluid: str,
    t_evap_c: float,
    t_cond_c: float,
    superheat_k: float,
    subcooling_k: float,
    eta_s: float,
    q_cond_kw: float,
) -> None:
    """Waliduje fizyczną poprawność parametrów wejściowych obiegu podkrytycznego."""
    if fluid not in REFRIGERANTS:
        raise ValueError(
            f"Nieobsługiwany czynnik '{fluid}'. Dostępne: {list(REFRIGERANTS.keys())}"
        )

    limits = get_fluid_limits(fluid)
    t_crit_c = limits["T_crit_C"]
    t_min_c = limits["T_min_C"]

    if t_evap_c <= t_min_c + 1.0:
        raise ValueError(
            f"Temperatura parowania ({t_evap_c:.1f} °C) jest zbyt bliska minimalnej "
            f"temperaturze modelu dla {fluid} ({t_min_c:.1f} °C)."
        )

    if t_cond_c >= t_crit_c - 2.0:
        raise ValueError(
            f"Temperatura skraplania ({t_cond_c:.1f} °C) przekracza bezpieczny limit "
            f"obiegu podkrytycznego dla {fluid} (T_crit = {t_crit_c:.1f} °C)."
        )

    if t_evap_c >= t_cond_c - 2.0:
        raise ValueError(
            f"Temperatura parowania ({t_evap_c:.1f} °C) musi być niższa od "
            f"temperatury skraplania ({t_cond_c:.1f} °C) o co najmniej 2 K."
        )

    if superheat_k < 0.0 or superheat_k > 40.0:
        raise ValueError(
            f"Przegrzanie ({superheat_k:.1f} K) musi mieścić się w przedziale [0, 40] K."
        )

    if subcooling_k < 0.0 or subcooling_k > 35.0:
        raise ValueError(
            f"Dochłodzenie ({subcooling_k:.1f} K) musi mieścić się w przedziale [0, 35] K."
        )

    if t_cond_c - subcooling_k <= t_evap_c:
        raise ValueError(
            "Temperatura po dochłodzeniu za skraplaczem nie może być niższa niż temperatura parowania."
        )

    if not (0.1 <= eta_s <= 1.0):
        raise ValueError(
            f"Sprawność izentropowa sprężarki ({eta_s:.2f}) musi należeć do przedziału [0.1, 1.0]."
        )

    if q_cond_kw <= 0.0:
        raise ValueError(
            f"Moc grzewcza skraplacza ({q_cond_kw:.2f} kW) musi być dodatnia."
        )
