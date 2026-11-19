"""Panel boczny aplikacji: przełącznik języka EN/PL oraz konfiguracja parametrów obiegu."""

from typing import Tuple
import streamlit as st

from src.cycle_model import CycleInput
from src.i18n import SUPPORTED_LANGS, t
from src.utils import (
    REFRIGERANTS,
    SCENARIO_PRESETS,
    get_fluid_limits,
    get_preset_text,
    get_refrigerant_text,
)


def _apply_preset(preset_id: str) -> None:
    """Zapisuje wartości wybranego scenariusza do session_state."""
    if preset_id in SCENARIO_PRESETS:
        p = SCENARIO_PRESETS[preset_id]
        st.session_state["fluid_code"] = p.fluid
        st.session_state["t_evap_c"] = p.t_evap_c
        st.session_state["t_cond_c"] = p.t_cond_c
        st.session_state["superheat_k"] = p.superheat_k
        st.session_state["subcooling_k"] = p.subcooling_k
        st.session_state["eta_s"] = p.eta_s
        st.session_state["q_cond_kw"] = p.q_cond_kw


def _on_preset_change() -> None:
    """Callback wywoływany przy zmianie gotowego scenariusza."""
    preset_id = st.session_state.get("selected_preset", "custom")
    if preset_id != "custom":
        _apply_preset(preset_id)


def _mark_custom() -> None:
    """Przełącza etykietę scenariusza na ustawienia własne po ręcznej zmianie suwaka."""
    st.session_state["selected_preset"] = "custom"


def init_sidebar_state() -> None:
    """Inicjalizuje domyślny język oraz domyślny scenariusz przy pierwszym uruchomieniu."""
    if "lang" not in st.session_state:
        st.session_state["lang"] = "pl"
    if "selected_preset" not in st.session_state:
        st.session_state["selected_preset"] = "air_floor_spring"
        _apply_preset("air_floor_spring")


def render_sidebar() -> Tuple[str, CycleInput, dict]:
    """Renderuje panel boczny i zwraca `(lang, CycleInput, fluid_limits)`."""
    init_sidebar_state()

    with st.sidebar:
        lang = st.radio(
            t("lang_label", st.session_state["lang"]),
            options=list(SUPPORTED_LANGS),
            key="lang",
            horizontal=True,
            format_func=lambda code: t(f"lang_{code}", code),
        )

        st.divider()
        st.header(t("sidebar_header", lang))

        preset_options = ["custom"] + list(SCENARIO_PRESETS.keys())
        selected_preset = st.selectbox(
            t("preset_label", lang),
            options=preset_options,
            key="selected_preset",
            on_change=_on_preset_change,
            format_func=lambda k: (
                t("preset_custom", lang)
                if k == "custom"
                else get_preset_text(k, lang)["label"]
            ),
            help=t("preset_help", lang),
        )

        if selected_preset != "custom":
            st.info(get_preset_text(selected_preset, lang)["explanation"])

        st.divider()

        fluid_keys = list(REFRIGERANTS.keys())
        fluid_code = st.selectbox(
            t("fluid_label", lang),
            options=fluid_keys,
            format_func=lambda k: (
                f"{get_refrigerant_text(k, lang)['name']} "
                f"[{REFRIGERANTS[k].safety_group}, GWP={REFRIGERANTS[k].gwp}]"
            ),
            key="fluid_code",
            on_change=_mark_custom,
            help=t("fluid_help", lang),
        )

        ref_info = REFRIGERANTS[fluid_code]
        ref_text = get_refrigerant_text(fluid_code, lang)
        try:
            limits = get_fluid_limits(fluid_code)
        except Exception as exc:
            st.error(t("fluid_limit_error", lang, fluid=fluid_code, exc=exc))
            limits = {"T_crit_C": 95.0, "p_crit_bar": 40.0, "T_min_C": -50.0}

        st.caption(
            t(
                "fluid_meta",
                lang,
                formula=ref_info.chemical_formula,
                t_crit=limits["T_crit_C"],
                p_crit=limits["p_crit_bar"],
                desc=ref_text["description"],
            )
        )

        st.divider()
        st.subheader(t("source_temps_header", lang))

        t_evap_c = st.slider(
            t("t_evap_label", lang),
            min_value=-25.0,
            max_value=20.0,
            step=0.5,
            key="t_evap_c",
            on_change=_mark_custom,
            help=t("t_evap_help", lang),
        )

        min_cond_safe = max(20.0, t_evap_c + 5.0)
        max_cond_safe = max(
            min_cond_safe + 1.0, min(85.0, float(int(limits["T_crit_C"] - 5.0)))
        )
        if st.session_state.get("t_cond_c", 35.0) < min_cond_safe:
            st.session_state["t_cond_c"] = min_cond_safe
        elif st.session_state.get("t_cond_c", 35.0) > max_cond_safe:
            st.session_state["t_cond_c"] = max_cond_safe

        t_cond_c = st.slider(
            t("t_cond_label", lang),
            min_value=min_cond_safe,
            max_value=max_cond_safe,
            step=0.5,
            key="t_cond_c",
            on_change=_mark_custom,
            help=t("t_cond_help", lang),
        )

        st.subheader(t("cycle_comp_header", lang))

        superheat_k = st.slider(
            t("superheat_label", lang),
            min_value=0.0,
            max_value=20.0,
            step=0.5,
            key="superheat_k",
            on_change=_mark_custom,
            help=t("superheat_help", lang),
        )

        max_subcool_safe = max(
            0.5, min(20.0, float(int((t_cond_c - t_evap_c - 1.0) * 2)) / 2.0)
        )
        if st.session_state.get("subcooling_k", 4.0) > max_subcool_safe:
            st.session_state["subcooling_k"] = max_subcool_safe

        subcooling_k = st.slider(
            t("subcooling_label", lang),
            min_value=0.0,
            max_value=max_subcool_safe,
            step=0.5,
            key="subcooling_k",
            on_change=_mark_custom,
            help=t("subcooling_help", lang),
        )

        eta_s = st.slider(
            t("eta_s_label", lang),
            min_value=0.45,
            max_value=0.95,
            step=0.01,
            key="eta_s",
            on_change=_mark_custom,
            help=t("eta_s_help", lang),
        )

        q_cond_kw = st.number_input(
            t("q_cond_label", lang),
            min_value=1.0,
            max_value=500.0,
            step=0.5,
            key="q_cond_kw",
            on_change=_mark_custom,
            help=t("q_cond_help", lang),
        )

    cycle_input = CycleInput(
        fluid=fluid_code,
        t_evap_c=t_evap_c,
        t_cond_c=t_cond_c,
        superheat_k=superheat_k,
        subcooling_k=subcooling_k,
        eta_s=eta_s,
        q_cond_kw=q_cond_kw,
    )
    return lang, cycle_input, limits
