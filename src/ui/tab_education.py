"""Zakładka Edukacja: ustrukturyzowane lekcje, mini-laboratoria TESPy na żywo i interaktywne testy."""

from typing import Callable, Dict, List
import streamlit as st

from src.cycle_model import CycleInput, CycleResult, HeatPumpCycle
from src.education import LESSONS, Lesson, get_lesson_text, get_question_text
from src.i18n import normalize_lang, t
from src.utils import REFRIGERANTS


def _solve_lab_cycle(inp: CycleInput, lang: str) -> CycleResult:
    """Pomocniczo rozwiązuje obieg dla mini-laboratorium edukacyjnego."""
    return HeatPumpCycle(inp, lang=lang).solve(lang=lang)


def _render_mini_lab(lesson: Lesson, base_input: CycleInput, lang: str) -> None:
    """Renderuje interaktywne mini-laboratorium TESPy dopasowane do wybranej lekcji."""
    is_en = normalize_lang(lang) == "en"
    lab = lesson.lab_type

    if lab == "superheat_lab":
        sh_val = st.slider(
            "Test ΔT_sh [K]" if is_en else "Przetestuj przegrzanie ΔT_sh [K]",
            min_value=0.0,
            max_value=18.0,
            value=5.0,
            step=1.0,
            key="edu_lab_sh",
        )
        res_ref = _solve_lab_cycle(
            CycleInput(fluid=base_input.fluid, t_evap_c=0.0, t_cond_c=45.0, superheat_k=0.0, subcooling_k=4.0),
            lang,
        )
        res_cur = _solve_lab_cycle(
            CycleInput(fluid=base_input.fluid, t_evap_c=0.0, t_cond_c=45.0, superheat_k=sh_val, subcooling_k=4.0),
            lang,
        )
        c1, c2, c3 = st.columns(3)
        c1.metric(
            t("edu_lab_metric_t2", lang),
            f"{res_cur.t_discharge_c:.1f} °C",
            delta=f"{res_cur.t_discharge_c - res_ref.t_discharge_c:+.1f} K vs ΔT_sh=0",
            delta_color="inverse",
        )
        c2.metric(
            "T₁ (ssanie)" if not is_en else "T₁ (suction)",
            f"{res_cur.t_1_c:.1f} °C",
            delta=f"{res_cur.t_1_c - res_ref.t_1_c:+.1f} K",
        )
        c3.metric(
            t("edu_lab_metric_cop", lang),
            f"{res_cur.cop_heating:.2f}",
            delta=f"{res_cur.cop_heating - res_ref.cop_heating:+.3f}",
        )
        if sh_val < 2.0:
            st.warning(
                "Uwaga: przy ΔT_sh < 2 K w rzeczywistej sprężarce istnieje ryzyko zassania kropel cieczy!"
                if not is_en
                else "Warning: at ΔT_sh < 2 K a real compressor risks ingesting liquid droplets!"
            )

    elif lab == "compressor_lab":
        eta_val = st.slider(
            "Test η_s [-]" if is_en else "Przetestuj sprawność izentropową η_s [-]",
            min_value=0.50,
            max_value=0.95,
            value=0.75,
            step=0.05,
            key="edu_lab_eta",
        )
        res_ideal = _solve_lab_cycle(
            CycleInput(fluid=base_input.fluid, t_evap_c=0.0, t_cond_c=45.0, eta_s=1.0),
            lang,
        )
        res_cur = _solve_lab_cycle(
            CycleInput(fluid=base_input.fluid, t_evap_c=0.0, t_cond_c=45.0, eta_s=eta_val),
            lang,
        )
        c1, c2, c3, c4 = st.columns(4)
        c1.metric(t("edu_lab_metric_cop", lang), f"{res_cur.cop_heating:.2f}", delta=f"{res_cur.cop_heating - res_ideal.cop_heating:+.2f} vs η_s=1")
        c2.metric(t("edu_lab_metric_pcomp", lang), f"{res_cur.p_comp_kw:.2f} kW", delta=f"{res_cur.p_comp_kw - res_ideal.p_comp_kw:+.2f} kW", delta_color="inverse")
        c3.metric(t("edu_lab_metric_t2", lang), f"{res_cur.t_discharge_c:.1f} °C", delta=f"{res_cur.t_discharge_c - res_ideal.t_discharge_c:+.1f} K", delta_color="inverse")
        c4.metric(t("edu_lab_metric_pr", lang), f"{res_cur.pressure_ratio:.2f}")

    elif lab == "subcooling_lab":
        sc_val = st.slider(
            "Test ΔT_sc [K]" if is_en else "Przetestuj dochłodzenie ΔT_sc [K]",
            min_value=0.0,
            max_value=15.0,
            value=5.0,
            step=1.0,
            key="edu_lab_sc",
        )
        res_0 = _solve_lab_cycle(
            CycleInput(fluid=base_input.fluid, t_evap_c=0.0, t_cond_c=45.0, subcooling_k=0.0),
            lang,
        )
        res_cur = _solve_lab_cycle(
            CycleInput(fluid=base_input.fluid, t_evap_c=0.0, t_cond_c=45.0, subcooling_k=sc_val),
            lang,
        )
        c1, c2, c3 = st.columns(3)
        c1.metric(
            t("edu_lab_metric_x4", lang),
            f"{res_cur.x_4 * 100:.1f} %",
            delta=f"{(res_cur.x_4 - res_0.x_4) * 100:+.1f} pp",
            delta_color="inverse",
        )
        c2.metric(
            t("edu_lab_metric_qevap", lang),
            f"{res_cur.q_evap_kw:.2f} kW",
            delta=f"{res_cur.q_evap_kw - res_0.q_evap_kw:+.2f} kW",
        )
        c3.metric(
            t("edu_lab_metric_cop", lang),
            f"{res_cur.cop_heating:.2f}",
            delta=f"{res_cur.cop_heating - res_0.cop_heating:+.3f}",
        )

    elif lab == "valve_lab":
        t_cond_val = st.slider(
            "Test T_cond [°C]" if is_en else "Zmień T_cond [°C] i zobacz wpływ na flash gas (x₄)",
            min_value=30.0,
            max_value=65.0,
            value=45.0,
            step=5.0,
            key="edu_lab_valve_tcond",
        )
        res_cur = _solve_lab_cycle(
            CycleInput(fluid=base_input.fluid, t_evap_c=0.0, t_cond_c=t_cond_val, subcooling_k=4.0),
            lang,
        )
        c1, c2, c3 = st.columns(3)
        c1.metric(t("edu_lab_metric_x4", lang), f"{res_cur.x_4 * 100:.1f} %")
        c2.metric("T₃ → T₄", f"{res_cur.t_3_c:.1f} °C → {res_cur.t_4_c:.1f} °C")
        c3.metric(t("edu_lab_metric_pr", lang), f"{res_cur.pressure_ratio:.2f}")

    elif lab == "carnot_lab":
        t_cond_val = st.radio(
            "Select emitter:" if is_en else "Wybierz system grzewczy:",
            options=[35.0, 55.0],
            horizontal=True,
            format_func=lambda v: (
                f"Underfloor ({v:.0f}°C)" if is_en and v == 35.0
                else f"Radiators ({v:.0f}°C)" if is_en
                else f"Podłogówka ({v:.0f}°C)" if v == 35.0
                else f"Grzejniki ({v:.0f}°C)"
            ),
            key="edu_lab_carnot_mode",
        )
        res_cur = _solve_lab_cycle(
            CycleInput(fluid=base_input.fluid, t_evap_c=0.0, t_cond_c=t_cond_val, q_cond_kw=10.0),
            lang,
        )
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("ΔT_lift", f"{res_cur.delta_t_lift_k:.0f} K")
        c2.metric(t("edu_lab_metric_carnot", lang), f"{res_cur.cop_carnot:.2f}")
        c3.metric(t("edu_lab_metric_cop", lang), f"{res_cur.cop_heating:.2f}")
        c4.metric(t("edu_lab_metric_pcomp", lang), f"{res_cur.p_comp_kw:.2f} kW")

    elif lab == "refrigerant_lab":
        col_a, col_b = st.columns(2)
        fluid_keys = list(REFRIGERANTS.keys())
        f1 = col_a.selectbox("Fluid A" if is_en else "Czynnik A", options=fluid_keys, index=0, key="edu_ref_a")
        f2 = col_b.selectbox("Fluid B" if is_en else "Czynnik B", options=fluid_keys, index=6, key="edu_ref_b")
        r1 = _solve_lab_cycle(CycleInput(fluid=f1, t_evap_c=0.0, t_cond_c=45.0), lang)
        r2 = _solve_lab_cycle(CycleInput(fluid=f2, t_evap_c=0.0, t_cond_c=45.0), lang)
        with col_a:
            st.info(
                f"**{f1}** (`{REFRIGERANTS[f1].safety_group}`, GWP={REFRIGERANTS[f1].gwp})\n\n"
                f"- COP: `{r1.cop_heating:.2f}` | T₂: `{r1.t_discharge_c:.1f} °C`\n"
                f"- p₁/p₂: `{r1.p_evap_bar:.1f} / {r1.p_cond_bar:.1f} bar` (Π={r1.pressure_ratio:.2f})"
            )
        with col_b:
            st.info(
                f"**{f2}** (`{REFRIGERANTS[f2].safety_group}`, GWP={REFRIGERANTS[f2].gwp})\n\n"
                f"- COP: `{r2.cop_heating:.2f}` | T₂: `{r2.t_discharge_c:.1f} °C`\n"
                f"- p₁/p₂: `{r2.p_evap_bar:.1f} / {r2.p_cond_bar:.1f} bar` (Π={r2.pressure_ratio:.2f})"
            )


