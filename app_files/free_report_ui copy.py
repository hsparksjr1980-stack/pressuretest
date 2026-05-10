# free_report_ui.py

from __future__ import annotations

import streamlit as st

from pdf_report_engine import build_free_snapshot_pdf
from report_templates import (
    build_executive_summary_text,
    build_risk_lines,
    collect_report_data,
    money,
    safe_text,
)
from ui_styles import close_shell, open_shell, render_card, render_page_header, render_section_intro


def _inject_styles() -> None:
    st.markdown(
        """
        <style>
        .fr-card {
            border: 1px solid #E2E8F0;
            border-radius: 18px;
            padding: 1rem;
            background: #FFFFFF;
            box-shadow: 0 14px 34px rgba(15, 23, 42, 0.05);
            min-height: 132px;
        }
        .fr-label {
            text-transform: uppercase;
            letter-spacing: .08em;
            font-size: .72rem;
            color: #64748B;
            font-weight: 700;
            margin-bottom: .35rem;
        }
        .fr-score {
            font-size: 1.7rem;
            line-height: 1.1;
            font-weight: 800;
            color: #0B1730;
        }
        .fr-note {
            margin-top: .45rem;
            color: #5B6577;
            font-size: .9rem;
            line-height: 1.45;
        }
        .fr-summary {
            border: 1px solid #E2E8F0;
            border-radius: 18px;
            padding: 1rem 1.1rem;
            background: #F8FAFC;
            color: #334155;
            line-height: 1.55;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _format_score(item: dict | object) -> str:
    if isinstance(item, dict):
        return safe_text(item.get("display"))
    return safe_text(item)


def render_free_report() -> None:
    _inject_styles()
    report_data = collect_report_data(report_type="free_snapshot")
    pdf = build_free_snapshot_pdf(report_data)
    st.session_state["free_report_generated"] = True

    open_shell()

    render_page_header(
        eyebrow="Free Pressure Snapshot",
        title="Your early diligence signal",
        subtitle="A concise PDF snapshot of current fit, concept, financial signals, primary pressure points, and next-step diligence actions.",
        wide=True,
    )

    col1, col2, col3 = st.columns(3, gap="large")
    with col1:
        render_card(
            label="Current posture",
            title=report_data["recommendation"],
            body="A directional read from the work completed so far.",
            navy=True,
        )
    with col2:
        render_card(
            label="Top pressure point",
            title=report_data["top_risk"],
            body="The first issue to validate before relying on the current assumptions.",
            soft=True,
        )
    with col3:
        render_card(
            label="Opportunity",
            title=safe_text(report_data.get("franchise_name"), "Not recorded"),
            body="The concept currently being reviewed.",
        )

    st.markdown('<div class="rc-gap-lg"></div>', unsafe_allow_html=True)

    render_section_intro(
        title="Score snapshot",
        body="These are directional signals for organizing diligence, not predictions or recommendations to buy, invest, or proceed.",
    )

    visible_scores = [
        ("Franchise Fit", report_data["scores"].get("Franchise Fit")),
        ("Brand & Territory", report_data["scores"].get("Brand & Territory")),
        ("Concept Validation", report_data["scores"].get("Concept Validation")),
        ("Financial Model", report_data["scores"].get("Financial Model")),
    ]

    cols = st.columns(4, gap="large")
    for col, (label, item) in zip(cols, visible_scores):
        with col:
            st.markdown(
                f"""
                <div class="fr-card">
                    <div class="fr-label">{label}</div>
                    <div class="fr-score">{_format_score(item)}</div>
                    <div class="fr-note">Current directional signal based on available inputs.</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown('<div class="rc-gap-lg"></div>', unsafe_allow_html=True)

    left, right = st.columns([1.05, 1], gap="large")
    with left:
        render_section_intro(
            title="Plain-English summary",
            body="This is the same core message included in the downloadable snapshot.",
        )
        st.markdown(
            f"<div class='fr-summary'>{build_executive_summary_text(report_data)}</div>",
            unsafe_allow_html=True,
        )

    with right:
        render_section_intro(
            title="Download your snapshot",
            body="Use the PDF as an early diligence memo and checklist starter.",
        )
        st.download_button(
            "Download Free Pressure Snapshot PDF",
            pdf,
            file_name="pressuretest_free_pressure_snapshot.pdf",
            mime="application/pdf",
            use_container_width=True,
            type="primary",
        )
        st.caption("The free snapshot is intentionally concise. Deeper scenario planning and execution workflows belong in Pro.")

    st.markdown('<div class="rc-gap-lg"></div>', unsafe_allow_html=True)

    render_section_intro(
        title="Main pressure points to resolve",
        body="Treat these as diligence prompts to validate, not final conclusions.",
    )
    for item in build_risk_lines(report_data)[:5]:
        st.markdown(f"- {item}")

    st.markdown('<div class="rc-gap-lg"></div>', unsafe_allow_html=True)

    snapshot = report_data.get("financial_snapshot", {})
    with st.expander("Financial snapshot included in the executive report", expanded=False):
        rows = [
            {"Metric": key, "Current value": value if value != "-" else money(0) if key in {"Selected loan amount", "Monthly rent + NNN"} else "-"}
            for key, value in snapshot.items()
        ]
        st.table(rows)

    if st.button("Continue to Plans & Support", use_container_width=True, type="primary"):
        st.session_state["current_page"] = "Plans & Support"
        st.rerun()

    close_shell()
