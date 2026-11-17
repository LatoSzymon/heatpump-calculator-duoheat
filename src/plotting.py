"""Moduł wizualizacji wykresów termodynamicznych log(p)-h, T-s oraz map sprawności."""

from typing import Dict, Any
import numpy as np
import plotly.graph_objects as go
import CoolProp.CoolProp as CP


def _compute_saturation_dome(fluid: str, n_points: int = 120) -> Dict[str, np.ndarray]:
    """Wyznacza krzywą nasycenia (x=0 oraz x=1) dla zadanego czynnika chłodniczego."""
    t_min = max(CP.PropsSI("Tmin", fluid) + 2.0, 223.15)  # min. -50°C lub T_min + 2K
    t_crit = CP.PropsSI("Tcrit", fluid)

    # Zagęszczenie punktów w pobliżu punktu krytycznego
    t_vals = np.concatenate(
        [
            np.linspace(t_min, t_crit - 5.0, int(n_points * 0.75), endpoint=False),
            np.linspace(t_crit - 5.0, t_crit - 0.05, int(n_points * 0.25)),
        ]
    )

    p_liq, h_liq, s_liq = [], [], []
    p_vap, h_vap, s_vap = [], [], []
    t_c_list = []

    for tk in t_vals:
        try:
            pl = CP.PropsSI("P", "T", tk, "Q", 0.0, fluid) / 1e5
            hl = CP.PropsSI("H", "T", tk, "Q", 0.0, fluid) / 1e3
            sl = CP.PropsSI("S", "T", tk, "Q", 0.0, fluid) / 1e3

            pv = CP.PropsSI("P", "T", tk, "Q", 1.0, fluid) / 1e5
            hv = CP.PropsSI("H", "T", tk, "Q", 1.0, fluid) / 1e3
            sv = CP.PropsSI("S", "T", tk, "Q", 1.0, fluid) / 1e3

            p_liq.append(pl)
            h_liq.append(hl)
            s_liq.append(sl)
            p_vap.append(pv)
            h_vap.append(hv)
            s_vap.append(sv)
            t_c_list.append(tk - 273.15)
        except Exception:
            continue

    # Punkt krytyczny spinający obie gałęzie
    p_crit = CP.PropsSI("pcrit", fluid) / 1e5
    h_crit = CP.PropsSI("H", "T", t_crit - 0.01, "Q", 0.5, fluid) / 1e3
    s_crit = CP.PropsSI("S", "T", t_crit - 0.01, "Q", 0.5, fluid) / 1e3

    h_dome = np.array(h_liq + [h_crit] + h_vap[::-1])
    p_dome = np.array(p_liq + [p_crit] + p_vap[::-1])
    s_dome = np.array(s_liq + [s_crit] + s_vap[::-1])
    t_dome = np.array(t_c_list + [t_crit - 273.15] + t_c_list[::-1])

    return {
        "h_dome": h_dome,
        "p_dome": p_dome,
        "s_dome": s_dome,
        "t_dome": t_dome,
    }


def create_ph_diagram(plot_data: Dict[str, Any]) -> go.Figure:
    """Tworzy interaktywny wykres log(p)-h (Molliera) z naniesionym obiegiem pompy ciepła."""
    fluid = plot_data["fluid"]
    dome = _compute_saturation_dome(fluid)

    fig = go.Figure()

    # 1. Krzywa nasycenia (dzwon dwufazowy)
    fig.add_trace(
        go.Scatter(
            x=dome["h_dome"],
            y=dome["p_dome"],
            mode="lines",
            name="Krzywa nasycenia (x=0 / x=1)",
            line=dict(color="#64748B", width=2, dash="dash"),
            fill="toself",
            fillcolor="rgba(148, 163, 184, 0.12)",
            hovertemplate="h = %{x:.1f} kJ/kg<br>p = %{y:.2f} bar<extra>Nasycenie</extra>",
        )
    )

    # 2. Zamknięty obieg pompy ciepła (1 -> 2 -> 3 -> 4 -> 1)
    h_cycle = plot_data["h_kj_kg"] + [plot_data["h_kj_kg"][0]]
    p_cycle = plot_data["p_bar"] + [plot_data["p_bar"][0]]
    t_cycle = plot_data["T_c"] + [plot_data["T_c"][0]]

    fig.add_trace(
        go.Scatter(
            x=h_cycle,
            y=p_cycle,
            mode="lines",
            name="Obieg pompy ciepła",
            line=dict(color="#EF4444", width=3.5),
            hoverinfo="skip",
        )
    )

    # 3. Punkty węzłowe (1, 2, 3, 4)
    labels = ["1 (Ssanie)", "2 (Tłoczenie)", "3 (Za skraplaczem)", "4 (Za zaworem)"]
    fig.add_trace(
        go.Scatter(
            x=plot_data["h_kj_kg"],
            y=plot_data["p_bar"],
            mode="markers+text",
            name="Punkty węzłowe (1–4)",
            text=["1", "2", "3", "4"],
            textposition=["bottom right", "top right", "top left", "bottom left"],
            textfont=dict(size=14, color="#1E293B", family="Arial Black"),
            marker=dict(
                size=11,
                color="#DC2626",
                line=dict(width=2, color="#FFFFFF"),
            ),
            customdata=np.column_stack((labels, plot_data["T_c"], plot_data["s_kj_kgk"])),
            hovertemplate=(
                "<b>Punkt %{customdata[0]}</b><br>"
                "p = %{y:.2f} bar<br>"
                "h = %{x:.2f} kJ/kg<br>"
                "T = %{customdata[1]:.2f} °C<br>"
                "s = %{customdata[2]:.4f} kJ/(kg·K)<extra></extra>"
            ),
        )
    )

    fig.update_layout(
        title=f"Wykres log(p)-h (Molliera) — czynnik {fluid}",
        xaxis_title="Entalpia właściwa h [kJ/kg]",
        yaxis_title="Ciśnienie absolutne p [bar] (skala log)",
        yaxis_type="log",
        template="plotly_white",
        height=520,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=50, r=30, t=70, b=50),
    )

    return fig


