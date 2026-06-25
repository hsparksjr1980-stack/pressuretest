from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import html

import streamlit as st

from branding import APP_PRODUCT
from decision_engine import build_decision_packet
from ui_styles import close_shell, open_shell, render_action_banner, render_page_header

NOTE = (
    "This is not legal, financial, tax, lending, or investment advice. Risk labels are based only on the information provided. "
    "Low Concern does not mean safe or recommended. It means this area does not currently appear to be a primary concern based on the answers entered."
)

FDD_TRANSLATION_DEFINITION = (
    "The FDD is important, but it is often system-wide. It may not prove the model works in the user's specific market, rent structure, labor market, "
    "buildout environment, supply chain, customer-demand profile, brand-awareness conditions, operator situation, or financing pressure."
)

RISK_LABELS = ["Low Concern", "Needs Verification", "Material Risk", "Stop and Review"]


@dataclass(frozen=True)
class CriticalIssue:
    title: str
    risk_label: str
    why_it_matters: str
    verify_next: str


def _items(values: list[str]) -> str:
    return "\n".join(f"- {item}" for item in values if item)


def _recommendation_label(value: object) -> str:
    labels = {
        "Proceed": "Move Forward",
        "Do Not Proceed": "Walk Away",
        "Proceed with Conditions": "Proceed Only If Conditions Are Met",
    }
    return labels.get(str(value), str(value or "Not enough data"))


def _assessment_depth() -> str:
    depth = str(st.session_state.get("assessment_depth") or "Quick Assessment")
    return depth if depth in {"Quick Assessment", "Full Review"} else "Quick Assessment"


def _truthy(*keys: str) -> bool:
    for key in keys:
        value = st.session_state.get(key)
        if isinstance(value, bool) and value:
            return True
        if isinstance(value, str) and value.strip().lower() in {"yes", "signed", "received", "pending", "true"}:
            return True
    return False


def _answer(key: str) -> str:
    return str(st.session_state.get(key) or "").strip()


def _problematic(value: str, triggers: set[str]) -> bool:
    return value.strip().lower() in {item.lower() for item in triggers}


def _fdd_translation_triggered() -> bool:
    checks = [
        _problematic(_answer("fdd_market_proof"), {"Somewhat, but the market is still developing", "No, this is a new or unproven market", "Not sure"}),
        _problematic(_answer("fdd_market_similarity"), {"Somewhat similar", "No, different market or unclear comparison", "Not sure"}),
        _problematic(_answer("similar_market_franchisee_calls"), {"No", "Not yet", "Not sure"}),
        _problematic(_answer("local_cost_difference"), {"Some differences", "Material differences", "Not sure yet"}),
    ]
    if any(checks):
        return True
    if not st.session_state.get("fdd_received") and not st.session_state.get("received_fdd"):
        return True
    return False


def _fdd_translation_summary() -> list[str]:
    items: list[str] = [FDD_TRANSLATION_DEFINITION]
    captured = [
        ("Market proof", _answer("fdd_market_proof")),
        ("Comparable examples", _answer("fdd_market_similarity")),
        ("Similar-market franchisee calls", _answer("similar_market_franchisee_calls")),
        ("Local cost differences", _answer("local_cost_difference")),
    ]
    for label, value in captured:
        if value:
            items.append(f"{label}: {value}")
    if len(items) == 1:
        items.append("System-wide information may not translate directly to this market. Local economics should be validated before further commitment.")
    return items


def _missing_evidence() -> list[str]:
    missing = []
    if not st.session_state.get("fdd_received") and not st.session_state.get("received_fdd"):
        missing.append("FDD receipt or review is not confirmed.")
    if not st.session_state.get("franchisee_validation_complete"):
        missing.append("Current franchisee validation calls are not documented.")
    if not st.session_state.get("former_franchisee_validation_complete"):
        missing.append("Former franchisee validation is not documented.")
    if not st.session_state.get("item_19_verified"):
        missing.append("Unit economics have not been independently verified.")
    if not st.session_state.get("buildout_bid_verified"):
        missing.append("Buildout cost support is missing or incomplete.")
    if not st.session_state.get("working_capital_verified"):
        missing.append("Working capital cushion has not been documented.")
    if _fdd_translation_triggered():
        missing.append("FDD Translation Risk has not been resolved with local-market evidence.")
    return missing[:8]


