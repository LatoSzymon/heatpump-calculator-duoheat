"""Interaktywna aplikacja webowa Streamlit do symulacji obiegu pompy ciepła (TESPy + SciPy)."""

import streamlit as st

from src.cycle_model import CycleInput, HeatPumpCycle
from src.optimizer import (
    find_evap_temp_for_target_cop,
    optimize_subcooling,
    run_sensitivity_grid,
)
from src.plotting import (
    create_ph_diagram,
    create_ts_diagram,
    create_cop_contour_plot,
)
from src.utils import REFRIGERANTS, get_fluid_limits


st.set_page_config(
    page_title="Kalkulator Obiegu Pompy Ciepła (TESPy + SciPy)",
    page_icon="🔥",
    layout="wide",
)

st.title("🔥 Kalkulator i Symulator Obiegu Pompy Ciepła")
st.markdown(
    "Symulacja jednostopniowego obiegu sprężarkowej pompy ciepła z przegrzaniem i dochłodzeniem "
    "oparta na bibliotekach **TESPy**, **CoolProp** oraz **SciPy**."
)

# --- PANEL BOCZNY (PARAMETRY WEJŚCIOWE) ---
with st.sidebar:
    st.header("⚙️ Parametry wejściowe")

    fluid_code = st.selectbox(
        "Czynnik chłodniczy",
        options=list(REFRIGERANTS.keys()),
        format_func=lambda k: f"{REFRIGERANTS[k].name} [{REFRIGERANTS[k].safety_group}, GWP={REFRIGERANTS[k].gwp}]",
        index=0,
    )

    ref_info = REFRIGERANTS[fluid_code]
    limits = get_fluid_limits(fluid_code)
    st.caption(
        f"**Wzór:** `{ref_info.chemical_formula}` | "
        f"**T_crit:** `{limits['T_crit_C']:.1f} °C` | "
        f"**p_crit:** `{limits['p_crit_bar']:.1f} bar`\n\n"
        f"{ref_info.description}"
    )

    st.divider()

    max_cond_slider = min(85.0, float(int(limits["T_crit_C"] - 5.0)))

    t_evap_c = st.slider(
        "Temperatura parowania T_evap [°C]",
        min_value=-30.0,
        max_value=25.0,
        value=0.0,
        step=0.5,
        help="Temperatura nasycenia czynnika w parowniku (dolne źródło).",
    )

    t_cond_c = st.slider(
        "Temperatura skraplania T_cond [°C]",
        min_value=20.0,
        max_value=max_cond_slider,
        value=min(45.0, max_cond_slider - 5.0),
        step=0.5,
        help="Temperatura nasycenia czynnika w skraplaczu (górne źródło).",
    )

    superheat_k = st.slider(
        "Przegrzanie pary za parownikiem ΔT_sh [K]",
        min_value=0.0,
        max_value=25.0,
        value=5.0,
        step=0.5,
    )

    subcooling_k = st.slider(
        "Dochłodzenie cieczy za skraplaczem ΔT_sc [K]",
        min_value=0.0,
        max_value=20.0,
        value=5.0,
        step=0.5,
    )

    eta_s = st.slider(
        "Sprawność izentropowa sprężarki η_s [-]",
        min_value=0.40,
        max_value=0.95,
        value=0.78,
        step=0.01,
    )

    q_cond_kw = st.number_input(
        "Zadana moc grzewcza skraplacza Q_cond [kW]",
        min_value=0.5,
        max_value=1000.0,
        value=10.0,
        step=0.5,
    )

# --- URUCHOMIENIE SYMULACJI TESPy ---
cycle_input = CycleInput(
    fluid=fluid_code,
    t_evap_c=t_evap_c,
    t_cond_c=t_cond_c,
    superheat_k=superheat_k,
    subcooling_k=subcooling_k,
    eta_s=eta_s,
    q_cond_kw=q_cond_kw,
)

try:
    result = HeatPumpCycle(cycle_input).solve()
except Exception as exc:
    st.error(f"⚠️ Błąd walidacji lub zbieżności modelu: {exc}")
    st.stop()

# --- KARTY KPI ---
col1, col2, col3, col4, col5, col6 = st.columns(6)
col1.metric("COP (Grzanie)", f"{result.cop_heating:.2f}", f"Carnot: {result.cop_carnot:.2f}")
col2.metric("Moc grzewcza Q_cond", f"{result.q_cond_kw:.2f} kW")
col3.metric("Moc sprężarki P_el", f"{result.p_comp_kw:.2f} kW")
col4.metric("Moc parownika Q_evap", f"{result.q_evap_kw:.2f} kW")
col5.metric("Strumień masy ṁ", f"{result.mass_flow_kg_s * 1000:.1f} g/s", f"{result.v_dot_suction_m3_h:.2f} m³/h")
col6.metric("Spręż Π = p₂/p₁", f"{result.pressure_ratio:.2f}", f"{result.p_evap_bar:.1f} → {result.p_cond_bar:.1f} bar")

