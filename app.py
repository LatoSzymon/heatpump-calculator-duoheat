"""Interaktywna aplikacja webowa Streamlit do nauki i symulacji obiegu pompy ciepła (TESPy + SciPy)."""

from dataclasses import asdict  #konwersja klasy danych na zwykły słownik. PRzyda się przy cachowaniu
import streamlit as st #Streamlit - odpowiada za generowanie interfejsuwebowego w Pythonie bez htmla PRAKTYCZNA RZECZ

from src.cycle_model import CycleInput, CycleResult, HeatPumpCycle 
from src.i18n import t
from src.optimizer import (
    find_evap_temp_for_target_cop,
    optimize_subcooling,
    run_sensitivity_grid,
)
from src.ui.sidebar import render_sidebar
from src.ui.sim_controls import init_cycle_state, render_simulation_controls
from src.ui.styles import inject_custom_css
from src.ui.tab_education import render_education_page
from src.ui.tabs_simulation import (
    render_charts_tab,
    render_glossary_tab,
    render_kpi_cards,
    render_mechanics_tab,
    render_scipy_tab,
    render_table_tab,
)

st.set_page_config(         #konfigurujemy przeglądarkę przez Streamlit
    page_title=t("page_title", st.session_state.get("lang", "pl")),     #Tytuł idzie od pliku i18n, a ze słownika sesji wyciągamy język - domyślnie pl
    layout="wide",          #rozciąga apkę na całość ekranu
    initial_sidebar_state="auto",   #sidebar domyślnie rozciągnięty na desktopie, a na mobilkach zwinięty
)

inject_custom_css() #wstrzykujemy sobie custom css żeby nie zaśmiecać tu stylami. Można by dać .streamlit/config.toml, ale tam jest mniej opcji


@st.cache_data(show_spinner=False)      #dekorator cache Streamlita. Streamlit wykonuje cay skrypt od góry do dołu po każdym kliknięciu użytkownika (XD) to zapisujemy dzięki temu wyniki funkcji dla danych argumentów. Oszczędność zasobów i czasu. show_spinner to parametr czy pokazywać komunikat ładowania st
def solve_cycle_cached(params_dict: dict, lang: str = "pl") -> CycleResult:     #opakowujemy symulację
    """Buforuje wyniki rozwiązania sieci TESPy dla identycznych parametrów i języka."""
    return HeatPumpCycle(CycleInput(**params_dict), lang=lang).solve(lang=lang)     #rozpakowuje params_dict jako argument do CycleInput. Tworzy model HeatPumpCycle i zwraca kompletny wynik obliczen TESpy. Więcej w definicji

#basal model

@st.cache_data(show_spinner=False)      
def find_evap_temp_cached(params_dict: dict, target_cop: float, lang: str = "pl") -> dict: #wrapper z cachem dla funkcji szukającej temperatury
    return find_evap_temp_for_target_cop(CycleInput(**params_dict), target_cop=target_cop, lang=lang)


@st.cache_data(show_spinner=False)  #wrapper z cachem dla optymalizacji chłodzenia.
def optimize_subcooling_cached(params_dict: dict, pinch_sink_temp_c: float) -> dict:
    return optimize_subcooling(CycleInput(**params_dict), pinch_sink_temp_c=pinch_sink_temp_c)


@st.cache_data(show_spinner=False)  #wrapper z cachem dla najcięższej obliczeniowo funkcji!
def run_sensitivity_grid_cached(    #Generujemy siatkę dla zakresu temperatur parowania i skraplania
    params_dict: dict,              #Krotki dla zakresów gwarantuje ich niezmienność w cache
    t_evap_range: tuple,            #Siatka ma domyślnie 36 pełnych symulacji TESpy
    t_cond_range: tuple,
    n_points: int = 6,
    lang: str = "pl",
) -> dict:
    return run_sensitivity_grid(
        CycleInput(**params_dict),
        t_evap_range=t_evap_range,
        t_cond_range=t_cond_range,
        n_points=n_points,
        lang=lang,
    )


