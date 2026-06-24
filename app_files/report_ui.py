from __future__ import annotations

from datetime import datetime

import streamlit as st

from branding import APP_PRODUCT
from decision_engine import build_decision_packet
from ui_styles import close_shell, open_shell, render_action_banner, render_page_header

NOTE = "Educational diligence summary only. Verify assumptions before making commitments."


def _items(values: list[str]) -> str:
    return "\n".join(f"- {item}" for item in values if item)


def _recommendation_label(value: object) -> str:
    labels = {
        "Proceed": "Move Forward",
        "Do Not Proceed": "Walk Away",
        "Proceed with Conditions": "Proceed Only If Conditions Are Met",
    }
    return labels.get(str(value), str(value or "Not enough data"))


def _missing_evidence() -> list[str]:
    missing = []
    if not st.session_state.get("fdd_received") and not st.session_state.get("received_fdd"):
        missing.append("FDD receipt or review is not confirmed.")
    if not st.session_state.get("franchisee_validation_complete"):
        missing.append("Franchisee validation calls are not documented.")
    if not st.session_state.get("item_19_verified"):
        missing.append("Unit economics have not been independently verified.")
    if not st.session_state.get("buildout_bid_verified"):
        missing.append("Buildout support is missing or incomplete.")
    if not st.session_state.get("working_capital_verified"):
        missing.append("Working capital cushion has not been documented.")
    return missing[:8]


def _report_text() -> str:
    packet = build_decision_packet()
    scores = packet.get("phase_scores", {}) or {}
    risks = list(dict.fromkeys(list(packet.get("risks", [])) + list(packet.get("key_risks", []))))[:8]
    conditions = list(dict.fromkeys(list(packet.get("conditions", []))))[:8]
    recommendation = _recommendation_label(packet.get("recommendation"))
    sections = [
        ("Executive Summary", [packet.get("summary", "Based on the information provided, this report is ready for review.")]),
        ("Current Decision Stage", [str(st.session_state.get("final_decision_choice") or "Current stage not recorded")]),
        ("Recommendation", [recommendation]),
        ("Top Risks", risks or ["No major risk has been recorded yet."]),
        ("Missing Evidence", _missing_evidence() or ["No missing evidence has been flagged yet."]),
        ("Operator Fit Summary", [f"Score: {scores.get('readiness', 'Not scored yet')}" ]),
        ("Opportunity Review Summary", [f"Score: {scores.get('concept', 'Not scored yet')}" ]),
        ("Financial Reality Summary", [f"Score: {scores.get('financial', 'Not scored yet')}" ]),
        ("Commitment Risk Summary", [f"Score: {scores.get('post_discovery', 'Not scored yet')}" ]),
        ("Questions to Ask the Franchisor", ["Which assumptions are based on mature units?", "What support is provided after signing?", "What causes new owners to miss plan?"]),
        ("Questions to Ask Franchisees", ["What would you verify before signing again?", "What costs were higher than expected?", "Would you open another unit?"]),
        ("Questions to Ask Advisors", ["How much working capital should be held back?", "Do the agreements create conflicts?", "What assumptions should be adjusted?"]),
        ("Recommended Next Steps", conditions or ["Collect missing evidence, validate assumptions, and slow the process until key items are verified."]),
        ("Important Note", [NOTE]),
    ]
    lines = [f"{APP_PRODUCT} - Franchise Opportunity Report", f"Prepared: {datetime.now().strftime('%Y-%m-%d')}", ""]
    for title, items in sections:
        lines.extend([title, "-" * len(title), _items(items), ""])
    lines.extend(["Want a second set of eyes?", "Request a reviewed franchise opportunity report before making commitments."])
    return "\n".join(lines)


def _render_request_form() -> None:
    with st.expander("Request Review", expanded=False):
        with st.form("review_request_form"):
            st.text_input("Name", key="review_name", value=st.session_state.get("full_name", ""))
            st.text_input("Email", key="review_email", value=st.session_state.get("email", ""))
            st.text_input("Franchise brand", key="review_brand", value=st.session_state.get("franchise_name", ""))
            st.text_input("Current stage", key="review_stage")
            st.text_input("Amount at risk", key="review_amount_at_risk")
            st.selectbox("Have you received the FDD?", ["", "Yes", "No", "Not sure"], key="review_fdd")
            st.selectbox("Have you signed anything?", ["", "Yes", "No", "Not sure"], key="review_signed")
            st.text_area("What do you want reviewed?", key="review_scope")
            st.selectbox("Preferred contact method", ["", "Email", "Phone", "Text"], key="review_contact_method")
            submitted = st.form_submit_button("Request Review", type="primary")
        if submitted:
            st.session_state["review_requested"] = True
            st.success("Request captured for beta follow-up.")


def _render_feedback_form() -> None:
    with st.expander("Beta feedback", expanded=False):
        with st.form("beta_feedback_form"):
            st.selectbox("Would this have changed your decision?", ["", "Yes", "No", "Not sure"], key="feedback_changed_decision")
            st.text_area("What question was missing?", key="feedback_missing_question")
            st.text_area("What felt too soft?", key="feedback_too_soft")
            st.text_area("What felt too harsh?", key="feedback_too_harsh")
            st.selectbox("Would you consider a reviewed version?", ["", "Yes", "No", "Maybe"], key="feedback_reviewed_version")
            st.selectbox("Would you show this report to an advisor or partner?", ["", "Yes", "No", "Maybe"], key="feedback_share_report")
            st.text_area("What part was most useful?", key="feedback_most_useful")
            st.text_area("What part was confusing?", key="feedback_confusing")
            submitted = st.form_submit_button("Submit beta feedback")
        if submitted:
            st.session_state["beta_feedback_submitted"] = True
            st.success("Feedback captured. Thank you.")


def render_report_screen() -> None:
    report_text = _report_text()
    packet = build_decision_packet()
    recommendation = _recommendation_label(packet.get("recommendation"))
    open_shell()
    render_page_header(eyebrow=APP_PRODUCT, title="Report", subtitle="A cautious franchise diligence report built from your responses.", wide=True)
    render_action_banner(eyebrow="Report posture", title=recommendation, body=packet.get("summary", "Complete the workflow to improve the report."), chips=["Savable", "Copyable", "Exportable"])
    st.text_area("Copyable report", value=report_text, height=420)
    st.download_button("Download Text Report", data=report_text, file_name="pressuretest_franchise_report.txt", mime="text/plain", use_container_width=True)
    st.markdown("### Want a second set of eyes?")
    st.write("Request a reviewed franchise opportunity report that checks assumptions, highlights red flags, and gives you a clearer question list.")
    _render_request_form()
    _render_feedback_form()
    st.caption(NOTE)
    st.session_state["report_generated"] = True
    close_shell()
