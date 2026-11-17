"""Moduł wizualizacji: schemat obiegu, bilans energii, wykresy log(p)-h, T-s oraz mapy sprawności."""

from typing import Dict, Any, TYPE_CHECKING
import numpy as np
import plotly.graph_objects as go
import CoolProp.CoolProp as CP

if TYPE_CHECKING:
    from src.cycle_model import CycleResult


def _compute_saturation_dome(fluid: str, n_points: int = 120) -> Dict[str, Any]:
    """Wyznacza krzywą nasycenia (x=0 oraz x=1) dla zadanego czynnika chłodniczego."""
    t_min = max(CP.PropsSI("Tmin", fluid) + 2.0, 223.15)
    t_crit = CP.PropsSI("Tcrit", fluid)

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
            pl = CP.PropsSI("P", "T", float(tk), "Q", 0.0, fluid) / 1e5
            hl = CP.PropsSI("H", "T", float(tk), "Q", 0.0, fluid) / 1e3
            sl = CP.PropsSI("S", "T", float(tk), "Q", 0.0, fluid) / 1e3

            pv = CP.PropsSI("P", "T", float(tk), "Q", 1.0, fluid) / 1e5
            hv = CP.PropsSI("H", "T", float(tk), "Q", 1.0, fluid) / 1e3
            sv = CP.PropsSI("S", "T", float(tk), "Q", 1.0, fluid) / 1e3

            p_liq.append(pl)
            h_liq.append(hl)
            s_liq.append(sl)
            p_vap.append(pv)
            h_vap.append(hv)
            s_vap.append(sv)
            t_c_list.append(float(tk) - 273.15)
        except Exception:
            continue

    if not h_liq:
        raise ValueError(f"Nie udało się wyznaczyć krzywej nasycenia dla czynnika {fluid}.")

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
        "h_crit": h_crit,
        "p_crit": p_crit,
        "s_crit": s_crit,
        "t_crit_c": t_crit - 273.15,
    }


