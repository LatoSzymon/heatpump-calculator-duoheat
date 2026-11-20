"""Moduł wizualizacji: schemat obiegu, bilans energii, wykresy log(p)-h, T-s oraz mapy sprawności."""

from typing import Dict, Any, TYPE_CHECKING
import numpy as np
import plotly.graph_objects as go
import CoolProp.CoolProp as CP

from src.i18n import normalize_lang, t

if TYPE_CHECKING:
    from src.cycle_model import CycleResult

_FONT_FAMILY = "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
_GRID_COLOR = "rgba(148, 163, 184, 0.14)"
_ZERO_COLOR = "rgba(148, 163, 184, 0.22)"
_HOVER_STYLE = dict(
    bgcolor="#0b2435",
    bordercolor="#0693e3",
    font=dict(color="#f1f5f9", family=_FONT_FAMILY, size=12),
)


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
    h_crit = 0.5 * (h_liq[-1] + h_vap[-1])
    s_crit = 0.5 * (s_liq[-1] + s_vap[-1])

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


def create_cycle_schematic(result: "CycleResult", lang: str = "pl") -> go.Figure:
    """
    Tworzy interaktywny, responsywny schemat ideowy 4-elementowego obiegu pompy ciepła
    z przezroczystym tłem (kompatybilny z trybem ciemnym i jasnym) oraz bez nakładających się etykiet.
    """
    pd_data = result.plot_data
    p_vals = pd_data["p_bar"]
    t_vals = pd_data["T_c"]

    fig = go.Figure()

    pipes = [
        dict(x=[8.0, 6.3], y=[1.2, 1.2], color="#0693e3", name=t("plot_pipe_4_evap", lang)),
        dict(x=[3.7, 2.0, 2.0], y=[1.2, 1.2, 2.45], color="#8ed1fc", name=t("plot_pipe_1_suction", lang)),
        dict(x=[2.0, 2.0, 3.7], y=[3.55, 4.8, 4.8], color="#ff5a1f", name=t("plot_pipe_2_hot", lang)),
        dict(x=[6.3, 8.0, 8.0], y=[4.8, 4.8, 3.5], color="#ff6900", name=t("plot_pipe_3_liq", lang)),
        dict(x=[8.0, 8.0], y=[2.5, 1.2], color="#0693e3", name=t("plot_pipe_4_two", lang)),
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
            fillcolor="rgba(255, 90, 31, 0.14)", line=dict(color="#ff5a1f", width=2.5),
        ),
        dict(
            type="rect", x0=3.7, y0=0.65, x1=6.3, y1=1.75,
            fillcolor="rgba(6, 147, 227, 0.14)", line=dict(color="#0693e3", width=2.5),
        ),
        dict(
            type="circle", x0=1.35, y0=2.35, x1=2.65, y1=3.65,
            fillcolor="rgba(255, 105, 0, 0.14)", line=dict(color="#ff6900", width=2.5),
        ),
        dict(
            type="rect", x0=7.35, y0=2.5, x1=8.65, y1=3.5,
            fillcolor="rgba(0, 208, 132, 0.14)", line=dict(color="#00d084", width=2.5),
        ),
    ]

    node_x = [2.0, 2.8, 7.2, 8.0]
    node_y = [1.85, 4.8, 4.8, 1.85]
    node_labels = ["1", "2", "3", "4"]
    node_colors = ["#0693e3", "#ff5a1f", "#ff6900", "#0693e3"]
    node_hovers = [
        t("plot_hover_pt1", lang, T=t_vals[0], p=p_vals[0]),
        t("plot_hover_pt2", lang, T=t_vals[1], p=p_vals[1]),
        t("plot_hover_pt3", lang, T=t_vals[2], p=p_vals[2]),
        t("plot_hover_pt4", lang, T=t_vals[3], p=p_vals[3], x=result.x_4 * 100),
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
        dict(x=5.0, y=4.8, text=t("plot_ann_cond", lang), showarrow=False, font=dict(color="#ff8a5c", size=13, family=_FONT_FAMILY)),
        dict(x=5.0, y=1.2, text=t("plot_ann_evap", lang), showarrow=False, font=dict(color="#67c8ff", size=13, family=_FONT_FAMILY)),
        dict(x=2.0, y=3.0, text=t("plot_ann_comp", lang), showarrow=False, font=dict(color="#ff9f5a", size=11, family=_FONT_FAMILY)),
        dict(x=8.0, y=3.0, text=t("plot_ann_valve", lang), showarrow=False, font=dict(color="#4ade80", size=11, family=_FONT_FAMILY)),

        dict(
            x=5.0, y=6.0, ax=5.0, ay=5.4, xref="x", yref="y", axref="x", ayref="y",
            showarrow=True, arrowhead=2, arrowsize=1.3, arrowwidth=3, arrowcolor="#ff5a1f",
        ),
        dict(
            x=5.0, y=6.35,
            text=t("plot_ann_qcond", lang, q=result.q_cond_kw),
            showarrow=False, font=dict(color="#ff8a5c", size=13, family=_FONT_FAMILY),
        ),
        dict(
            x=5.0, y=0.6, ax=5.0, ay=0.0, xref="x", yref="y", axref="x", ayref="y",
            showarrow=True, arrowhead=2, arrowsize=1.3, arrowwidth=3, arrowcolor="#0693e3",
        ),
        dict(
            x=5.0, y=-0.35,
            text=t("plot_ann_qevap", lang, q=result.q_evap_kw),
            showarrow=False, font=dict(color="#67c8ff", size=13, family=_FONT_FAMILY),
        ),
        dict(
            x=1.3, y=3.0, ax=0.25, ay=3.0, xref="x", yref="y", axref="x", ayref="y",
            showarrow=True, arrowhead=2, arrowsize=1.3, arrowwidth=3, arrowcolor="#ff8a3d",
        ),
        dict(
            x=0.35, y=3.55,
            text=t("plot_ann_pcomp", lang, p=result.p_comp_kw),
            showarrow=False, font=dict(color="#ff9f5a", size=12, family=_FONT_FAMILY),
        ),

        dict(x=1.05, y=1.85, text=f"<b>{t_vals[0]:.1f} °C</b><br>{p_vals[0]:.2f} bar", showarrow=False, font=dict(size=11, color="#67c8ff", family=_FONT_FAMILY)),
        dict(x=2.8, y=5.45, text=f"<b>{t_vals[1]:.1f} °C</b><br>{p_vals[1]:.2f} bar", showarrow=False, font=dict(size=11, color="#ff8a5c", family=_FONT_FAMILY)),
        dict(x=7.2, y=5.45, text=f"<b>{t_vals[2]:.1f} °C</b><br>{p_vals[2]:.2f} bar", showarrow=False, font=dict(size=11, color="#ff9f5a", family=_FONT_FAMILY)),
        dict(x=9.1, y=1.85, text=f"<b>{t_vals[3]:.1f} °C</b><br>x = {result.x_4 * 100:.0f}%", showarrow=False, font=dict(size=11, color="#67c8ff", family=_FONT_FAMILY)),

        dict(x=2.0, y=4.25, ax=2.0, ay=3.75, xref="x", yref="y", axref="x", ayref="y", showarrow=True, arrowhead=2, arrowcolor="#ff5a1f", arrowwidth=2),
        dict(x=8.0, y=2.05, ax=8.0, ay=2.45, xref="x", yref="y", axref="x", ayref="y", showarrow=True, arrowhead=2, arrowcolor="#0693e3", arrowwidth=2),
    ]

    fig.update_layout(
        shapes=shapes,
        annotations=annotations,
        font=dict(family=_FONT_FAMILY, color="#e2e8f0"),
        hoverlabel=_HOVER_STYLE,
        xaxis=dict(range=[-0.4, 10.2], visible=False, fixedrange=True),
        yaxis=dict(range=[-0.65, 6.7], visible=False, fixedrange=True),
        height=400,
        margin=dict(l=5, r=5, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    return fig


def create_energy_balance_bar(result: "CycleResult", lang: str = "pl") -> go.Figure:
    """Tworzy czytelny wykres bilansu energii: Q_evap + P_el = Q_cond bez nakładającej się legendy."""
    fig = go.Figure()
    lbl_src = t("plot_bal_sources", lang)
    lbl_out = t("plot_bal_output", lang)

    fig.add_trace(
        go.Bar(
            y=[lbl_src],
            x=[result.q_evap_kw],
            name=f"{t('plot_bal_evap', lang)} ({result.q_evap_kw:.2f} kW)",
            orientation="h",
            marker=dict(color="#0693e3"),
            text=f"{t('plot_bal_evap', lang)}: {result.q_evap_kw:.2f} kW",
            textposition="inside",
            insidetextanchor="middle",
        )
    )
    fig.add_trace(
        go.Bar(
            y=[lbl_src],
            x=[result.p_comp_kw],
            name=f"{t('plot_bal_comp', lang)} ({result.p_comp_kw:.2f} kW)",
            orientation="h",
            marker=dict(color="#ff6900"),
            text=f"{t('plot_bal_comp', lang)}: {result.p_comp_kw:.2f} kW",
            textposition="inside",
            insidetextanchor="middle",
        )
    )
    fig.add_trace(
        go.Bar(
            y=[lbl_out],
            x=[result.q_cond_kw],
            name=f"{t('plot_bal_cond', lang)} ({result.q_cond_kw:.2f} kW)",
            orientation="h",
            marker=dict(color="#ff5a1f"),
            text=f"Q_cond = {result.q_cond_kw:.2f} kW (COP {result.cop_heating:.2f})",
            textposition="inside",
            insidetextanchor="middle",
        )
    )

    fig.update_layout(
        barmode="stack",
        title=dict(
            text=t("plot_bal_title", lang, q_evap=result.q_evap_kw, p_comp=result.p_comp_kw, q_cond=result.q_cond_kw),
            font=dict(size=13, family=_FONT_FAMILY, color="#f1f5f9"),
        ),
        font=dict(family=_FONT_FAMILY, color="#cbd5e1", size=12),
        hoverlabel=_HOVER_STYLE,
        xaxis=dict(
            title=t("plot_bal_yaxis", lang),
            gridcolor=_GRID_COLOR,
            zerolinecolor=_ZERO_COLOR,
        ),
        yaxis=dict(gridcolor="rgba(0,0,0,0)"),
        height=190,
        showlegend=False,
        margin=dict(l=10, r=10, t=40, b=40),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    return fig


def create_ph_diagram(plot_data: Dict[str, Any], lang: str = "pl") -> go.Figure:
    """Tworzy interaktywny wykres log(p)-h (Molliera) z naniesionym obiegiem pompy ciepła."""
    fluid = plot_data["fluid"]
    dome = _compute_saturation_dome(fluid)
    is_en = normalize_lang(lang) == "en"

    fig = go.Figure()

    # 1. Krzywa nasycenia (dzwon dwufazowy)
    fig.add_trace(
        go.Scatter(
            x=dome["h_dome"],
            y=dome["p_dome"],
            mode="lines",
            name=t("plot_dome_name", lang),
            line=dict(color="#94A3B8", width=2, dash="dash"),
            fill="toself",
            fillcolor="rgba(148, 163, 184, 0.12)",
            hovertemplate=f"h = %{{x:.1f}} kJ/kg<br>p = %{{y:.2f}} bar<extra>{t('plot_dome_name', lang)}</extra>",
        )
    )

    # 2. Zamknięty obieg pompy ciepła (1 -> 2 -> 3 -> 4 -> 1)
    fig.add_trace(
        go.Scatter(
            x=plot_data["path_h_kj_kg"],
            y=plot_data["path_p_bar"],
            mode="lines",
            name=t("plot_cycle_name", lang, fluid=fluid),
            line=dict(color="#ff5a1f", width=3.5),
            hoverinfo="skip",
        )
    )

    # 3. Punkty węzłowe (1, 2, 3, 4)
    labels = (
        ["1 (Suction)", "2 (Discharge)", "3 (Condenser out)", "4 (Valve out)"]
        if is_en
        else ["1 (Ssanie)", "2 (Tłoczenie)", "3 (Za skraplaczem)", "4 (Za zaworem)"]
    )
    pt_word = t("plot_pt_prefix", lang)
    fig.add_trace(
        go.Scatter(
            x=plot_data["h_kj_kg"],
            y=plot_data["p_bar"],
            mode="markers+text",
            name="Points (1–4)" if is_en else "Punkty (1–4)",
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
                f"<b>{pt_word} %{{customdata[0]}}</b><br>"
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
        text="Two-phase region<br>(liquid + vapor)" if is_en else "Obszar dwufazowy<br>(ciecz + para)",
        showarrow=False,
        font=dict(size=11, color="#94A3B8"),
    )
    fig.add_annotation(
        x=h_min + 0.08 * (h_max - h_min),
        y=float(np.log10(plot_data["p_cond_bar"] * 0.75)),
        text="Subcooled<br>liquid" if is_en else "Ciecz<br>dochłodzona",
        showarrow=False,
        font=dict(size=10, color="#38BDF8"),
    )
    fig.add_annotation(
        x=h_max - 0.05 * (h_max - h_min),
        y=float(np.log10(p_mid)),
        text="Superheated<br>vapor" if is_en else "Para<br>przegrzana",
        showarrow=False,
        font=dict(size=10, color="#F87171"),
    )

    fig.update_layout(
        title=dict(text=t("plot_ph_title", lang, fluid=fluid), font=dict(size=15, family=_FONT_FAMILY, color="#f1f5f9")),
        font=dict(family=_FONT_FAMILY, color="#cbd5e1", size=12),
        hoverlabel=_HOVER_STYLE,
        xaxis=dict(title=t("plot_ph_xaxis", lang), gridcolor=_GRID_COLOR, zerolinecolor=_ZERO_COLOR),
        yaxis=dict(title=t("plot_ph_yaxis", lang), type="log", gridcolor=_GRID_COLOR, zerolinecolor=_ZERO_COLOR),
        height=460,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.24,
            xanchor="center",
            x=0.5,
            font=dict(size=11),
        ),
        margin=dict(l=48, r=16, t=52, b=110),
    )

    return fig


def create_ts_diagram(plot_data: Dict[str, Any], lang: str = "pl") -> go.Figure:
    """Tworzy interaktywny wykres T-s z gładkimi przemianami oraz punktami na krzywej nasycenia."""
    fluid = plot_data["fluid"]
    dome = _compute_saturation_dome(fluid)
    is_en = normalize_lang(lang) == "en"

    fig = go.Figure()

    # 1. Krzywa nasycenia
    fig.add_trace(
        go.Scatter(
            x=dome["s_dome"],
            y=dome["t_dome"],
            mode="lines",
            name=t("plot_dome_name", lang),
            line=dict(color="#94A3B8", width=2, dash="dash"),
            fill="toself",
            fillcolor="rgba(148, 163, 184, 0.12)",
            hovertemplate=f"s = %{{x:.4f}} kJ/(kg·K)<br>T = %{{y:.1f}} °C<extra>{t('plot_dome_name', lang)}</extra>",
        )
    )

    # 2. Gładka ścieżka przemian z punktami nasycenia
    fig.add_trace(
        go.Scatter(
            x=plot_data["path_s_kj_kgk"],
            y=plot_data["path_T_c"],
            mode="lines",
            name="Cycle processes" if is_en else "Przemiany obiegu",
            line=dict(color="#0693e3", width=3.5),
            hoverinfo="skip",
        )
    )

    # 3. Główne punkty węzłowe (1, 2, 3, 4)
    labels = (
        ["1 (Suction)", "2 (Discharge)", "3 (Condenser out)", "4 (Valve out)"]
        if is_en
        else ["1 (Ssanie)", "2 (Tłoczenie)", "3 (Za skraplaczem)", "4 (Za zaworem)"]
    )
    pt_word = t("plot_pt_prefix", lang)
    fig.add_trace(
        go.Scatter(
            x=plot_data["s_kj_kgk"],
            y=plot_data["T_c"],
            mode="markers+text",
            name="Points (1–4)" if is_en else "Punkty (1–4)",
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
                f"<b>{pt_word} %{{customdata[0]}}</b><br>"
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
        text="Two-phase region<br>(isothermal phase change)" if is_en else "Obszar dwufazowy<br>(stała T podczas przemiany)",
        showarrow=False, font=dict(size=10, color="#94A3B8"),
    )

    fig.update_layout(
        title=dict(text=t("plot_ts_title", lang, fluid=fluid), font=dict(size=15, family=_FONT_FAMILY, color="#f1f5f9")),
        font=dict(family=_FONT_FAMILY, color="#cbd5e1", size=12),
        hoverlabel=_HOVER_STYLE,
        xaxis=dict(title=t("plot_ts_xaxis", lang), gridcolor=_GRID_COLOR, zerolinecolor=_ZERO_COLOR),
        yaxis=dict(title=t("plot_ts_yaxis", lang), gridcolor=_GRID_COLOR, zerolinecolor=_ZERO_COLOR),
        height=460,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.24,
            xanchor="center",
            x=0.5,
            font=dict(size=11),
        ),
        margin=dict(l=48, r=16, t=52, b=110),
    )

    return fig


def create_cop_contour_plot(
    sensitivity_data: Dict[str, Any],
    current_t_evap: float,
    current_t_cond: float,
    lang: str = "pl",
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

    op_label = t("plot_current_op", lang)
    fig.add_trace(
        go.Scatter(
            x=[current_t_evap],
            y=[current_t_cond],
            mode="markers+text",
            name=op_label,
            text=[op_label],
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
        title=dict(text=t("plot_contour_title", lang), font=dict(size=14, family=_FONT_FAMILY, color="#f1f5f9")),
        font=dict(family=_FONT_FAMILY, color="#cbd5e1", size=12),
        hoverlabel=_HOVER_STYLE,
        xaxis=dict(title=t("plot_contour_xaxis", lang), gridcolor=_GRID_COLOR),
        yaxis=dict(title=t("plot_contour_yaxis", lang), gridcolor=_GRID_COLOR),
        height=480,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=48, r=20, t=52, b=52),
    )

    return fig


def create_subcooling_curve_plot(opt_res: Dict[str, Any], lang: str = "pl") -> go.Figure:
    """Tworzy wykres zależności efektywnego COP od stopnia dochłodzenia ΔT_sc."""
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=opt_res["curve_sc_k"],
            y=opt_res["curve_cop"],
            mode="lines+markers",
            name=t("plot_subcool_curve", lang),
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
            text=[t("plot_subcool_opt", lang, sc=opt_res["optimal_subcooling_k"], cop=opt_res["max_cop"])],
            textposition="bottom center",
            marker=dict(size=13, symbol="star", color="#EF4444"),
        )
    )
    fig.update_layout(
        title=dict(text=t("plot_subcool_title", lang), font=dict(size=14, family=_FONT_FAMILY, color="#f1f5f9")),
        font=dict(family=_FONT_FAMILY, color="#cbd5e1", size=12),
        hoverlabel=_HOVER_STYLE,
        xaxis=dict(title=t("plot_subcool_xaxis", lang), gridcolor=_GRID_COLOR, zerolinecolor=_ZERO_COLOR),
        yaxis=dict(title=t("plot_subcool_yaxis", lang), gridcolor=_GRID_COLOR, zerolinecolor=_ZERO_COLOR),
        height=340,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=45, r=20, t=48, b=85),
        legend=dict(orientation="h", yanchor="top", y=-0.28, xanchor="center", x=0.5),
    )
    return fig
