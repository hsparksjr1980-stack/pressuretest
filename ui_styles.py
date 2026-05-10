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
            }}

            .rc-gap-sm {{ height: 0.5rem; }}
            .rc-gap-md {{ height: 1rem; }}
            .rc-gap-lg {{ height: 1.5rem; }}

            .rc-eyebrow {{
                font-size: 0.75rem;
                font-weight: 700;
                letter-spacing: 0.08em;
                text-transform: uppercase;
                color: {PRIMARY};
                margin-bottom: 0.6rem;
            }}

            .rc-title {{
                font-size: 2.25rem;
                font-weight: 800;
                line-height: 1.05;
                color: {NAVY};
                margin-bottom: 0.45rem;
            }}

            .rc-title-wide {{
                font-size: 2.25rem;
            }}

            .rc-subtitle {{
                font-size: 1rem;
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
                border-radius: 16px;
                padding: 1rem;
                margin-bottom: 0.75rem;
            }}

            .rc-card-soft {{
                background: #FFF7ED;
            }}

            .rc-card-navy {{
                background: #0B1730;
                color: #F8FAFC;
                border-color: #0B1730;
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
                font-size: 1.1rem;
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
                background: #FFF7ED;
                border: 1px solid #FED7AA;
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
                background: #0B1730;
                color: #F8FAFC;
                border: 1px solid #0B1730;
                border-radius: 16px;
                padding: 1rem;
                margin-bottom: 1rem;
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
<<<<<<< HEAD

# Phase 1.1: anchored slider helper styles
ANCHORED_SLIDER_CSS = """
<style>
.pt-slider-guide {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.5rem;
    margin: -0.35rem 0 0.35rem 0;
}
.pt-slider-guide div {
    border: 1px solid rgba(15, 23, 42, 0.10);
    border-radius: 0.75rem;
    padding: 0.45rem 0.55rem;
    background: rgba(248, 250, 252, 0.88);
    min-height: 58px;
}
.pt-slider-guide strong {
    display: block;
    font-size: 0.72rem;
    color: #0f172a;
    margin-bottom: 0.15rem;
}
.pt-slider-guide span {
    display: block;
    font-size: 0.72rem;
    line-height: 1.15rem;
    color: #475569;
}
.pt-slider-selected {
    font-size: 0.78rem;
    line-height: 1.2rem;
    color: #334155;
    background: rgba(241, 245, 249, 0.72);
    border-left: 3px solid #334155;
    border-radius: 0.35rem;
    padding: 0.4rem 0.55rem;
    margin: 0.15rem 0 0.95rem 0;
}
</style>
"""
=======
>>>>>>> fec65288cb896b4679e84e61241f185fa625e150