def _decision_critical_issues() -> list[CriticalIssue]:
    issues: list[CriticalIssue] = []

    def add(title: str, risk_label: str, why: str, verify: str) -> None:
        if title not in {item.title for item in issues}:
            issues.append(CriticalIssue(title, risk_label, why, verify))

    if not st.session_state.get("fdd_received") and not st.session_state.get("received_fdd"):
        add(
            "FDD not confirmed",
            "Stop and Review",
            "The FDD is a baseline document for understanding fees, obligations, restrictions, and system-level information before further commitment.",
            "Confirm receipt and review the FDD with an attorney before signing or paying additional non-refundable amounts.",
        )

    if _fdd_translation_triggered():
        add(
            "FDD Translation Risk",
            "Material Risk",
            "System-wide information may not translate directly to this market, rent structure, labor market, buildout environment, customer demand, or financing pressure.",
            "Validate local economics using similar-market franchisees, local rent/labor/buildout quotes, and lender/CPA assumptions.",
        )

    if _truthy("signed_anything") or _problematic(_answer("review_signed"), {"Yes"}):
        add(
            "Agreement signed or commitment already made",
            "Stop and Review",
            "Signed agreements or pending obligations can reduce your ability to pause, renegotiate, or walk away.",
            "List every signed document, deadline, deposit, and cancellation right before making the next move.",
        )

    if _truthy("lease_signed", "lease_pending"):
        add(
            "Lease signed or pending",
            "Stop and Review",
            "Lease exposure can become a major personal and business obligation even before the franchise is operating.",
            "Have the lease, guarantees, rent escalations, assignment terms, and exit limits reviewed before proceeding.",
        )

    if _truthy("personal_guarantee_required", "sba_loan_required", "major_loan_required"):
        add(
            "Personal guarantee or major debt involved",
            "Material Risk",
            "Debt and guarantees can materially affect downside exposure if ramp-up is slower, costs are higher, or the business underperforms.",
            "Confirm guarantee scope, required liquidity, debt service coverage, and downside runway with lender and CPA.",
        )

    capital_score = int(st.session_state.get("capital_flexibility_score", 3) or 3)
    if capital_score <= 2:
        add(
            "Limited cash flexibility",
            "Material Risk",
            "Low reserves after launch can turn normal startup friction into an emergency.",
            "Recalculate launch budget, working capital, debt service, and personal living runway under a slower ramp scenario.",
        )

    economics_score = int(st.session_state.get("cv_economic_confidence_score", 3) or 3)
    if economics_score <= 2 or st.session_state.get("cv_q13") == "No":
        add(
            "Revenue assumptions unsupported",
            "Material Risk",
            "This assumption appears aggressive if revenue examples are not supported by comparable market evidence.",
            "Verify local sales assumptions with similar-market franchisees, actual cost quotes, and conservative breakeven math.",
        )

    if not st.session_state.get("buildout_bid_verified"):
        add(
            "Buildout costs unclear",
            "Needs Verification",
            "Buildout overruns can materially affect required capital, debt needs, opening timeline, and break-even pressure.",
            "Get current local bids, landlord work-letter clarity, contingency estimates, and lender-recognized budget assumptions.",
        )

    if not st.session_state.get("franchisee_validation_complete"):
        add(
            "Current franchisee validation missing",
            "Needs Verification",
            "Franchisees are one of the best ways to test whether franchisor claims match operating reality.",
            "Speak with current franchisees, including operators in similar markets and cost structures.",
        )

    if not st.session_state.get("former_franchisee_validation_complete"):
        add(
            "Former franchisee validation missing",
            "Needs Verification",
            "Former operators may surface issues that are less visible in sales materials or curated validation calls.",
            "Ask for former franchisees or independently identify closed/transferred units and document what changed their decision.",
        )

    if st.session_state.get("rc_q22") == "No":
        add(
            "Walk-away discipline is weak",
            "Material Risk",
            "If you are not willing to walk away, pressure, sunk cost, or excitement can override evidence.",
            "Write explicit walk-away conditions before the next deposit, signature, lease step, or loan commitment.",
        )

    if not issues:
        add(
            "No primary decision-critical issue identified yet",
            "Low Concern",
            "Based on the information provided, no single issue currently appears to dominate the decision.",
            "Continue validating assumptions and avoid treating unanswered items as resolved.",
        )

    priority = {"Stop and Review": 0, "Material Risk": 1, "Needs Verification": 2, "Low Concern": 3}
    return sorted(issues, key=lambda item: priority.get(item.risk_label, 9))[:5]


def _risk_class(label: str) -> str:
    return {
        "Low Concern": "risk-low",
        "Needs Verification": "risk-verify",
        "Material Risk": "risk-material",
        "Stop and Review": "risk-stop",
    }.get(label, "risk-verify")


def _issue_text(issue: CriticalIssue) -> list[str]:
    return [
        f"Issue: {issue.title}",
        f"Risk label: {issue.risk_label}",
        f"Why it matters: {issue.why_it_matters}",
        f"What to verify next: {issue.verify_next}",
    ]


