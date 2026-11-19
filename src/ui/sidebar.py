"""Pasek boczny aplikacji: przełącznik języka EN/PL oraz nawigacja (Symulacja / Edukacja z listą lekcji)."""

from typing import Tuple
import streamlit as st

from src.education import LESSONS, get_lesson_text
from src.i18n import SUPPORTED_LANGS, t


def init_nav_state() -> None:
    """Inicjalizuje stan nawigacji i języka w session_state."""
    if "lang" not in st.session_state:
        st.session_state["lang"] = "pl"
    if "active_section" not in st.session_state:
        st.session_state["active_section"] = "simulation"
    if "edu_selected_lesson" not in st.session_state:
        st.session_state["edu_selected_lesson"] = LESSONS[0].id


def _select_simulation() -> None:
    st.session_state["active_section"] = "simulation"


def _select_lesson(lesson_id: str) -> None:
    st.session_state["active_section"] = "education"
    st.session_state["edu_selected_lesson"] = lesson_id


def render_sidebar() -> Tuple[str, str]:
    """Renderuje pasek boczny nawigacji i zwraca `(lang, active_section)`."""
    init_nav_state()

    with st.sidebar:
        lang = st.radio(
            t("lang_label", st.session_state["lang"]),
            options=list(SUPPORTED_LANGS),
            key="lang",
            horizontal=True,
            format_func=lambda code: t(f"lang_{code}", code),
        )

        st.divider()
        st.header(t("nav_header", lang))

        active_section = st.session_state["active_section"]
        sim_type = "primary" if active_section == "simulation" else "secondary"
        if st.button(
            t("nav_simulation", lang),
            key="nav_btn_simulation",
            type=sim_type,
            use_container_width=True,
            on_click=_select_simulation,
        ):
            active_section = "simulation"

        edu_expanded = active_section == "education"
        with st.expander(t("nav_education", lang), expanded=edu_expanded):
            if "edu_completed" in st.session_state:
                done = len(st.session_state["edu_completed"])
                st.caption(t("edu_progress_label", lang, done=done, total=len(LESSONS)))
            for lesson in LESSONS:
                l_title = get_lesson_text(lesson, lang)["title"]
                is_current = (
                    active_section == "education"
                    and st.session_state.get("edu_selected_lesson") == lesson.id
                )
                btn_type = "primary" if is_current else "secondary"
                st.button(
                    l_title,
                    key=f"nav_lesson_{lesson.id}",
                    type=btn_type,
                    use_container_width=True,
                    on_click=_select_lesson,
                    args=(lesson.id,),
                )

    return lang, st.session_state["active_section"]