def render_education_tab(base_input: CycleInput, lang: str) -> None:
    """Renderuje zakładkę Edukacja z paskiem postępu, lekcjami, laboratorium i quizami."""
    st.subheader(t("edu_title", lang))
    st.markdown(t("edu_intro", lang))

    if "edu_completed" not in st.session_state:
        st.session_state["edu_completed"] = set()
    if "edu_checked" not in st.session_state:
        st.session_state["edu_checked"] = {}

    completed_count = len(st.session_state["edu_completed"])
    total_lessons = len(LESSONS)
    st.progress(completed_count / total_lessons)
    st.caption(t("edu_progress_label", lang, done=completed_count, total=total_lessons))

    lesson_map: Dict[str, Lesson] = {lesson.id: lesson for lesson in LESSONS}
    selected_id = st.selectbox(
        t("edu_select_lesson", lang),
        options=list(lesson_map.keys()),
        key="edu_selected_lesson",
        format_func=lambda lid: get_lesson_text(lesson_map[lid], lang)["title"],
    )

    lesson = lesson_map[selected_id]
    l_txt = get_lesson_text(lesson, lang)

    st.markdown(f"### {l_txt['title']}")
    st.caption(l_txt["subtitle"])

    # 1. Teoria
    with st.container(border=True):
        st.markdown(f"#### {t('edu_theory_header', lang)}")
        st.markdown(l_txt["theory"])

    # 2. Mini-laboratorium na żywo
    with st.container(border=True):
        st.markdown(f"#### {t('edu_lab_header', lang)}")
        try:
            _render_mini_lab(lesson, base_input, lang)
        except Exception as exc:
            st.warning(f"Lab error: {exc}")

    # 3. Interaktywny test wiedzy
    with st.container(border=True):
        st.markdown(f"#### {t('edu_quiz_header', lang)}")

        user_answers: Dict[str, int] = {}
        for idx, q in enumerate(lesson.questions, start=1):
            q_txt = get_question_text(q, lang)
            options: List[str] = q_txt["options"]  # type: ignore[assignment]
            choice_idx = st.radio(
                f"**{idx}. {q_txt['prompt']}**",
                options=list(range(len(options))),
                format_func=lambda i, opts=options: opts[i],
                key=f"quiz_{lesson.id}_{q.id}",
            )
            user_answers[q.id] = choice_idx

        btn_col1, btn_col2 = st.columns([1, 1])
        if btn_col1.button(t("edu_check_btn", lang), key=f"check_{lesson.id}", type="primary"):
            st.session_state["edu_checked"][lesson.id] = True
            score = sum(
                1 for q in lesson.questions if user_answers[q.id] == q.correct_idx
            )
            if score >= 1:
                st.session_state["edu_completed"].add(lesson.id)

        if btn_col2.button(t("edu_reset_btn", lang), key=f"reset_{lesson.id}"):
            st.session_state["edu_checked"][lesson.id] = False
            st.session_state["edu_completed"].discard(lesson.id)

        if st.session_state["edu_checked"].get(lesson.id, False):
            score = sum(
                1 for q in lesson.questions if user_answers[q.id] == q.correct_idx
            )
            total_q = len(lesson.questions)
            st.info(t("edu_score_banner", lang, score=score, total=total_q))
            if score == total_q:
                st.success(t("edu_perfect", lang))

            for idx, q in enumerate(lesson.questions, start=1):
                q_txt = get_question_text(q, lang)
                options = q_txt["options"]  # type: ignore[assignment]
                if user_answers[q.id] == q.correct_idx:
                    st.success(f"**{idx}.** {t('edu_answer_correct', lang)}")
                else:
                    st.error(
                        f"**{idx}.** {t('edu_answer_wrong', lang, correct=options[q.correct_idx])}"
                    )
                st.markdown(f"{t('edu_explanation_prefix', lang)} {q_txt['explanation']}")