def _report_sections() -> list[tuple[str, list[str]]]:
    packet = build_decision_packet()
    scores = packet.get("phase_scores", {}) or {}
    risks = list(dict.fromkeys(list(packet.get("risks", [])) + list(packet.get("key_risks", []))))[:8]
    conditions = list(dict.fromkeys(list(packet.get("conditions", []))))[:8]
    recommendation = _recommendation_label(packet.get("recommendation"))
    critical_lines: list[str] = []
    for issue in _decision_critical_issues():
        critical_lines.extend(_issue_text(issue) + [""])

    sections: list[tuple[str, list[str]]] = [
        ("Franchise Pressure-Test Report", [str(st.session_state.get("franchise_name") or "Franchise opportunity not named")]),
        ("Assessment Type", [_assessment_depth()]),
        ("Current Stage", [str(st.session_state.get("final_decision_choice") or "Current stage not recorded")]),
        ("Recommendation", [recommendation]),
        ("Decision-Critical Issues", critical_lines or ["No decision-critical issue has been identified yet."]),
        ("Top Risks", risks or ["No major risk has been recorded yet."]),
        ("Missing Evidence", _missing_evidence() or ["No missing evidence has been flagged yet."]),
    ]
    if _fdd_translation_triggered():
        sections.append(("FDD Translation Risk", _fdd_translation_summary()))
    sections.extend(
        [
            ("Operator Fit Summary", [f"Score: {scores.get('readiness', 'Not scored yet')}", str(st.session_state.get("rc_biggest_concern") or "No operator-fit concern note entered.")]),
            ("Opportunity Review Summary", [f"Score: {scores.get('concept', 'Not scored yet')}", str(st.session_state.get("cv_risk_notes") or "No opportunity-review risk note entered.")]),
            ("Financial Reality Summary", [f"Score: {scores.get('financial', 'Not scored yet')}", "Local economics should be validated before further commitment."]),
            ("Commitment Risk Summary", [f"Score: {scores.get('post_discovery', 'Not scored yet')}", str(st.session_state.get("final_decision_conditions") or "No final conditions recorded yet.")]),
            ("Questions to Ask Franchisor", ["Which assumptions are based on mature units?", "What support is provided after signing?", "What causes new owners to miss plan?", "What local market evidence supports this territory or location?"]),
            ("Questions to Ask Franchisees", ["What would you verify before signing again?", "What costs were higher than expected?", "Would you open another unit?", "How did your market compare to the examples provided before signing?"]),
            ("Questions to Ask Lender/CPA/Attorney", ["How much working capital should be held back?", "Do the agreements create conflicts?", "What assumptions should be adjusted?", "What personal exposure exists if ramp-up is slower than expected?"]),
            ("Recommended Next Steps", conditions or ["Collect missing evidence, validate assumptions, and slow the process until key items are verified."]),
            ("Important Note", [NOTE]),
            ("Request Paid Review CTA", ["Want a second set of eyes? PressureTest can prepare a reviewed franchise opportunity report that checks your assumptions, highlights red flags, and gives you a clearer question list before you sign, borrow, lease, or invest."]),
        ]
    )
    return sections


def _report_text() -> str:
    lines = [f"{APP_PRODUCT} - Franchise Pressure-Test Report", f"Prepared: {datetime.now().strftime('%Y-%m-%d')}", ""]
    for title, items in _report_sections():
        lines.extend([title, "-" * len(title), _items(items), ""])
    return "\n".join(lines)


