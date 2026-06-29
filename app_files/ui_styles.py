from __future__ import annotations

import html
from collections.abc import Sequence

import streamlit as st

from theme import BG, BORDER, CARD, NAVY, PRIMARY, TEXT, TEXT_MUTED


def inject_global_styles() -> None:
    st.markdown(
        f"""
        <style>
            .stApp {{
                background: {BG};
                color: {TEXT};
            }}

            .block-container {{
                max-width: 1120px;
                padding-top: 1rem;
                padding-bottom: 2rem;
            }}

            .rc-shell {{
                width: 100%;
                margin: 0 auto;
                background: rgba(255, 255, 255, 0.66);
                border: 1px solid rgba(216, 222, 232, 0.78);
                border-radius: 18px;
                padding: 1.35rem;
                box-shadow: 0 22px 55px rgba(15, 23, 42, 0.07);
                backdrop-filter: blur(8px);
            }}

            .rc-gap-sm {{ height: 0.5rem; }}
            .rc-gap-md {{ height: 1rem; }}
            .rc-gap-lg {{ height: 1.5rem; }}

            .rc-eyebrow {{
                font-size: 0.75rem;
                font-weight: 800;
                letter-spacing: 0.08em;
                text-transform: uppercase;
                color: {PRIMARY};
                margin-bottom: 0.6rem;
            }}

            .rc-title {{
                font-size: 2.45rem;
                font-weight: 800;
                line-height: 1.02;
                color: {NAVY};
                margin-bottom: 0.45rem;
            }}

            .rc-title-wide {{
                font-size: 2.25rem;
            }}

            .rc-subtitle {{
                font-size: 1.03rem;
                line-height: 1.5;
                color: {TEXT_MUTED};
                margin-bottom: 0.9rem;
            }}

            .rc-card,
            .rc-card-soft,
            .rc-card-navy,
            .rc-bullet-panel {{
                background: {CARD};
                border: 1px solid {BORDER};
                border-radius: 12px;
                padding: 1rem 1.05rem;
                margin-bottom: 0.8rem;
                box-shadow: 0 12px 30px rgba(15, 23, 42, 0.055);
            }}

            .rc-card-soft {{
                background: #F8FAFC;
            }}

            .rc-card-navy {{
                background: linear-gradient(135deg, #111827 0%, #1F2937 100%);
                color: #F8FAFC;
                border-color: #111827;
            }}

            .rc-card-navy .rc-card-label,
            .rc-card-navy .rc-card-title,
            .rc-card-navy .rc-card-body,
            .rc-card-navy .rc-kicker,
            .rc-card-navy .rc-section-title,
            .rc-card-navy .rc-section-body {{
                color: #F8FAFC !important;
            }}

            .rc-card-label,
            .rc-kicker {{
                font-size: 0.72rem;
                font-weight: 700;
                letter-spacing: 0.08em;
                text-transform: uppercase;
                color: {PRIMARY};
                margin-bottom: 0.35rem;
            }}

            .rc-card-title,
            .rc-section-title {{
                font-size: 1.08rem;
                font-weight: 800;
                line-height: 1.25;
                color: {NAVY};
                margin-bottom: 0.25rem;
            }}

            .rc-card-body,
            .rc-section-body,
            .rc-body,
            .rc-muted,
            .rc-note {{
                font-size: 0.95rem;
                line-height: 1.5;
                color: {TEXT_MUTED};
            }}

            .rc-badge {{
                display: inline-block;
                padding: 0.3rem 0.6rem;
                border-radius: 999px;
                background: #F8FAFC;
                border: 1px solid #D8DEE8;
                color: {NAVY};
                font-size: 0.78rem;
                font-weight: 700;
                margin-right: 0.35rem;
                margin-bottom: 0.35rem;
            }}

            .rc-list {{
                margin: 0.5rem 0 0 1rem;
                padding-left: 0.4rem;
                color: {TEXT};
            }}

            .rc-list li {{
                margin-bottom: 0.3rem;
            }}

            .rc-action-banner {{
                background: linear-gradient(135deg, #111827 0%, #233044 100%);
                color: #F8FAFC;
                border: 1px solid #111827;
                border-radius: 14px;
                padding: 1.1rem 1.15rem;
                margin-bottom: 1rem;
                box-shadow: 0 18px 40px rgba(17, 24, 39, 0.18);
            }}

            .rc-action-banner .rc-kicker,
            .rc-action-banner .rc-section-title,
            .rc-action-banner .rc-body {{
                color: #F8FAFC !important;
            }}

            .rc-chip-row {{
                margin-top: 0.7rem;
            }}

            .rc-chip {{
                display: inline-block;
                padding: 0.3rem 0.6rem;
                border-radius: 999px;
                background: rgba(255,255,255,0.1);
                border: 1px solid rgba(255,255,255,0.16);
                color: #F8FAFC;
                font-size: 0.78rem;
                font-weight: 700;
                margin-right: 0.35rem;
                margin-bottom: 0.35rem;
            }}

            .pt-panel {{
                background: #FFFFFF;
                border: 1px solid #D8DEE8;
                border-radius: 14px;
                padding: 1.1rem;
                box-shadow: 0 14px 34px rgba(15, 23, 42, 0.055);
                margin-bottom: 1rem;
            }}

            .pt-hero {{
                background: linear-gradient(135deg, #111827 0%, #233044 58%, #314256 100%);
                border: 1px solid rgba(255,255,255,.12);
                border-radius: 18px;
                padding: 1.7rem;
                color: #F8FAFC;
                box-shadow: 0 24px 60px rgba(17, 24, 39, .24);
                margin-bottom: 1rem;
            }}

            .pt-hero h1 {{
                color: #F8FAFC;
                font-size: 2.65rem;
                line-height: 1.02;
                margin: .25rem 0 .65rem 0;
                letter-spacing: 0;
            }}

            .pt-hero p {{
                color: #E5E7EB;
                font-size: 1.03rem;
                line-height: 1.58;
                margin: 0;
                max-width: 760px;
            }}

            .pt-mini-grid {{
                display: grid;
                grid-template-columns: repeat(3, minmax(0, 1fr));
                gap: .8rem;
            }}

            .pt-mini-card {{
                background: #FFFFFF;
                border: 1px solid #D8DEE8;
                border-radius: 12px;
                padding: .9rem;
                box-shadow: 0 10px 24px rgba(15, 23, 42, .045);
            }}

            .pt-mini-card strong {{
                display: block;
                color: #111827;
                margin-bottom: .25rem;
            }}

            .pt-mini-card span {{
                color: #526071;
                font-size: .92rem;
                line-height: 1.45;
            }}

            .pt-sidebar-panel {{
                background: #FFFFFF;
                border: 1px solid #D8DEE8;
                border-radius: 12px;
                padding: .85rem .9rem;
                margin: .65rem 0;
                box-shadow: 0 10px 24px rgba(15, 23, 42, .045);
            }}

            .pt-sidebar-kicker {{
                color: #92400E;
                font-size: .68rem;
                font-weight: 850;
                letter-spacing: .08em;
                text-transform: uppercase;
                margin-bottom: .25rem;
            }}

            .pt-sidebar-title {{
                color: #111827;
                font-size: .98rem;
                line-height: 1.22;
                font-weight: 850;
                margin-bottom: .2rem;
            }}

            .pt-sidebar-muted {{
                color: #526071;
                font-size: .82rem;
                line-height: 1.35;
            }}

            .pt-sidebar-track {{
                height: .4rem;
                background: #E5E7EB;
                border-radius: 999px;
                overflow: hidden;
                margin-top: .55rem;
            }}

            .pt-sidebar-track > div {{
                height: 100%;
                background: linear-gradient(90deg, #B45309, #D97706);
                border-radius: 999px;
            }}

            @media (max-width: 760px) {{
                .rc-shell {{
                    padding: .9rem;
                    border-radius: 14px;
                    box-shadow: none;
                }}
                .pt-hero {{
                    padding: 1.1rem;
                    border-radius: 14px;
                }}
                .pt-hero h1 {{
                    font-size: 1.85rem;
                }}
                .pt-mini-grid {{
                    grid-template-columns: 1fr;
                }}
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def open_shell() -> None:
    st.markdown('<div class="rc-shell">', unsafe_allow_html=True)


def close_shell() -> None:
    st.markdown("</div>", unsafe_allow_html=True)


def render_page_header(*, eyebrow: str, title: str, subtitle: str, wide: bool = False) -> None:
    title_class = "rc-title rc-title-wide" if wide else "rc-title"
    st.markdown(
        f"""
        <div class="rc-eyebrow">{html.escape(eyebrow)}</div>
        <div class="{title_class}">{html.escape(title)}</div>
        <div class="rc-subtitle">{html.escape(subtitle)}</div>
        """,
        unsafe_allow_html=True,
    )


def render_card(
    *,
    label: str,
    title: str,
    body: str,
    soft: bool = False,
    navy: bool = False,
) -> None:
    card_class = "rc-card"
    if navy:
        card_class = "rc-card-navy"
    elif soft:
        card_class = "rc-card-soft"

    st.markdown(
        f"""
        <div class="{card_class}">
            <div class="rc-card-label">{html.escape(label)}</div>
            <div class="rc-card-title">{html.escape(title)}</div>
            <div class="rc-card-body">{html.escape(body)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_section_intro(*, title: str, body: str) -> None:
    st.markdown(
        f"""
        <div class="rc-section-title">{html.escape(title)}</div>
        <div class="rc-section-body">{html.escape(body)}</div>
        """,
        unsafe_allow_html=True,
    )


def _safe_items(items: Sequence[str]) -> str:
    return "".join(f"<li>{html.escape(item)}</li>" for item in items)


def _safe_chips(chips: Sequence[str]) -> str:
    return "".join(f'<span class="rc-chip">{html.escape(chip)}</span>' for chip in chips)


def render_action_banner(
    *,
    title: str,
    body: str,
    eyebrow: str = "Focus",
    chips: Sequence[str] | None = None,
) -> None:
    chip_html = f'<div class="rc-chip-row">{_safe_chips(chips)}</div>' if chips else ""
    st.markdown(
        f"""
        <div class="rc-action-banner">
            <div class="rc-kicker">{html.escape(eyebrow)}</div>
            <div class="rc-section-title">{html.escape(title)}</div>
            <div class="rc-body">{html.escape(body)}</div>
            {chip_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_bullet_panel(
    label: str,
    title: str,
    items: Sequence[str] | None = None,
    empty_text: str = "No items available.",
) -> None:
    resolved_items = list(items or [])
    body_html = (
        f'<ul class="rc-list">{_safe_items(resolved_items)}</ul>'
        if resolved_items
        else f'<div class="rc-muted">{html.escape(empty_text)}</div>'
    )
    st.markdown(
        f"""
        <div class="rc-bullet-panel">
            <div class="rc-kicker">{html.escape(label)}</div>
            <div class="rc-section-title">{html.escape(title)}</div>
            {body_html}
        </div>
        """,
        unsafe_allow_html=True,
    )
