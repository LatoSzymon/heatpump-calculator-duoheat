"""Spójne style CSS w kolorystyce projektu DUOHEAT oraz pełna responsywność mobilna."""

import streamlit as st


def inject_custom_css() -> None:
    """Wstrzykuje arkusz stylów aplikacji do strony Streamlit."""
    st.markdown(
        """
        <style>
        .block-container {
            padding-top: 2rem !important;
            padding-bottom: 0.75rem !important;
        }
        [data-testid="stAppViewContainer"] > .main {
            display: flex;
            flex-direction: column;
            min-height: 100vh;
        }
        .kpi-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
            gap: 0.75rem;
            margin: 0.5rem 0 1rem 0;
        }
        .kpi-card {
            background-color: rgba(18, 52, 74, 0.75);
            border: 1px solid rgba(6, 147, 227, 0.28);
            border-top: 3px solid #ff5a1f;
            border-radius: 10px;
            padding: 0.85rem 1rem;
        }
        .kpi-label {
            font-size: 0.8rem;
            opacity: 0.8;
            margin-bottom: 0.25rem;
        }
        .kpi-value {
            font-size: 1.55rem;
            font-weight: 700;
            line-height: 1.2;
        }
        .kpi-sub {
            font-size: 0.78rem;
            color: #0693e3;
            margin-top: 0.25rem;
        }
        .step-card {
            background-color: rgba(18, 52, 74, 0.65);
            border: 1px solid rgba(171, 184, 195, 0.20);
            border-left: 4px solid #64748B;
            border-radius: 8px;
            padding: 0.85rem 1rem;
            margin-bottom: 0.7rem;
            color: inherit;
            line-height: 1.5;
        }
        .step-evap { border-left-color: #0693e3; }
        .step-comp { border-left-color: #ff5a1f; }
        .step-cond { border-left-color: #ff6900; }
        .step-valve { border-left-color: #00d084; }
        .app-footer {
            margin-top: 0.5rem;
            margin-bottom: 0;
            text-align: center;
            opacity: 0.85;
            font-size: 0.88rem;
            padding: 0.5rem 0 0.25rem 0;
        }
        .app-footer a {
            color: #ff5a1f;
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
                padding-top: 1.25rem !important;
                padding-bottom: 0.5rem !important;
            }
            h1 {
                font-size: 1.4rem !important;
                line-height: 1.25 !important;
            }
            h2, h3 {
                font-size: 1.12rem !important;
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
            .app-footer {
                font-size: 0.8rem;
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