def _render_issue_cards() -> None:
    st.markdown("### Decision-Critical Issues")
    st.caption("The 3–5 issues most likely to change the decision, trigger a pause, or require verification before further commitment.")
    for issue in _decision_critical_issues():
        st.markdown(
            f"""
            <div class="pt-risk-card {_risk_class(issue.risk_label)}">
                <div class="pt-risk-topline">
                    <strong>{html.escape(issue.title)}</strong>
                    <span>{html.escape(issue.risk_label)}</span>
                </div>
                <p><strong>Why it matters:</strong> {html.escape(issue.why_it_matters)}</p>
                <p><strong>What to verify next:</strong> {html.escape(issue.verify_next)}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


def _render_request_form() -> None:
    with st.expander("Request Paid Review", expanded=False):
        st.write("PressureTest can prepare a reviewed franchise opportunity report that checks your assumptions, highlights red flags, and gives you a clearer question list before you sign, borrow, lease, or invest.")
        with st.form("review_request_form"):
            st.text_input("Name", key="review_name", value=st.session_state.get("full_name", ""))
            st.text_input("Email", key="review_email", value=st.session_state.get("email", ""))
            st.text_input("Franchise brand", key="review_brand", value=st.session_state.get("franchise_name", ""))
            st.text_input("Stage", key="review_stage")
            st.text_input("Capital at risk", key="review_amount_at_risk")
            st.selectbox("FDD received?", ["", "Yes", "No", "Not sure"], key="review_fdd")
            st.selectbox("Signed anything?", ["", "Yes", "No", "Not sure"], key="review_signed")
            st.text_area("What do you want reviewed?", key="review_scope")
            st.selectbox("Preferred contact method", ["", "Email", "Phone", "Text"], key="review_contact_method")
            submitted = st.form_submit_button("Request Paid Review", type="primary")
        if submitted:
            st.session_state["paid_review_requested"] = True
            st.session_state["review_requested"] = True
            st.session_state["review_request_payload"] = {
                "name": st.session_state.get("review_name", ""),
                "email": st.session_state.get("review_email", ""),
                "brand": st.session_state.get("review_brand", ""),
                "stage": st.session_state.get("review_stage", ""),
                "capital_at_risk": st.session_state.get("review_amount_at_risk", ""),
                "fdd_received": st.session_state.get("review_fdd", ""),
                "signed_anything": st.session_state.get("review_signed", ""),
                "scope": st.session_state.get("review_scope", ""),
                "contact_method": st.session_state.get("review_contact_method", ""),
            }
            st.success("Request captured for beta follow-up.")
            st.json(st.session_state["review_request_payload"])


def _render_feedback_form() -> None:
    with st.expander("Beta feedback", expanded=False):
        with st.form("beta_feedback_form"):
            st.selectbox("Would this have changed your decision?", ["", "Yes", "No", "Not sure"], key="feedback_changed_decision")
            st.selectbox("Did this make you slow down?", ["", "Yes", "No", "Not sure"], key="feedback_slow_down")
            st.text_area("What question is missing?", key="feedback_missing_question")
            st.text_area("What felt too soft?", key="feedback_too_soft")
            st.text_area("What felt too harsh?", key="feedback_too_harsh")
            st.selectbox("Would you pay $299 for a reviewed version?", ["", "Yes", "No", "Maybe"], key="feedback_pay_299")
            st.selectbox("Would you show this to your spouse, lender, CPA, attorney, or business partner?", ["", "Yes", "No", "Maybe"], key="feedback_share_report")
            st.text_area("What part was most useful?", key="feedback_most_useful")
            st.text_area("What part was confusing?", key="feedback_confusing")
            submitted = st.form_submit_button("Submit beta feedback")
        if submitted:
            st.session_state["beta_feedback_submitted"] = True
            st.session_state["beta_feedback_payload"] = {
                "changed_decision": st.session_state.get("feedback_changed_decision", ""),
                "slowed_down": st.session_state.get("feedback_slow_down", ""),
                "missing_question": st.session_state.get("feedback_missing_question", ""),
                "too_soft": st.session_state.get("feedback_too_soft", ""),
                "too_harsh": st.session_state.get("feedback_too_harsh", ""),
                "pay_299": st.session_state.get("feedback_pay_299", ""),
                "share_report": st.session_state.get("feedback_share_report", ""),
                "most_useful": st.session_state.get("feedback_most_useful", ""),
                "confusing": st.session_state.get("feedback_confusing", ""),
            }
            st.success("Feedback captured. Thank you.")
            st.json(st.session_state["beta_feedback_payload"])


def render_report_screen() -> None:
    report_text = _report_text()
    packet = build_decision_packet()
    recommendation = _recommendation_label(packet.get("recommendation"))
    open_shell()
    render_page_header(eyebrow=APP_PRODUCT, title="Report", subtitle="A decision memo built from your Franchise Beta responses.", wide=True)
    render_action_banner(eyebrow="Recommendation", title=recommendation, body=packet.get("summary", "Complete the workflow to improve the report."), chips=[_assessment_depth(), "Decision memo", "Exportable"])
    _render_issue_cards()
    if _fdd_translation_triggered():
        st.markdown("### FDD Translation Risk")
        st.info(FDD_TRANSLATION_DEFINITION)
        for item in _fdd_translation_summary()[1:]:
            st.write(f"- {item}")
    st.markdown("### Copy / Export")
    st.text_area("Copyable report", value=report_text, height=520)
    st.download_button("Download Text Report", data=report_text, file_name="pressuretest_franchise_report.txt", mime="text/plain", use_container_width=True)
    st.markdown("### Want a second set of eyes?")
    st.write("PressureTest can prepare a reviewed franchise opportunity report that checks your assumptions, highlights red flags, and gives you a clearer question list before you sign, borrow, lease, or invest.")
    _render_request_form()
    _render_feedback_form()
    st.caption(NOTE)
    st.session_state["report_generated"] = True
    close_shell()
