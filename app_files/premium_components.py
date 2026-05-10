from __future__ import annotations

import html
from typing import Iterable

import streamlit as st


def esc(value: object) -> str:
    return html.escape(str(value or ""))


def inject_premium_css() -> None:
    st.markdown(
        """
        <style>
        :root {
          --pt-navy:#0B1220; --pt-slate:#334155; --pt-muted:#64748B;
          --pt-line:rgba(15,23,42,.10); --pt-soft:#F8FAFC; --pt-card:#FFFFFF;
          --pt-orange:#F97316; --pt-orange-dark:#C2410C; --pt-green:#16A34A;
          --pt-blue:#2563EB; --pt-ink:#111827;
        }
        html, body, [data-testid="stAppViewContainer"] {background:#F8FAFC;}
        .block-container {padding-top: 1.5rem; padding-bottom: 4rem; max-width: 1240px;}
        [data-testid="stSidebar"] {background: linear-gradient(180deg,#FFFFFF 0%,#F8FAFC 100%); border-right:1px solid var(--pt-line);}
        [data-testid="stSidebar"] button {border-radius: 14px; min-height: 2.35rem; border:1px solid rgba(15,23,42,.09); box-shadow:none;}
        [data-testid="stSidebar"] details {border:0;}
        [data-testid="stSidebar"] summary {font-weight:850; color:var(--pt-navy); letter-spacing:-.02em;}
        h1,h2,h3 {letter-spacing:-.035em; color:var(--pt-navy);} p, li, label {color:var(--pt-slate);} small {color:var(--pt-muted);}
        .pt-hero {border:1px solid var(--pt-line); border-radius:30px; padding:1.7rem 1.75rem; margin-bottom:1.1rem; background: radial-gradient(circle at top right, rgba(37,99,235,.10), transparent 30%), radial-gradient(circle at bottom left, rgba(249,115,22,.12), transparent 26%), linear-gradient(135deg,#FFFFFF 0%,#F8FAFC 100%); box-shadow:0 20px 60px rgba(15,23,42,.08);}
        .pt-eyebrow {font-size:.74rem; font-weight:800; text-transform:uppercase; letter-spacing:.11em; color:var(--pt-orange-dark); margin-bottom:.35rem;}
        .pt-title {font-size:2.05rem; line-height:1.05; font-weight:850; color:var(--pt-navy); margin:0 0 .45rem 0;}
        .pt-subtitle {font-size:1.03rem; color:#475569; max-width:760px; line-height:1.55; margin:0;}
        .pt-card {border:1px solid var(--pt-line); border-radius:24px; background:rgba(255,255,255,.94); padding:1.08rem; box-shadow:0 14px 36px rgba(15,23,42,.055); height:100%;}
        .pt-card h3 {font-size:1.02rem; margin:.12rem 0 .38rem 0;}
        .pt-card p {font-size:.92rem; margin:.15rem 0; line-height:1.48; color:#475569;}
        .pt-metric {border:1px solid var(--pt-line); border-radius:22px; background:#fff; padding:1.05rem; box-shadow:0 12px 30px rgba(15,23,42,.045);}
        .pt-metric-label {font-size:.73rem; font-weight:800; text-transform:uppercase; letter-spacing:.09em; color:var(--pt-muted);}
        .pt-metric-value {font-size:1.35rem; font-weight:850; color:var(--pt-navy); margin-top:.2rem;}
        .pt-pill {display:inline-flex; align-items:center; gap:.35rem; padding:.28rem .58rem; border-radius:999px; border:1px solid rgba(249,115,22,.18); background:rgba(249,115,22,.09); color:var(--pt-orange-dark); font-size:.72rem; font-weight:800; text-transform:uppercase; letter-spacing:.05em;}
        .pt-note {border:1px dashed rgba(15,23,42,.18); border-radius:18px; padding:.85rem .95rem; background:#fff; color:#475569; font-size:.91rem; line-height:1.45;}
        .pt-divider {height:1px; background:var(--pt-line); margin:1.1rem 0;}
        .pt-workflow-item {border:1px solid rgba(15,23,42,.08); border-radius:18px; background:#fff; padding:.88rem .95rem; margin:.55rem 0; box-shadow:0 8px 18px rgba(15,23,42,.035);}
        .pt-workflow-item h4 {margin:0 0 .2rem 0; color:var(--pt-navy); font-size:.98rem; letter-spacing:-.02em;}
        .pt-workflow-item p {margin:0; color:#64748B; font-size:.84rem; line-height:1.35;}
        .pt-lock-card {border:1px solid rgba(15,23,42,.08); border-radius:28px; background:linear-gradient(135deg,#FFFFFF,#F8FAFC); padding:1.45rem; box-shadow:0 18px 50px rgba(15,23,42,.07);}
        .pt-path {display:flex; gap:.6rem; flex-wrap:wrap; margin:.6rem 0 1rem 0;}
        .pt-path-step {border:1px solid rgba(15,23,42,.08); background:#fff; border-radius:999px; padding:.45rem .72rem; font-size:.82rem; font-weight:800; color:#334155;}
        .pt-path-step-active {background:#0B1220; color:#fff; border-color:#0B1220;}
        .pt-tier-grid {display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:1rem; margin:1rem 0;}
        .pt-tier-card {border:1px solid var(--pt-line); border-radius:26px; background:#fff; padding:1.2rem; box-shadow:0 16px 42px rgba(15,23,42,.06); height:100%;}
        .pt-tier-card-pro {border-color:rgba(249,115,22,.30); box-shadow:0 18px 52px rgba(249,115,22,.10);}
        .pt-tier-price {font-size:1.55rem; font-weight:850; color:var(--pt-navy); margin:.25rem 0 .45rem 0;}
        .pt-feature-list {margin:.8rem 0 0 0; padding-left:1.05rem;}
        .pt-feature-list li {margin:.28rem 0; font-size:.92rem; color:#334155;}
        .pt-upgrade-strip {border:1px solid rgba(249,115,22,.20); border-radius:22px; background:linear-gradient(135deg,rgba(249,115,22,.10),rgba(255,255,255,.98)); padding:1rem 1.05rem; margin:1rem 0;}
        .pt-upgrade-strip h3 {margin:0 0 .3rem 0; font-size:1.08rem;}
        .pt-upgrade-strip p {margin:0; color:#475569; line-height:1.45;}
        div.stButton > button[kind="primary"] {background: linear-gradient(135deg,#F97316,#EA580C); border:0; border-radius:14px; font-weight:800;}
        div.stButton > button {border-radius:14px; font-weight:700;}
        @media (max-width: 900px) {.pt-tier-grid {grid-template-columns:1fr;}}
        </style>
        """,
        unsafe_allow_html=True,
    )


