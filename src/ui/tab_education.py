"""Podstrona Edukacja: lekcje z ilustracjami wpływu (TESPy + Plotly) oraz wydzielony quiz."""

from typing import Dict, List
import numpy as np
import plotly.graph_objects as go
import streamlit as st

from src.cycle_model import CycleInput, CycleResult, HeatPumpCycle
from src.education import LESSONS, Lesson, get_lesson_text, get_question_text
from src.i18n import normalize_lang, t
from src.utils import REFRIGERANTS


@st.cache_data(show_spinner=False)
def _solve_lab_cycle_cached(
    fluid: str,
    t_evap_c: float,
    t_cond_c: float,
    superheat_k: float = 5.0,
    subcooling_k: float = 4.0,
    eta_s: float = 0.78,
    q_cond_kw: float = 10.0,
    lang: str = "pl",
) -> CycleResult:
    """Buforowane wywołanie solvera TESPy dla ilustracji edukacyjnych."""
    inp = CycleInput(
        fluid=fluid,
        t_evap_c=t_evap_c,
        t_cond_c=t_cond_c,
        superheat_k=superheat_k,
        subcooling_k=subcooling_k,
        eta_s=eta_s,
        q_cond_kw=q_cond_kw,
    )
    return HeatPumpCycle(inp, lang=lang).solve(lang=lang)


def _base_layout(fig: go.Figure, title: str, x_title: str, y_title: str) -> go.Figure:
    fig.update_layout(
        title=dict(text=title, font=dict(size=14)),
        xaxis_title=x_title,
        yaxis_title=y_title,
        height=320,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=45, r=20, t=45, b=45),
        legend=dict(orientation="h", yanchor="top", y=-0.22, xanchor="center", x=0.5),
    )
    return fig


