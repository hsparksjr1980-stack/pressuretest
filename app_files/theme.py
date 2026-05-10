from __future__ import annotations

import streamlit as st

NAVY = "#0B1730"
NAVY_2 = "#13213A"
PRIMARY = "#F97316"
PRIMARY_HOVER = "#EA580C"
ACCENT = "#FBBF24"
BG = "#F8FAFC"
CARD = "#FFFFFF"
BORDER = "#E2E8F0"
TEXT = "#0F172A"
TEXT_MUTED = "#5B6577"


def apply_theme() -> None:
    st.markdown(
        f"""
        <style>
            .stApp {{
                background-color: {BG};
                color: {TEXT};
            }}

            .block-container {{
                max-width: 1120px;
                padding-top: 1rem;
                padding-bottom: 2rem;
            }}

            [data-testid="stSidebar"] {{
                background: #DCEAF7;
                border-right: 1px solid rgba(11, 23, 48, 0.08);
            }}

            [data-testid="stSidebar"] .stMarkdown,
            [data-testid="stSidebar"] label,
            [data-testid="stSidebar"] p,
            [data-testid="stSidebar"] span,
            [data-testid="stSidebar"] div {{
                color: {TEXT};
            }}

            [data-testid="stSidebar"] hr {{
                border-color: rgba(11, 23, 48, 0.10);
            }}

            [data-testid="stSidebar"] button {{
                width: 100%;
                background: rgba(255, 255, 255, 0.72);
                color: {TEXT};
                border: 1px solid rgba(11, 23, 48, 0.10);
                border-radius: 12px;
            }}

            [data-testid="stSidebar"] button:hover {{
                background: rgba(249, 115, 22, 0.10);
                color: {TEXT};
                border-color: rgba(249, 115, 22, 0.30);
            }}

            [data-testid="stSidebar"] button:focus,
            [data-testid="stSidebar"] button:active {{
                color: {TEXT};
                border-color: rgba(249, 115, 22, 0.40);
                box-shadow: 0 0 0 0.2rem rgba(249, 115, 22, 0.15);
            }}

            [data-testid="stSidebar"] button[kind="primary"] {{
                background: {PRIMARY};
                color: #FFFFFF;
                border: 1px solid {PRIMARY};
            }}

            [data-testid="stSidebar"] button[kind="primary"]:hover {{
                background: {PRIMARY_HOVER};
                color: #FFFFFF;
                border-color: {PRIMARY_HOVER};
            }}

            div[data-testid="stButton"] > button {{
                border-radius: 12px;
                border: 1px solid rgba(15, 23, 42, 0.10);
                background: {CARD};
                color: {TEXT};
            }}

            div[data-testid="stButton"] > button:hover {{
                border-color: rgba(249, 115, 22, 0.35);
                color: {TEXT};
            }}

            div[data-testid="stButton"] > button[kind="primary"] {{
                background: {PRIMARY};
                color: #FFFFFF;
                border: 1px solid {PRIMARY};
            }}

            div[data-testid="stButton"] > button[kind="primary"]:hover {{
                background: {PRIMARY_HOVER};
                border-color: {PRIMARY_HOVER};
                color: #FFFFFF;
            }}

            .stTextInput input,
            .stTextArea textarea,
            .stSelectbox div[data-baseweb="select"] > div {{
                border-radius: 12px;
                border-color: {BORDER};
            }}

            .stProgress > div > div > div > div {{
                background: linear-gradient(90deg, {ACCENT}, {PRIMARY});
            }}

            [data-testid="stMetric"] {{
                background: {CARD};
                border: 1px solid {BORDER};
                border-radius: 16px;
                padding: 0.75rem 0.9rem;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )
