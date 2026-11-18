"""Interaktywna aplikacja webowa Streamlit do nauki i symulacji obiegu pompy ciepła (TESPy + SciPy)."""

from dataclasses import asdict
import streamlit as st

from src.cycle_model import CycleInput, CycleResult, HeatPumpCycle
from src.optimizer import (
    find_evap_temp_for_target_cop,
    optimize_subcooling,
    run_sensitivity_grid,
)
from src.plotting import (
    create_cop_contour_plot,
    create_cycle_schematic,
    create_energy_balance_bar,
    create_ph_diagram,
    create_subcooling_curve_plot,
    create_ts_diagram,
)
from src.utils import REFRIGERANTS, SCENARIO_PRESETS, get_fluid_limits


st.set_page_config(
    page_title="Kalkulator Obiegu Pompy Ciepła — Instytut Naukowy",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="auto",
)

# Spójne style dla trybu ciemnego/jasnego oraz responsywny layout mobilny
st.markdown(
    """
    <style>
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
        gap: 0.75rem;
        margin: 0.5rem 0 1rem 0;
    }
    .kpi-card {
        background-color: rgba(148, 163, 184, 0.08);
        border: 1px solid rgba(148, 163, 184, 0.20);
        border-radius: 10px;
        padding: 0.85rem 1rem;
    }
    .kpi-label {
        font-size: 0.8rem;
        opacity: 0.75;
        margin-bottom: 0.25rem;
    }
    .kpi-value {
        font-size: 1.55rem;
        font-weight: 700;
        line-height: 1.2;
    }
    .kpi-sub {
        font-size: 0.78rem;
        color: #38BDF8;
        margin-top: 0.25rem;
    }
    .step-card {
        background-color: rgba(148, 163, 184, 0.08);
        border: 1px solid rgba(148, 163, 184, 0.18);
        border: 4px solid #64748B;
        padding: 0.85rem 1rem;
        margin-bottom: 0.7rem;
        color: inherit;
        line-height: 1.5;
    }
    .step-evap { border-color: #0EA5E9; }
    .step-comp { border-color: #EF4444; }
    .step-cond { border-color: #F97316; }
    .step-valve { border-color: #22C55E; }
    .app-footer {
        margin-top: auto;
        text-align: center;
        opacity: 0.8;
        font-size: 0.9rem;
        padding: 1rem 0 0.5rem 0;
    }
    .app-footer a {
        color: #38BDF8;
        text-decoration: none;
        font-weight: 600;
    }
    .app-footer a:hover {
        text-decoration: underline;
    }
    @media (max-width: 768px) {
        .block-container {
            padding-left: 0.75rem !important;
            padding-right: 0.75rem !important;
            padding-top: 1rem !important;
        }
        h1 {
            font-size: 1.45rem !important;
            line-height: 1.25 !important;
        }
        h2, h3 {
            font-size: 1.15rem !important;
        }
        [data-baseweb="tab-list"] {
            overflow-x: auto !important;
            flex-wrap: nowrap !important;
            scrollbar-width: none;
            -webkit-overflow-scrolling: touch;
            gap: 0.25rem;
        }
        [data-baseweb="tab-list"]::-webkit-scrollbar {
            display: none;
        }
        [data-baseweb="tab"] {
            white-space: nowrap !important;
            flex-shrink: 0 !important;
            padding: 0.5rem 0.75rem !important;
            font-size: 0.9rem !important;
        }
        .stButton > button, .stDownloadButton > button {
            min-height: 44px;
            width: 100%;
        }
        .kpi-grid {
            grid-template-columns: repeat(2, 1fr);
            gap: 0.5rem;
        }
        .kpi-card {
            padding: 0.65rem 0.75rem;
        }
        .kpi-value {
            font-size: 1.2rem;
        }
        .step-card {
            padding: 0.75rem 0.85rem;
            font-size: 0.92rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data(show_spinner=False)
def solve_cycle_cached(params_dict: dict) -> CycleResult:
    """Buforuje wyniki rozwiązania sieci TESPy dla identycznych parametrów."""
    return HeatPumpCycle(CycleInput(**params_dict)).solve()


@st.cache_data(show_spinner=False)
def find_evap_temp_cached(params_dict: dict, target_cop: float) -> dict:
    return find_evap_temp_for_target_cop(CycleInput(**params_dict), target_cop=target_cop)


@st.cache_data(show_spinner=False)
def optimize_subcooling_cached(params_dict: dict, pinch_sink_temp_c: float) -> dict:
    return optimize_subcooling(CycleInput(**params_dict), pinch_sink_temp_c=pinch_sink_temp_c)


@st.cache_data(show_spinner=False)
def run_sensitivity_grid_cached(
    params_dict: dict,
    t_evap_range: tuple,
    t_cond_range: tuple,
    n_points: int = 6,
) -> dict:
    return run_sensitivity_grid(
        CycleInput(**params_dict),
        t_evap_range=t_evap_range,
        t_cond_range=t_cond_range,
        n_points=n_points,
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
    """Przełącza etykietę scenariusza na 'Własne ustawienia' po ręcznej zmianie suwaka."""
    st.session_state["selected_preset"] = "custom"


# Inicjalizacja domyślnego scenariusza przy pierwszym uruchomieniu
if "selected_preset" not in st.session_state:
    st.session_state["selected_preset"] = "air_floor_spring"
    _apply_preset("air_floor_spring")

# --- NAGŁÓWEK ---
st.title("Kalkulator i Symulator Obiegu Pompy Ciepła")
st.markdown(
    "Narzędzie szkoleniowo-badawcze oparte na **TESPy**, **CoolProp** i **SciPy**. "
    "Zmieniaj parametry w panelu bocznym, aby na żywo obserwować, jak zmienia się praca sprężarki, "
    "ciśnienia oraz współczynnik efektywności **COP**."
)

# --- PANEL BOCZNY (PARAMETRY WEJŚCIOWE) ---
with st.sidebar:
    st.header("Konfiguracja obiegu")

    preset_options = ["custom"] + list(SCENARIO_PRESETS.keys())
    selected_preset = st.selectbox(
        "Gotowy scenariusz (szybki start)",
        options=preset_options,
        key="selected_preset",
        on_change=_on_preset_change,
        format_func=lambda k: (
            "Własne ustawienia" if k == "custom" else SCENARIO_PRESETS[k].label
        ),
        help="Wybierz typowy przypadek z praktyki inżynierskiej, aby zobaczyć realistyczne wartości.",
    )

    if selected_preset != "custom":
        st.info(SCENARIO_PRESETS[selected_preset].explanation)

    st.divider()

    fluid_keys = list(REFRIGERANTS.keys())
    fluid_code = st.selectbox(
        "Czynnik chłodniczy",
        options=fluid_keys,
        format_func=lambda k: f"{REFRIGERANTS[k].name} [{REFRIGERANTS[k].safety_group}, GWP={REFRIGERANTS[k].gwp}]",
        key="fluid_code",
        on_change=_mark_custom,
        help="Substancja krążąca w zamkniętym obiegu, która wrze w niskiej temperaturze i skrapla się w wysokiej.",
    )

    ref_info = REFRIGERANTS[fluid_code]
    try:
        limits = get_fluid_limits(fluid_code)
    except Exception as exc:
        st.error(f"Nie udało się pobrać własności czynnika {fluid_code}: {exc}")
        limits = {"T_crit_C": 95.0, "p_crit_bar": 40.0, "T_min_C": -50.0}

    st.caption(
        f"**Wzór:** `{ref_info.chemical_formula}` | "
        f"**T_kryt:** `{limits['T_crit_C']:.1f} °C` | "
        f"**p_kryt:** `{limits['p_crit_bar']:.1f} bar`\n\n"
        f"{ref_info.description}"
    )

    st.divider()
    st.subheader("Temperatury źródeł")

    t_evap_c = st.slider(
        "Temperatura parowania T_evap [°C]",
        min_value=-25.0,
        max_value=20.0,
        step=0.5,
        key="t_evap_c",
        on_change=_mark_custom,
        help="Temperatura wrzenia czynnika w parowniku. Zwykle jest o ok. 5–7 K niższa od temperatury powietrza lub gruntu.",
    )

    min_cond_safe = max(20.0, t_evap_c + 5.0)
    max_cond_safe = max(min_cond_safe + 1.0, min(85.0, float(int(limits["T_crit_C"] - 5.0))))
    if st.session_state.get("t_cond_c", 35.0) < min_cond_safe:
        st.session_state["t_cond_c"] = min_cond_safe
    elif st.session_state.get("t_cond_c", 35.0) > max_cond_safe:
        st.session_state["t_cond_c"] = max_cond_safe

    t_cond_c = st.slider(
        "Temperatura skraplania T_cond [°C]",
        min_value=min_cond_safe,
        max_value=max_cond_safe,
        step=0.5,
        key="t_cond_c",
        on_change=_mark_custom,
        help="Temperatura skraplania w skraplaczu. Ok. 35°C dla podłogówki, 50–60°C dla grzejników i CWU.",
    )

    st.subheader("Parametry obiegu i sprężarki")

    superheat_k = st.slider(
        "Przegrzanie pary za parownikiem ΔT_sh [K]",
        min_value=0.0,
        max_value=20.0,
        step=0.5,
        key="superheat_k",
        on_change=_mark_custom,
        help="Dodatkowe podgrzanie pary przed sprężarką (typowo 4–7 K). Chroni sprężarkę przed zalaniem ciekłym czynnikiem.",
    )

    max_subcool_safe = max(0.5, min(20.0, float(int((t_cond_c - t_evap_c - 1.0) * 2)) / 2.0))
    if st.session_state.get("subcooling_k", 4.0) > max_subcool_safe:
        st.session_state["subcooling_k"] = max_subcool_safe

    subcooling_k = st.slider(
        "Dochłodzenie cieczy za skraplaczem ΔT_sc [K]",
        min_value=0.0,
        max_value=max_subcool_safe,
        step=0.5,
        key="subcooling_k",
        on_change=_mark_custom,
        help="Schłodzenie skroplonej cieczy poniżej temperatury skraplania. Zwiększa wydajność i zmniejsza straty na zaworze.",
    )

    eta_s = st.slider(
        "Sprawność izentropowa sprężarki η_s [-]",
        min_value=0.45,
        max_value=0.95,
        step=0.01,
        key="eta_s",
        on_change=_mark_custom,
        help="Określa, jak blisko idealnego sprężania bez strat pracuje rzeczywista sprężarka (typowo 0.70–0.82).",
    )

    q_cond_kw = st.number_input(
        "Moc grzewcza dla budynku Q_cond [kW]",
        min_value=1.0,
        max_value=500.0,
        step=0.5,
        key="q_cond_kw",
        on_change=_mark_custom,
        help="Docelowa moc cieplna dostarczana przez skraplacz do instalacji grzewczej.",
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
cycle_dict = asdict(cycle_input)

result: CycleResult | None = None
simulation_error: str | None = None
try:
    result = solve_cycle_cached(cycle_dict)
except ValueError as exc:
    simulation_error = f"Nieprawidłowe parametry fizyczne obiegu: {exc}"
except RuntimeError as exc:
    simulation_error = (
        f"Solver TESPy nie osiągnął zbieżności dla wybranych parametrów ({exc}). "
        "Spróbuj zmienić temperaturę parowania/skraplania lub wybrać inny czynnik."
    )
except Exception as exc:
    simulation_error = f"Wystąpił nieoczekiwany błąd obliczeniowy: {exc}"

if simulation_error or result is None:
    st.error(f"{simulation_error}")
    st.info("Skoryguj parametry w panelu bocznym lub wybierz jeden z gotowych scenariuszy.")
else:
    # --- KARTY KPI (responsywna siatka CSS: 6 kolumn na desktopie, 2 na mobile) ---
    st.markdown(
        f"""
        <div class="kpi-grid">
            <div class="kpi-card">
                <div class="kpi-label">COP (Efektywność)</div>
                <div class="kpi-value">{result.cop_heating:.2f}</div>
                <div class="kpi-sub">{result.eta_exergetic * 100:.0f}% Carnota ({result.cop_carnot:.2f})</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Ciepło do budynku Q_cond</div>
                <div class="kpi-value">{result.q_cond_kw:.2f} kW</div>
                <div class="kpi-sub">ΔT_lift = {result.delta_t_lift_k:.1f} K</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Pobór prądu P_el</div>
                <div class="kpi-value">{result.p_comp_kw:.2f} kW</div>
                <div class="kpi-sub">{result.p_comp_kw / result.q_cond_kw * 100:.0f}% energii</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Ciepło z natury Q_evap</div>
                <div class="kpi-value">{result.q_evap_kw:.2f} kW</div>
                <div class="kpi-sub">{result.q_evap_kw / result.q_cond_kw * 100:.0f}% za darmo</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Temp. tłoczenia T₂</div>
                <div class="kpi-value">{result.t_discharge_c:.1f} °C</div>
                <div class="kpi-sub">ṁ = {result.mass_flow_kg_s * 1000:.1f} g/s</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Spręż Π = p₂ / p₁</div>
                <div class="kpi-value">{result.pressure_ratio:.2f}</div>
                <div class="kpi-sub">{result.p_evap_bar:.1f} → {result.p_cond_bar:.1f} bar</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if result.t_discharge_c > 115.0:
        st.warning(
            f"⚠️ Uwaga inżynierska: Wysoka temperatura tłoczenia sprężarki (**{result.t_discharge_c:.1f} °C**). "
            "W rzeczywistym układzie powyżej ~115–120 °C olej smarny ulega przegrzaniu — rozważ obniżenie `T_cond`, "
            "zmniejszenie przegrzania lub zmianę czynnika."
        )

    st.divider()

    # --- ZAKŁADKI APLIKACJI ---
    tab_mechanics, tab_charts, tab_table, tab_scipy, tab_glossary = st.tabs(
        [
            "Schemat i mechanika",
            "Wykresy log(p)-h i T-s",
            "Punkty i bilans",
            "Optymalizacja (SciPy)",
            "Słowniczek",
        ]
    )

    # === ZAKŁADKA 1: SCHEMAT I TŁUMACZENIE MECHANIK ===
    with tab_mechanics:
        st.subheader("Jak działa pompa ciepła? (Obieg na żywo)")
        st.markdown(
            "Pompa ciepła **nie wytwarza** ciepła ze spalania — ona je **przepompowuje** z chłodnego otoczenia "
            "(powietrze/grunt) do ciepłego budynku, wykorzystując zjawiska **wrzenia** i **skraplania** czynnika chłodniczego."
        )

        mech_col1, mech_col2 = st.columns([1.2, 1.0])

        with mech_col1:
            try:
                st.plotly_chart(
                    create_cycle_schematic(result),
                    width="stretch",
                    theme="streamlit",
                    config={"displayModeBar": False, "responsive": True},
                )
                st.plotly_chart(
                    create_energy_balance_bar(result),
                    width="stretch",
                    theme="streamlit",
                    config={"displayModeBar": False, "responsive": True},
                )
            except Exception as exc:
                st.error(f"Nie udało się wygenerować schematu obiegu: {exc}")

        with mech_col2:
            st.markdown("#### 4 etapy obiegu dla Twoich aktualnych nastaw:")

            st.markdown(
                f"""
                <div class="step-card step-evap">
                    <strong>4 → 1. Parowanie i przegrzanie (Parownik)</strong><br>
                    Ciekły czynnik o niskim ciśnieniu (<code>{result.p_evap_bar:.2f} bar</code>) wpływa do parownika w temperaturze
                    <strong>{result.t_4_c:.1f} °C</strong>. Ponieważ wrze w temperaturze niższej niż otoczenie, pobiera
                    <strong>{result.q_evap_kw:.2f} kW</strong> darmowego ciepła i zamienia się w parę
                    (dodatkowo przegrzaną o <code>{superheat_k:.1f} K</code> do <strong>{result.t_1_c:.1f} °C</strong>, aby żadna kropla nie trafiła do sprężarki).
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown(
                f"""
                <div class="step-card step-comp">
                    <strong>1 → 2. Sprężanie (Sprężarka)</strong><br>
                    Sprężarka zasysa chłodną parę (<code>{result.v_dot_suction_m3_h:.2f} m³/h</code>) i podnosi jej ciśnienie
                    <strong>{result.pressure_ratio:.2f}-krotnie</strong> (do <code>{result.p_cond_bar:.2f} bar</code>), zużywając
                    <strong>{result.p_comp_kw:.2f} kW</strong> energii elektrycznej. Wzrost ciśnienia gwałtownie podnosi
                    temperaturę pary aż do <strong>{result.t_discharge_c:.1f} °C</strong>.
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown(
                f"""
                <div class="step-card step-cond">
                    <strong>2 → 3. Skraplanie i dochłodzenie (Skraplacz)</strong><br>
                    Gorąca para oddaje <strong>{result.q_cond_kw:.2f} kW</strong> ciepła wodzie w instalacji grzewczej:
                    najpierw chłodzi się do <strong>{t_cond_c:.1f} °C</strong> (<code>{result.q_desuperheat_kw:.2f} kW</code>),
                    następnie skrapla (<code>{result.q_cond_latent_kw:.2f} kW</code>), a na końcu jest dochładzana o
                    <code>{subcooling_k:.1f} K</code> do <strong>{result.t_3_c:.1f} °C</strong> (<code>{result.q_subcool_kw:.2f} kW</code>).
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown(
                f"""
                <div class="step-card step-valve">
                    <strong>3 → 4. Rozprężanie izentalpowe (Zawór dławiący)</strong><br>
                    Ciecz pod wysokim ciśnieniem przeciska się przez zawór rozprężny. Ciśnienie spada z
                    <code>{result.p_cond_bar:.2f}</code> do <code>{result.p_evap_bar:.2f} bar</code>, przez co czynnik
                    gwałtownie stygnie do <strong>{result.t_4_c:.1f} °C</strong>. Część cieczy (<strong>{result.x_4 * 100:.1f}%</strong>)
                    odparowuje natychmiast (tzw. <em>flash gas</em>), a reszta trafia do parownika i cykl się powtarza.
                </div>
                """,
                unsafe_allow_html=True,
            )

    # === ZAKŁADKA 2: WYKRESY TERMODYNAMICZNE ===
    with tab_charts:
        with st.expander("Jak czytać wykres Molliera log(p)-h oraz wykres T-s?", expanded=False):
            st.markdown(
                """
                - **Szary „dzwon” (krzywa nasycenia):** oddziela obszar cieczy (po lewej), mieszaniny wrzącej cieczy i pary (w środku) oraz pary przegrzanej (po prawej).
                - **Wykres log(p)-h (po lewej):** Oś pionowa to ciśnienie, a pozioma to energia czynnika (entalpia `h`).
                  - Poziome odcinki to wymiana ciepła przy stałym ciśnieniu: długość odcinka `4→1` to ciepło pobrane z natury (`q_evap`), a długość `2→3` to ciepło oddane do budynku (`q_cond`).
                  - Różnica `h₂ - h₁` to praca włożona przez sprężarkę. **Im krótszy odcinek `1→2` względem `2→3`, tym wyższe COP!**
                  - Pionowy odcinek `3→4` oznacza dławienie przy stałej entalpii (`h = const`).
                - **Wykres T-s (po prawej):** Pokazuje temperaturę w funkcji entropii. Wyraźnie widać na nim, jak wysoka jest temperatura tłoczenia w punkcie `2` oraz że parowanie (`4→1`) i skraplanie (`2→3`) w obszarze dwufazowym odbywają się w stałej temperaturze.
                """
            )

        chart_col1, chart_col2 = st.columns(2)
        with chart_col1:
            try:
                st.plotly_chart(
                    create_ph_diagram(result.plot_data),
                    width="stretch",
                    theme="streamlit",
                    config={"displaylogo": False, "responsive": True},
                )
            except Exception as exc:
                st.error(f"Błąd generowania wykresu log(p)-h: {exc}")
        with chart_col2:
            try:
                st.plotly_chart(
                    create_ts_diagram(result.plot_data),
                    width="stretch",
                    theme="streamlit",
                    config={"displaylogo": False, "responsive": True},
                )
            except Exception as exc:
                st.error(f"Błąd generowania wykresu T-s: {exc}")

    # === ZAKŁADKA 3: TABELA PUNKTÓW I BILANS ===
    with tab_table:
        st.subheader("Parametry termodynamiczne w punktach węzłowych (1–4)")
        st.dataframe(result.state_points_df, width="stretch", hide_index=True)

        csv_bytes = result.state_points_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Pobierz tabelę stanów jako CSV",
            data=csv_bytes,
            file_name=f"obieg_{fluid_code}_Tevap{t_evap_c}_Tcond{t_cond_c}.csv",
            mime="text/csv",
        )

        st.divider()
        st.subheader("Struktura wymiany ciepła w wymiennikach oraz bilans TESPy")

        heat_col1, heat_col2 = st.columns(2)
        with heat_col1:
            st.markdown("**Skraplacz (oddawanie ciepła do budynku):**")
            st.write(f"- Schładzanie gorącej pary (desuperheating): **{result.q_desuperheat_kw:.2f} kW** ({result.q_desuperheat_kw / result.q_cond_kw * 100:.1f}%)")
            st.write(f"- Skraplanie izotermiczne (ciepło utajone): **{result.q_cond_latent_kw:.2f} kW** ({result.q_cond_latent_kw / result.q_cond_kw * 100:.1f}%)")
            st.write(f"- Dochładzanie cieczy (subcooling): **{result.q_subcool_kw:.2f} kW** ({result.q_subcool_kw / result.q_cond_kw * 100:.1f}%)")

        with heat_col2:
            st.markdown("**Parownik (pobieranie ciepła z otoczenia):**")
            st.write(f"- Odparowanie w obszarze dwufazowym: **{result.q_evap_latent_kw:.2f} kW** ({result.q_evap_latent_kw / result.q_evap_kw * 100:.1f}%)")
            st.write(f"- Przegrzanie pary przed sprężarką: **{result.q_superheat_kw:.2f} kW** ({result.q_superheat_kw / result.q_evap_kw * 100:.1f}%)")

        b_col1, b_col2, b_col3 = st.columns(3)
        b_col1.info(f"**Sprawność egzergowa (względem obiegu Carnota):** `{result.eta_exergetic * 100:.1f} %`")
        b_col2.info(f"**Współczynnik chłodniczy (EER / COP_chł):** `{result.cop_cooling:.2f}`")
        b_col3.success(
            f"**Błąd zamknięcia bilansu energii (TESPy):** `{result.energy_balance_error_w:.4e} W`"
        )

    # === ZAKŁADKA 4: OPTYMALIZACJA I ANALIZA WRAŻLIWOŚCI (SCIPY) ===
    with tab_scipy:
        st.subheader("1. Poszukiwanie wymaganej temperatury parowania (`scipy.optimize.root_scalar`)")
        st.caption(
            "Sprawdź, jak ciepłe musi być dolne źródło (powietrze/grunt), aby przy obecnej temperaturze skraplania osiągnąć zadane COP."
        )
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
                root_res = find_evap_temp_cached(cycle_dict, target_cop=target_cop)
                st.success(
                    f"Aby osiągnąć **COP = {target_cop:.2f}** przy $T_{{cond}} = {t_cond_c:.1f}\\text{{ °C}}$, "
                    f"wymagana temperatura parowania wynosi **$T_{{evap}} = {root_res['t_evap_c']:.2f}\\text{{ °C}}$** "
                    f"(pobór mocy sprężarki: `{root_res['p_comp_kw']:.2f} kW`, liczba iteracji Brentq: `{root_res['iterations']}`)."
                )
            except Exception as err:
                st.warning(f"Nie można wyznaczyć temperatury parowania: {err}")

        st.divider()

        st.subheader("2. Optymalizacja dochłodzenia cieczy (`scipy.optimize.minimize_scalar`)")
        st.caption(
            "Dochłodzenie poprawia COP, ale jest ograniczone temperaturą wody powracającej z grzejników/podłogówki. "
            "Poniżej widać, gdzie znajduje się fizyczne optimum."
        )
        opt_col1, opt_col2 = st.columns([1, 2])
        with opt_col1:
            max_return_temp = max(21.0, t_cond_c - 3.0)
            default_return = min(max(20.0, t_cond_c - 10.0), max_return_temp)
            sink_return_temp = st.slider(
                "Temperatura wody powrotnej z instalacji CO [°C]",
                min_value=20.0,
                max_value=max_return_temp,
                value=default_return,
                step=1.0,
            )
            try:
                opt_res = optimize_subcooling_cached(cycle_dict, pinch_sink_temp_c=sink_return_temp)
                st.info(
                    f"Optymalny stopień dochłodzenia dla powrotu `{sink_return_temp:.1f} °C` "
                    f"wynosi **$\\Delta T_{{sc,opt}} = {opt_res['optimal_subcooling_k']:.2f}\\text{{ K}}$** "
                    f"(efektywne **COP = {opt_res['max_cop']:.2f}**)."
                )
            except Exception as err:
                opt_res = None
                st.warning(f"Błąd optymalizacji dochłodzenia: {err}")
        with opt_col2:
            if opt_res is not None:
                try:
                    st.plotly_chart(
                        create_subcooling_curve_plot(opt_res),
                        width="stretch",
                        theme="streamlit",
                    )
                except Exception as exc:
                    st.error(f"Błąd rysowania krzywej dochłodzenia: {exc}")

        st.divider()

        st.subheader("3. Mapa sprawności COP = f(T_evap, T_cond) (`scipy.interpolate.RegularGridInterpolator`)")
        st.caption(
            "Mapa pokazuje, jak silnie spada COP, gdy rośnie różnica temperatur (prawy dolny róg vs lewy górny róg). "
            "Czerwona gwiazdka wskazuje Twój aktualny punkt pracy."
        )

        evap_grid_min = min(-15.0, t_evap_c - 2.0)
        evap_grid_max = max(15.0, t_evap_c + 2.0)
        cond_grid_min = max(evap_grid_max + 5.0, min(30.0, t_cond_c - 2.0))
        cond_grid_max = min(float(int(limits["T_crit_C"] - 5.0)), max(60.0, t_cond_c + 2.0))

        try:
            with st.spinner("Obliczanie siatki punktów TESPy i interpolacji kubicznej SciPy..."):
                sens_data = run_sensitivity_grid_cached(
                    cycle_dict,
                    t_evap_range=(evap_grid_min, evap_grid_max),
                    t_cond_range=(cond_grid_min, cond_grid_max),
                    n_points=5,
                )
                st.plotly_chart(
                    create_cop_contour_plot(sens_data, t_evap_c, t_cond_c),
                    width="stretch",
                    theme="streamlit",
                )
        except Exception as err:
            st.warning(f"Nie udało się wygenerować mapy wrażliwości COP: {err}")

    # === ZAKŁADKA 5: SŁOWNICZEK DLA NOWYCH PRACOWNIKÓW ===
    with tab_glossary:
        st.subheader("Kompendium pojęć termodynamicznych")
        st.markdown(
            "Poniżej zebrano najważniejsze pojęcia, które pojawiają się podczas pracy z pompami ciepła w naszym instytucie."
        )

        g_col1, g_col2 = st.columns(2)

        with g_col1:
            st.markdown(
                """
                #### 1. Współczynnik COP i granica Carnota
                - **COP (Coefficient of Performance):** stosunek ciepła oddanego do budynku ($Q_{cond}$) do pobranej energii elektrycznej ($P_{el}$). Wartość `COP = 4.0` oznacza, że z `1 kWh` prądu uzyskujemy `4 kWh` ciepła (`3 kWh` pochodzi z natury!).
                - **Obieg Carnota ($COP_{Carnot} = T_{cond} / (T_{cond} - T_{evap})$):** teoretyczne maksimum sprawności dla danych temperatur (w Kelvinach). Rzeczywiste pompy osiągają zwykle `45–60%` granicy Carnota (tzw. **sprawność egzergowa**).
                - **Złota zasada:** im mniejszy skok temperatury $\\Delta T_{lift} = T_{cond} - T_{evap}$, tym wyższe COP. Dlatego ogrzewanie podłogowe (`35°C`) jest znacznie oszczędniejsze od grzejników (`55°C`).

                #### 2. Przegrzanie ($\\Delta T_{sh}$) i dochłodzenie ($\\Delta T_{sc}$)
                - **Przegrzanie (Superheat):** ogrzanie pary w parowniku powyżej temperatury wrzenia. Chroni sprężarkę przed uderzeniem hydraulicznym (ciecz jest nieściśliwa!). Zbyt duże przegrzanie podnosi jednak temperaturę tłoczenia $T_2$.
                - **Dochłodzenie (Subcooling):** schłodzenie skroplonej cieczy poniżej temperatury skraplania. Zmniejsza ilość pary powstającej na zaworze rozprężnym (*flash gas*) i zwiększa ilość ciepła odbieranego w parowniku.
                """
            )

        with g_col2:
            st.markdown(
                """
                #### 3. Własności czynnika i parametry sprężarki
                - **Stopień suchości ($x$):** udział masowy pary w mieszaninie dwufazowej ($x=0$ to czysta ciecz nasycona, $x=1$ to czysta para nasycona). Za zaworem dławiącym czynnik ma zwykle $x \\approx 0.15\\text{--}0.35$.
                - **Sprawność izentropowa ($\\eta_s$):** miara strat wewnętrznych sprężarki (tarcie, straty przepływowe, nieszczelności). Dla $\\eta_s = 1.0$ sprężanie byłoby idealnie odwracalne ($s = \\text{const}$).
                - **Spręż ($\\Pi = p_2 / p_1$):** stosunek ciśnienia po stronie wysokiej do niskiej. Duży spręż obciąża mechanicznie sprężarkę i obniża jej sprawność objętościową.

                #### 4. Dobór czynnika chłodniczego (GWP i bezpieczeństwo)
                - **GWP (Global Warming Potential):** wskaźnik potencjału tworzenia efektu cieplarnianego (dla CO₂ = 1). Nowoczesne konstrukcje przechodzą na czynniki o ultraniskim GWP (np. **R290 propan**, **R1234yf**).
                - **Klasy bezpieczeństwa (ASHRAE 34):**
                  - `A1` — nietoksyczne, niepalne (np. R134a, R410A)
                  - `A2L` — nietoksyczne, trudno palne (np. R32, R1234yf)
                  - `A3` — nietoksyczne, wysoce palne (np. R290, R600a — wymagają odpowiedniej strefy bezpieczeństwa)
                  - `B2L` — toksyczne, trudno palne (np. R717 amoniak — układy przemysłowe)
                """
            )

# --- STOPKA ---
st.divider()
st.markdown(
    '<div class="app-footer">'
    'Autor aplikacji: <a href="https://github.com/LatoSzymon" target="_blank">Szymon Lato</a> '
    '• Kalkulator Obiegu Pompy Ciepła (TESPy + CoolProp + SciPy)'
    "</div>",
    unsafe_allow_html=True,
)