def create_cycle_schematic(result: "CycleResult") -> go.Figure:
    """
    Tworzy interaktywny, responsywny schemat ideowy 4-elementowego obiegu pompy ciepła
    z przezroczystym tłem (kompatybilny z trybem ciemnym i jasnym) oraz bez nakładających się etykiet.
    """
    pd_data = result.plot_data
    p_vals = pd_data["p_bar"]
    t_vals = pd_data["T_c"]

    fig = go.Figure()

    pipes = [
        dict(x=[8.0, 6.3], y=[1.2, 1.2], color="#0284C7", name="4 → Parownik (wrzenie)"),
        dict(x=[3.7, 2.0, 2.0], y=[1.2, 1.2, 2.45], color="#38BDF8", name="1 (Ssanie sprężarki)"),
        dict(x=[2.0, 2.0, 3.7], y=[3.55, 4.8, 4.8], color="#EF4444", name="2 (Gorąca para)"),
        dict(x=[6.3, 8.0, 8.0], y=[4.8, 4.8, 3.5], color="#F97316", name="3 (Ciecz pod ciśnieniem)"),
        dict(x=[8.0, 8.0], y=[2.5, 1.2], color="#0EA5E9", name="4 (Mieszanina dwufazowa)"),
    ]

    for pipe in pipes:
        fig.add_trace(
            go.Scatter(
                x=pipe["x"],
                y=pipe["y"],
                mode="lines",
                line=dict(color=pipe["color"], width=5),
                hoverinfo="text",
                text=pipe["name"],
                showlegend=False,
            )
        )

    shapes = [
        dict(
            type="rect", x0=3.7, y0=4.25, x1=6.3, y1=5.35,
            fillcolor="rgba(239, 68, 68, 0.14)", line=dict(color="#EF4444", width=2.5),
        ),
        dict(
            type="rect", x0=3.7, y0=0.65, x1=6.3, y1=1.75,
            fillcolor="rgba(14, 165, 233, 0.14)", line=dict(color="#0EA5E9", width=2.5),
        ),
        dict(
            type="circle", x0=1.35, y0=2.35, x1=2.65, y1=3.65,
            fillcolor="rgba(249, 115, 22, 0.14)", line=dict(color="#F97316", width=2.5),
        ),
        dict(
            type="rect", x0=7.35, y0=2.5, x1=8.65, y1=3.5,
            fillcolor="rgba(34, 197, 94, 0.14)", line=dict(color="#22C55E", width=2.5),
        ),
    ]

    node_x = [2.0, 2.8, 7.2, 8.0]
    node_y = [1.85, 4.8, 4.8, 1.85]
    node_labels = ["1", "2", "3", "4"]
    node_colors = ["#0284C7", "#DC2626", "#EA580C", "#0EA5E9"]
    node_hovers = [
        f"<b>Punkt 1: Ssanie sprężarki</b><br>T = {t_vals[0]:.1f} °C | p = {p_vals[0]:.2f} bar",
        f"<b>Punkt 2: Tłoczenie sprężarki</b><br>T = {t_vals[1]:.1f} °C | p = {p_vals[1]:.2f} bar",
        f"<b>Punkt 3: Za skraplaczem</b><br>T = {t_vals[2]:.1f} °C | p = {p_vals[2]:.2f} bar",
        f"<b>Punkt 4: Za zaworem dławiącym</b><br>T = {t_vals[3]:.1f} °C | p = {p_vals[3]:.2f} bar | x = {result.x_4 * 100:.1f}%",
    ]

    fig.add_trace(
        go.Scatter(
            x=node_x,
            y=node_y,
            mode="markers+text",
            text=node_labels,
            textposition="middle center",
            textfont=dict(color="white", size=13, family="Arial Black"),
            marker=dict(size=25, color=node_colors, line=dict(width=2, color="white")),
            hovertext=node_hovers,
            hoverinfo="text",
            showlegend=False,
        )
    )

    annotations = [
        dict(x=5.0, y=4.8, text="<b>SKRAPLACZ</b><br><span style='font-size:11px'>Oddaje ciepło</span>", showarrow=False, font=dict(color="#F87171", size=13)),
        dict(x=5.0, y=1.2, text="<b>PAROWNIK</b><br><span style='font-size:11px'>Pobiera ciepło</span>", showarrow=False, font=dict(color="#38BDF8", size=13)),
        dict(x=2.0, y=3.0, text="<b>SPRĘŻARKA</b>", showarrow=False, font=dict(color="#FB923C", size=11)),
        dict(x=8.0, y=3.0, text="<b>ZAWÓR</b><br><span style='font-size:10px'>dławiący</span>", showarrow=False, font=dict(color="#4ADE80", size=11)),

        dict(
            x=5.0, y=6.0, ax=5.0, ay=5.4, xref="x", yref="y", axref="x", ayref="y",
            showarrow=True, arrowhead=2, arrowsize=1.3, arrowwidth=3, arrowcolor="#EF4444",
        ),
        dict(
            x=5.0, y=6.35,
            text=f"<b>Q_cond = {result.q_cond_kw:.2f} kW</b> (do budynku)",
            showarrow=False, font=dict(color="#F87171", size=13),
        ),
        dict(
            x=5.0, y=0.6, ax=5.0, ay=0.0, xref="x", yref="y", axref="x", ayref="y",
            showarrow=True, arrowhead=2, arrowsize=1.3, arrowwidth=3, arrowcolor="#0EA5E9",
        ),
        dict(
            x=5.0, y=-0.35,
            text=f"<b>Q_evap = {result.q_evap_kw:.2f} kW</b> (z otoczenia)",
            showarrow=False, font=dict(color="#38BDF8", size=13),
        ),
        dict(
            x=1.3, y=3.0, ax=0.25, ay=3.0, xref="x", yref="y", axref="x", ayref="y",
            showarrow=True, arrowhead=2, arrowsize=1.3, arrowwidth=3, arrowcolor="#F97316",
        ),
        dict(
            x=0.35, y=3.55,
            text=f"<b>P_el = {result.p_comp_kw:.2f} kW</b><br>(Prąd)",
            showarrow=False, font=dict(color="#FB923C", size=12),
        ),

        dict(x=1.05, y=1.85, text=f"<b>{t_vals[0]:.1f} °C</b><br>{p_vals[0]:.2f} bar", showarrow=False, font=dict(size=11, color="#38BDF8")),
        dict(x=2.8, y=5.45, text=f"<b>{t_vals[1]:.1f} °C</b><br>{p_vals[1]:.2f} bar", showarrow=False, font=dict(size=11, color="#F87171")),
        dict(x=7.2, y=5.45, text=f"<b>{t_vals[2]:.1f} °C</b><br>{p_vals[2]:.2f} bar", showarrow=False, font=dict(size=11, color="#FB923C")),
        dict(x=9.1, y=1.85, text=f"<b>{t_vals[3]:.1f} °C</b><br>x = {result.x_4 * 100:.0f}% pary", showarrow=False, font=dict(size=11, color="#38BDF8")),

        dict(x=2.0, y=4.25, ax=2.0, ay=3.75, xref="x", yref="y", axref="x", ayref="y", showarrow=True, arrowhead=2, arrowcolor="#EF4444", arrowwidth=2),
        dict(x=8.0, y=2.05, ax=8.0, ay=2.45, xref="x", yref="y", axref="x", ayref="y", showarrow=True, arrowhead=2, arrowcolor="#0EA5E9", arrowwidth=2),
    ]

    fig.update_layout(
        shapes=shapes,
        annotations=annotations,
        xaxis=dict(range=[-0.4, 10.2], visible=False, fixedrange=True),
        yaxis=dict(range=[-0.65, 6.7], visible=False, fixedrange=True),
        height=400,
        margin=dict(l=5, r=5, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    return fig


def create_energy_balance_bar(result: "CycleResult") -> go.Figure:
    """Tworzy czytelny wykres bilansu energii: Q_evap + P_el = Q_cond bez nakładającej się legendy."""
    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            y=["Źródło"],
            x=[result.q_evap_kw],
            name=f"Z natury ({result.q_evap_kw:.2f} kW)",
            orientation="h",
            marker=dict(color="#0284C7"),
            text=f"Z natury: {result.q_evap_kw:.2f} kW",
            textposition="inside",
            insidetextanchor="middle",
        )
    )
    fig.add_trace(
        go.Bar(
            y=["Źródło"],
            x=[result.p_comp_kw],
            name=f"Prąd ({result.p_comp_kw:.2f} kW)",
            orientation="h",
            marker=dict(color="#EA580C"),
            text=f"Prąd: {result.p_comp_kw:.2f} kW",
            textposition="inside",
            insidetextanchor="middle",
        )
    )
    fig.add_trace(
        go.Bar(
            y=["Budynek"],
            x=[result.q_cond_kw],
            name=f"Do budynku ({result.q_cond_kw:.2f} kW)",
            orientation="h",
            marker=dict(color="#DC2626"),
            text=f"Q_cond = {result.q_cond_kw:.2f} kW (COP {result.cop_heating:.2f})",
            textposition="inside",
            insidetextanchor="middle",
        )
    )

    fig.update_layout(
        barmode="stack",
        title="Bilans mocy: Q_evap + P_el = Q_cond",
        xaxis_title="Moc [kW]",
        height=190,
        showlegend=False,
        margin=dict(l=10, r=10, t=40, b=40),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    return fig


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
            name="Nasycenie (x=0 / x=1)",
            line=dict(color="#94A3B8", width=2, dash="dash"),
            fill="toself",
            fillcolor="rgba(148, 163, 184, 0.12)",
            hovertemplate="h = %{x:.1f} kJ/kg<br>p = %{y:.2f} bar<extra>Nasycenie</extra>",
        )
    )

    # 2. Zamknięty obieg pompy ciepła (1 -> 2 -> 3 -> 4 -> 1)
    fig.add_trace(
        go.Scatter(
            x=plot_data["path_h_kj_kg"],
            y=plot_data["path_p_bar"],
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
            name="Punkty (1–4)",
            text=["1", "2", "3", "4"],
            textposition=["bottom right", "top right", "top left", "bottom left"],
            textfont=dict(size=14, family="Arial Black"),
            marker=dict(
                size=11,
                color="#EF4444",
                line=dict(width=2, color="#FFFFFF"),
            ),
            customdata=list(zip(labels, plot_data["T_c"], plot_data["s_kj_kgk"])),
            hovertemplate=(
                "<b>Punkt %{customdata[0]}</b><br>"
                "p = %{y:.2f} bar<br>"
                "h = %{x:.2f} kJ/kg<br>"
                "T = %{customdata[1]:.2f} °C<br>"
                "s = %{customdata[2]:.4f} kJ/(kg·K)<extra></extra>"
            ),
        )
    )

    # UWAGA: Na osi logarytmicznej Plotly (yaxis_type="log") współrzędna y adnotacji musi być w skali log10!
    h_min = float(np.min(dome["h_dome"]))
    h_max = float(np.max(dome["h_dome"]))
    p_mid = float(np.sqrt(plot_data["p_evap_bar"] * plot_data["p_cond_bar"]))
    fig.add_annotation(
        x=dome["h_crit"],
        y=float(np.log10(p_mid)),
        text="Obszar dwufazowy<br>(ciecz + para)",
        showarrow=False,
        font=dict(size=11, color="#94A3B8"),
    )
    fig.add_annotation(
        x=h_min + 0.08 * (h_max - h_min),
        y=float(np.log10(plot_data["p_cond_bar"] * 0.75)),
        text="Ciecz<br>dochłodzona",
        showarrow=False,
        font=dict(size=10, color="#38BDF8"),
    )
    fig.add_annotation(
        x=h_max - 0.05 * (h_max - h_min),
        y=float(np.log10(p_mid)),
        text="Para<br>przegrzana",
        showarrow=False,
        font=dict(size=10, color="#F87171"),
    )

    fig.update_layout(
        title=f"Wykres log(p)-h (Molliera) — {fluid}",
        xaxis_title="Entalpia właściwa h [kJ/kg]",
        yaxis_title="Ciśnienie absolutne p [bar] (log)",
        yaxis_type="log",
        height=490,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", yanchor="top", y=-0.24, xanchor="center", x=0.5),
        margin=dict(l=45, r=20, t=50, b=105),
    )

    return fig


