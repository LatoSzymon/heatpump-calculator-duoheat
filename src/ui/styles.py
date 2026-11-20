"""Spójny system stylów CSS w kolorystyce projektu DUOHEAT oraz pełna responsywność mobilna."""

import streamlit as st


def inject_custom_css() -> None:
    """Wstrzykuje arkusz stylów aplikacji do strony Streamlit."""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

        :root {
            --dh-bg: #0d2b3e;
            --dh-bg-deep: #09202f;
            --dh-surface: rgba(18, 52, 74, 0.72);
            --dh-surface-strong: rgba(21, 61, 86, 0.90);
            --dh-border: rgba(142, 209, 252, 0.16);
            --dh-border-hover: rgba(142, 209, 252, 0.34);
            --dh-orange: #ff5a1f;
            --dh-orange-soft: rgba(255, 90, 31, 0.14);
            --dh-amber: #ff8a3d;
            --dh-blue: #0693e3;
            --dh-blue-light: #67c8ff;
            --dh-green: #00d084;
            --dh-danger: #fb7185;
            --dh-text: #f1f5f9;
            --dh-text-muted: #a8c2d4;
            --dh-radius: 12px;
            --dh-radius-sm: 8px;
            --dh-shadow: 0 6px 20px rgba(4, 17, 26, 0.24);
        }

        /* Global typography & subtle ambient backdrop */
        html, body, [class*="css"] {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }

        [data-testid="stAppViewContainer"] {
            background:
                radial-gradient(900px 420px at 88% -6%, rgba(6, 147, 227, 0.14), transparent 60%),
                radial-gradient(640px 360px at 10% -4%, rgba(255, 90, 31, 0.10), transparent 58%),
                var(--dh-bg);
        }

        [data-testid="stHeader"] {
            background: rgba(13, 43, 62, 0.82) !important;
            backdrop-filter: blur(10px);
            border-bottom: 1px solid rgba(142, 209, 252, 0.10);
        }

        .block-container,
        [data-testid="stMainBlockContainer"] {
            padding-top: 2.25rem !important;
            padding-bottom: 1rem !important;
            max-width: 1380px;
        }

        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0b2435 0%, #0f2f44 100%);
            border-right: 1px solid var(--dh-border);
        }

        [data-testid="stSidebar"] .block-container {
            padding-top: 1.25rem !important;
        }

        .sidebar-brand {
            padding: 0.75rem 0.85rem;
            border-radius: var(--dh-radius-sm);
            background: linear-gradient(135deg, rgba(255, 90, 31, 0.14), rgba(6, 147, 227, 0.10));
            border: 1px solid rgba(255, 90, 31, 0.28);
            margin-bottom: 1rem;
        }

        .sidebar-brand-title {
            font-size: 0.92rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            color: var(--dh-text);
            display: flex;
            align-items: center;
            gap: 0.45rem;
        }

        .sidebar-brand-dot {
            width: 8px;
            height: 8px;
            border-radius: 999px;
            background: var(--dh-orange);
            box-shadow: 0 0 10px rgba(255, 90, 31, 0.75);
            display: inline-block;
            flex-shrink: 0;
        }

        .sidebar-brand-sub {
            font-size: 0.76rem;
            color: var(--dh-text-muted);
            margin-top: 0.2rem;
        }

        .sidebar-section-label {
            font-size: 0.72rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.09em;
            color: var(--dh-text-muted);
            margin: 0.25rem 0 0.5rem 0;
        }

        [data-testid="stSidebar"] .stButton > button {
            justify-content: flex-start !important;
            text-align: left !important;
            border-radius: var(--dh-radius-sm) !important;
            padding: 0.52rem 0.75rem !important;
            font-size: 0.86rem !important;
            font-weight: 500 !important;
            line-height: 1.35 !important;
            border: 1px solid rgba(142, 209, 252, 0.14) !important;
            transition: background-color 0.18s ease, border-color 0.18s ease, transform 0.15s ease !important;
        }

        [data-testid="stSidebar"] .stButton > button:hover {
            border-color: var(--dh-border-hover) !important;
            transform: translateX(2px);
        }

        [data-testid="stSidebar"] .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #ff5a1f 0%, #e64d14 100%) !important;
            border-color: rgba(255, 138, 61, 0.55) !important;
            color: #ffffff !important;
            font-weight: 600 !important;
            box-shadow: 0 4px 12px rgba(255, 90, 31, 0.28);
        }

        /* App Hero Header */
        .app-hero {
            padding: 0.25rem 0 1.1rem 0;
            margin-bottom: 0.5rem;
            border-bottom: 1px solid rgba(142, 209, 252, 0.12);
        }

        .app-brand-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.45rem;
            font-size: 0.7rem;
            font-weight: 700;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            color: var(--dh-blue-light);
            background: rgba(6, 147, 227, 0.12);
            border: 1px solid rgba(6, 147, 227, 0.30);
            border-radius: 999px;
            padding: 0.22rem 0.68rem;
            margin-bottom: 0.55rem;
        }

        .app-brand-badge::before {
            content: "";
            width: 6px;
            height: 6px;
            border-radius: 999px;
            background: var(--dh-orange);
        }

        .app-hero-title {
            font-size: 1.95rem;
            font-weight: 700;
            line-height: 1.2;
            letter-spacing: -0.02em;
            color: var(--dh-text);
            margin: 0;
        }

        .app-hero-subtitle {
            font-size: 0.96rem;
            color: var(--dh-text-muted);
            margin: 0.38rem 0 0 0;
            line-height: 1.45;
        }

        /* Elevated Streamlit bordered containers */
        [data-testid="stVerticalBlockBorderWrapper"] {
            background: linear-gradient(180deg, rgba(18, 52, 74, 0.62) 0%, rgba(14, 42, 61, 0.72) 100%);
            border: 1px solid var(--dh-border) !important;
            border-radius: var(--dh-radius) !important;
            box-shadow: var(--dh-shadow);
        }

        /* Configuration panel headings, fluid chips & preset callout */
        .ctrl-card-header {
            display: flex;
            align-items: baseline;
            justify-content: space-between;
            gap: 0.75rem;
            margin-bottom: 0.65rem;
            padding-bottom: 0.55rem;
            border-bottom: 1px solid rgba(142, 209, 252, 0.12);
        }

        .ctrl-card-title {
            font-size: 1.08rem;
            font-weight: 700;
            color: var(--dh-text);
            margin: 0;
        }

        .ctrl-section-title {
            font-size: 0.74rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: var(--dh-blue-light);
            margin: 0.1rem 0 0.6rem 0;
        }

        .fluid-chips {
            display: flex;
            flex-wrap: wrap;
            gap: 0.35rem;
            margin: 0.35rem 0 0.45rem 0;
        }

        .fluid-chip {
            display: inline-flex;
            align-items: center;
            gap: 0.25rem;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.72rem;
            font-weight: 500;
            color: #dbeafe;
            background: rgba(13, 43, 62, 0.78);
            border: 1px solid rgba(142, 209, 252, 0.22);
            border-radius: 6px;
            padding: 0.18rem 0.48rem;
        }

        .fluid-chip-safe-a1 {
            border-color: rgba(0, 208, 132, 0.45);
            color: #6ee7b7;
        }

        .fluid-chip-safe-a2l {
            border-color: rgba(255, 138, 61, 0.45);
            color: #fdba74;
        }

        .fluid-chip-safe-a3 {
            border-color: rgba(255, 90, 31, 0.50);
            color: #fca5a5;
        }

        .fluid-chip-safe-b2l {
            border-color: rgba(251, 113, 133, 0.55);
            color: #fda4af;
        }

        .fluid-desc {
            font-size: 0.8rem;
            line-height: 1.45;
            color: var(--dh-text-muted);
            margin-bottom: 15px;
        }

        .preset-banner {
            margin-top: 0.75rem;
            padding: 0.65rem 0.9rem;
            border-radius: var(--dh-radius-sm);
            background: rgba(6, 147, 227, 0.10);
            border: 1px solid rgba(6, 147, 227, 0.26);
            border-left: 3px solid var(--dh-blue);
            font-size: 0.85rem;
            line-height: 1.48;
            color: #dcebf7;
        }

        /* KPI Cards Grid */
        .kpi-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(175px, 1fr));
            gap: 0.8rem;
            margin: 0.85rem 0 1.1rem 0;
        }

        .kpi-card {
            background: linear-gradient(180deg, rgba(22, 62, 88, 0.84) 0%, rgba(15, 45, 65, 0.92) 100%);
            border: 1px solid var(--dh-border);
            border-top: 3px solid var(--dh-orange);
            border-radius: var(--dh-radius);
            padding: 0.9rem 1rem;
            box-shadow: 0 4px 14px rgba(4, 17, 26, 0.22);
            transition: transform 0.18s ease, border-color 0.18s ease, box-shadow 0.18s ease;
        }

        .kpi-card:hover {
            transform: translateY(-2px);
            border-color: var(--dh-border-hover);
            box-shadow: 0 8px 22px rgba(4, 17, 26, 0.34);
        }

        .kpi-accent-primary { border-top-color: #ff5a1f; }
        .kpi-accent-heat { border-top-color: #ff8a3d; }
        .kpi-accent-power { border-top-color: #f59e0b; }
        .kpi-accent-ambient { border-top-color: #0693e3; }
        .kpi-accent-temp { border-top-color: #38bdf8; }
        .kpi-accent-ratio { border-top-color: #00d084; }

        .kpi-card--warn {
            border-top-color: var(--dh-danger) !important;
            border-color: rgba(251, 113, 133, 0.45);
            background: linear-gradient(180deg, rgba(95, 31, 48, 0.48) 0%, rgba(15, 45, 65, 0.92) 100%);
        }

        .kpi-label {
            font-size: 0.72rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--dh-text-muted);
            margin-bottom: 0.35rem;
        }

        .kpi-value {
            font-size: 1.58rem;
            font-weight: 700;
            line-height: 1.18;
            color: var(--dh-text);
            font-variant-numeric: tabular-nums;
            letter-spacing: -0.02em;
        }

        .kpi-sub {
            font-size: 0.78rem;
            font-weight: 500;
            color: var(--dh-blue-light);
            margin-top: 0.35rem;
            font-variant-numeric: tabular-nums;
        }

        .kpi-card--warn .kpi-sub {
            color: #fda4af;
        }

        /* Summary Metric Strip (Tab 3) */
        .summary-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 0.8rem;
            margin-top: 0.75rem;
        }

        .summary-card {
            background: rgba(13, 43, 62, 0.65);
            border: 1px solid var(--dh-border);
            border-left: 3px solid var(--dh-blue);
            border-radius: var(--dh-radius-sm);
            padding: 0.8rem 0.95rem;
        }

        .summary-card--ok {
            border-left-color: var(--dh-green);
        }

        .summary-label {
            font-size: 0.73rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--dh-text-muted);
        }

        .summary-value {
            font-family: 'JetBrains Mono', monospace;
            font-size: 1.22rem;
            font-weight: 600;
            color: var(--dh-text);
            margin-top: 0.25rem;
            font-variant-numeric: tabular-nums;
        }

        .summary-sub {
            font-size: 0.76rem;
            color: var(--dh-blue-light);
            margin-top: 0.18rem;
        }

        .summary-card--ok .summary-sub {
            color: #6ee7b7;
        }

        /* Tabs bar polish */
        [data-baseweb="tab-list"] {
            gap: 0.35rem;
            border-bottom: 1px solid var(--dh-border) !important;
            padding-bottom: 0.15rem;
            margin-bottom: 0.85rem;
        }

        [data-baseweb="tab"] {
            border-radius: var(--dh-radius-sm) var(--dh-radius-sm) 0 0 !important;
            padding: 0.55rem 0.95rem !important;
            font-size: 0.9rem !important;
            font-weight: 500 !important;
            color: var(--dh-text-muted) !important;
            transition: background-color 0.15s ease, color 0.15s ease;
        }

        [data-baseweb="tab"]:hover {
            background-color: rgba(142, 209, 252, 0.08) !important;
            color: var(--dh-text) !important;
        }

        [data-baseweb="tab"][aria-selected="true"] {
            color: var(--dh-text) !important;
            font-weight: 600 !important;
            background-color: rgba(255, 90, 31, 0.10) !important;
        }

        [data-baseweb="tab-highlight"] {
            background-color: var(--dh-orange) !important;
            height: 3px !important;
        }

        /* 4-stage process cards */
        .step-card {
            background: linear-gradient(180deg, rgba(20, 56, 80, 0.72) 0%, rgba(14, 42, 61, 0.82) 100%);
            border: 1px solid var(--dh-border);
            border-left: 4px solid #64748b;
            border-radius: 10px;
            padding: 0.9rem 1.05rem;
            margin-bottom: 0.75rem;
            color: #e2edf5;
            font-size: 0.9rem;
            line-height: 1.56;
            box-shadow: 0 3px 12px rgba(4, 17, 26, 0.18);
            transition: border-color 0.18s ease, transform 0.15s ease;
        }

        .step-card:hover {
            border-color: var(--dh-border-hover);
            transform: translateX(2px);
        }

        .step-card strong:first-child {
            display: inline-block;
            font-size: 0.94rem;
            color: var(--dh-text);
            margin-bottom: 0.25rem;
        }

        .step-card code {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.82rem;
            color: #dbeafe;
            background: rgba(6, 147, 227, 0.16);
            border: 1px solid rgba(6, 147, 227, 0.26);
            border-radius: 4px;
            padding: 0.08rem 0.34rem;
        }

        .step-evap { border-left-color: #0693e3; }
        .step-comp { border-left-color: #ff5a1f; }
        .step-cond { border-left-color: #ff8a3d; }
        .step-valve { border-left-color: #00d084; }

        /* Native Streamlit st.metric upgrade (used in Education mini-labs) */
        [data-testid="stMetric"] {
            background: linear-gradient(180deg, rgba(20, 56, 80, 0.70) 0%, rgba(13, 43, 62, 0.82) 100%);
            border: 1px solid var(--dh-border);
            border-radius: 10px;
            padding: 0.7rem 0.9rem;
        }

        [data-testid="stMetricLabel"] {
            font-size: 0.76rem !important;
            color: var(--dh-text-muted) !important;
            font-weight: 600 !important;
        }

        [data-testid="stMetricValue"] {
            font-size: 1.42rem !important;
            font-weight: 700 !important;
            font-variant-numeric: tabular-nums;
            color: var(--dh-text) !important;
        }

        /* Education lesson header */
        .edu-lesson-header {
            margin: 0.2rem 0 0.9rem 0;
        }

        .edu-lesson-eyebrow {
            display: inline-block;
            font-size: 0.74rem;
            font-weight: 600;
            color: var(--dh-blue-light);
            background: rgba(6, 147, 227, 0.12);
            border: 1px solid rgba(6, 147, 227, 0.26);
            border-radius: 6px;
            padding: 0.2rem 0.6rem;
            margin-bottom: 0.45rem;
        }

        .edu-lesson-title {
            font-size: 1.42rem;
            font-weight: 700;
            color: var(--dh-text);
            margin: 0;
            line-height: 1.28;
        }

        /* Buttons & Download buttons */
        .stDownloadButton > button {
            border-radius: var(--dh-radius-sm) !important;
            border: 1px solid rgba(6, 147, 227, 0.38) !important;
            background: rgba(6, 147, 227, 0.12) !important;
            color: var(--dh-text) !important;
            font-weight: 600 !important;
            transition: background-color 0.18s ease, border-color 0.18s ease !important;
        }

        .stDownloadButton > button:hover {
            background: rgba(6, 147, 227, 0.24) !important;
            border-color: var(--dh-blue-light) !important;
        }

        /* Dataframe container polish */
        [data-testid="stDataFrame"] {
            border: 1px solid var(--dh-border);
            border-radius: 10px;
            overflow: hidden;
        }

        /* Footer */
        .app-footer {
            margin-top: 1.5rem;
            padding: 0.95rem 0 0.35rem 0;
            border-top: 1px solid rgba(142, 209, 252, 0.14);
            text-align: center;
            color: var(--dh-text-muted);
            font-size: 0.84rem;
            line-height: 1.5;
        }

        .app-footer a {
            color: var(--dh-orange);
            text-decoration: none;
            font-weight: 600;
            transition: color 0.15s ease;
        }

        .app-footer a:hover {
            color: var(--dh-amber);
            text-decoration: underline;
        }

        /* Responsive adjustments */
        @media (max-width: 768px) {
            .block-container,
            [data-testid="stMainBlockContainer"] {
                padding-left: 0.75rem !important;
                padding-right: 0.75rem !important;
                padding-top: 1.4rem !important;
                padding-bottom: 0.6rem !important;
            }

            .app-hero-title {
                font-size: 1.42rem;
            }

            .app-hero-subtitle {
                font-size: 0.88rem;
            }

            h2, h3 {
                font-size: 1.12rem !important;
            }

            [data-baseweb="tab-list"] {
                overflow-x: auto !important;
                flex-wrap: nowrap !important;
                scrollbar-width: none;
                -webkit-overflow-scrolling: touch;
                gap: 0.2rem;
            }

            [data-baseweb="tab-list"]::-webkit-scrollbar {
                display: none;
            }

            [data-baseweb="tab"] {
                white-space: nowrap !important;
                flex-shrink: 0 !important;
                padding: 0.5rem 0.75rem !important;
                font-size: 0.86rem !important;
            }

            .stButton > button,
            .stDownloadButton > button {
                min-height: 44px;
                width: 100%;
            }

            .kpi-grid {
                grid-template-columns: repeat(2, 1fr);
                gap: 0.55rem;
            }

            .kpi-card {
                padding: 0.7rem 0.8rem;
            }

            .kpi-value {
                font-size: 1.25rem;
            }

            .summary-grid {
                grid-template-columns: 1fr;
                gap: 0.55rem;
            }

            .step-card {
                padding: 0.78rem 0.88rem;
                font-size: 0.88rem;
            }

            .edu-lesson-title {
                font-size: 1.2rem;
            }

            .app-footer {
                font-size: 0.78rem;
                margin-top: 1rem;
            }
        }

        @media (max-width: 420px) {
            .kpi-grid {
                grid-template-columns: 1fr;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
