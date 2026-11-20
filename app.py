"""Interaktywna aplikacja webowa Streamlit do nauki i symulacji obiegu pompy ciepła (TESPy + SciPy)."""

from dataclasses import asdict
import streamlit as st

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

st.set_page_config(
    page_title=t("page_title", st.session_state.get("lang", "pl")),
    layout="wide",
    initial_sidebar_state="auto",
)

inject_custom_css()


@st.cache_data(show_spinner=False)
def solve_cycle_cached(params_dict: dict, lang: str = "pl") -> CycleResult:
    """Buforuje wyniki rozwiązania sieci TESPy dla identycznych parametrów i języka."""
    return HeatPumpCycle(CycleInput(**params_dict), lang=lang).solve(lang=lang)


@st.cache_data(show_spinner=False)
def find_evap_temp_cached(
    params_dict: dict, target_cop: float, lang: str = "pl"
) -> dict:
    return find_evap_temp_for_target_cop(
        CycleInput(**params_dict), target_cop=target_cop, lang=lang
    )


@st.cache_data(show_spinner=False)
def optimize_subcooling_cached(params_dict: dict, pinch_sink_temp_c: float) -> dict:
    return optimize_subcooling(
        CycleInput(**params_dict), pinch_sink_temp_c=pinch_sink_temp_c
    )


@st.cache_data(show_spinner=False)
def run_sensitivity_grid_cached(
    params_dict: dict,
    t_evap_range: tuple,
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
lang, active_section = render_sidebar()
init_cycle_state()

# --- NAGŁÓWEK ---
st.markdown(
    f"""
    <div class="app-hero">
        <div class="app-brand-badge">{t("brand_badge", lang)}</div>
        <h1 class="app-hero-title">{t("app_title", lang)}</h1>
        <p class="app-hero-subtitle">{t("app_subtitle", lang)}</p>
    </div>
    """,
    unsafe_allow_html=True,
)

if active_section == "education":
    base_input = CycleInput(
        fluid=st.session_state.get("fluid_code", "R290"),
        t_evap_c=st.session_state.get("t_evap_c", 2.0),
        t_cond_c=st.session_state.get("t_cond_c", 35.0),
        superheat_k=st.session_state.get("superheat_k", 5.0),
        subcooling_k=st.session_state.get("subcooling_k", 4.0),
        eta_s=st.session_state.get("eta_s", 0.78),
        q_cond_kw=st.session_state.get("q_cond_kw", 10.0),
    )
    render_education_page(base_input, lang)
else:
    # --- PODSTRONA SYMULACJA: KONFIGURACJA OBIEGU + KPI + ZAKŁADKI ---
    cycle_input, limits = render_simulation_controls(lang)
    cycle_dict = asdict(cycle_input)

    result: CycleResult | None = None
    simulation_error: str | None = None
    try:
        result = solve_cycle_cached(cycle_dict, lang=lang)
    except ValueError as exc:
        simulation_error = t("err_invalid_params", lang, exc=exc)
    except RuntimeError as exc:
        simulation_error = t("err_tespy_converge", lang, exc=exc)
    except Exception as exc:
        simulation_error = t("err_unexpected", lang, exc=exc)

    if simulation_error or result is None:
        st.error(simulation_error)
        st.info(t("err_hint", lang))
    else:
        render_kpi_cards(result, lang)

        (
            tab_mechanics,
            tab_charts,
            tab_table,
            tab_scipy,
            tab_glossary,
        ) = st.tabs(
            [
                t("tab_mechanics", lang),
                t("tab_charts", lang),
                t("tab_table", lang),
                t("tab_scipy", lang),
                t("tab_glossary", lang),
            ]
        )

        with tab_mechanics:
            render_mechanics_tab(result, cycle_input, lang)

        with tab_charts:
            render_charts_tab(result, lang)

        with tab_table:
            render_table_tab(result, cycle_input, lang)

        with tab_scipy:
            render_scipy_tab(
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
st.markdown(t("footer_html", lang), unsafe_allow_html=True)
