from __future__ import annotations

import streamlit as st

NAVY = "#111827"
NAVY_2 = "#1F2937"
PRIMARY = "#B45309"
PRIMARY_HOVER = "#92400E"
ACCENT = "#D97706"
BG = "#F5F7FA"
CARD = "#FFFFFF"
BORDER = "#D8DEE8"
TEXT = "#0F172A"
TEXT_MUTED = "#526071"


def apply_theme() -> None:
    st.markdown(
        f"""
        <style>
            .stApp {{
                background:
                    radial-gradient(circle at 18% -10%, rgba(180, 83, 9, 0.08), transparent 28%),
                    linear-gradient(180deg, #F8FAFC 0%, {BG} 44%, #EEF2F7 100%);
                color: {TEXT};
            }}

            .block-container {{
                max-width: 1180px;
                padding-top: 1.35rem;
                padding-bottom: 3rem;
            }}

            [data-testid="stSidebar"] {{
                background: #F8FAFC;
                border-right: 1px solid rgba(15, 23, 42, 0.08);
                box-shadow: 12px 0 36px rgba(15, 23, 42, 0.04);
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
                background: rgba(255, 255, 255, 0.86);
                color: {TEXT};
                border: 1px solid rgba(15, 23, 42, 0.10);
                border-radius: 12px;
                min-height: 2.45rem;
                font-weight: 650;
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
                min-height: 2.65rem;
                font-weight: 700;
                box-shadow: 0 8px 18px rgba(15, 23, 42, 0.045);
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
                background: #FFFFFF;
                min-height: 2.65rem;
                box-shadow: 0 6px 16px rgba(15, 23, 42, 0.035);
            }}

            label, .stRadio label, .stSelectbox label, .stTextInput label, .stTextArea label {{
                color: #1F2937 !important;
                font-weight: 650 !important;
            }}

            div[role="radiogroup"] label {{
                background: #FFFFFF;
                border: 1px solid #D8DEE8;
                border-radius: 999px;
                padding: .35rem .65rem;
                margin-right: .25rem;
            }}

            .stProgress > div > div > div > div {{
                background: linear-gradient(90deg, {ACCENT}, {PRIMARY});
            }}

            [data-testid="stMetric"] {{
                background: {CARD};
                border: 1px solid {BORDER};
                border-radius: 12px;
                padding: 0.75rem 0.9rem;
                box-shadow: 0 10px 24px rgba(15, 23, 42, 0.045);
            }}

            div[data-testid="stExpander"] {{
                border: 1px solid {BORDER};
                border-radius: 12px;
                background: rgba(255,255,255,.82);
                box-shadow: 0 12px 28px rgba(15, 23, 42, 0.04);
                overflow: hidden;
            }}

            div[data-testid="stExpander"] details summary p {{
                font-weight: 800;
                color: {TEXT};
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )
