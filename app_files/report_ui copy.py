# report_ui.py

from __future__ import annotations

import streamlit as st

from branding import APP_PRODUCT
from pdf_report_engine import build_executive_report_pdf
from report_templates import (
    build_condition_lines,
    build_decision_headline,
    build_executive_summary_text,
    build_risk_lines,
    build_strength_lines,
    collect_report_data,
)
from ui_styles import (
    close_shell,
    open_shell,
    render_action_banner,
    render_bullet_panel,
    render_card,
    render_page_header,
    render_section_intro,
)


def _inject_local_styles() -> None:
    st.markdown(
        """
        <style>
            .rr-note {
                font-size: 0.92rem;
                line-height: 1.55;
                color: #5B6577;
            }
            .rr-report-preview {
                border: 1px solid #E2E8F0;
                border-radius: 18px;
                background: #FFFFFF;
                padding: 1.1rem 1.2rem;
                box-shadow: 0 16px 40px rgba(15, 23, 42, 0.06);
            }
            .rr-report-preview h4 {
                margin: 0 0 .45rem 0;
                color: #0B1730;
            }
            .rr-report-preview p {
                margin: 0;
                color: #5B6577;
                line-height: 1.55;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_report_screen() -> None:
    _inject_local_styles()
    report_data = collect_report_data(report_type="executive")
    pdf_bytes = build_executive_report_pdf(report_data)

    open_shell()

    render_page_header(
        eyebrow=APP_PRODUCT,
        title="Executive Diligence Report",
        subtitle="Export a cleaner operator packet with the decision posture, key risks, conditions, financial snapshot, and next-step checklist.",
        wide=True,
    )

    render_action_banner(
        eyebrow="Report posture",
        title=report_data["recommendation"],
        body=build_decision_headline(report_data),
        chips=["Printable PDF", "Decision memo", "Operator packet"],
    )

    col1, col2, col3 = st.columns(3, gap="large")
    with col1:
        render_card(
            label="Recommendation",
            title=report_data["recommendation"],
            body="The current decision posture based on completed workflow signals.",
            navy=True,
        )
    with col2:
        render_card(
            label="Main pressure point",
            title=report_data["top_risk"],
            body="The biggest unresolved issue to validate before committing.",
            soft=True,
        )
    with col3:
        render_card(
            label="Final call",
            title=report_data["final_choice"],
            body="The decision currently recorded in the workflow.",
        )

    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

    left, right = st.columns([1.05, 1], gap="large")

    with left:
        render_section_intro(
            title="What the PDF includes",
            body="The report is structured as a reusable diligence memo, not a raw app printout.",
        )
        render_bullet_panel(
            label="Executive report",
            title="Contents",
            items=[
                "Executive summary and decision snapshot",
                "Section scores and pressure signals",
                "Main risks and proceed conditions",
                "Financial snapshot",
                "Next-step checklist",
                "Educational boundary notice",
            ],
        )

    with right:
        render_section_intro(
            title="Download",
            body="Use this as a discussion packet for personal review, partner conversations, lender preparation, or advisor review.",
        )
        st.download_button(
            label="Download Executive Report PDF",
            data=pdf_bytes,
            file_name="pressuretest_executive_diligence_report.pdf",
            mime="application/pdf",
            type="primary",
            use_container_width=True,
        )
        st.caption("PressureTest outputs are educational and should be independently validated.")

    st.markdown('<div class="rc-gap-lg"></div>', unsafe_allow_html=True)

    render_section_intro(
        title="Report preview",
        body="This is the plain-English content the PDF organizes into a printable operator packet.",
    )

    st.markdown(
        f"""
        <div class="rr-report-preview">
            <h4>Executive summary</h4>
            <p>{build_executive_summary_text(report_data)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_a, col_b, col_c = st.columns(3, gap="large")
    with col_a:
        render_bullet_panel("Strengths", "What looks stronger", build_strength_lines(report_data)[:5])
    with col_b:
        render_bullet_panel("Risks", "Main pressure points", build_risk_lines(report_data)[:5])
    with col_c:
        render_bullet_panel("Conditions", "Before proceeding", build_condition_lines(report_data)[:5])

    close_shell()
