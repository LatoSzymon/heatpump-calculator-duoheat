"""Funkcje pomocnicze, konwersje jednostek, presety scenariuszy oraz baza czynników chłodniczych."""

from dataclasses import dataclass
from typing import Dict
import CoolProp.CoolProp as CP

from src.i18n import normalize_lang, t


@dataclass(frozen=True)
class RefrigerantInfo:
    """Metadane czynnika chłodniczego."""

    code: str
    name: str
    chemical_formula: str
    safety_group: str
    gwp: int
    description: str


@dataclass(frozen=True)
class ScenarioPreset:
    """Gotowy scenariusz pracy pompy ciepła do celów edukacyjnych."""

    id: str
    label: str
    fluid: str
    t_evap_c: float
    t_cond_c: float
    superheat_k: float
    subcooling_k: float
    eta_s: float
    q_cond_kw: float
    explanation: str


REFRIGERANTS: Dict[str, RefrigerantInfo] = {
    "R290": RefrigerantInfo(
        code="R290",
        name="R290 (Propan)",
        chemical_formula="C3H8",
        safety_group="A3",
        gwp=3,
        description="Naturalny węglowodór o bardzo niskim GWP i doskonałych własnościach termodynamicznych (wysoka palność A3).",
    ),
    "R32": RefrigerantInfo(
        code="R32",
        name="R32 (Difluorometan)",
        chemical_formula="CH2F2",
        safety_group="A2L",
        gwp=675,
        description="Popularny czynnik w nowoczesnych pompach ciepła powietrze-woda i klimatyzatorach (niska palność A2L).",
    ),
    "R134a": RefrigerantInfo(
        code="R134a",
        name="R134a (Tetrafluoroetan)",
        chemical_formula="CF3CH2F",
        safety_group="A1",
        gwp=1430,
        description="Klasyczny czynnik HFC stosowany w średnio- i wysokotemperaturowych układach (niepalny A1).",
    ),
    "R410A": RefrigerantInfo(
        code="R410A",
        name="R410A (Mieszanina R32/R125)",
        chemical_formula="CH2F2 / CHF2CF3 (50/50%)",
        safety_group="A1",
        gwp=2088,
        description="Bliskoazeotropowa mieszanina o wysokim ciśnieniu roboczym, szeroko stosowana w starszych układach.",
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
        description="Przemysłowy czynnik naturalny o bardzo wysokim cieple parowania i wysokiej temperaturze tłoczenia.",
    ),
}


SCENARIO_PRESETS: Dict[str, ScenarioPreset] = {
    "air_floor_spring": ScenarioPreset(
        id="air_floor_spring",
        label="Powietrzna PC + podłogówka (wiosna/jesień, +7°C)",
        fluid="R290",
        t_evap_c=2.0,
        t_cond_c=35.0,
        superheat_k=5.0,
        subcooling_k=4.0,
        eta_s=0.78,
        q_cond_kw=10.0,
        explanation=(
            "Optymalne warunki pracy: mała różnica temperatur między powietrzem zewnętrznym (+7°C, parowanie +2°C) "
            "a ogrzewaniem podłogowym (~30–35°C) zapewnia bardzo wysoki współczynnik COP."
        ),
    ),
    "air_radiators_winter": ScenarioPreset(
        id="air_radiators_winter",
        label="Powietrzna PC + grzejniki (mroźna zima, -7°C)",
        fluid="R290",
        t_evap_c=-12.0,
        t_cond_c=55.0,
        superheat_k=6.0,
        subcooling_k=5.0,
        eta_s=0.74,
        q_cond_kw=10.0,
        explanation=(
            "Trudne warunki zimowe: duży skok temperatury (ΔT = 67 K) między zimnym powietrzem (-7°C, parowanie -12°C) "
            "a gorącymi grzejnikami (55°C) zmusza sprężarkę do cięższej pracy i wyraźnie obniża COP."
        ),
    ),
    "ground_floor": ScenarioPreset(
        id="ground_floor",
        label="Gruntowa PC + podłogówka (stabilne źródło)",
        fluid="R32",
        t_evap_c=0.0,
        t_cond_c=35.0,
        superheat_k=5.0,
        subcooling_k=5.0,
        eta_s=0.80,
        q_cond_kw=12.0,
        explanation=(
            "Grunt na głębokości kilku metrów ma stabilną temperaturę przez cały rok, dzięki czemu parownik "
            "pracuje stabilnie w okolicach 0°C nawet w środku zimy."
        ),
    ),
    "dhw_heating": ScenarioPreset(
        id="dhw_heating",
        label="Grzanie ciepłej wody użytkowej (CWU 55°C)",
        fluid="R290",
        t_evap_c=2.0,
        t_cond_c=60.0,
        superheat_k=5.0,
        subcooling_k=5.0,
        eta_s=0.75,
        q_cond_kw=8.0,
        explanation=(
            "Podgrzewanie wody w zasobniku CWU do 55°C wymaga wysokiej temperatury skraplania (~60°C), "
            "co podnosi ciśnienie tłoczenia i obniża sprawność w porównaniu z ogrzewaniem podłogowym."
        ),
    ),
}