def _render_mini_lab(lesson: Lesson, base_input: CycleInput, lang: str) -> None:
    """Renderuje ilustrację wpływu (metryki + wykres Plotly z TESPy) dla wybranej lekcji."""
    is_en = normalize_lang(lang) == "en"
    lab = lesson.lab_type
    fluid = base_input.fluid

    if lab == "superheat_lab":
        sh_val = st.slider(
            "Test ΔT_sh [K]" if is_en else "Przetestuj przegrzanie ΔT_sh [K]",
            min_value=0.0,
            max_value=18.0,
            value=5.0,
            step=1.0,
            key="edu_lab_sh",
        )
        res_ref = _solve_lab_cycle_cached(fluid, 0.0, 45.0, superheat_k=0.0, subcooling_k=4.0, lang=lang)
        res_cur = _solve_lab_cycle_cached(fluid, 0.0, 45.0, superheat_k=sh_val, subcooling_k=4.0, lang=lang)

        c1, c2, c3 = st.columns(3)
        c1.metric(
            t("edu_lab_metric_t2", lang),
            f"{res_cur.t_discharge_c:.1f} °C",
            delta=f"{res_cur.t_discharge_c - res_ref.t_discharge_c:+.1f} K vs ΔT_sh=0",
            delta_color="inverse",
        )
        c2.metric(
            "T1 (suction)" if is_en else "T1 (ssanie)",
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
                "Warning: at ΔT_sh < 2 K a real compressor risks ingesting liquid droplets."
                if is_en
                else "Uwaga: przy ΔT_sh < 2 K w rzeczywistej sprężarce istnieje ryzyko zassania kropel cieczy."
            )

        sh_grid = np.linspace(0.0, 18.0, 10)
        t2_grid = [_solve_lab_cycle_cached(fluid, 0.0, 45.0, superheat_k=float(s), subcooling_k=4.0, lang=lang).t_discharge_c for s in sh_grid]
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=sh_grid, y=t2_grid, mode="lines+markers", name="T2 [°C]", line=dict(color="#EF4444", width=3)))
        fig.add_trace(go.Scatter(x=[sh_val], y=[res_cur.t_discharge_c], mode="markers", name="Selected" if is_en else "Wybrany punkt", marker=dict(size=12, color="#38BDF8", symbol="diamond")))
        _base_layout(
            fig,
            "Impact of Superheat ΔT_sh on Discharge Temperature T2" if is_en else "Wpływ przegrzania ΔT_sh na temperaturę tłoczenia T2",
            "ΔT_sh [K]",
            "T2 [°C]",
        )
        st.plotly_chart(fig, width="stretch", theme="streamlit", config={"displayModeBar": False})

    elif lab == "compressor_lab":
        eta_val = st.slider(
            "Test η_s [-]" if is_en else "Przetestuj sprawność izentropową η_s [-]",
            min_value=0.50,
            max_value=0.95,
            value=0.75,
            step=0.05,
            key="edu_lab_eta",
        )
        res_ideal = _solve_lab_cycle_cached(fluid, 0.0, 45.0, eta_s=1.0, lang=lang)
        res_cur = _solve_lab_cycle_cached(fluid, 0.0, 45.0, eta_s=eta_val, lang=lang)

        c1, c2, c3, c4 = st.columns(4)
        c1.metric(t("edu_lab_metric_cop", lang), f"{res_cur.cop_heating:.2f}", delta=f"{res_cur.cop_heating - res_ideal.cop_heating:+.2f} vs η_s=1")
        c2.metric(t("edu_lab_metric_pcomp", lang), f"{res_cur.p_comp_kw:.2f} kW", delta=f"{res_cur.p_comp_kw - res_ideal.p_comp_kw:+.2f} kW", delta_color="inverse")
        c3.metric(t("edu_lab_metric_t2", lang), f"{res_cur.t_discharge_c:.1f} °C", delta=f"{res_cur.t_discharge_c - res_ideal.t_discharge_c:+.1f} K", delta_color="inverse")
        c4.metric(t("edu_lab_metric_pr", lang), f"{res_cur.pressure_ratio:.2f}")

        eta_grid = np.linspace(0.50, 0.95, 10)
        cop_grid = [_solve_lab_cycle_cached(fluid, 0.0, 45.0, eta_s=float(e), lang=lang).cop_heating for e in eta_grid]
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=eta_grid, y=cop_grid, mode="lines+markers", name="COP [-]", line=dict(color="#F97316", width=3)))
        fig.add_trace(go.Scatter(x=[eta_val], y=[res_cur.cop_heating], mode="markers", name="Selected" if is_en else "Wybrany punkt", marker=dict(size=12, color="#38BDF8", symbol="diamond")))
        _base_layout(
            fig,
            "Impact of Isentropic Efficiency η_s on COP" if is_en else "Wpływ sprawności izentropowej η_s na COP",
            "η_s [-]",
            "COP [-]",
        )
        st.plotly_chart(fig, width="stretch", theme="streamlit", config={"displayModeBar": False})

    elif lab == "subcooling_lab":
        sc_val = st.slider(
            "Test ΔT_sc [K]" if is_en else "Przetestuj dochłodzenie ΔT_sc [K]",
            min_value=0.0,
            max_value=15.0,
            value=5.0,
            step=1.0,
            key="edu_lab_sc",
        )
        res_0 = _solve_lab_cycle_cached(fluid, 0.0, 45.0, subcooling_k=0.0, lang=lang)
        res_cur = _solve_lab_cycle_cached(fluid, 0.0, 45.0, subcooling_k=sc_val, lang=lang)

        c1, c2, c3 = st.columns(3)
        c1.metric(t("edu_lab_metric_x4", lang), f"{res_cur.x_4 * 100:.1f} %", delta=f"{(res_cur.x_4 - res_0.x_4) * 100:+.1f} pp", delta_color="inverse")
        c2.metric(t("edu_lab_metric_qevap", lang), f"{res_cur.q_evap_kw:.2f} kW", delta=f"{res_cur.q_evap_kw - res_0.q_evap_kw:+.2f} kW")
        c3.metric(t("edu_lab_metric_cop", lang), f"{res_cur.cop_heating:.2f}", delta=f"{res_cur.cop_heating - res_0.cop_heating:+.3f}")

        sc_grid = np.linspace(0.0, 15.0, 10)
        cop_grid = [_solve_lab_cycle_cached(fluid, 0.0, 45.0, subcooling_k=float(s), lang=lang).cop_heating for s in sc_grid]
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=sc_grid, y=cop_grid, mode="lines+markers", name="COP [-]", line=dict(color="#22C55E", width=3)))
        fig.add_trace(go.Scatter(x=[sc_val], y=[res_cur.cop_heating], mode="markers", name="Selected" if is_en else "Wybrany punkt", marker=dict(size=12, color="#EF4444", symbol="diamond")))
        _base_layout(
            fig,
            "Impact of Subcooling ΔT_sc on COP (at fixed T_cond)" if is_en else "Wpływ dochłodzenia ΔT_sc na COP (przy stałym T_cond)",
            "ΔT_sc [K]",
            "COP [-]",
        )
        st.plotly_chart(fig, width="stretch", theme="streamlit", config={"displayModeBar": False})

    elif lab == "valve_lab":
        t_cond_val = st.slider(
            "Test T_cond [°C]" if is_en else "Zmień T_cond [°C] i zobacz wpływ na flash gas (x4)",
            min_value=30.0,
            max_value=65.0,
            value=45.0,
            step=5.0,
            key="edu_lab_valve_tcond",
        )
        res_cur = _solve_lab_cycle_cached(fluid, 0.0, t_cond_val, subcooling_k=4.0, lang=lang)
        c1, c2, c3 = st.columns(3)
        c1.metric(t("edu_lab_metric_x4", lang), f"{res_cur.x_4 * 100:.1f} %")
        c2.metric("T3 -> T4", f"{res_cur.t_3_c:.1f} °C -> {res_cur.t_4_c:.1f} °C")
        c3.metric(t("edu_lab_metric_pr", lang), f"{res_cur.pressure_ratio:.2f}")

        tc_grid = np.linspace(30.0, 65.0, 8)
        x4_grid = [_solve_lab_cycle_cached(fluid, 0.0, float(tc), subcooling_k=4.0, lang=lang).x_4 * 100.0 for tc in tc_grid]
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=tc_grid, y=x4_grid, mode="lines+markers", name="Flash gas x4 [%]", line=dict(color="#0EA5E9", width=3)))
        fig.add_trace(go.Scatter(x=[t_cond_val], y=[res_cur.x_4 * 100.0], mode="markers", name="Selected" if is_en else "Wybrany punkt", marker=dict(size=12, color="#EF4444", symbol="diamond")))
        _base_layout(
            fig,
            "Flash Gas Fraction x4 vs Condensing Temperature T_cond" if is_en else "Udział pary rozprężnej x4 w zależności od T_cond",
            "T_cond [°C]",
            "x4 [%]",
        )
        st.plotly_chart(fig, width="stretch", theme="streamlit", config={"displayModeBar": False})

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
        res_cur = _solve_lab_cycle_cached(fluid, 0.0, t_cond_val, q_cond_kw=10.0, lang=lang)
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("ΔT_lift", f"{res_cur.delta_t_lift_k:.0f} K")
        c2.metric(t("edu_lab_metric_carnot", lang), f"{res_cur.cop_carnot:.2f}")
        c3.metric(t("edu_lab_metric_cop", lang), f"{res_cur.cop_heating:.2f}")
        c4.metric(t("edu_lab_metric_pcomp", lang), f"{res_cur.p_comp_kw:.2f} kW")

        tc_grid = np.linspace(30.0, 65.0, 8)
        results = [_solve_lab_cycle_cached(fluid, 0.0, float(tc), q_cond_kw=10.0, lang=lang) for tc in tc_grid]
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=tc_grid, y=[r.cop_carnot for r in results], mode="lines+markers", name="COP Carnot", line=dict(color="#94A3B8", width=2, dash="dash")))
        fig.add_trace(go.Scatter(x=tc_grid, y=[r.cop_heating for r in results], mode="lines+markers", name="COP (TESPy)", line=dict(color="#EF4444", width=3)))
        fig.add_trace(go.Scatter(x=[t_cond_val], y=[res_cur.cop_heating], mode="markers", name="Selected" if is_en else "Wybrany system", marker=dict(size=12, color="#38BDF8", symbol="diamond")))
        _base_layout(
            fig,
            "Real COP vs Carnot Limit (T_evap = 0°C)" if is_en else "Rzeczywiste COP na tle granicy Carnota (T_evap = 0°C)",
            "T_cond [°C]",
            "COP [-]",
        )
        st.plotly_chart(fig, width="stretch", theme="streamlit", config={"displayModeBar": False})

    elif lab == "refrigerant_lab":
        col_a, col_b = st.columns(2)
        fluid_keys = list(REFRIGERANTS.keys())
        f1 = col_a.selectbox("Fluid A" if is_en else "Czynnik A", options=fluid_keys, index=0, key="edu_ref_a")
        f2 = col_b.selectbox("Fluid B" if is_en else "Czynnik B", options=fluid_keys, index=6, key="edu_ref_b")
        r1 = _solve_lab_cycle_cached(f1, 0.0, 45.0, lang=lang)
        r2 = _solve_lab_cycle_cached(f2, 0.0, 45.0, lang=lang)
        with col_a:
            st.info(
                f"**{f1}** (`{REFRIGERANTS[f1].safety_group}`, GWP={REFRIGERANTS[f1].gwp})\n\n"
                f"- COP: `{r1.cop_heating:.2f}` | T2: `{r1.t_discharge_c:.1f} °C`\n"
                f"- p1/p2: `{r1.p_evap_bar:.1f} / {r1.p_cond_bar:.1f} bar` (Π={r1.pressure_ratio:.2f})"
            )
        with col_b:
            st.info(
                f"**{f2}** (`{REFRIGERANTS[f2].safety_group}`, GWP={REFRIGERANTS[f2].gwp})\n\n"
                f"- COP: `{r2.cop_heating:.2f}` | T2: `{r2.t_discharge_c:.1f} °C`\n"
                f"- p1/p2: `{r2.p_evap_bar:.1f} / {r2.p_cond_bar:.1f} bar` (Π={r2.pressure_ratio:.2f})"
            )

        all_res = [_solve_lab_cycle_cached(fk, 0.0, 45.0, lang=lang) for fk in fluid_keys]
        fig = go.Figure()
        fig.add_trace(go.Bar(x=fluid_keys, y=[r.t_discharge_c for r in all_res], name="T2 [°C]", marker_color="#EF4444"))
        _base_layout(
            fig,
            "Discharge Temperature T2 Across Refrigerants (0°C / 45°C)" if is_en else "Porównanie temperatury tłoczenia T2 czynników (0°C / 45°C)",
            "Refrigerant" if is_en else "Czynnik",
            "T2 [°C]",
        )
        st.plotly_chart(fig, width="stretch", theme="streamlit", config={"displayModeBar": False})


def render_education_page(base_input: CycleInput, lang: str) -> None:
    """Renderuje podstronę Edukacja z teorią, ilustracją wpływu i osobną sekcją quizu."""
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
    selected_id = st.session_state.get("edu_selected_lesson", LESSONS[0].id)
    if selected_id not in lesson_map:
        selected_id = LESSONS[0].id

    lesson = lesson_map[selected_id]
    l_txt = get_lesson_text(lesson, lang)

    st.markdown(f"### {l_txt['title']}")
    st.caption(l_txt["subtitle"])

    tab_learn, tab_quiz = st.tabs(
        [t("edu_tab_theory_lab", lang), t("edu_tab_quiz", lang)]
    )

    with tab_learn:
        with st.container(border=True):
            st.markdown(f"#### {t('edu_theory_header', lang)}")
            st.markdown(l_txt["theory"])

        with st.container(border=True):
            st.markdown(f"#### {t('edu_lab_header', lang)}")
            try:
                _render_mini_lab(lesson, base_input, lang)
            except Exception as exc:
                st.warning(f"Lab error: {exc}")

    with tab_quiz:
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
