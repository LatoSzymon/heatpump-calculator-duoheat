"""Zakładki symulacji i analizy: KPI, Schemat, Wykresy, Tabela, Optymalizacja SciPy i Słowniczek."""

from typing import Callable
import streamlit as st

from src.cycle_model import CycleInput, CycleResult
from src.i18n import t
from src.plotting import (
    create_cop_contour_plot,
    create_cycle_schematic,
    create_energy_balance_bar,
    create_ph_diagram,
    create_subcooling_curve_plot,
    create_ts_diagram,
)


def render_kpi_cards(result: CycleResult, lang: str) -> None:
    """Renderuje responsywną siatkę 6 kart KPI oraz ostrzeżenie o wysokiej temp. tłoczenia."""
    t_dis_warn_cls = " kpi-card--warn" if result.t_discharge_c > 115.0 else ""
    st.markdown(
        f"""
        <div class="kpi-grid">
            <div class="kpi-card kpi-accent-primary">
                <div class="kpi-label">{t("kpi_cop_label", lang)}</div>
                <div class="kpi-value">{result.cop_heating:.2f}</div>
                <div class="kpi-sub">{t("kpi_cop_sub", lang, pct=result.eta_exergetic * 100, carnot=result.cop_carnot)}</div>
            </div>
            <div class="kpi-card kpi-accent-heat">
                <div class="kpi-label">{t("kpi_qcond_label", lang)}</div>
                <div class="kpi-value">{result.q_cond_kw:.2f} kW</div>
                <div class="kpi-sub">ΔT_lift = {result.delta_t_lift_k:.1f} K</div>
            </div>
            <div class="kpi-card kpi-accent-power">
                <div class="kpi-label">{t("kpi_pcomp_label", lang)}</div>
                <div class="kpi-value">{result.p_comp_kw:.2f} kW</div>
                <div class="kpi-sub">{t("kpi_pcomp_sub", lang, pct=result.p_comp_kw / result.q_cond_kw * 100)}</div>
            </div>
            <div class="kpi-card kpi-accent-ambient">
                <div class="kpi-label">{t("kpi_qevap_label", lang)}</div>
                <div class="kpi-value">{result.q_evap_kw:.2f} kW</div>
                <div class="kpi-sub">{t("kpi_qevap_sub", lang, pct=result.q_evap_kw / result.q_cond_kw * 100)}</div>
            </div>
            <div class="kpi-card kpi-accent-temp{t_dis_warn_cls}">
                <div class="kpi-label">{t("kpi_tdis_label", lang)}</div>
                <div class="kpi-value">{result.t_discharge_c:.1f} °C</div>
                <div class="kpi-sub">ṁ = {result.mass_flow_kg_s * 1000:.1f} g/s</div>
            </div>
            <div class="kpi-card kpi-accent-ratio">
                <div class="kpi-label">{t("kpi_pr_label", lang)}</div>
                <div class="kpi-value">{result.pressure_ratio:.2f}</div>
                <div class="kpi-sub">{result.p_evap_bar:.1f} → {result.p_cond_bar:.1f} bar</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if result.t_discharge_c > 115.0:
        st.warning(t("warn_high_t_discharge", lang, t_dis=result.t_discharge_c))


def render_mechanics_tab(result: CycleResult, cycle_input: CycleInput, lang: str) -> None:
    """Renderuje zakładkę 1: Schemat ideowy i 4 etapy obiegu."""
    st.subheader(t("mech_title", lang))
    st.markdown(t("mech_intro", lang))

    mech_col1, mech_col2 = st.columns([1.2, 1.0])

    with mech_col1:
        try:
            st.plotly_chart(
                create_cycle_schematic(result, lang=lang),
                width="stretch",
                theme="streamlit",
                config={"displayModeBar": False, "responsive": True},
            )
            st.plotly_chart(
                create_energy_balance_bar(result, lang=lang),
                width="stretch",
                theme="streamlit",
                config={"displayModeBar": False, "responsive": True},
            )
        except Exception as exc:
            st.error(t("err_schematic", lang, exc=exc))

    with mech_col2:
        st.markdown(t("mech_stages_title", lang))
        st.markdown(
            t(
                "stage_1_html",
                lang,
                p_evap=result.p_evap_bar,
                t_4=result.t_4_c,
                q_evap=result.q_evap_kw,
                sh=cycle_input.superheat_k,
                t_1=result.t_1_c,
            ),
            unsafe_allow_html=True,
        )
        st.markdown(
            t(
                "stage_2_html",
                lang,
                v_dot=result.v_dot_suction_m3_h,
                pr=result.pressure_ratio,
                p_cond=result.p_cond_bar,
                p_comp=result.p_comp_kw,
                t_dis=result.t_discharge_c,
            ),
            unsafe_allow_html=True,
        )
        st.markdown(
            t(
                "stage_3_html",
                lang,
                q_cond=result.q_cond_kw,
                t_cond=cycle_input.t_cond_c,
                q_desup=result.q_desuperheat_kw,
                q_lat=result.q_cond_latent_kw,
                sc=cycle_input.subcooling_k,
                t_3=result.t_3_c,
                q_sub=result.q_subcool_kw,
            ),
            unsafe_allow_html=True,
        )
        st.markdown(
            t(
                "stage_4_html",
                lang,
                p_cond=result.p_cond_bar,
                p_evap=result.p_evap_bar,
                t_4=result.t_4_c,
                x_4_pct=result.x_4 * 100,
            ),
            unsafe_allow_html=True,
        )


def render_charts_tab(result: CycleResult, lang: str) -> None:
    """Renderuje zakładkę 2: Wykresy log(p)-h i T-s."""
    with st.expander(t("charts_guide_title", lang), expanded=False):
        st.markdown(t("charts_guide_md", lang))

    chart_col1, chart_col2 = st.columns(2)
    with chart_col1:
        try:
            st.plotly_chart(
                create_ph_diagram(result.plot_data, lang=lang),
                width="stretch",
                theme="streamlit",
                config={"displaylogo": False, "responsive": True},
            )
        except Exception as exc:
            st.error(t("err_ph", lang, exc=exc))
    with chart_col2:
        try:
            st.plotly_chart(
                create_ts_diagram(result.plot_data, lang=lang),
                width="stretch",
                theme="streamlit",
                config={"displaylogo": False, "responsive": True},
            )
        except Exception as exc:
            st.error(t("err_ts", lang, exc=exc))


def render_table_tab(result: CycleResult, cycle_input: CycleInput, lang: str) -> None:
    """Renderuje zakładkę 3: Tabela stanów, eksport CSV oraz bilans energii."""
    st.subheader(t("table_title", lang))
    st.dataframe(result.state_points_df, width="stretch", hide_index=True)

    csv_bytes = result.state_points_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label=t("download_csv", lang),
        data=csv_bytes,
        file_name=f"cycle_{cycle_input.fluid}_Tevap{cycle_input.t_evap_c}_Tcond{cycle_input.t_cond_c}.csv",
        mime="text/csv",
    )

    st.divider()
    st.subheader(t("heat_struct_title", lang))

    heat_col1, heat_col2 = st.columns(2, gap="medium")
    with heat_col1:
        with st.container(border=True):
            st.markdown(t("cond_breakdown_title", lang))
            st.write(t("cond_desup", lang, val=result.q_desuperheat_kw, pct=result.q_desuperheat_kw / result.q_cond_kw * 100))
            st.write(t("cond_latent", lang, val=result.q_cond_latent_kw, pct=result.q_cond_latent_kw / result.q_cond_kw * 100))
            st.write(t("cond_subcool", lang, val=result.q_subcool_kw, pct=result.q_subcool_kw / result.q_cond_kw * 100))

    with heat_col2:
        with st.container(border=True):
            st.markdown(t("evap_breakdown_title", lang))
            st.write(t("evap_latent", lang, val=result.q_evap_latent_kw, pct=result.q_evap_latent_kw / result.q_evap_kw * 100))
            st.write(t("evap_superheat", lang, val=result.q_superheat_kw, pct=result.q_superheat_kw / result.q_evap_kw * 100))

    st.markdown(
        f"""
        <div class="summary-grid">
            <div class="summary-card">
                <div class="summary-label">{t("summary_exergy_label", lang)}</div>
                <div class="summary-value">{result.eta_exergetic * 100:.1f} %</div>
                <div class="summary-sub">{t("summary_exergy_sub", lang)}</div>
            </div>
            <div class="summary-card">
                <div class="summary-label">{t("summary_eer_label", lang)}</div>
                <div class="summary-value">{result.cop_cooling:.2f}</div>
                <div class="summary-sub">{t("summary_eer_sub", lang)}</div>
            </div>
            <div class="summary-card summary-card--ok">
                <div class="summary-label">{t("summary_balance_label", lang)}</div>
                <div class="summary-value">{result.energy_balance_error_w:.4e} W</div>
                <div class="summary-sub">{t("summary_balance_sub", lang)}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_scipy_tab(
    cycle_dict: dict,
    cycle_input: CycleInput,
    limits: dict,
    lang: str,
    find_evap_temp_cached: Callable,
    optimize_subcooling_cached: Callable,
    run_sensitivity_grid_cached: Callable,
) -> None:
    """Renderuje zakładkę 4: Narzędzia optymalizacyjne SciPy."""
    t_evap_c = cycle_input.t_evap_c
    t_cond_c = cycle_input.t_cond_c

    with st.container(border=True):
        st.subheader(t("scipy_1_title", lang))
        st.caption(t("scipy_1_caption", lang))
        sc_col1, sc_col2 = st.columns([1, 2], gap="medium")
        with sc_col1:
            target_cop = st.number_input(
                t("scipy_target_cop", lang),
                min_value=1.5,
                max_value=10.0,
                value=4.0,
                step=0.1,
            )
        with sc_col2:
            try:
                root_res = find_evap_temp_cached(cycle_dict, target_cop=target_cop, lang=lang)
                st.success(
                    t(
                        "scipy_1_success",
                        lang,
                        cop=target_cop,
                        t_cond=t_cond_c,
                        t_evap=root_res["t_evap_c"],
                        p_comp=root_res["p_comp_kw"],
                        iters=root_res["iterations"],
                    )
                )
            except Exception as err:
                st.warning(t("scipy_1_err", lang, err=err))

    with st.container(border=True):
        st.subheader(t("scipy_2_title", lang))
        st.caption(t("scipy_2_caption", lang))
        opt_col1, opt_col2 = st.columns([1, 2], gap="medium")
        with opt_col1:
            max_return_temp = max(21.0, t_cond_c - 3.0)
            default_return = min(max(20.0, t_cond_c - 10.0), max_return_temp)
            sink_return_temp = st.slider(
                t("scipy_return_temp", lang),
                min_value=20.0,
                max_value=max_return_temp,
                value=default_return,
                step=1.0,
            )
            try:
                opt_res = optimize_subcooling_cached(cycle_dict, pinch_sink_temp_c=sink_return_temp)
                st.info(
                    t(
                        "scipy_2_info",
                        lang,
                        t_ret=sink_return_temp,
                        sc_opt=opt_res["optimal_subcooling_k"],
                        max_cop=opt_res["max_cop"],
                    )
                )
            except Exception as err:
                opt_res = None
                st.warning(t("scipy_2_err", lang, err=err))
        with opt_col2:
            if opt_res is not None:
                try:
                    st.plotly_chart(
                        create_subcooling_curve_plot(opt_res, lang=lang),
                        width="stretch",
                        theme="streamlit",
                        config={"displaylogo": False, "responsive": True},
                    )
                except Exception as exc:
                    st.error(t("scipy_2_plot_err", lang, exc=exc))

    with st.container(border=True):
        st.subheader(t("scipy_3_title", lang))
        st.caption(t("scipy_3_caption", lang))

        evap_grid_min = min(-15.0, t_evap_c - 2.0)
        evap_grid_max = max(15.0, t_evap_c + 2.0)
        cond_grid_min = max(evap_grid_max + 5.0, min(30.0, t_cond_c - 2.0))
        cond_grid_max = min(float(int(limits["T_crit_C"] - 5.0)), max(60.0, t_cond_c + 2.0))

        try:
            with st.spinner(t("scipy_3_spinner", lang)):
                sens_data = run_sensitivity_grid_cached(
                    cycle_dict,
                    t_evap_range=(evap_grid_min, evap_grid_max),
                    t_cond_range=(cond_grid_min, cond_grid_max),
                    n_points=5,
                    lang=lang,
                )
                st.plotly_chart(
                    create_cop_contour_plot(sens_data, t_evap_c, t_cond_c, lang=lang),
                    width="stretch",
                    theme="streamlit",
                    config={"displaylogo": False, "responsive": True},
                )
        except Exception as err:
            st.warning(t("scipy_3_err", lang, err=err))


def render_glossary_tab(lang: str) -> None:
    """Renderuje zakładkę Słowniczek pojęć termodynamicznych."""
    st.subheader(t("glossary_title", lang))
    st.markdown(t("glossary_intro", lang))

    g_col1, g_col2 = st.columns(2, gap="medium")
    with g_col1:
        with st.container(border=True):
            st.markdown(t("glossary_col1_md", lang))
    with g_col2:
        with st.container(border=True):
            st.markdown(t("glossary_col2_md", lang))
