"""Dane merytoryczne lekcji oraz interaktywnych testów dla zakładki Edukacja (PL / EN)."""

from dataclasses import dataclass
from typing import Dict, List

from src.i18n import normalize_lang


@dataclass(frozen=True)
class QuizQuestion:
    """Pojedyncze pytanie testowe z objaśnieniem w dwóch językach."""

    id: str
    prompt: Dict[str, str]
    options: Dict[str, List[str]]
    correct_idx: int
    explanation: Dict[str, str]


@dataclass(frozen=True)
class Lesson:
    """Lekcja edukacyjna: teoria, identyfikator mini-laboratorium oraz zestaw pytań."""

    id: str
    title: Dict[str, str]
    subtitle: Dict[str, str]
    theory: Dict[str, str]
    lab_type: str
    questions: List[QuizQuestion]


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
        questions=[
            QuizQuestion(
                id="q_sh_1",
                prompt={
                    "pl": "Jaka jest główna rola przegrzania pary (ΔT_sh > 0 K) za parownikiem?",
                    "en": "What is the primary purpose of evaporator superheat (ΔT_sh > 0 K)?",
                },
                options={
                    "pl": [
                        "Ochrona sprężarki przed zassaniem ciekłego czynnika (uderzeniem hydraulicznym)",
                        "Obniżenie temperatury tłoczenia T₂ na wyjściu ze sprężarki",
                        "Zwiększenie ciśnienia skraplania p₂ w skraplaczu",
                        "Zastąpienie zaworu dławiącego w obiegu",
                    ],
                    "en": [
                        "Protecting the compressor from ingesting liquid refrigerant (liquid slugging)",
                        "Lowering the compressor discharge temperature T₂",
                        "Increasing the condensation pressure p₂ in the condenser",
                        "Replacing the expansion valve in the cycle",
                    ],
                },
                correct_idx=0,
                explanation={
                    "pl": (
                        "Sprężarki są zaprojektowane wyłącznie do sprężania gazu. Nawet niewielka ilość cieczy na ssaniu (punkt 1) "
                        "może uszkodzić zawory lub tłoki/spirale. Przegrzanie o 4–7 K gwarantuje, że czynnik jest w 100% suchą parą."
                    ),
                    "en": (
                        "Compressors are designed solely for vapor. Even small amounts of liquid at suction (point 1) "
                        "can damage valves or scrolls/pistons. A 4–7 K superheat guarantees 100% dry vapor enters the compressor."
                    ),
                },
            ),
            QuizQuestion(
                id="q_sh_2",
                prompt={
                    "pl": "Co stanie się z temperaturą tłoczenia T₂, jeśli zwiększymy przegrzanie ΔT_sh z 2 K do 15 K?",
                    "en": "What happens to the discharge temperature T₂ if superheat ΔT_sh increases from 2 K to 15 K?",
                },
                options={
                    "pl": [
                        "Temperatura T₂ wyraźnie wzrośnie, bo sprężamy cieplejszą parę",
                        "Temperatura T₂ spadnie poniżej temperatury skraplania",
                        "Temperatura T₂ nie zmieni się w ogóle",
                        "Ciśnienie parowania p₁ wzrośnie dwukrotnie",
                    ],
                    "en": [
                        "T₂ increases noticeably because the compressor starts from a warmer vapor state",
                        "T₂ drops below the condensation temperature",
                        "T₂ remains completely unchanged",
                        "Evaporation pressure p₁ doubles",
                    ],
                },
                correct_idx=0,
                explanation={
                    "pl": (
                        "Sprężanie rozpoczyna się od temperatury T₁ = T_evap + ΔT_sh. Im wyższe T₁, tym wyższa temperatura końcowa T₂ "
                        "po sprężeniu — co możesz sprawdzić bezpośrednio w mini-laboratorium powyżej!"
                    ),
                    "en": (
                        "Compression starts at T₁ = T_evap + ΔT_sh. A higher starting temperature T₁ directly shifts the final "
                        "discharge temperature T₂ upward — which you can verify right in the mini-lab above!"
                    ),
                },
            ),
        ],
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
        questions=[
            QuizQuestion(
                id="q_comp_1",
                prompt={
                    "pl": "Jeśli sprawność izentropowa sprężarki η_s spada z 0.85 do 0.60 (przy stałym Q_cond), to:",
                    "en": "If compressor isentropic efficiency η_s drops from 0.85 to 0.60 (at constant Q_cond), then:",
                },
                options={
                    "pl": [
                        "Pobór prądu P_el rośnie, T₂ rośnie, a COP spada",
                        "Pobór prądu P_el maleje, a COP rośnie",
                        "Spręż Π = p₂/p₁ rośnie dwukrotnie",
                        "Temperatura parowania spada do zera absolutnego",
                    ],
                    "en": [
                        "Electrical power P_el increases, T₂ rises, and COP drops",
                        "Electrical power P_el decreases and COP improves",
                        "Pressure ratio Π = p₂/p₁ doubles",
                        "Evaporation temperature drops to absolute zero",
                    ],
                },
                correct_idx=0,
                explanation={
                    "pl": (
                        "Spadek η_s oznacza większe straty wewnętrzne w sprężarce. Aby wykonać to samo sprężanie z p₁ do p₂, "
                        "silnik musi pobrać więcej prądu (P_el = ṁ·(h₂ - h₁)), co bezpośrednio obniża COP = Q_cond / P_el i przegrzewa parę na tłoczeniu."
                    ),
                    "en": (
                        "Lower η_s means higher internal losses. To compress from p₁ to p₂, the motor needs more electrical power "
                        "(P_el = ṁ·(h₂ - h₁)), which directly lowers COP = Q_cond / P_el and overheats the discharge vapor."
                    ),
                },
            ),
            QuizQuestion(
                id="q_comp_2",
                prompt={
                    "pl": "Od czego bezpośrednio zależy wartość sprężu Π = p₂ / p₁ w naszym modelu?",
                    "en": "What directly determines the pressure ratio Π = p₂ / p₁ in our cycle model?",
                },
                options={
                    "pl": [
                        "Od temperatur parowania i skraplania oraz własności czynnika chłodniczego",
                        "Wyłącznie od mocy grzewczej budynku Q_cond [kW]",
                        "Wyłącznie od sprawności izentropowej η_s",
                        "Od koloru izolacji rur",
                    ],
                    "en": [
                        "From evaporation and condensation temperatures and the refrigerant's saturation curve",
                        "Solely from the building heating demand Q_cond [kW]",
                        "Solely from isentropic efficiency η_s",
                        "From the color of pipe insulation",
                    ],
                },
                correct_idx=0,
                explanation={
                    "pl": (
                        "Ciśnienia p₁ i p₂ to ciśnienia nasycenia odpowiadające T_evap i T_cond dla wybranego czynnika. "
                        "Zmiana mocy Q_cond zmienia jedynie strumień masy czynnika ṁ, nie zmieniając ciśnień ani sprężu Π."
                    ),
                    "en": (
                        "Pressures p₁ and p₂ are saturation pressures corresponding to T_evap and T_cond for the chosen fluid. "
                        "Changing Q_cond only scales mass flow rate ṁ without changing pressures or Π."
                    ),
                },
            ),
        ],
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
        questions=[
            QuizQuestion(
                id="q_sc_1",
                prompt={
                    "pl": "Jak umiarkowane dochłodzenie cieczy (ΔT_sc) wpływa na pracę obiegu przy stałych T_evap i T_cond?",
                    "en": "How does moderate liquid subcooling (ΔT_sc) affect the cycle at fixed T_evap and T_cond?",
                },
                options={
                    "pl": [
                        "Zmniejsza ilość flash gas (x₄) za zaworem i zwiększa współczynnik COP",
                        "Zwiększa ilość flash gas i obniża COP",
                        "Powoduje zamarznięcie sprężarki",
                        "Zmienia kierunek przepływu ciepła w skraplaczu",
                    ],
                    "en": [
                        "Reduces flash gas (x₄) after the valve and increases COP",
                        "Increases flash gas and lowers COP",
                        "Causes the compressor to freeze",
                        "Reverses heat flow direction in the condenser",
                    ],
                },
                correct_idx=0,
                explanation={
                    "pl": (
                        "Dochłodzenie obniża entalpię h₃ na wylocie ze skraplacza. Ponieważ na zaworze h₄ = h₃, punkt 4 przesuwa się "
                        "w lewo na wykresie log(p)-h (niższe x₄), co zwiększa użyteczną różnicę entalpii w parowniku (h₁ - h₄) i podnosi COP."
                    ),
                    "en": (
                        "Subcooling lowers outlet enthalpy h₃. Since throttling is isenthalpic (h₄ = h₃), point 4 shifts left "
                        "on the log(p)-h diagram (lower x₄), widening the evaporator enthalpy gain (h₁ - h₄) and raising COP."
                    ),
                },
            ),
            QuizQuestion(
                id="q_sc_2",
                prompt={
                    "pl": "Co w rzeczywistej instalacji ogranicza maksymalne możliwe dochłodzenie ΔT_sc?",
                    "en": "What physically limits the maximum achievable subcooling ΔT_sc in a real heating system?",
                },
                options={
                    "pl": [
                        "Temperatura wody powrotnej z instalacji grzewczej (nie można schłodzić czynnika poniżej powrotu)",
                        "Moc elektryczna licznika w budynku",
                        "Objętość skraplacza nie ma żadnego związku z temperaturą wody",
                        "Ciśnienie atmosferyczne na zewnątrz budynku",
                    ],
                    "en": [
                        "The return water temperature from the heating loop (refrigerant cannot cool below return water)",
                        "The building's electrical meter capacity",
                        "Condenser heat transfer has no relation to water temperature",
                        "Outdoor atmospheric pressure",
                    ],
                },
                correct_idx=0,
                explanation={
                    "pl": (
                        "Z II zasady termodynamiki ciepło płynie od cieplejszego czynnika do chłodniejszej wody powrotnej. "
                        "Próba wymuszenia większego dochłodzenia wymagałaby podniesienia T_cond, co z kolei psuje COP (zobacz zakładkę Optymalizacja SciPy!)."
                    ),
                    "en": (
                        "By the Second Law of Thermodynamics, heat flows from warmer refrigerant to cooler return water. "
                        "Forcing subcooling beyond that pinch requires raising T_cond, which hurts COP (see the SciPy Optimization tab!)."
                    ),
                },
            ),
        ],
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
        questions=[
            QuizQuestion(
                id="q_val_1",
                prompt={
                    "pl": "Która wielkość termodynamiczna pozostaje stała podczas idealnego dławienia w zaworze (3 → 4)?",
                    "en": "Which thermodynamic property remains constant during ideal throttling across the valve (3 → 4)?",
                },
                options={
                    "pl": [
                        "Entalpia właściwa h (h₃ = h₄)",
                        "Temperatura T (T₃ = T₄)",
                        "Ciśnienie p (p₃ = p₄)",
                        "Entropia właściwa s (s₃ = s₄)",
                    ],
                    "en": [
                        "Specific enthalpy h (h₃ = h₄)",
                        "Temperature T (T₃ = T₄)",
                        "Pressure p (p₃ = p₄)",
                        "Specific entropy s (s₃ = s₄)",
                    ],
                },
                correct_idx=0,
                explanation={
                    "pl": (
                        "Dławienie jest przemianą izentalpową (h = const) i nieodwracalną (entropia rośnie: s₄ > s₃). "
                        "Na wykresie log(p)-h widać to jako idealnie pionową linię w dół od punktu 3 do punktu 4."
                    ),
                    "en": (
                        "Throttling is isenthalpic (h = const) and irreversible (entropy increases: s₄ > s₃). "
                        "On the log(p)-h diagram, it appears as a vertical straight line going down from point 3 to point 4."
                    ),
                },
            ),
            QuizQuestion(
                id="q_val_2",
                prompt={
                    "pl": "Co oznacza wartość stopnia suchości x₄ = 0.25 za zaworem rozprężnym?",
                    "en": "What does a vapor quality of x₄ = 0.25 after the expansion valve mean?",
                },
                options={
                    "pl": [
                        "25% masy czynnika to już para (flash gas), a 75% to ciecz gotowa do wrzenia w parowniku",
                        "25% czynnika wyciekło z instalacji",
                        "Zawór jest otwarty w 25%",
                        "Temperatura wynosi 25 °C",
                    ],
                    "en": [
                        "25% of the refrigerant mass has flashed into vapor, and 75% is liquid ready to boil in the evaporator",
                        "25% of the refrigerant leaked out",
                        "The valve is 25% open",
                        "The temperature is 25 °C",
                    ],
                },
                correct_idx=0,
                explanation={
                    "pl": (
                        "Stopień suchości x ∈ [0, 1] to stosunek masy pary do całkowitej masy mieszaniny dwufazowej. "
                        "Tylko pozostałe (1 - x₄) = 75% cieczy może odparować w parowniku, pobierając ciepło utajone z otoczenia."
                    ),
                    "en": (
                        "Vapor quality x ∈ [0, 1] is the vapor mass fraction in a two-phase mixture. "
                        "Only the remaining (1 - x₄) = 75% liquid can evaporate in the evaporator to absorb latent ambient heat."
                    ),
                },
            ),
        ],
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
        questions=[
            QuizQuestion(
                id="q_cop_1",
                prompt={
                    "pl": "Dlaczego pompa ciepła współpracująca z ogrzewaniem podłogowym (T_cond = 35°C) ma znacznie wyższe COP niż z grzejnikami (T_cond = 55°C)?",
                    "en": "Why does a heat pump with underfloor heating (T_cond = 35°C) have a much higher COP than with radiators (T_cond = 55°C)?",
                },
                options={
                    "pl": [
                        "Mniejsza różnica temperatur ΔT_lift oznacza niższy spręż Π i mniejszą pracę sprężarki",
                        "Woda w podłogówce ma mniejsze ciepło właściwe",
                        "Grzejniki blokują przepływ czynnika w parowniku",
                        "W 55°C prawo zachowania energii przestaje obowiązywać",
                    ],
                    "en": [
                        "A smaller temperature lift ΔT_lift means a lower pressure ratio Π and less compressor work",
                        "Underfloor water has lower specific heat",
                        "Radiators block refrigerant flow in the evaporator",
                        "Energy conservation fails above 55°C",
                    ],
                },
                correct_idx=0,
                explanation={
                    "pl": (
                        "Z wzoru Carnota COP_Carnot = T_cond / ΔT_lift wynika wprost: zmniejszenie ΔT_lift z 55 K (np. 0→55°C) "
                        "do 35 K (0→35°C) drastycznie podnosi granicę sprawności i zmniejsza pobór prądu sprężarki."
                    ),
                    "en": (
                        "From Carnot's formula COP_Carnot = T_cond / ΔT_lift, reducing ΔT_lift from 55 K (e.g., 0→55°C) "
                        "to 35 K (0→35°C) dramatically raises the efficiency ceiling and cuts compressor electricity use."
                    ),
                },
            ),
            QuizQuestion(
                id="q_cop_2",
                prompt={
                    "pl": "Jeśli pompa ciepła ma COP_grzewcze = 4.5, to ile wynosi jej współczynnik chłodniczy (EER / COP_chłodnicze)?",
                    "en": "If a heat pump has COP_heating = 4.5, what is its cooling COP (EER / COP_cooling)?",
                },
                options={
                    "pl": ["3.5", "4.5", "5.5", "2.25"],
                    "en": ["3.5", "4.5", "5.5", "2.25"],
                },
                correct_idx=0,
                explanation={
                    "pl": (
                        "Z bilansu energii Q_cond = Q_evap + P_el po podzieleniu przez P_el otrzymujemy dokładną tożsamość: "
                        "COP_grzewcze = COP_chłodnicze + 1. Zatem 4.5 - 1 = 3.5."
                    ),
                    "en": (
                        "Dividing the energy balance Q_cond = Q_evap + P_el by P_el gives the exact identity: "
                        "COP_heating = COP_cooling + 1. Therefore 4.5 - 1 = 3.5."
                    ),
                },
            ),
        ],
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
        questions=[
            QuizQuestion(
                id="q_ref_1",
                prompt={
                    "pl": "Dlaczego propan (R290) ma klasę bezpieczeństwa A3 i jakie są jego główne zalety?",
                    "en": "Why does propane (R290) carry safety class A3, and what are its main advantages?",
                },
                options={
                    "pl": [
                        "Jest nietoksyczny (A) i wysoce palny (3); ma ultraniskie GWP = 3 i wysoką sprawność",
                        "Jest toksyczny i niepalny; ma bardzo wysokie GWP",
                        "Jest niepalny, dlatego nie wymaga żadnych zabezpieczeń",
                        "Może pracować tylko w temperaturach powyżej 100°C",
                    ],
                    "en": [
                        "It is non-toxic (A) and highly flammable (3); it has ultra-low GWP = 3 and high efficiency",
                        "It is toxic and non-flammable; it has very high GWP",
                        "It is non-flammable so it needs no safety measures",
                        "It can only operate above 100°C",
                    ],
                },
                correct_idx=0,
                explanation={
                    "pl": (
                        "W klasyfikacji ASHRAE 34 litera 'A' oznacza niską toksyczność, a '3' wysoką palność. "
                        "R290 (propan) świetnie sprawdza się w pompach ciepła typu monoblok na zewnątrz budynku, łącząc GWP = 3 z doskonałym COP."
                    ),
                    "en": (
                        "In ASHRAE 34, 'A' denotes low toxicity and '3' denotes high flammability. "
                        "R290 (propane) excels in outdoor monoblock heat pumps, combining GWP = 3 with high COP."
                    ),
                },
            ),
            QuizQuestion(
                id="q_ref_2",
                prompt={
                    "pl": "Który czynnik z bazy kalkulatora osiąga najwyższą temperaturę tłoczenia T₂ przy tych samych temperaturach pracy (np. 0°C / 45°C)?",
                    "en": "Which refrigerant in our database reaches the highest discharge temperature T₂ at identical temperatures (e.g., 0°C / 45°C)?",
                },
                options={
                    "pl": [
                        "R717 (Amoniak)",
                        "R600a (Izobutan)",
                        "R1234yf",
                        "R134a",
                    ],
                    "en": [
                        "R717 (Ammonia)",
                        "R600a (Isobutane)",
                        "R1234yf",
                        "R134a",
                    ],
                },
                correct_idx=0,
                explanation={
                    "pl": (
                        "Amoniak (R717) ma bardzo wysoki wykładnik izentropowy, przez co podczas sprężania jego temperatura tłoczenia T₂ "
                        "rośnie znacznie silniej niż np. dla R600a czy R1234yf. Sprawdź to w porównywarce czynników powyżej!"
                    ),
                    "en": (
                        "Ammonia (R717) has a high isentropic exponent, causing its discharge temperature T₂ to rise much more steeply "
                        "during compression than R600a or R1234yf. Try comparing them in the lab above!"
                    ),
                },
            ),
        ],
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


def get_question_text(question: QuizQuestion, lang: str = "pl") -> Dict[str, object]:
    """Zwraca zlokalizowane pola pytania testowego."""
    norm = normalize_lang(lang)
    return {
        "prompt": question.prompt[norm],
        "options": question.options[norm],
        "correct_idx": question.correct_idx,
        "explanation": question.explanation[norm],
    }