def create_ts_diagram(plot_data: Dict[str, Any]) -> go.Figure:
    """Tworzy interaktywny wykres T-s z gładkimi przemianami oraz punktami na krzywej nasycenia."""
    fluid = plot_data["fluid"]
    dome = _compute_saturation_dome(fluid)

    fig = go.Figure()

    # 1. Krzywa nasycenia
    fig.add_trace(
        go.Scatter(
            x=dome["s_dome"],
            y=dome["t_dome"],
            mode="lines",
            name="Nasycenie (x=0 / x=1)",
            line=dict(color="#94A3B8", width=2, dash="dash"),
            fill="toself",
            fillcolor="rgba(148, 163, 184, 0.12)",
            hovertemplate="s = %{x:.4f} kJ/(kg·K)<br>T = %{y:.1f} °C<extra>Nasycenie</extra>",
        )
    )

    # 2. Gładka ścieżka przemian z punktami nasycenia
    fig.add_trace(
        go.Scatter(
            x=plot_data["path_s_kj_kgk"],
            y=plot_data["path_T_c"],
            mode="lines",
            name="Przemiany obiegu",
            line=dict(color="#3B82F6", width=3.5),
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
            name="Punkty (1–4)",
            text=["1", "2", "3", "4"],
            textposition=["bottom right", "top right", "bottom left", "bottom left"],
            textfont=dict(size=14, family="Arial Black"),
            marker=dict(
                size=11,
                color="#3B82F6",
                line=dict(width=2, color="#FFFFFF"),
            ),
            customdata=list(zip(labels, plot_data["p_bar"], plot_data["h_kj_kg"])),
            hovertemplate=(
                "<b>Punkt %{customdata[0]}</b><br>"
                "T = %{y:.2f} °C<br>"
                "s = %{x:.4f} kJ/(kg·K)<br>"
                "p = %{customdata[1]:.2f} bar<br>"
                "h = %{customdata[2]:.2f} kJ/kg<extra></extra>"
            ),
        )
    )

    t_mid = 0.5 * (plot_data["t_evap_c"] + plot_data["t_cond_c"])
    fig.add_annotation(
        x=dome["s_crit"], y=t_mid,
        text="Obszar dwufazowy<br>(stała T podczas przemiany)",
        showarrow=False, font=dict(size=10, color="#94A3B8"),
    )

    fig.update_layout(
        title=f"Wykres T-s (Temperatura–Entropia) — {fluid}",
        xaxis_title="Entropia właściwa s [kJ/(kg·K)]",
        yaxis_title="Temperatura T [°C]",
        height=490,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", yanchor="top", y=-0.24, xanchor="center", x=0.5),
        margin=dict(l=45, r=20, t=50, b=105),
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
        title="Mapa efektywności COP = f(T_parowania, T_skraplania) [SciPy]",
        xaxis_title="Temperatura parowania T_evap [°C]",
        yaxis_title="Temperatura skraplania T_cond [°C]",
        height=480,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=45, r=20, t=50, b=50),
    )

    return fig


