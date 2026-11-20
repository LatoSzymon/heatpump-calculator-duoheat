"""Centralny moduł internacjonalizacji (PL / EN) dla aplikacji kalkulatora pompy ciepła."""

from typing import Dict

SUPPORTED_LANGS = ("pl", "en")

TRANSLATIONS: Dict[str, Dict[str, str]] = {
    "pl": {
        # App & Header
        "page_title": "Kalkulator Obiegu Pompy Ciepła — Instytut Naukowy",
        "brand_badge": "PROJEKT DUOHEAT",
        "brand_tagline": "Symulator obiegu termodynamicznego",
        "app_title": "Kalkulator i Symulator Obiegu Pompy Ciepła",
        "app_subtitle": "Narzędzie szkoleniowo-badawcze (TESPy, CoolProp i SciPy).",
        "footer_html": (
            '<div class="app-footer">'
            'Autor aplikacji: <a href="https://github.com/LatoSzymon" target="_blank">Szymon Lato</a> '
            '• Kalkulator Obiegu Pompy Ciepła • Projekt <a href="https://duoheat.pl" target="_blank">DUOHEAT</a>'
            "</div>"
        ),
        # Language switcher & Navigation
        "lang_label": "Język / Language",
        "lang_pl": "Polski (PL)",
        "lang_en": "English (EN)",
        "nav_header": "Nawigacja",
        "nav_simulation": "Symulacja",
        "nav_education": "Edukacja",
        "edu_lessons_expander": "Lekcje (wybierz temat)",
        # Sidebar
        "sidebar_header": "Konfiguracja obiegu",
        "scenario_fluid_header": "Scenariusz i czynnik",
        "preset_label": "Gotowy scenariusz (szybki start)",
        "preset_custom": "Własne ustawienia",
        "preset_help": "Wybierz typowy przypadek z praktyki inżynierskiej, aby zobaczyć realistyczne wartości.",
        "fluid_label": "Czynnik chłodniczy",
        "fluid_help": "Substancja krążąca w zamkniętym obiegu, która wrze w niskiej temperaturze i skrapla się w wysokiej.",
        "fluid_limit_error": "Nie udało się pobrać własności czynnika {fluid}: {exc}",
        "fluid_meta": "**Wzór:** `{formula}` | **T_kryt:** `{t_crit:.1f} °C` | **p_kryt:** `{p_crit:.1f} bar`\n\n{desc}",
        "source_temps_header": "Temperatury źródeł",
        "t_evap_label": "Temperatura parowania T_evap [°C]",
        "t_evap_help": "Temperatura wrzenia czynnika w parowniku. Zwykle jest o ok. 5–7 K niższa od temperatury powietrza lub gruntu.",
        "t_cond_label": "Temperatura skraplania T_cond [°C]",
        "t_cond_help": "Temperatura skraplania w skraplaczu. Ok. 35°C dla podłogówki, 50–60°C dla grzejników i CWU.",
        "cycle_comp_header": "Parametry obiegu i sprężarki",
        "superheat_label": "Przegrzanie pary za parownikiem ΔT_sh [K]",
        "superheat_help": "Dodatkowe podgrzanie pary przed sprężarką (typowo 4–7 K). Chroni sprężarkę przed zalaniem ciekłym czynnikiem.",
        "subcooling_label": "Dochłodzenie cieczy za skraplaczem ΔT_sc [K]",
        "subcooling_help": "Schłodzenie skroplonej cieczy poniżej temperatury skraplania. Zwiększa wydajność i zmniejsza straty na zaworze.",
        "eta_s_label": "Sprawność izentropowa sprężarki η_s [-]",
        "eta_s_help": "Określa, jak blisko idealnego sprężania bez strat pracuje rzeczywista sprężarka (typowo 0.70–0.82).",
        "q_cond_label": "Moc grzewcza dla budynku Q_cond [kW]",
        "q_cond_help": "Docelowa moc cieplna dostarczana przez skraplacz do instalacji grzewczej.",
        # Simulation errors & warnings
        "err_invalid_params": "Nieprawidłowe parametry fizyczne obiegu: {exc}",
        "err_tespy_converge": (
            "Solver TESPy nie osiągnął zbieżności dla wybranych parametrów ({exc}). "
            "Spróbuj zmienić temperaturę parowania/skraplania lub wybrać inny czynnik."
        ),
        "err_unexpected": "Wystąpił nieoczekiwany błąd obliczeniowy: {exc}",
        "err_hint": "Skoryguj parametry w panelu bocznym lub wybierz jeden z gotowych scenariuszy.",
        "warn_high_t_discharge": (
            "Uwaga inżynierska: Wysoka temperatura tłoczenia sprężarki (**{t_dis:.1f} °C**). "
            "W rzeczywistym układzie powyżej ~115–120 °C olej smarny ulega przegrzaniu — rozważ obniżenie `T_cond`, "
            "zmniejszenie przegrzania lub zmianę czynnika."
        ),
        # KPIs
        "kpi_cop_label": "COP (Efektywność)",
        "kpi_cop_sub": "{pct:.0f}% Carnota ({carnot:.2f})",
        "kpi_qcond_label": "Ciepło do budynku Q_cond",
        "kpi_pcomp_label": "Pobór prądu P_el",
        "kpi_pcomp_sub": "{pct:.0f}% energii",
        "kpi_qevap_label": "Ciepło z natury Q_evap",
        "kpi_qevap_sub": "{pct:.0f}% za darmo",
        "kpi_tdis_label": "Temp. tłoczenia T₂",
        "kpi_pr_label": "Spręż Π = p₂ / p₁",
        # Tabs
        "tab_mechanics": "Schemat i mechanika",
        "tab_charts": "Wykresy log(p)-h i T-s",
        "tab_table": "Punkty i bilans",
        "tab_scipy": "Optymalizacja (SciPy)",
        "tab_education": "Edukacja",
        "tab_glossary": "Słowniczek",
        # Tab 1: Mechanics
        "mech_title": "Jak działa pompa ciepła? (Obieg na żywo)",
        "mech_intro": (
            "Pompa ciepła **nie wytwarza** ciepła ze spalania — ona je **przepompowuje** z chłodnego otoczenia "
            "(powietrze/grunt) do ciepłego budynku, wykorzystując zjawiska **wrzenia** i **skraplania** czynnika chłodniczego."
        ),
        "err_schematic": "Nie udało się wygenerować schematu obiegu: {exc}",
        "mech_stages_title": "#### 4 etapy obiegu dla Twoich aktualnych nastaw:",
        "stage_1_html": (
            '<div class="step-card step-evap">'
            "<strong>4 → 1. Parowanie i przegrzanie (Parownik)</strong><br>"
            "Ciekły czynnik o niskim ciśnieniu (<code>{p_evap:.2f} bar</code>) wpływa do parownika w temperaturze "
            "<strong>{t_4:.1f} °C</strong>. Ponieważ wrze w temperaturze niższej niż otoczenie, pobiera "
            "<strong>{q_evap:.2f} kW</strong> darmowego ciepła i zamienia się w parę "
            "(dodatkowo przegrzaną o <code>{sh:.1f} K</code> do <strong>{t_1:.1f} °C</strong>, aby żadna kropla nie trafiła do sprężarki)."
            "</div>"
        ),
        "stage_2_html": (
            '<div class="step-card step-comp">'
            "<strong>1 → 2. Sprężanie (Sprężarka)</strong><br>"
            "Sprężarka zasysa chłodną parę (<code>{v_dot:.2f} m³/h</code>) i podnosi jej ciśnienie "
            "<strong>{pr:.2f}-krotnie</strong> (do <code>{p_cond:.2f} bar</code>), zużywając "
            "<strong>{p_comp:.2f} kW</strong> energii elektrycznej. Wzrost ciśnienia gwałtownie podnosi "
            "temperaturę pary aż do <strong>{t_dis:.1f} °C</strong>."
            "</div>"
        ),
        "stage_3_html": (
            '<div class="step-card step-cond">'
            "<strong>2 → 3. Skraplanie i dochłodzenie (Skraplacz)</strong><br>"
            "Gorąca para oddaje <strong>{q_cond:.2f} kW</strong> ciepła wodzie w instalacji grzewczej: "
            "najpierw chłodzi się do <strong>{t_cond:.1f} °C</strong> (<code>{q_desup:.2f} kW</code>), "
            "następnie skrapla (<code>{q_lat:.2f} kW</code>), a na końcu jest dochładzana o "
            "<code>{sc:.1f} K</code> do <strong>{t_3:.1f} °C</strong> (<code>{q_sub:.2f} kW</code>)."
            "</div>"
        ),
        "stage_4_html": (
            '<div class="step-card step-valve">'
            "<strong>3 → 4. Rozprężanie izentalpowe (Zawór dławiący)</strong><br>"
            "Ciecz pod wysokim ciśnieniem przeciska się przez zawór rozprężny. Ciśnienie spada z "
            "<code>{p_cond:.2f}</code> do <code>{p_evap:.2f} bar</code>, przez co czynnik "
            "gwałtownie stygnie do <strong>{t_4:.1f} °C</strong>. Część cieczy (<strong>{x_4_pct:.1f}%</strong>) "
            "odparowuje natychmiast (tzw. <em>flash gas</em>), a reszta trafia do parownika i cykl się powtarza."
            "</div>"
        ),
        # Tab 2: Charts
        "charts_guide_title": "Jak czytać wykres Molliera log(p)-h oraz wykres T-s?",
        "charts_guide_md": (
            "- **Szary „dzwon” (krzywa nasycenia):** oddziela obszar cieczy (po lewej), mieszaniny wrzącej cieczy i pary (w środku) oraz pary przegrzanej (po prawej).\n"
            "- **Wykres log(p)-h (po lewej):** Oś pionowa to ciśnienie, a pozioma to energia czynnika (entalpia `h`).\n"
            "  - Poziome odcinki to wymiana ciepła przy stałym ciśnieniu: długość odcinka `4→1` to ciepło pobrane z natury (`q_evap`), a długość `2→3` to ciepło oddane do budynku (`q_cond`).\n"
            "  - Różnica `h₂ - h₁` to praca włożona przez sprężarkę. **Im krótszy odcinek `1→2` względem `2→3`, tym wyższe COP!**\n"
            "  - Pionowy odcinek `3→4` oznacza dławienie przy stałej entalpii (`h = const`).\n"
            "- **Wykres T-s (po prawej):** Pokazuje temperaturę w funkcji entropii. Wyraźnie widać na nim, jak wysoka jest temperatura tłoczenia w punkcie `2` oraz że parowanie (`4→1`) i skraplanie (`2→3`) w obszarze dwufazowym odbywają się w stałej temperaturze."
        ),
        "err_ph": "Błąd generowania wykresu log(p)-h: {exc}",
        "err_ts": "Błąd generowania wykresu T-s: {exc}",
        # Tab 3: Table & Balance
        "table_title": "Parametry termodynamiczne w punktach węzłowych (1–4)",
        "download_csv": "Pobierz tabelę stanów jako CSV",
        "heat_struct_title": "Struktura wymiany ciepła w wymiennikach oraz bilans TESPy",
        "cond_breakdown_title": "**Skraplacz (oddawanie ciepła do budynku):**",
        "cond_desup": "- Schładzanie gorącej pary (desuperheating): **{val:.2f} kW** ({pct:.1f}%)",
        "cond_latent": "- Skraplanie izotermiczne (ciepło utajone): **{val:.2f} kW** ({pct:.1f}%)",
        "cond_subcool": "- Dochładzanie cieczy (subcooling): **{val:.2f} kW** ({pct:.1f}%)",
        "evap_breakdown_title": "**Parownik (pobieranie ciepła z otoczenia):**",
        "evap_latent": "- Odparowanie w obszarze dwufazowym: **{val:.2f} kW** ({pct:.1f}%)",
        "evap_superheat": "- Przegrzanie pary przed sprężarką: **{val:.2f} kW** ({pct:.1f}%)",
        "exergy_eff_box": "**Sprawność egzergowa (względem obiegu Carnota):** `{val:.1f} %`",
        "eer_box": "**Współczynnik chłodniczy (EER / COP_chł):** `{val:.2f}`",
        "tespy_err_box": "**Błąd zamknięcia bilansu energii (TESPy):** `{val:.4e} W`",
        "summary_exergy_label": "Sprawność egzergowa",
        "summary_exergy_sub": "Względem obiegu Carnota",
        "summary_eer_label": "Współczynnik chłodniczy (EER)",
        "summary_eer_sub": "COP_chł = COP_grz − 1",
        "summary_balance_label": "Błąd bilansu energii (TESPy)",
        "summary_balance_sub": "Zamknięcie bilansu sieci",
        # Tab 4: SciPy
        "scipy_1_title": "1. Poszukiwanie wymaganej temperatury parowania (`scipy.optimize.root_scalar`)",
        "scipy_1_caption": "Sprawdź, jak ciepłe musi być dolne źródło (powietrze/grunt), aby przy obecnej temperaturze skraplania osiągnąć zadane COP.",
        "scipy_target_cop": "Docelowy współczynnik COP_grzewcze [-]",
        "scipy_1_success": (
            "Aby osiągnąć **COP = {cop:.2f}** przy $T_{{cond}} = {t_cond:.1f}\\text{{ °C}}$, "
            "wymagana temperatura parowania wynosi **$T_{{evap}} = {t_evap:.2f}\\text{{ °C}}$** "
            "(pobór mocy sprężarki: `{p_comp:.2f} kW`, liczba iteracji Brentq: `{iters}`)."
        ),
        "scipy_1_err": "Nie można wyznaczyć temperatury parowania: {err}",
        "scipy_2_title": "2. Optymalizacja dochłodzenia cieczy (`scipy.optimize.minimize_scalar`)",
        "scipy_2_caption": (
            "Dochłodzenie poprawia COP, ale jest ograniczone temperaturą wody powracającej z grzejników/podłogówki. "
            "Poniżej widać, gdzie znajduje się fizyczne optimum."
        ),
        "scipy_return_temp": "Temperatura wody powrotnej z instalacji CO [°C]",
        "scipy_2_info": (
            "Optymalny stopień dochłodzenia dla powrotu `{t_ret:.1f} °C` "
            "wynosi **$\\Delta T_{{sc,opt}} = {sc_opt:.2f}\\text{{ K}}$** "
            "(efektywne **COP = {max_cop:.2f}**)."
        ),
        "scipy_2_err": "Błąd optymalizacji dochłodzenia: {err}",
        "scipy_2_plot_err": "Błąd rysowania krzywej dochłodzenia: {exc}",
        "scipy_3_title": "3. Mapa sprawności COP = f(T_evap, T_cond) (`scipy.interpolate.RegularGridInterpolator`)",
        "scipy_3_caption": (
            "Mapa pokazuje, jak silnie spada COP, gdy rośnie różnica temperatur (prawy dolny róg vs lewy górny róg). "
            "Czerwona gwiazdka wskazuje Twój aktualny punkt pracy."
        ),
        "scipy_3_spinner": "Obliczanie siatki punktów TESPy i interpolacji kubicznej SciPy...",
        "scipy_3_err": "Nie udało się wygenerować mapy wrażliwości COP: {err}",
        # Tab 5: Glossary
        "glossary_title": "Kompendium pojęć termodynamicznych",
        "glossary_intro": "Poniżej zebrano najważniejsze pojęcia, które pojawiają się podczas pracy z pompami ciepła w naszym instytucie.",
        "glossary_col1_md": (
            "#### 1. Współczynnik COP i granica Carnota\n"
            "- **COP (Coefficient of Performance):** stosunek ciepła oddanego do budynku ($Q_{cond}$) do pobranej energii elektrycznej ($P_{el}$). Wartość `COP = 4.0` oznacza, że z `1 kWh` prądu uzyskujemy `4 kWh` ciepła (`3 kWh` pochodzi z natury!).\n"
            "- **Obieg Carnota ($COP_{Carnot} = T_{cond} / (T_{cond} - T_{evap})$):** teoretyczne maksimum sprawności dla danych temperatur (w Kelvinach). Rzeczywiste pompy osiągają zwykle `45–60%` granicy Carnota (tzw. **sprawność egzergowa**).\n"
            "- **Złota zasada:** im mniejszy skok temperatury $\\Delta T_{lift} = T_{cond} - T_{evap}$, tym wyższe COP. Dlatego ogrzewanie podłogowe (`35°C`) jest znacznie oszczędniejsze od grzejników (`55°C`).\n\n"
            "#### 2. Przegrzanie ($\\Delta T_{sh}$) i dochłodzenie ($\\Delta T_{sc}$)\n"
            "- **Przegrzanie (Superheat):** ogrzanie pary w parowniku powyżej temperatury wrzenia. Chroni sprężarkę przed uderzeniem hydraulicznym (ciecz jest nieściśliwa!). Zbyt duże przegrzanie podnosi jednak temperaturę tłoczenia $T_2$.\n"
            "- **Dochłodzenie (Subcooling):** schłodzenie skroplonej cieczy poniżej temperatury skraplania. Zmniejsza ilość pary powstającej na zaworze rozprężnym (*flash gas*) i zwiększa ilość ciepła odbieranego w parowniku."
        ),
        "glossary_col2_md": (
            "#### 3. Własności czynnika i parametry sprężarki\n"
            "- **Stopień suchości ($x$):** udział masowy pary w mieszaninie dwufazowej ($x=0$ to czysta ciecz nasycona, $x=1$ to czysta para nasycona). Za zaworem dławiącym czynnik ma zwykle $x \\approx 0.15\\text{--}0.35$.\n"
            "- **Sprawność izentropowa ($\\eta_s$):** miara strat wewnętrznych sprężarki (tarcie, straty przepływowe, nieszczelności). Dla $\\eta_s = 1.0$ sprężanie byłoby idealnie odwracalne ($s = \\text{const}$).\n"
            "- **Spręż ($\\Pi = p_2 / p_1$):** stosunek ciśnienia po stronie wysokiej do niskiej. Duży spręż obciąża mechanicznie sprężarkę i obniża jej sprawność objętościową.\n\n"
            "#### 4. Dobór czynnika chłodniczego (GWP i bezpieczeństwo)\n"
            "- **GWP (Global Warming Potential):** wskaźnik potencjału tworzenia efektu cieplarnianego (dla CO₂ = 1). Nowoczesne konstrukcje przechodzą na czynniki o ultraniskim GWP (np. **R290 propan**, **R1234yf**).\n"
            "- **Klasy bezpieczeństwa (ASHRAE 34):**\n"
            "  - `A1` — nietoksyczne, niepalne (np. R134a, R410A)\n"
            "  - `A2L` — nietoksyczne, trudno palne (np. R32, R1234yf)\n"
            "  - `A3` — nietoksyczne, wysoce palne (np. R290, R600a — wymagają odpowiedniej strefy bezpieczeństwa)\n"
            "  - `B2L` — toksyczne, trudno palne (np. R717 amoniak — układy przemysłowe)"
        ),
        # Education tab UI
        "edu_title": "Akademia Pompy Ciepła — Lekcje i Ilustracje Obiegu",
        "edu_intro": (
            "Poznaj działanie każdego elementu i znaczenie najważniejszych współczynników obiegu. "
            "Wybierz lekcję z paska bocznego, aby przeanalizować **teorię** oraz **interaktywną ilustrację wpływu (TESPy)**."
        ),
        "edu_select_lesson": "Wybierz lekcję:",
        "edu_theory_header": "1. Teoria i fizyka procesu",
        "edu_lab_header": "2. Ilustracja wpływu na działanie pompy ciepła (TESPy)",
        "edu_lab_metric_cop": "COP grzewcze",
        "edu_lab_metric_t2": "Temp. tłoczenia T₂",
        "edu_lab_metric_pcomp": "Moc sprężarki P_el",
        "edu_lab_metric_qevap": "Ciepło z natury Q_evap",
        "edu_lab_metric_x4": "Flash gas (x₄)",
        "edu_lab_metric_pr": "Spręż Π = p₂/p₁",
        "edu_lab_metric_carnot": "COP Carnota",
        # cycle_model.py state table & errors
        "col_point": "Punkt",
        "col_desc": "Opis stanu",
        "col_p": "p [bar]",
        "col_T": "T [°C]",
        "col_h": "h [kJ/kg]",
        "col_s": "s [kJ/(kg·K)]",
        "col_x": "x [-]",
        "col_rho": "ρ [kg/m³]",
        "single_phase": "Jednofazowy",
        "pt1_superheated": "Wlot do sprężarki (para przegrzana)",
        "pt1_saturated": "Wlot do sprężarki (para nasycona)",
        "pt2_desc": "Wylot ze sprężarki (gorąca para)",
        "pt3_subcooled": "Wylot ze skraplacza (ciecz dochłodzona)",
        "pt3_saturated": "Wylot ze skraplacza (ciecz nasycona)",
        "pt4_desc": "Wlot do parownika (mieszanina dwufazowa)",
        "err_tespy_not_converged": "Rozwiązanie sieci TESPy nie osiągnęło zbieżności dla zadanych parametrów.",
        # utils.py validation errors
        "val_bad_fluid": "Nieobsługiwany czynnik '{fluid}'. Dostępne: {avail}",
        "val_t_evap_min": "Temperatura parowania ({t_evap:.1f} °C) jest zbyt bliska minimalnej temperaturze modelu dla {fluid} ({t_min:.1f} °C).",
        "val_t_cond_crit": "Temperatura skraplania ({t_cond:.1f} °C) przekracza bezpieczny limit obiegu podkrytycznego dla {fluid} (T_crit = {t_crit:.1f} °C).",
        "val_t_evap_ge_cond": "Temperatura parowania ({t_evap:.1f} °C) musi być niższa od temperatury skraplania ({t_cond:.1f} °C) o co najmniej 2 K.",
        "val_superheat_range": "Przegrzanie ({sh:.1f} K) musi mieścić się w przedziale [0, 40] K.",
        "val_subcool_range": "Dochłodzenie ({sc:.1f} K) musi mieścić się w przedziale [0, 35] K.",
        "val_subcool_below_evap": "Temperatura po dochłodzeniu za skraplaczem nie może być niższa niż temperatura parowania.",
        "val_eta_range": "Sprawność izentropowa sprężarki ({eta:.2f}) musi należeć do przedziału [0.1, 1.0].",
        "val_q_cond_pos": "Moc grzewcza skraplacza ({q:.2f} kW) musi być dodatnia.",
        # optimizer.py
        "opt_empty_bracket": "Przedział poszukiwań temperatury parowania jest pusty dla zadanej temperatury skraplania.",
        "opt_out_of_range": "Zadane COP = {target:.2f} jest poza osiągalnym zakresem [{cmin:.2f}, {cmax:.2f}] dla T_evap w [{low:.1f}, {high:.1f}] °C.",
        "opt_col_tevap": "T_evap [°C]",
        "opt_col_tcond": "T_cond [°C]",
        "opt_col_cop": "COP [-]",
        "opt_col_pcomp": "P_comp [kW]",
        "opt_col_qevap": "Q_evap [kW]",
        # plotting.py
        "plot_pipe_4_evap": "4 → Parownik (wrzenie)",
        "plot_pipe_1_suction": "1 (Ssanie sprężarki)",
        "plot_pipe_2_hot": "2 (Gorąca para)",
        "plot_pipe_3_liq": "3 (Ciecz pod ciśnieniem)",
        "plot_pipe_4_two": "4 (Mieszanina dwufazowa)",
        "plot_hover_pt1": "<b>Punkt 1: Ssanie sprężarki</b><br>T = {T:.1f} °C | p = {p:.2f} bar",
        "plot_hover_pt2": "<b>Punkt 2: Tłoczenie sprężarki</b><br>T = {T:.1f} °C | p = {p:.2f} bar",
        "plot_hover_pt3": "<b>Punkt 3: Za skraplaczem</b><br>T = {T:.1f} °C | p = {p:.2f} bar",
        "plot_hover_pt4": "<b>Punkt 4: Za zaworem dławiącym</b><br>T = {T:.1f} °C | p = {p:.2f} bar | x = {x:.1f}%",
        "plot_ann_cond": "<b>SKRAPLACZ</b><br><span style='font-size:11px'>Oddaje ciepło</span>",
        "plot_ann_evap": "<b>PAROWNIK</b><br><span style='font-size:11px'>Pobiera ciepło</span>",
        "plot_ann_comp": "<b>SPRĘŻARKA</b>",
        "plot_ann_valve": "<b>ZAWÓR</b>",
        "plot_ann_qcond": "<b>Do budynku</b><br>Q_cond = {q:.2f} kW",
        "plot_ann_qevap": "<b>Z natury (za darmo)</b><br>Q_evap = {q:.2f} kW",
        "plot_ann_pcomp": "<b>Prąd</b><br>P_el = {p:.2f} kW",
        "plot_schematic_title": "Schemat pracy pompy ciepła (COP = {cop:.2f})",
        "plot_bal_evap": "Ciepło z natury Q_evap",
        "plot_bal_comp": "Prąd do sprężarki P_el",
        "plot_bal_cond": "Ciepło do budynku Q_cond",
        "plot_bal_sources": "Źródła energii",
        "plot_bal_output": "Efekt grzewczy",
        "plot_bal_title": "Bilans energii: {q_evap:.2f} kW + {p_comp:.2f} kW = {q_cond:.2f} kW",
        "plot_bal_yaxis": "Moc cieplna / elektryczna [kW]",
        "plot_dome_name": "Krzywa nasycenia (x=0 / x=1)",
        "plot_cycle_name": "Obieg pompy ciepła ({fluid})",
        "plot_ph_title": "Wykres log(p)-h (Molliera) — {fluid}",
        "plot_ph_xaxis": "Entalpia właściwa h [kJ/kg]",
        "plot_ph_yaxis": "Ciśnienie p [bar] (skala log)",
        "plot_ts_title": "Wykres T-s — {fluid}",
        "plot_ts_xaxis": "Entropia właściwa s [kJ/(kg·K)]",
        "plot_ts_yaxis": "Temperatura T [°C]",
        "plot_pt_prefix": "Punkt",
        "plot_current_op": "Aktualny punkt pracy",
        "plot_contour_title": "Mapa sprawności COP(T_evap, T_cond) — interpolacja kubiczna SciPy",
        "plot_contour_xaxis": "Temperatura parowania T_evap [°C]",
        "plot_contour_yaxis": "Temperatura skraplania T_cond [°C]",
        "plot_subcool_curve": "Efektywne COP(ΔT_sc)",
        "plot_subcool_opt": "Optimum ({sc:.2f} K, COP={cop:.2f})",
        "plot_subcool_title": "Wpływ dochłodzenia na COP (optymalizacja SciPy)",
        "plot_subcool_xaxis": "Dochłodzenie ΔT_sc [K]",
        "plot_subcool_yaxis": "Efektywne COP [-]",
    },
    "en": {
        # App & Header
        "page_title": "Heat Pump Cycle Calculator — Research Institute",
        "brand_badge": "DUOHEAT PROJECT",
        "brand_tagline": "Thermodynamic cycle simulator",
        "app_title": "Heat Pump Cycle Calculator & Simulator",
        "app_subtitle": "Training and research tool (TESPy, CoolProp and SciPy).",
        "footer_html": (
            '<div class="app-footer">'
            'Author: <a href="https://github.com/LatoSzymon" target="_blank">Szymon Lato</a> '
            '• Heat Pump Cycle Calculator • <a href="https://duoheat.pl" target="_blank">DUOHEAT</a> Project'
            "</div>"
        ),
        # Language switcher & Navigation
        "lang_label": "Language / Język",
        "lang_pl": "Polski (PL)",
        "lang_en": "English (EN)",
        "nav_header": "Navigation",
        "nav_simulation": "Simulation",
        "nav_education": "Education",
        "edu_lessons_expander": "Lessons (choose topic)",
        # Sidebar
        "sidebar_header": "Cycle Configuration",
        "scenario_fluid_header": "Scenario & Refrigerant",
        "preset_label": "Scenario preset (quick start)",
        "preset_custom": "Custom settings",
        "preset_help": "Select a typical engineering case to see realistic operating values.",
        "fluid_label": "Refrigerant",
        "fluid_help": "Working fluid circulating in the closed loop, boiling at low temperature and condensing at high temperature.",
        "fluid_limit_error": "Failed to fetch properties for refrigerant {fluid}: {exc}",
        "fluid_meta": "**Formula:** `{formula}` | **T_crit:** `{t_crit:.1f} °C` | **p_crit:** `{p_crit:.1f} bar`\n\n{desc}",
        "source_temps_header": "Source & Sink Temperatures",
        "t_evap_label": "Evaporation temperature T_evap [°C]",
        "t_evap_help": "Boiling temperature in the evaporator. Typically ~5–7 K below ambient air or ground temperature.",
        "t_cond_label": "Condensation temperature T_cond [°C]",
        "t_cond_help": "Condensation temperature in the condenser. ~35°C for underfloor heating, 50–60°C for radiators & DHW.",
        "cycle_comp_header": "Cycle & Compressor Parameters",
        "superheat_label": "Evaporator superheat ΔT_sh [K]",
        "superheat_help": "Additional vapor heating before the compressor (typically 4–7 K). Protects the compressor from liquid slugging.",
        "subcooling_label": "Condenser subcooling ΔT_sc [K]",
        "subcooling_help": "Cooling condensed liquid below saturation temperature. Increases capacity and reduces throttling losses.",
        "eta_s_label": "Compressor isentropic efficiency η_s [-]",
        "eta_s_help": "Indicates how close the real compressor is to ideal lossless compression (typically 0.70–0.82).",
        "q_cond_label": "Heating capacity for building Q_cond [kW]",
        "q_cond_help": "Target thermal power delivered by the condenser to the heating system.",
        # Simulation errors & warnings
        "err_invalid_params": "Invalid physical cycle parameters: {exc}",
        "err_tespy_converge": (
            "TESPy solver did not converge for the selected parameters ({exc}). "
            "Try adjusting evaporation/condensation temperatures or choosing another refrigerant."
        ),
        "err_unexpected": "An unexpected calculation error occurred: {exc}",
        "err_hint": "Adjust parameters in the sidebar or select one of the preset scenarios.",
        "warn_high_t_discharge": (
            "Engineering note: High compressor discharge temperature (**{t_dis:.1f} °C**). "
            "Above ~115–120 °C lubricating oil degrades in real systems — consider lowering `T_cond`, "
            "reducing superheat, or changing the refrigerant."
        ),
        # KPIs
        "kpi_cop_label": "COP (Efficiency)",
        "kpi_cop_sub": "{pct:.0f}% of Carnot ({carnot:.2f})",
        "kpi_qcond_label": "Heat to building Q_cond",
        "kpi_pcomp_label": "Electricity input P_el",
        "kpi_pcomp_sub": "{pct:.0f}% of total heat",
        "kpi_qevap_label": "Ambient heat Q_evap",
        "kpi_qevap_sub": "{pct:.0f}% free energy",
        "kpi_tdis_label": "Discharge temp. T₂",
        "kpi_pr_label": "Pressure ratio Π = p₂ / p₁",
        # Tabs
        "tab_mechanics": "Schematic & Mechanics",
        "tab_charts": "log(p)-h & T-s Diagrams",
        "tab_table": "State Points & Balance",
        "tab_scipy": "Optimization (SciPy)",
        "tab_education": "Education",
        "tab_glossary": "Glossary",
        # Tab 1: Mechanics
        "mech_title": "How does a heat pump work? (Live cycle)",
        "mech_intro": (
            "A heat pump **does not generate** heat by combustion — it **pumps** heat from a cold environment "
            "(air/ground) into a warm building using **evaporation** and **condensation** of a refrigerant."
        ),
        "err_schematic": "Failed to generate cycle schematic: {exc}",
        "mech_stages_title": "#### 4 cycle stages for your current settings:",
        "stage_1_html": (
            '<div class="step-card step-evap">'
            "<strong>4 → 1. Evaporation & Superheating (Evaporator)</strong><br>"
            "Low-pressure liquid refrigerant (<code>{p_evap:.2f} bar</code>) enters the evaporator at "
            "<strong>{t_4:.1f} °C</strong>. Because it boils below ambient temperature, it absorbs "
            "<strong>{q_evap:.2f} kW</strong> of free heat and turns into vapor "
            "(further superheated by <code>{sh:.1f} K</code> to <strong>{t_1:.1f} °C</strong> so no liquid droplets reach the compressor)."
            "</div>"
        ),
        "stage_2_html": (
            '<div class="step-card step-comp">'
            "<strong>1 → 2. Compression (Compressor)</strong><br>"
            "The compressor draws cool vapor (<code>{v_dot:.2f} m³/h</code>) and raises its pressure "
            "<strong>{pr:.2f}×</strong> (to <code>{p_cond:.2f} bar</code>), consuming "
            "<strong>{p_comp:.2f} kW</strong> of electrical power. The pressure rise sharply increases "
            "the vapor temperature up to <strong>{t_dis:.1f} °C</strong>."
            "</div>"
        ),
        "stage_3_html": (
            '<div class="step-card step-cond">'
            "<strong>2 → 3. Condensation & Subcooling (Condenser)</strong><br>"
            "Hot vapor delivers <strong>{q_cond:.2f} kW</strong> of heat to the heating water: "
            "first cooling to <strong>{t_cond:.1f} °C</strong> (<code>{q_desup:.2f} kW</code>), "
            "then condensing (<code>{q_lat:.2f} kW</code>), and finally subcooling by "
            "<code>{sc:.1f} K</code> to <strong>{t_3:.1f} °C</strong> (<code>{q_sub:.2f} kW</code>)."
            "</div>"
        ),
        "stage_4_html": (
            '<div class="step-card step-valve">'
            "<strong>3 → 4. Isenthalpic Expansion (Expansion Valve)</strong><br>"
            "High-pressure liquid passes through the expansion valve. Pressure drops from "
            "<code>{p_cond:.2f}</code> to <code>{p_evap:.2f} bar</code>, causing the refrigerant "
            "to cool rapidly to <strong>{t_4:.1f} °C</strong>. Part of the liquid (<strong>{x_4_pct:.1f}%</strong>) "
            "flashes into vapor immediately (<em>flash gas</em>), and the rest enters the evaporator to repeat the cycle."
            "</div>"
        ),
        # Tab 2: Charts
        "charts_guide_title": "How to read the Mollier log(p)-h and T-s diagrams?",
        "charts_guide_md": (
            "- **Gray saturation dome:** separates the subcooled liquid region (left), two-phase boiling/condensing mixture (inside), and superheated vapor (right).\n"
            "- **log(p)-h diagram (left):** Vertical axis is pressure, horizontal axis is specific enthalpy `h` (energy).\n"
            "  - Horizontal segments represent constant-pressure heat transfer: `4→1` length is heat absorbed from nature (`q_evap`), and `2→3` length is heat delivered to the building (`q_cond`).\n"
            "  - The difference `h₂ - h₁` is compressor work. **The shorter `1→2` is compared to `2→3`, the higher the COP!**\n"
            "  - Vertical segment `3→4` shows throttling at constant enthalpy (`h = const`).\n"
            "- **T-s diagram (right):** Shows temperature vs. entropy. Clearly illustrates the high discharge temperature at point `2` and isothermal evaporation (`4→1`) / condensation (`2→3`) inside the dome."
        ),
        "err_ph": "Error generating log(p)-h diagram: {exc}",
        "err_ts": "Error generating T-s diagram: {exc}",
        # Tab 3: Table & Balance
        "table_title": "Thermodynamic Properties at State Points (1–4)",
        "download_csv": "Download state table as CSV",
        "heat_struct_title": "Heat Exchanger Breakdown & TESPy Energy Balance",
        "cond_breakdown_title": "**Condenser (heat delivered to building):**",
        "cond_desup": "- Hot vapor desuperheating: **{val:.2f} kW** ({pct:.1f}%)",
        "cond_latent": "- Isothermal condensation (latent heat): **{val:.2f} kW** ({pct:.1f}%)",
        "cond_subcool": "- Liquid subcooling: **{val:.2f} kW** ({pct:.1f}%)",
        "evap_breakdown_title": "**Evaporator (heat absorbed from ambient):**",
        "evap_latent": "- Two-phase evaporation: **{val:.2f} kW** ({pct:.1f}%)",
        "evap_superheat": "- Vapor superheating before compressor: **{val:.2f} kW** ({pct:.1f}%)",
        "exergy_eff_box": "**Exergetic efficiency (vs. Carnot cycle):** `{val:.1f} %`",
        "eer_box": "**Cooling COP (EER / COP_cool):** `{val:.2f}`",
        "tespy_err_box": "**Energy balance closure error (TESPy):** `{val:.4e} W`",
        "summary_exergy_label": "Exergetic efficiency",
        "summary_exergy_sub": "Relative to Carnot cycle",
        "summary_eer_label": "Cooling COP (EER)",
        "summary_eer_sub": "COP_cool = COP_heat − 1",
        "summary_balance_label": "Energy balance error (TESPy)",
        "summary_balance_sub": "Network balance closure",
        # Tab 4: SciPy
        "scipy_1_title": "1. Finding Required Evaporation Temperature (`scipy.optimize.root_scalar`)",
        "scipy_1_caption": "Check how warm the heat source (air/ground) must be to reach a target COP at the current condensation temperature.",
        "scipy_target_cop": "Target heating COP [-]",
        "scipy_1_success": (
            "To achieve **COP = {cop:.2f}** at $T_{{cond}} = {t_cond:.1f}\\text{{ °C}}$, "
            "the required evaporation temperature is **$T_{{evap}} = {t_evap:.2f}\\text{{ °C}}$** "
            "(compressor power: `{p_comp:.2f} kW`, Brentq iterations: `{iters}`)."
        ),
        "scipy_1_err": "Cannot determine evaporation temperature: {err}",
        "scipy_2_title": "2. Liquid Subcooling Optimization (`scipy.optimize.minimize_scalar`)",
        "scipy_2_caption": (
            "Subcooling improves COP, but is physically limited by the return water temperature from radiators/underfloor heating. "
            "Below you can see the physical optimum."
        ),
        "scipy_return_temp": "Heating system return water temperature [°C]",
        "scipy_2_info": (
            "Optimal subcooling for `{t_ret:.1f} °C` return water "
            "is **$\\Delta T_{{sc,opt}} = {sc_opt:.2f}\\text{{ K}}$** "
            "(effective **COP = {max_cop:.2f}**)."
        ),
        "scipy_2_err": "Subcooling optimization error: {err}",
        "scipy_2_plot_err": "Error plotting subcooling curve: {exc}",
        "scipy_3_title": "3. Efficiency Map COP = f(T_evap, T_cond) (`scipy.interpolate.RegularGridInterpolator`)",
        "scipy_3_caption": (
            "The map shows how strongly COP drops as the temperature lift increases (bottom-right vs top-left). "
            "The red star marks your current operating point."
        ),
        "scipy_3_spinner": "Computing TESPy grid points and SciPy cubic interpolation...",
        "scipy_3_err": "Failed to generate COP sensitivity map: {err}",
        # Tab 5: Glossary
        "glossary_title": "Thermodynamic Terms Compendium",
        "glossary_intro": "Below are the key concepts used when working with heat pumps at our research institute.",
        "glossary_col1_md": (
            "#### 1. COP & Carnot Limit\n"
            "- **COP (Coefficient of Performance):** ratio of heat delivered to the building ($Q_{cond}$) to electrical power consumed ($P_{el}$). `COP = 4.0` means `1 kWh` of electricity yields `4 kWh` of heat (`3 kWh` comes from nature!).\n"
            "- **Carnot Cycle ($COP_{Carnot} = T_{cond} / (T_{cond} - T_{evap})$):** theoretical maximum efficiency for given temperatures (in Kelvin). Real heat pumps typically reach `45–60%` of Carnot (called **exergetic efficiency**).\n"
            "- **Golden rule:** the smaller the temperature lift $\\Delta T_{lift} = T_{cond} - T_{evap}$, the higher the COP. That is why underfloor heating (`35°C`) is much more efficient than radiators (`55°C`).\n\n"
            "#### 2. Superheat ($\\Delta T_{sh}$) & Subcooling ($\\Delta T_{sc}$)\n"
            "- **Superheat:** heating vapor in the evaporator above its boiling point. Protects the compressor from liquid slugging (liquid is incompressible!). Excessive superheat, however, raises discharge temperature $T_2$.\n"
            "- **Subcooling:** cooling condensed liquid below its condensation temperature. Reduces *flash gas* at the expansion valve and increases heat absorbed in the evaporator."
        ),
        "glossary_col2_md": (
            "#### 3. Fluid Properties & Compressor Parameters\n"
            "- **Vapor Quality ($x$):** mass fraction of vapor in a two-phase mixture ($x=0$ is saturated liquid, $x=1$ is saturated vapor). After the throttling valve, typically $x \\approx 0.15\\text{--}0.35$.\n"
            "- **Isentropic Efficiency ($\\eta_s$):** measure of internal compressor losses (friction, flow losses, leakage). For $\\eta_s = 1.0$, compression would be ideally reversible ($s = \\text{const}$).\n"
            "- **Pressure Ratio ($\\Pi = p_2 / p_1$):** ratio of high-side to low-side pressure. High pressure ratio stresses the compressor mechanically and reduces volumetric efficiency.\n\n"
            "#### 4. Refrigerant Selection (GWP & Safety)\n"
            "- **GWP (Global Warming Potential):** greenhouse warming impact relative to CO₂ (= 1). Modern designs transition to ultra-low GWP fluids (e.g., **R290 propane**, **R1234yf**).\n"
            "- **Safety Classes (ASHRAE 34):**\n"
            "  - `A1` — non-toxic, non-flammable (e.g. R134a, R410A)\n"
            "  - `A2L` — non-toxic, mildly flammable (e.g. R32, R1234yf)\n"
            "  - `A3` — non-toxic, highly flammable (e.g. R290, R600a — require safety zones)\n"
            "  - `B2L` — toxic, mildly flammable (e.g. R717 ammonia — industrial systems)"
        ),
        # Education tab UI
        "edu_title": "Heat Pump Academy — Lessons & Cycle Illustrations",
        "edu_intro": (
            "Learn how each component works and what the key thermodynamic coefficients mean. "
            "Select a lesson from the sidebar to explore **theory** and **live impact illustrations (TESPy)**."
        ),
        "edu_select_lesson": "Select a lesson:",
        "edu_theory_header": "1. Theory & Physics",
        "edu_lab_header": "2. Live Impact Illustration (TESPy)",
        "edu_lab_metric_cop": "Heating COP",
        "edu_lab_metric_t2": "Discharge temp. T₂",
        "edu_lab_metric_pcomp": "Compressor power P_el",
        "edu_lab_metric_qevap": "Ambient heat Q_evap",
        "edu_lab_metric_x4": "Flash gas (x₄)",
        "edu_lab_metric_pr": "Pressure ratio Π",
        "edu_lab_metric_carnot": "Carnot COP",
        # cycle_model.py state table & errors
        "col_point": "Point",
        "col_desc": "State description",
        "col_p": "p [bar]",
        "col_T": "T [°C]",
        "col_h": "h [kJ/kg]",
        "col_s": "s [kJ/(kg·K)]",
        "col_x": "x [-]",
        "col_rho": "ρ [kg/m³]",
        "single_phase": "Single-phase",
        "pt1_superheated": "Compressor inlet (superheated vapor)",
        "pt1_saturated": "Compressor inlet (saturated vapor)",
        "pt2_desc": "Compressor outlet (hot vapor)",
        "pt3_subcooled": "Condenser outlet (subcooled liquid)",
        "pt3_saturated": "Condenser outlet (saturated liquid)",
        "pt4_desc": "Evaporator inlet (two-phase mixture)",
        "err_tespy_not_converged": "TESPy network solver failed to converge for the given parameters.",
        # utils.py validation errors
        "val_bad_fluid": "Unsupported refrigerant '{fluid}'. Available: {avail}",
        "val_t_evap_min": "Evaporation temperature ({t_evap:.1f} °C) is too close to the minimum model temperature for {fluid} ({t_min:.1f} °C).",
        "val_t_cond_crit": "Condensation temperature ({t_cond:.1f} °C) exceeds the safe subcritical limit for {fluid} (T_crit = {t_crit:.1f} °C).",
        "val_t_evap_ge_cond": "Evaporation temperature ({t_evap:.1f} °C) must be at least 2 K below condensation temperature ({t_cond:.1f} °C).",
        "val_superheat_range": "Superheat ({sh:.1f} K) must be within [0, 40] K.",
        "val_subcool_range": "Subcooling ({sc:.1f} K) must be within [0, 35] K.",
        "val_subcool_below_evap": "Subcooled liquid temperature after the condenser cannot be lower than evaporation temperature.",
        "val_eta_range": "Compressor isentropic efficiency ({eta:.2f}) must be within [0.1, 1.0].",
        "val_q_cond_pos": "Condenser heating capacity ({q:.2f} kW) must be positive.",
        # optimizer.py
        "opt_empty_bracket": "Evaporation temperature search bracket is empty for the given condensation temperature.",
        "opt_out_of_range": "Target COP = {target:.2f} is outside the achievable range [{cmin:.2f}, {cmax:.2f}] for T_evap in [{low:.1f}, {high:.1f}] °C.",
        "opt_col_tevap": "T_evap [°C]",
        "opt_col_tcond": "T_cond [°C]",
        "opt_col_cop": "COP [-]",
        "opt_col_pcomp": "P_comp [kW]",
        "opt_col_qevap": "Q_evap [kW]",
        # plotting.py
        "plot_pipe_4_evap": "4 → Evaporator (boiling)",
        "plot_pipe_1_suction": "1 (Compressor suction)",
        "plot_pipe_2_hot": "2 (Hot vapor)",
        "plot_pipe_3_liq": "3 (High-pressure liquid)",
        "plot_pipe_4_two": "4 (Two-phase mixture)",
        "plot_hover_pt1": "<b>Point 1: Compressor suction</b><br>T = {T:.1f} °C | p = {p:.2f} bar",
        "plot_hover_pt2": "<b>Point 2: Compressor discharge</b><br>T = {T:.1f} °C | p = {p:.2f} bar",
        "plot_hover_pt3": "<b>Point 3: Condenser outlet</b><br>T = {T:.1f} °C | p = {p:.2f} bar",
        "plot_hover_pt4": "<b>Point 4: Valve outlet</b><br>T = {T:.1f} °C | p = {p:.2f} bar | x = {x:.1f}%",
        "plot_ann_cond": "<b>CONDENSER</b><br><span style='font-size:11px'>Rejects heat</span>",
        "plot_ann_evap": "<b>EVAPORATOR</b><br><span style='font-size:11px'>Absorbs heat</span>",
        "plot_ann_comp": "<b>COMPRESSOR</b>",
        "plot_ann_valve": "<b>VALVE</b>",
        "plot_ann_qcond": "<b>To building</b><br>Q_cond = {q:.2f} kW",
        "plot_ann_qevap": "<b>From nature (free)</b><br>Q_evap = {q:.2f} kW",
        "plot_ann_pcomp": "<b>Electricity</b><br>P_el = {p:.2f} kW",
        "plot_schematic_title": "Heat Pump Cycle Schematic (COP = {cop:.2f})",
        "plot_bal_evap": "Ambient heat Q_evap",
        "plot_bal_comp": "Compressor power P_el",
        "plot_bal_cond": "Heat to building Q_cond",
        "plot_bal_sources": "Energy inputs",
        "plot_bal_output": "Heating output",
        "plot_bal_title": "Energy balance: {q_evap:.2f} kW + {p_comp:.2f} kW = {q_cond:.2f} kW",
        "plot_bal_yaxis": "Thermal / Electrical Power [kW]",
        "plot_dome_name": "Saturation dome (x=0 / x=1)",
        "plot_cycle_name": "Heat pump cycle ({fluid})",
        "plot_ph_title": "log(p)-h (Mollier) Diagram — {fluid}",
        "plot_ph_xaxis": "Specific enthalpy h [kJ/kg]",
        "plot_ph_yaxis": "Pressure p [bar] (log scale)",
        "plot_ts_title": "T-s Diagram — {fluid}",
        "plot_ts_xaxis": "Specific entropy s [kJ/(kg·K)]",
        "plot_ts_yaxis": "Temperature T [°C]",
        "plot_pt_prefix": "Point",
        "plot_current_op": "Current operating point",
        "plot_contour_title": "COP(T_evap, T_cond) Efficiency Map — SciPy Cubic Interpolation",
        "plot_contour_xaxis": "Evaporation temperature T_evap [°C]",
        "plot_contour_yaxis": "Condensation temperature T_cond [°C]",
        "plot_subcool_curve": "Effective COP(ΔT_sc)",
        "plot_subcool_opt": "Optimum ({sc:.2f} K, COP={cop:.2f})",
        "plot_subcool_title": "Subcooling Effect on COP (SciPy Optimization)",
        "plot_subcool_xaxis": "Subcooling ΔT_sc [K]",
        "plot_subcool_yaxis": "Effective COP [-]",
    },
}


def normalize_lang(lang: str | None) -> str:
    """Zwraca znormalizowany kod języka ('pl' lub 'en')."""
    if lang in SUPPORTED_LANGS:
        return lang
    return "pl"


def t(key: str, lang: str = "pl", **kwargs) -> str:
    """Pobiera przetłumaczony tekst dla podanego klucza i języka."""
    norm = normalize_lang(lang)
    text = TRANSLATIONS[norm].get(key)
    if text is None:
        text = TRANSLATIONS["pl"].get(key, key)
    if kwargs:
        return text.format(**kwargs)
    return text