def hero(title: str, subtitle: str, eyebrow: str = "PressureTest Franchise") -> None:
    st.markdown(
        f"""
        <div class="pt-hero">
          <div class="pt-eyebrow">{esc(eyebrow)}</div>
          <div class="pt-title">{esc(title)}</div>
          <p class="pt-subtitle">{esc(subtitle)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def metric_card(label: str, value: str, helper: str = "") -> None:
    st.markdown(
        f"""
        <div class="pt-metric">
          <div class="pt-metric-label">{esc(label)}</div>
          <div class="pt-metric-value">{esc(value)}</div>
          <p>{esc(helper)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def info_card(title: str, body: str, pill: str | None = None) -> None:
    pill_html = f'<span class="pt-pill">{esc(pill)}</span>' if pill else ""
    st.markdown(
        f"""
        <div class="pt-card">
          {pill_html}
          <h3>{esc(title)}</h3>
          <p>{esc(body)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def tier_card(title: str, price: str, body: str, features: Iterable[str], badge: str | None = None, pro: bool = False) -> None:
    badge_html = f'<span class="pt-pill">{esc(badge)}</span>' if badge else ""
    feature_html = "".join(f"<li>{esc(feature)}</li>" for feature in features)
    pro_class = " pt-tier-card-pro" if pro else ""
    st.markdown(
        f"""
        <div class="pt-tier-card{pro_class}">
          {badge_html}
          <h3>{esc(title)}</h3>
          <div class="pt-tier-price">{esc(price)}</div>
          <p>{esc(body)}</p>
          <ul class="pt-feature-list">{feature_html}</ul>
        </div>
        """,
        unsafe_allow_html=True,
    )


def upgrade_strip(title: str, body: str) -> None:
    st.markdown(
        f"""
        <div class="pt-upgrade-strip">
          <h3>{esc(title)}</h3>
          <p>{esc(body)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def checklist(items: Iterable[str]) -> None:
    st.markdown("\n".join([f"- {item}" for item in items]))