def create_subcooling_curve_plot(opt_res: Dict[str, Any]) -> go.Figure:
    """Tworzy wykres zależności efektywnego COP od stopnia dochłodzenia ΔT_sc."""
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=opt_res["curve_sc_k"],
            y=opt_res["curve_cop"],
            mode="lines+markers",
            name="Efektywne COP",
            line=dict(color="#3B82F6", width=3),
            marker=dict(size=6),
            hovertemplate="ΔT_sc = %{x:.1f} K<br>COP = %{y:.3f}<extra></extra>",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=[opt_res["optimal_subcooling_k"]],
            y=[opt_res["max_cop"]],
            mode="markers+text",
            name="Optimum",
            text=[f"Optimum ({opt_res['optimal_subcooling_k']:.1f} K)"],
            textposition="bottom center",
            marker=dict(size=13, symbol="star", color="#EF4444"),
        )
    )
    fig.update_layout(
        title="Wpływ dochłodzenia ΔT_sc na efektywne COP",
        xaxis_title="Dochłodzenie ΔT_sc [K]",
        yaxis_title="COP grzewcze [-]",
        height=330,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=40, r=20, t=45, b=85),
        legend=dict(orientation="h", yanchor="top", y=-0.28, xanchor="center", x=0.5),
    )
    return fig