REFRIGERANTS_EN: Dict[str, Dict[str, str]] = {
    "R290": {
        "name": "R290 (Propane)",
        "description": "Natural hydrocarbon with ultra-low GWP and excellent thermodynamic properties (high flammability A3).",
    },
    "R32": {
        "name": "R32 (Difluoromethane)",
        "description": "Popular refrigerant in modern air-to-water heat pumps and air conditioners (mildly flammable A2L).",
    },
    "R134a": {
        "name": "R134a (Tetrafluoroethane)",
        "description": "Classic HFC refrigerant used in medium- and high-temperature systems (non-flammable A1).",
    },
    "R410A": {
        "name": "R410A (R32/R125 Blend)",
        "description": "Near-azeotropic blend with high operating pressure, widely used in older systems.",
    },
    "R1234yf": {
        "name": "R1234yf (Tetrafluoropropene)",
        "description": "Synthetic HFO refrigerant with ultra-low GWP, drop-in replacement direction for R134a.",
    },
    "R600a": {
        "name": "R600a (Isobutane)",
        "description": "Natural hydrocarbon with low operating pressures and high critical temperature.",
    },
    "R717": {
        "name": "R717 (Ammonia)",
        "description": "Industrial natural refrigerant with very high latent heat and high discharge temperature.",
    },
}

SCENARIO_PRESETS_EN: Dict[str, Dict[str, str]] = {
    "air_floor_spring": {
        "label": "Air-source HP + underfloor heating (spring/autumn, +7°C)",
        "explanation": (
            "Optimal operating conditions: small temperature lift between outdoor air (+7°C, evaporation +2°C) "
            "and underfloor heating (~30–35°C) yields a very high COP."
        ),
    },
    "air_radiators_winter": {
        "label": "Air-source HP + radiators (cold winter, -7°C)",
        "explanation": (
            "Harsh winter conditions: large temperature lift (ΔT = 67 K) between cold outdoor air (-7°C, evaporation -12°C) "
            "and hot radiators (55°C) forces the compressor to work harder and noticeably lowers COP."
        ),
    },
    "ground_floor": {
        "label": "Ground-source HP + underfloor heating (stable source)",
        "explanation": (
            "Ground at a few meters depth maintains a stable temperature year-round, allowing the evaporator "
            "to operate steadily around 0°C even in mid-winter."
        ),
    },
    "dhw_heating": {
        "label": "Domestic hot water heating (DHW 55°C)",
        "explanation": (
            "Heating domestic hot water tank to 55°C requires a high condensation temperature (~60°C), "
            "raising discharge pressure and lowering efficiency compared to underfloor heating."
        ),
    },
}


def get_refrigerant_text(code: str, lang: str = "pl") -> Dict[str, str]:
    """Zwraca zlokalizowaną nazwę i opis czynnika chłodniczego."""
    ref = REFRIGERANTS[code]
    if normalize_lang(lang) == "en" and code in REFRIGERANTS_EN:
        return REFRIGERANTS_EN[code]
    return {"name": ref.name, "description": ref.description}


def get_preset_text(preset_id: str, lang: str = "pl") -> Dict[str, str]:
    """Zwraca zlokalizowaną etykietę i opis scenariusza."""
    preset = SCENARIO_PRESETS[preset_id]
    if normalize_lang(lang) == "en" and preset_id in SCENARIO_PRESETS_EN:
        return SCENARIO_PRESETS_EN[preset_id]
    return {"label": preset.label, "explanation": preset.explanation}


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
    lang: str = "pl",
) -> None:
    """Waliduje fizyczną poprawność parametrów wejściowych obiegu podkrytycznego."""
    if fluid not in REFRIGERANTS:
        raise ValueError(
            t("val_bad_fluid", lang, fluid=fluid, avail=list(REFRIGERANTS.keys()))
        )

    limits = get_fluid_limits(fluid)
    t_crit_c = limits["T_crit_C"]
    t_min_c = limits["T_min_C"]

    if t_evap_c <= t_min_c + 1.0:
        raise ValueError(
            t("val_t_evap_min", lang, t_evap=t_evap_c, fluid=fluid, t_min=t_min_c)
        )

    if t_cond_c >= t_crit_c - 2.0:
        raise ValueError(
            t("val_t_cond_crit", lang, t_cond=t_cond_c, fluid=fluid, t_crit=t_crit_c)
        )

    if t_evap_c >= t_cond_c - 2.0:
        raise ValueError(
            t("val_t_evap_ge_cond", lang, t_evap=t_evap_c, t_cond=t_cond_c)
        )

    if superheat_k < 0.0 or superheat_k > 40.0:
        raise ValueError(t("val_superheat_range", lang, sh=superheat_k))

    if subcooling_k < 0.0 or subcooling_k > 35.0:
        raise ValueError(t("val_subcool_range", lang, sc=subcooling_k))

    if t_cond_c - subcooling_k <= t_evap_c:
        raise ValueError(t("val_subcool_below_evap", lang))

    if not (0.1 <= eta_s <= 1.0):
        raise ValueError(t("val_eta_range", lang, eta=eta_s))

    if q_cond_kw <= 0.0:
        raise ValueError(t("val_q_cond_pos", lang, q=q_cond_kw))
