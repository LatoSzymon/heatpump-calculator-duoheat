"""Dane merytoryczne lekcji dla podstrony Edukacja (PL / EN)."""

from dataclasses import dataclass
from typing import Dict, List

from src.i18n import normalize_lang


@dataclass(frozen=True)
class Lesson:
    """Lekcja edukacyjna: teoria oraz identyfikator ilustracji obliczeniowej."""

    id: str
    title: Dict[str, str]
    subtitle: Dict[str, str]
    theory: Dict[str, str]
    lab_type: str


LESSONS: List[Lesson] = [
    Lesson(
        id="evap_superheat",
        title={
            "pl": "1. Parownik i przegrzanie pary (ΔT_sh)",
            "en": "1. Evaporator & Vapor Superheat (ΔT_sh)",
        },
        subtitle={
            "pl": "Element: Parownik (4 → 1) | Współczynnik: Przegrzanie ΔT_sh [K]",
            "en": "Component: Evaporator (4 → 1) | Coefficient: Superheat ΔT_sh [K]",
        },
        theory={
            "pl": (
                "**Parownik** to wymiennik ciepła po stronie niskiego ciśnienia ($p_1$). Czynnik wpływa do niego jako zimna "
                "mieszanina cieczy i pary ($T_4 = T_{evap}$), wrze odbierając ciepło $Q_{evap}$ z powietrza lub gruntu, a następnie "
                "jest dodatkowo podgrzewany ponad temperaturę wrzenia o wartość **przegrzania** $\\Delta T_{sh}$:\n\n"
                "$$T_1 = T_{evap} + \\Delta T_{sh}$$\n\n"
                "- **Dlaczego przegrzanie jest kluczowe?** Chroni sprężarkę przed zassaniem kropel cieczy (tzw. *uderzeniem hydraulicznym*, gdyż ciecz jest nieściśliwa).\n"
                "- **Jaki jest kompromis?** Zbyt duże $\\Delta T_{sh}$ (np. > 12 K) nie zwiększa znacząco efektu grzewczego, a podnosi temperaturę tłoczenia sprężarki $T_2$ i zmniejsza gęstość zasysanej pary."
            ),
            "en": (
                "The **evaporator** is the low-pressure heat exchanger ($p_1$). Refrigerant enters as a cold two-phase "
                "mixture ($T_4 = T_{evap}$), boils while absorbing heat $Q_{evap}$ from ambient air or ground, and is then "
                "heated further above its boiling point by the **superheat** $\\Delta T_{sh}$:\n\n"
                "$$T_1 = T_{evap} + \\Delta T_{sh}$$\n\n"
                "- **Why is superheat critical?** It prevents liquid droplets from entering the compressor (avoiding *liquid slugging*, since liquids are incompressible).\n"
                "- **What is the trade-off?** Excessive $\\Delta T_{sh}$ (e.g., > 12 K) adds little useful heat, while raising compressor discharge temperature $T_2$ and lowering suction vapor density."
            ),
        },
        lab_type="superheat_lab",
    ),
    Lesson(
        id="comp_eta",
        title={
            "pl": "2. Sprężarka, spręż (Π) i sprawność izentropowa (η_s)",
            "en": "2. Compressor, Pressure Ratio (Π) & Isentropic Efficiency (η_s)",
        },
        subtitle={
            "pl": "Element: Sprężarka (1 → 2) | Współczynniki: Π = p₂/p₁ oraz η_s [-]",
            "en": "Component: Compressor (1 → 2) | Coefficients: Π = p₂/p₁ & η_s [-]",
        },
        theory={
            "pl": (
                "**Sprężarka** to serce pompy ciepła napędzane energią elektryczną ($P_{el}$). Podnosi ciśnienie pary z $p_1$ do $p_2$, "
                "dzięki czemu jej temperatura gwałtownie rośnie ($T_2 > T_{cond}$) i ciepło może zostać oddane do budynku.\n\n"
                "- **Spręż ($\\Pi = p_2 / p_1$):** stosunek ciśnienia skraplania do ciśnienia parowania. Im większa różnica temperatur, tym wyższe $\\Pi$.\n"
                "- **Sprawność izentropowa ($\\eta_s$):** porównuje idealne sprężanie bez strat ($s = \\text{const}$) do rzeczywistego:\n\n"
                "$$\\eta_s = \\frac{h_{2s} - h_1}{h_2 - h_1}$$\n\n"
                "Gdy $\\eta_s$ spada (np. z 0.85 do 0.60), sprężarka marnuje więcej prądu na tarcie i zawirowania, co zamienia się w dodatkowe ciepło podnoszące $T_2$ i obniżające COP."
            ),
            "en": (
                "The **compressor** is the electrically driven heart of the heat pump ($P_{el}$). It raises vapor pressure from $p_1$ to $p_2$, "
                "sharply increasing its temperature ($T_2 > T_{cond}$) so heat can flow into the building.\n\n"
                "- **Pressure ratio ($\\Pi = p_2 / p_1$):** ratio of condensing pressure to evaporating pressure. Larger temperature lifts produce higher $\\Pi$.\n"
                "- **Isentropic efficiency ($\\eta_s$):** compares ideal lossless compression ($s = \\text{const}$) to actual compression:\n\n"
                "$$\\eta_s = \\frac{h_{2s} - h_1}{h_2 - h_1}$$\n\n"
                "When $\\eta_s$ drops (e.g., from 0.85 to 0.60), more electrical work is lost to friction and irreversibilities, raising $T_2$ and reducing COP."
            ),
        },
        lab_type="compressor_lab",
    ),
    Lesson(
        id="cond_subcool",
        title={
            "pl": "3. Skraplacz i dochłodzenie cieczy (ΔT_sc)",
            "en": "3. Condenser & Liquid Subcooling (ΔT_sc)",
        },
        subtitle={
            "pl": "Element: Skraplacz (2 → 3) | Współczynnik: Dochłodzenie ΔT_sc [K]",
            "en": "Component: Condenser (2 → 3) | Coefficient: Subcooling ΔT_sc [K]",
        },
        theory={
            "pl": (
                "**Skraplacz** oddaje ciepło $Q_{cond}$ do instalacji grzewczej w **trzech etapach**:\n"
                "1. **Schładzanie gorącej pary** (*desuperheating*) od $T_2$ do $T_{cond}$,\n"
                "2. **Skraplanie izotermiczne** w stałej temperaturze $T_{cond}$ (największa część ciepła utajonego),\n"
                "3. **Dochłodzenie cieczy** (*subcooling*) o $\\Delta T_{sc}$ poniżej temperatury skraplania ($T_3 = T_{cond} - \\Delta T_{sc}$).\n\n"
                "- **Po co dochładzamy ciecz?** Chłodniejsza ciecz przed zaworem dławiącym daje mniej pary rozprężnej (*flash gas*) za zaworem, "
                "więcej ciepła trafia z natury ($Q_{evap}$), a COP rośnie — bez dodatkowej pracy sprężarki!"
            ),
            "en": (
                "The **condenser** rejects heat $Q_{cond}$ to the heating system in **three zones**:\n"
                "1. **Desuperheating** hot vapor from $T_2$ down to $T_{cond}$,\n"
                "2. **Isothermal condensation** at constant $T_{cond}$ (the largest latent heat portion),\n"
                "3. **Liquid subcooling** by $\\Delta T_{sc}$ below the condensation temperature ($T_3 = T_{cond} - \\Delta T_{sc}$).\n\n"
                "- **Why subcool?** Cooler liquid before the expansion valve produces less *flash gas* after throttling, "
                "increasing free ambient heat $Q_{evap}$ and boosting COP without extra compressor work!"
            ),
        },
        lab_type="subcooling_lab",
    ),
    Lesson(
        id="valve_flash",
        title={
            "pl": "4. Zawór dławiący i stopień suchości (x₄)",
            "en": "4. Expansion Valve & Vapor Quality (x₄)",
        },
        subtitle={
            "pl": "Element: Zawór rozprężny (3 → 4) | Współczynnik: Stopień suchości x₄ [-]",
            "en": "Component: Expansion Valve (3 → 4) | Coefficient: Vapor Quality x₄ [-]",
        },
        theory={
            "pl": (
                "**Zawór dławiący (rozprężny)** zamyka pętlę między stroną wysokiego ciśnienia ($p_2$) a stroną niskiego ciśnienia ($p_1$).\n\n"
                "- **Przemiana izentalpowa ($h_3 = h_4$):** zawór nie wykonuje pracy mechanicznej i jest izolowany cieplnie, więc entalpia czynnika pozostaje stała.\n"
                "- **Spadek temperatury i *flash gas*:** gwałtowny spadek ciśnienia zmusza część ciekłego czynnika do natychmiastowego odparowania, co schładza resztę cieczy do $T_4 = T_{evap}$.\n"
                "- **Stopień suchości ($x_4$):** określa udział masowy pary w mieszaninie na wejściu do parownika ($x=0$ to czysta ciecz, $x=1$ to czysta para). "
                "Zwykle $x_4 \\approx 0.15\\text{--}0.35$. Im mniejsze $x_4$, tym więcej ciekłego czynnika może odebrać ciepło w parowniku."
            ),
            "en": (
                "The **expansion (throttling) valve** bridges the high-pressure side ($p_2$) and low-pressure side ($p_1$).\n\n"
                "- **Isenthalpic process ($h_3 = h_4$):** the valve performs no shaft work and is adiabatic, so specific enthalpy remains constant.\n"
                "- **Temperature drop & *flash gas*:** the sudden pressure drop forces a fraction of liquid to flash into vapor, cooling the remaining liquid down to $T_4 = T_{evap}$.\n"
                "- **Vapor quality ($x_4$):** mass fraction of vapor at the evaporator inlet ($x=0$ is saturated liquid, $x=1$ is saturated vapor). "
                "Typically $x_4 \\approx 0.15\\text{--}0.35$. Lower $x_4$ leaves more liquid available to absorb heat in the evaporator."
            ),
        },
        lab_type="valve_lab",
    ),
    Lesson(
        id="cop_carnot",
        title={
            "pl": "5. Współczynnik COP, granica Carnota i sprawność egzergowa (η_ex)",
            "en": "5. COP, Carnot Limit & Exergetic Efficiency (η_ex)",
        },
        subtitle={
            "pl": "Współczynniki: COP_grzewcze, COP_chłodnicze, COP_Carnot, η_ex",
            "en": "Coefficients: COP_heating, COP_cooling, COP_Carnot, η_ex",
        },
        theory={
            "pl": (
                "**COP (Coefficient of Performance)** to najważniejszy miernik opłacalności pompy ciepła:\n\n"
                "$$\\text{COP}_{grzewcze} = \\frac{Q_{cond}}{P_{el}} = \\frac{Q_{evap} + P_{el}}{P_{el}} = \\text{COP}_{chłodnicze} + 1$$\n\n"
                "Teoretyczne maksimum wyznacza **obieg Carnota** (temperatury w **Kelvinach**!):\n\n"
                "$$\\text{COP}_{Carnot} = \\frac{T_{cond}\\,[\\text{K}]}{T_{cond}\\,[\\text{K}] - T_{evap}\\,[\\text{K}]} = \\frac{T_{cond}}{\\Delta T_{lift}}$$\n\n"
                "- **Sprawność egzergowa ($\\eta_{ex} = \\text{COP} / \\text{COP}_{Carnot}$):** mówi, jaki procent ideału osiąga rzeczywista pompa (zwykle `45–60%`).\n"
                "- **Złota zasada:** im mniejszy skok temperatury $\\Delta T_{lift}$, tym wyższe COP!"
            ),
            "en": (
                "**COP (Coefficient of Performance)** is the primary efficiency metric of a heat pump:\n\n"
                "$$\\text{COP}_{heating} = \\frac{Q_{cond}}{P_{el}} = \\frac{Q_{evap} + P_{el}}{P_{el}} = \\text{COP}_{cooling} + 1$$\n\n"
                "The theoretical upper limit is given by the **Carnot cycle** (temperatures in **Kelvin**!):\n\n"
                "$$\\text{COP}_{Carnot} = \\frac{T_{cond}\\,[\\text{K}]}{T_{cond}\\,[\\text{K}] - T_{evap}\\,[\\text{K}]} = \\frac{T_{cond}}{\\Delta T_{lift}}$$\n\n"
                "- **Exergetic efficiency ($\\eta_{ex} = \\text{COP} / \\text{COP}_{Carnot}$):** shows what fraction of the Carnot limit a real unit achieves (typically `45–60%`).\n"
                "- **Golden rule:** the smaller the temperature lift $\\Delta T_{lift}$, the higher the COP!"
            ),
        },
        lab_type="carnot_lab",
    ),
    Lesson(
        id="refrigerants_gwp",
        title={
            "pl": "6. Czynniki chłodnicze, GWP i bezpieczeństwo (ASHRAE 34)",
            "en": "6. Refrigerants, GWP & Safety Classes (ASHRAE 34)",
        },
        subtitle={
            "pl": "Dobór czynnika: R290, R32, R134a, R410A, R1234yf, R600a, R717",
            "en": "Fluid Selection: R290, R32, R134a, R410A, R1234yf, R600a, R717",
        },
        theory={
            "pl": (
                "Wybór **czynnika chłodniczego** decyduje o ciśnieniach pracy, temperaturze tłoczenia $T_2$, punkcie krytycznym $T_{crit}$ oraz wpływie na środowisko:\n\n"
                "- **GWP (Global Warming Potential):** potencjał cieplarniany względem $\\text{CO}_2$ (`GWP = 1`). Stare czynniki HFC (jak `R410A`, `GWP = 2088`) są wycofywane na rzecz czynników naturalnych (`R290` propan, `GWP = 3`) lub HFO (`R1234yf`, `GWP = 4`).\n"
                "- **Klasy bezpieczeństwa ASHRAE 34:** pierwsza litera oznacza toksyczność (`A` — nietoksyczne, `B` — toksyczne), a cyfra/litera palność (`1` — niepalne, `2L` — trudno palne, `3` — wysoce palne).\n"
                "- **Punkt krytyczny ($T_{crit}$):** w obiegu podkrytycznym temperatura skraplania musi pozostać poniżej $T_{crit}$."
            ),
            "en": (
                "The **refrigerant** determines operating pressures, discharge temperature $T_2$, critical temperature $T_{crit}$, and environmental impact:\n\n"
                "- **GWP (Global Warming Potential):** greenhouse impact relative to $\\text{CO}_2$ (`GWP = 1`). Legacy HFCs (like `R410A`, `GWP = 2088`) are being phased down in favor of natural fluids (`R290` propane, `GWP = 3`) or HFOs (`R1234yf`, `GWP = 4`).\n"
                "- **ASHRAE 34 Safety Classes:** the letter indicates toxicity (`A` — non-toxic, `B` — toxic) and the number/suffix indicates flammability (`1` — non-flammable, `2L` — mildly flammable, `3` — highly flammable).\n"
                "- **Critical Point ($T_{crit}$):** in a subcritical cycle, condensation temperature must stay below $T_{crit}$."
            ),
        },
        lab_type="refrigerant_lab",
    ),
]


def get_lesson_text(lesson: Lesson, lang: str = "pl") -> Dict[str, str]:
    """Zwraca zlokalizowane pola tekstowe lekcji."""
    norm = normalize_lang(lang)
    return {
        "title": lesson.title[norm],
        "subtitle": lesson.subtitle[norm],
        "theory": lesson.theory[norm],
    }