st.divider()

# --- ZAKŁADKI WIZUALIZACJI I ANALIZ ---
tab_charts, tab_table, tab_scipy = st.tabs(
    [
        "📈 Wykresy termodynamiczne (log(p)-h oraz T-s)",
        "📋 Tabela punktów węzłowych i bilans",
        "🧮 Optymalizacja i analiza wrażliwości (SciPy)",
    ]
)

with tab_charts:
    chart_col1, chart_col2 = st.columns(2)
    with chart_col1:
        st.plotly_chart(create_ph_diagram(result.plot_data), use_container_width=True)
    with chart_col2:
        st.plotly_chart(create_ts_diagram(result.plot_data), use_container_width=True)

with tab_table:
    st.subheader("Parametry termodynamiczne w punktach węzłowych (1–4)")
    st.dataframe(result.state_points_df, use_container_width=True, hide_index=True)

    csv_bytes = result.state_points_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Pobierz tabelę stanów jako CSV",
        data=csv_bytes,
        file_name=f"obieg_{fluid_code}_Tevap{t_evap_c}_Tcond{t_cond_c}.csv",
        mime="text/csv",
    )

    st.subheader("Podsumowanie energetyczne i egzergowe")
    b_col1, b_col2, b_col3 = st.columns(3)
    b_col1.info(f"**Sprawność egzergowa (względem obiegu Carnota):** `{result.eta_exergetic * 100:.1f} %`")
    b_col2.info(f"**Współczynnik chłodniczy (EER / COP_chł):** `{result.cop_cooling:.2f}`")
    b_col3.success(
        f"**Błąd zamknięcia bilansu energii (TESPy):** `{result.energy_balance_error_w:.4e} W`"
    )

with tab_scipy:
    st.subheader("1. Poszukiwanie wymaganej temperatury parowania (`scipy.optimize.root_scalar`)")
    sc_col1, sc_col2 = st.columns([1, 2])
    with sc_col1:
        target_cop = st.number_input(
            "Docelowy współczynnik COP_grzewcze [-]",
            min_value=1.5,
            max_value=10.0,
            value=4.0,
            step=0.1,
        )
    with sc_col2:
        try:
            root_res = find_evap_temp_for_target_cop(cycle_input, target_cop=target_cop)
            st.success(
                f"Aby osiągnąć **COP = {target_cop:.2f}** przy $T_{{cond}} = {t_cond_c:.1f}\\text{{ °C}}$, "
                f"wymagana temperatura parowania wynosi **$T_{{evap}} = {root_res['t_evap_c']:.2f}\\text{{ °C}}$** "
                f"(pobór mocy sprężarki: `{root_res['p_comp_kw']:.2f} kW`, liczba iteracji Brentq: `{root_res['iterations']}`)."
            )
        except ValueError as err:
            st.warning(str(err))

    st.divider()

    st.subheader("2. Optymalizacja dochłodzenia cieczy (`scipy.optimize.minimize_scalar`)")
    opt_col1, opt_col2 = st.columns([1, 2])
    with opt_col1:
        sink_return_temp = st.slider(
            "Temperatura wody powrotnej z instalacji CO [°C]",
            min_value=20.0,
            max_value=max(25.0, t_cond_c - 2.0),
            value=min(30.0, max(20.0, t_cond_c - 10.0)),
            step=1.0,
        )
    with opt_col2:
        opt_res = optimize_subcooling(cycle_input, pinch_sink_temp_c=sink_return_temp)
        st.info(
            f"Optymalny stopień dochłodzenia dla temperatury powrotu `{sink_return_temp:.1f} °C` "
            f"wynosi **$\\Delta T_{{sc,opt}} = {opt_res['optimal_subcooling_k']:.2f}\\text{{ K}}$**, "
            f"co pozwala osiągnąć maksymalny efektywny **COP = {opt_res['max_cop']:.2f}**."
        )

    st.divider()

    st.subheader("3. Mapa sprawności COP = f(T_evap, T_cond) (`scipy.interpolate.RegularGridInterpolator`)")
    with st.spinner("Obliczanie siatki punktów TESPy i interpolacji kubicznej SciPy..."):
        max_grid_cond = min(65.0, float(int(limits["T_crit_C"] - 8.0)))
        sens_data = run_sensitivity_grid(
            cycle_input,
            t_evap_range=(-15.0, 15.0),
            t_cond_range=(30.0, max_grid_cond),
            n_points=6,
        )
        st.plotly_chart(
            create_cop_contour_plot(sens_data, t_evap_c, t_cond_c),
            use_container_width=True,
        )
