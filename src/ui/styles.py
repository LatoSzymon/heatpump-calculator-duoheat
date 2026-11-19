"""Spójne style CSS dla trybu ciemnego/jasnego oraz responsywności mobilnej."""

import streamlit as st


def inject_custom_css() -> None:
    """Wstrzykuje arkusz stylów aplikacji do strony Streamlit."""
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
            border-left: 4px solid #64748B;
            border-radius: 8px;
            padding: 0.85rem 1rem;
            margin-bottom: 0.7rem;
            color: inherit;
            line-height: 1.5;
        }
        .step-evap { border-left-color: #0EA5E9; }
        .step-comp { border-left-color: #EF4444; }
        .step-cond { border-left-color: #F97316; }
        .step-valve { border-left-color: #22C55E; }
        .edu-card {
            background-color: rgba(56, 189, 248, 0.07);
            border: 1px solid rgba(56, 189, 248, 0.25);
            border-radius: 10px;
            padding: 1rem 1.15rem;
            margin-bottom: 0.85rem;
        }
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