# --- PASEK BOCZNY (JĘZYK + NAWIGACJA) ---
lang, active_section = render_sidebar()     #renderuje pasek boczny i odbiera z niego dwie wartości - jezyk i aktywną sekcję (edu/sym)
init_cycle_state()  #Wpisuje domyślne parametry obiegu do session_state. Stan suwaków nie ginie przy zmianie sekcji

# --- NAGŁÓWEK ---
st.title(t("app_title", lang))  #Nagłówek oraz podtytuł strony w wybranym języku
st.markdown(t("app_subtitle", lang))    

if active_section == "education":   #routing widoku edukacyjnego
    base_input = CycleInput(        #buduje obiekt CycleInput, wyciągając aktualne parametry z session_state
        fluid=st.session_state.get("fluid_code", "R290"),   #nawet gdy na ekranie nie ma suwaków to strona ma dostęp do ostatnio ustawionego obiegu
        t_evap_c=st.session_state.get("t_evap_c", 2.0),
        t_cond_c=st.session_state.get("t_cond_c", 35.0),
        superheat_k=st.session_state.get("superheat_k", 5.0),
        subcooling_k=st.session_state.get("subcooling_k", 4.0),
        eta_s=st.session_state.get("eta_s", 0.78),
        q_cond_kw=st.session_state.get("q_cond_kw", 10.0),
    )
    render_education_page(base_input, lang) #rysujemy część edukacyjną
else:
    # --- PODSTRONA SYMULACJA: KONFIGURACJA OBIEGU + KPI + ZAKŁADKI ---
    cycle_input, limits = render_simulation_controls(lang)  #rysuje panel z suwakami i listą czynników (zwraca gotowe CycleInput oraz słownik limits [limity temp. dla danego czynnika])
    cycle_dict = asdict(cycle_input)    #Zamienia obiekt CycleInput na zwykły słownik, więc można go przekazać do @st,cache_data

    result: CycleResult | None = None   
    simulation_error: str | None = None
    try:
        result = solve_cycle_cached(cycle_dict, lang=lang)  #wywołanie zbuforowanego solvera TESpy
    except ValueError as exc:
        simulation_error = t("err_invalid_params", lang, exc=exc)   #błędy parametrów wejściowych
    except RuntimeError as exc:
        simulation_error = t("err_tespy_converge", lang, exc=exc)   #błędy numeryczne solvera TESpy
    except Exception as exc:
        simulation_error = t("err_unexpected", lang, exc=exc)   #catch-all

    if simulation_error or result is None:
        st.error(simulation_error)  #wyświetla czerwony boks błędu
        st.info(t("err_hint", lang))    #wyświetla hint błędu
    else:
        render_kpi_cards(result, lang)  #Jeśli obliczenia są okej, to rysuje kafelki z wynikami KPI
        st.divider()    #Pozioma linia oddzielająca

        (
            tab_mechanics,
            tab_charts,
            tab_table,
            tab_scipy,
            tab_glossary,
        ) = st.tabs(                        #Tu tworzymy pięć zakładek
            [
                t("tab_mechanics", lang),
                t("tab_charts", lang),
                t("tab_table", lang),
                t("tab_scipy", lang),
                t("tab_glossary", lang),
            ]
        )

        with tab_mechanics:
            render_mechanics_tab(result, cycle_input, lang)   #renderujemy odpowiednie zakładki dla odpowiednich modułów

        with tab_charts:
            render_charts_tab(result, lang)

        with tab_table:
            render_table_tab(result, cycle_input, lang)

        with tab_scipy:     #Tu przekazujemy nasze funkcje z cache jako argumenty. Dependency injection
            render_scipy_tab(   #Wstrzykiwanie zależności, więc sam moduł UI nie musi sam wyliczać logiki cache'owania
                cycle_dict=cycle_dict,
                cycle_input=cycle_input,
                limits=limits,
                lang=lang,
                find_evap_temp_cached=find_evap_temp_cached,
                optimize_subcooling_cached=optimize_subcooling_cached,
                run_sensitivity_grid_cached=run_sensitivity_grid_cached,
            )

        with tab_glossary:
            render_glossary_tab(lang)

# --- STOPKA ---
st.divider()
st.markdown(t("footer_html", lang), unsafe_allow_html=True) #Renderujemy footer. unsafe_allow_html pozwala na własne tagi div, style inline i linki w stopce