def create_ts_diagram(plot_data: Dict[str, Any]) -> go.Figure:
    """Tworzy interaktywny wykres T-s z uwzględnieniem punktów załamania na krzywej nasycenia."""
    fluid = plot_data["fluid"]
    dome = _compute_saturation_dome(fluid)

    fig = go.Figure()

    # 1. Krzywa nasycenia
    fig.add_trace(
        go.Scatter(
            x=dome["s_dome"],
            y=dome["t_dome"],
            mode="lines",
            name="Krzywa nasycenia (x=0 / x=1)",
            line=dict(color="#64748B", width=2, dash="dash"),
            fill="toself",
            fillcolor="rgba(148, 163, 184, 0.12)",
            hovertemplate="s = %{x:.4f} kJ/(kg·K)<br>T = %{y:.1f} °C<extra>Nasycenie</extra>",
        )
    )

    # 2. Ścieżka przemian z punktami nasycenia (dokładny przebieg izobar w obszarze dwufazowym)
    fig.add_trace(
        go.Scatter(
            x=plot_data["path_s_kj_kgk"],
            y=plot_data["path_T_c"],
            mode="lines",
            name="Przemiany obiegu",
            line=dict(color="#2563EB", width=3.5),
            hoverinfo="skip",
        )
    )

    # 3. Główne punkty węzłowe (1, 2, 3, 4)
    labels = ["1 (Ssanie)", "2 (Tłoczenie)", "3 (Za skraplaczem)", "4 (Za zaworem)"]
    fig.add_trace(
        go.Scatter(
            x=plot_data["s_kj_kgk"],
            y=plot_data["T_c"],
            mode="markers+text",
            name="Punkty węzłowe (1–4)",
            text=["1", "2", "3", "4"],
            textposition=["bottom right", "top right", "bottom left", "bottom left"],
            textfont=dict(size=14, color="#1E293B", family="Arial Black"),
            marker=dict(
                size=11,
                color="#1D4ED8",
                line=dict(width=2, color="#FFFFFF"),
            ),
            customdata=np.column_stack((labels, plot_data["p_bar"], plot_data["h_kj_kg"])),
            hovertemplate=(
                "<b>Punkt %{customdata[0]}</b><br>"
                "T = %{y:.2f} °C<br>"
                "s = %{x:.4f} kJ/(kg·K)<br>"
                "p = %{customdata[1]:.2f} bar<br>"
                "h = %{customdata[2]:.2f} kJ/kg<extra></extra>"
            ),
        )
    )

    fig.update_layout(
        title=f"Wykres T-s (Temperatura-Entropia) — czynnik {fluid}",
        xaxis_title="Entropia właściwa s [kJ/(kg·K)]",
        yaxis_title="Temperatura T [°C]",
        template="plotly_white",
        height=520,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=50, r=30, t=70, b=50),
    )

    return fig


def create_cop_contour_plot(
    sensitivity_data: Dict[str, Any],
    current_t_evap: float,
    current_t_cond: float,
) -> go.Figure:
    """Tworzy mapę konturową COP = f(T_evap, T_cond) interpolowaną przy użyciu SciPy."""
    fig = go.Figure()

    fig.add_trace(
        go.Contour(
            x=sensitivity_data["fine_evap"],
            y=sensitivity_data["fine_cond"],
            z=sensitivity_data["fine_cop"].T,
            colorscale="Viridis",
            colorbar=dict(title="COP [-]"),
            contours=dict(
                coloring="heatmap",
                showlabels=True,
                labelfont=dict(size=12, color="white"),
            ),
            hovertemplate=(
                "T_evap = %{x:.1f} °C<br>"
                "T_cond = %{y:.1f} °C<br>"
                "<b>COP = %{z:.2f}</b><extra></extra>"
            ),
        )
    )

    # Aktualny punkt pracy
    fig.add_trace(
        go.Scatter(
            x=[current_t_evap],
            y=[current_t_cond],
            mode="markers+text",
            name="Aktualny punkt pracy",
            text=["Punkt pracy"],
            textposition="top center",
            textfont=dict(color="white", size=13),
            marker=dict(
                size=14,
                symbol="star",
                color="#EF4444",
                line=dict(width=2, color="white"),
            ),
        )
    )

    fig.update_layout(
        title="Mapa efektywności COP = f(T_parowania, T_skraplania) [interpolacja SciPy]",
        xaxis_title="Temperatura parowania T_evap [°C]",
        yaxis_title="Temperatura skraplania T_cond [°C]",
        template="plotly_white",
        height=500,
        margin=dict(l=50, r=30, t=70, b=50),
    )

    return fig
