# /Users/howardsparks/Desktop/pressuretest/report_ui.py

from __future__ import annotations

import io
import html
import os
from datetime import datetime

import streamlit as st
from reportlab.lib.colors import HexColor, black
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas

from decision_engine import build_decision_packet
from branding import APP_PRODUCT
from franchise_beta import (
    FDD_TRANSLATION_DEFINITION,
    RISK_NOTE,
    assessment_type_label,
    build_decision_critical_issues,
    fdd_translation_triggered,
    render_beta_styles,
    risk_badge,
    risk_label_for_score,
    save_beta_feedback,
    save_paid_review_request,
)
from report_templates import (
    build_condition_lines,
    build_decision_headline,
    build_executive_summary_text,
    build_profile_lines,
    build_risk_lines,
    build_score_lines,
    build_strength_lines,
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

NAVY = HexColor("#0B1730")
ORANGE = HexColor("#F97316")
AMBER = HexColor("#FBBF24")
SLATE = HexColor("#5B6577")
BORDER = HexColor("#E2E8F0")
SOFT = HexColor("#F8FAFC")
WHITE = HexColor("#FFFFFF")


def _safe_score(value: object) -> str:
    if value is None:
        return "—"
    try:
        return f"{float(value):.1f}"
    except Exception:
        return str(value)


def _score_value(value: object) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except Exception:
        return None


def _score_band(score: float | None) -> str:
    if score is None:
        return "neutral"
    if score >= 78:
        return "strong"
    if score >= 58:
        return "mixed"
    return "weak"


def _band_color(score: float | None) -> HexColor:
    band = _score_band(score)
    if band == "strong":
        return HexColor("#16A34A")
    if band == "mixed":
        return AMBER
    if band == "weak":
        return HexColor("#DC2626")
    return HexColor("#94A3B8")


def _get_logo_path() -> str:
    base = os.path.dirname(os.path.abspath(__file__))
    for name in ("logo.png", "logo.jpeg", "logo.jpg"):
        path = os.path.join(base, name)
        if os.path.exists(path):
            return path
    return os.path.join(base, "logo.png")


def _parse_conditions(raw: str | None) -> list[str]:
    if not raw:
        return []
    return [line.strip("-• ").strip() for line in raw.splitlines() if line.strip()]


def _derive_final_choice() -> str:
    explicit = st.session_state.get("final_decision_choice")
    if explicit:
        return str(explicit)

    move_forward = st.session_state.get("move_forward", False)
    walk_away = st.session_state.get("walk_away", False)

    if move_forward:
        return "Proceed"
    if walk_away:
        return "Do Not Proceed"
    return "Not recorded"


def _collect_report_data() -> dict:
    packet = build_decision_packet()
    has_any_progress = any(
        bool(st.session_state.get(key))
        for key in ("phase_0_complete", "phase_1_complete", "financial_model_done", "phase_2_complete", "phase_3_complete")
    )

    readiness = st.session_state.get("readiness_score")
    concept = st.session_state.get("concept_score") or st.session_state.get("concept_validation_score")
    financial = st.session_state.get("financial_score")
    post = st.session_state.get("post_discovery_score")
    pressure = st.session_state.get("pressure_test_score")

    overall_raw = packet.get("final_score", packet.get("weighted_score"))
    recommendation = packet.get("master_verdict", packet.get("recommendation", "Decision Summary"))
    if not has_any_progress:
        recommendation = "Needs More Evidence"
        overall_raw = None
    final_choice = _derive_final_choice()

    strengths = list(packet.get("strengths", []))
    if not strengths:
        if readiness is not None and float(readiness) >= 58:
            strengths.append("Personal and operational fit looks more workable than fragile.")
        if concept is not None and float(concept) >= 58:
            strengths.append("The concept looks directionally viable under current assumptions.")
        if financial is not None and float(financial) >= 58:
            strengths.append("The economics appear more grounded than purely aspirational.")
        if post is not None and float(post) >= 58:
            strengths.append("Discovery work is reducing unknowns and improving decision quality.")
        if pressure is not None and float(pressure) >= 58:
            strengths.append("The deal appears less fragile under stress than a weak deal would.")

    risks: list[str] = []
    for group in (packet.get("key_risks", []), packet.get("conditions", []), packet.get("risks", [])):
        for item in group:
            if item and item not in risks:
                risks.append(item)

    if not risks:
        if readiness is not None and float(readiness) < 58:
            risks.append("Fit, time demand, or downside tolerance may not align with the deal.")
        if concept is not None and float(concept) < 58:
            risks.append("The concept may be weaker or less durable than it first appears.")
        if financial is not None and float(financial) < 58:
            risks.append("The economics may be too thin under current assumptions.")
        if post is not None and float(post) < 58:
            risks.append("Too many unknowns may still be unresolved after discovery.")
        if pressure is not None and float(pressure) < 58:
            risks.append("The deal may break down when assumptions are stressed.")

    final_conditions = _parse_conditions(st.session_state.get("final_decision_conditions"))
    packet_conditions = [item for item in packet.get("conditions", []) if item]
    conditions: list[str] = []
    for item in final_conditions + packet_conditions:
        if item not in conditions:
            conditions.append(item)

    top_strength = strengths[0] if strengths else "No clear strength identified yet"
    top_risk = risks[0] if risks else "Not enough evidence yet"
    if not has_any_progress:
        risks = ["Not enough evidence has been entered to support a recommendation."]
        conditions = ["Complete the Quick Assessment before relying on the report."]
        top_risk = "Missing evidence"

    data = {
        "assessment_type": assessment_type_label(),
        "current_stage": st.session_state.get("current_page", "Report"),
        "full_name": st.session_state.get("full_name", ""),
        "email": st.session_state.get("email", ""),
        "city_state": st.session_state.get("city_state", ""),
        "franchise_name": st.session_state.get("franchise_name", ""),
        "units_considered": st.session_state.get("units_considered", ""),
        "ownership_style": st.session_state.get("ownership_style", ""),
        "recommendation": recommendation,
        "decision_action": packet.get("decision_action", ""),
        "final_choice": final_choice,
        "overall_score_display": _safe_score(overall_raw),
        "overall_score_value": _score_value(overall_raw),
        "scores": {
            "Franchise Fit": {"display": _safe_score(readiness), "value": _score_value(readiness)},
            "Concept Validation": {"display": _safe_score(concept), "value": _score_value(concept)},
            "Financial Model": {"display": _safe_score(financial), "value": _score_value(financial)},
            "Post-Discovery": {"display": _safe_score(post), "value": _score_value(post)},
            "Pressure Test": {"display": _safe_score(pressure), "value": _score_value(pressure)},
        },
        "strengths": strengths[:6],
        "risks": risks[:8],
        "conditions": conditions[:8],
        "premium_access": bool(st.session_state.get("premium_access", False)),
        "report_date": datetime.now().strftime("%Y-%m-%d"),
        "final_rationale": st.session_state.get("final_decision_rationale", ""),
        "top_strength": top_strength,
        "top_risk": top_risk,
    }
    data["decision_critical_issues"] = build_decision_critical_issues(data)
    data["risk_label"] = risk_label_for_score(data["overall_score_value"])
    data["fdd_translation_triggered"] = fdd_translation_triggered()
    return data


def _draw_footer(c: canvas.Canvas, width: float, page_no: int) -> None:
    c.setStrokeColor(BORDER)
    c.line(50, 34, width - 50, 34)
    c.setFont("Helvetica", 8)
    c.setFillColor(SLATE)
    c.drawString(50, 22, "PressureTest: Franchise — Decision Report")
    c.drawRightString(width - 50, 22, f"Page {page_no}")


def _new_page(c: canvas.Canvas, width: float, height: float, page_no: int) -> tuple[int, float]:
    _draw_footer(c, width, page_no)
    c.showPage()
    page_no += 1
    return page_no, height - 56


def _wrap_lines(text: str, max_width: float, font_name: str, font_size: int) -> list[str]:
    words = text.split()
    if not words:
        return [""]
    lines: list[str] = []
    current = words[0]
    for word in words[1:]:
        candidate = f"{current} {word}"
        if stringWidth(candidate, font_name, font_size) <= max_width:
            current = candidate
        else:
            lines.append(current)
            current = word
    lines.append(current)
    return lines


def _draw_wrapped_text(
    c: canvas.Canvas,
    text: str,
    x: float,
    y: float,
    max_width: float,
    font_name: str = "Helvetica",
    font_size: int = 10,
    leading: int = 14,
) -> float:
    c.setFont(font_name, font_size)
    for line in _wrap_lines(text, max_width, font_name, font_size):
        c.drawString(x, y, line)
        y -= leading
    return y


def _ensure_space(
    c: canvas.Canvas,
    y: float,
    needed: float,
    width: float,
    height: float,
    page_no: int,
) -> tuple[float, int]:
    if y - needed < 52:
        page_no, y = _new_page(c, width, height, page_no)
    return y, page_no


def _draw_section_header(c: canvas.Canvas, title: str, x: float, y: float, width: float) -> float:
    c.setStrokeColor(BORDER)
    c.line(x, y + 4, x + width, y + 4)
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(NAVY)
    c.drawString(x, y - 10, title)
    return y - 28


def _draw_bullets(
    c: canvas.Canvas,
    items: list[str],
    x: float,
    y: float,
    width: float,
    page_width: float,
    page_height: float,
    page_no: int,
    font_size: int = 10,
) -> tuple[float, int]:
    for item in items:
        y, page_no = _ensure_space(c, y, 24, page_width, page_height, page_no)
        lines = _wrap_lines(f"• {item}", width, "Helvetica", font_size)
        c.setFont("Helvetica", font_size)
        c.setFillColor(black)
        for line in lines:
            c.drawString(x, y, line)
            y -= 14
    return y, page_no


def _draw_metric_box(
    c: canvas.Canvas,
    x: float,
    y: float,
    w: float,
    h: float,
    label: str,
    value: str,
    score: float | None,
) -> None:
    accent = _band_color(score)
    c.setFillColor(WHITE)
    c.setStrokeColor(BORDER)
    c.roundRect(x, y - h, w, h, 10, fill=1, stroke=1)

    c.setFillColor(accent)
    c.roundRect(x + 10, y - 16, 44, 6, 3, fill=1, stroke=0)

    c.setFillColor(SLATE)
    c.setFont("Helvetica", 8)
    c.drawString(x + 10, y - 30, label.upper())

    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 15)
    c.drawString(x + 10, y - 50, value)


def _create_pdf(report_data: dict) -> bytes:
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=LETTER)
    width, height = LETTER
    page_no = 1

    left = 50
    right = 50
    usable_width = width - left - right
    y = height - 56

    logo_path = _get_logo_path()
    if os.path.exists(logo_path):
        try:
            logo = ImageReader(logo_path)
            c.drawImage(
                logo,
                left,
                y - 12,
                width=240,
                height=64,
                preserveAspectRatio=True,
                mask="auto",
            )
        except Exception:
            pass

    c.setFont("Helvetica-Bold", 22)
    c.setFillColor(NAVY)
    c.drawRightString(width - right, y + 2, "Franchise Pressure-Test Report")

    y -= 28
    c.setFont("Helvetica", 10)
    c.setFillColor(SLATE)
    c.drawRightString(width - right, y, f"Prepared on {report_data['report_date']}")

    y -= 26
    c.setStrokeColor(ORANGE)
    c.setLineWidth(2)
    c.line(left, y, width - right, y)

    y -= 26
    c.setFillColor(SOFT)
    c.setStrokeColor(BORDER)
    c.roundRect(left, y - 78, usable_width, 74, 12, fill=1, stroke=1)

    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(left + 14, y - 20, report_data["franchise_name"] or "Opportunity")
    c.setFont("Helvetica", 10)
    c.setFillColor(SLATE)
    c.drawString(left + 14, y - 38, build_decision_headline(report_data))
    c.drawString(left + 14, y - 56, f"Client: {report_data['full_name'] or '—'}")
    c.drawRightString(width - right - 14, y - 56, f"Ownership: {report_data['ownership_style'] or '—'}")

    y -= 104

    y = _draw_section_header(c, "Executive Summary", left, y, usable_width)
    c.setFillColor(black)
    y = _draw_wrapped_text(c, build_executive_summary_text(report_data), left, y, usable_width)
    y -= 10

    y, page_no = _ensure_space(c, y, 92, width, height, page_no)
    y = _draw_section_header(c, "Assessment Type and Stage", left, y, usable_width)
    y, page_no = _draw_bullets(
        c,
        [
            f"Assessment type: {report_data.get('assessment_type', 'Quick Assessment')}",
            f"Current stage: {report_data.get('current_stage', 'Report')}",
            RISK_NOTE,
        ],
        left,
        y,
        usable_width,
        width,
        height,
        page_no,
    )
    y -= 10

    y, page_no = _ensure_space(c, y, 108, width, height, page_no)
    y = _draw_section_header(c, "Decision Snapshot", left, y, usable_width)

    box_w = (usable_width - 24) / 3
    _draw_metric_box(c, left, y, box_w, 62, "Recommendation", report_data["recommendation"], report_data["overall_score_value"])
    _draw_metric_box(c, left + box_w + 12, y, box_w, 62, "Final Call", report_data["final_choice"], report_data["overall_score_value"])
    _draw_metric_box(c, left + (box_w + 12) * 2, y, box_w, 62, "Overall Score", report_data["overall_score_display"], report_data["overall_score_value"])
    y -= 82

    y, page_no = _ensure_space(c, y, 150, width, height, page_no)
    y = _draw_section_header(c, "Decision-Critical Issues", left, y, usable_width)
    issue_lines = [
        f"{issue['title']} ({issue['label']}): {issue['why']} Verify next: {issue['verify']}"
        for issue in report_data.get("decision_critical_issues", [])
    ]
    y, page_no = _draw_bullets(c, issue_lines, left, y, usable_width, width, height, page_no)
    y -= 10

    y, page_no = _ensure_space(c, y, 140, width, height, page_no)
    y = _draw_section_header(c, "Section Scores", left, y, usable_width)

    score_items = list(report_data["scores"].items())
    top_y = y
    first_row = score_items[:3]
    second_row = score_items[3:5]
    score_w = (usable_width - 24) / 3

    for idx, (label, item) in enumerate(first_row):
        _draw_metric_box(c, left + idx * (score_w + 12), top_y, score_w, 58, label, item["display"], item["value"])

    y -= 74
    for idx, (label, item) in enumerate(second_row):
        _draw_metric_box(c, left + idx * (score_w + 12), y, score_w, 58, label, item["display"], item["value"])

    y -= 84

    sections = [
        ("Top Risks", build_risk_lines(report_data)),
        ("Missing Evidence", build_condition_lines(report_data)),
        ("Operator Fit Summary", [f"Operator Fit score: {report_data['scores']['Franchise Fit']['display']}"]),
        ("Opportunity Review Summary", [f"Opportunity Review score: {report_data['scores']['Concept Validation']['display']}"]),
        ("Financial Reality Summary", [f"Financial score: {report_data['scores']['Financial Model']['display']}", f"Pressure Test score: {report_data['scores']['Pressure Test']['display']}"]),
        ("Commitment Risk Summary", [f"Commitment Review score: {report_data['scores']['Post-Discovery']['display']}"]),
        ("Questions to Ask Franchisor", ["Which similar-market units support these assumptions?", "What local cost differences should be expected?", "What risks have caused recent franchisees to miss plan?"]),
        ("Questions to Ask Franchisees", ["What surprised you after opening?", "How did local rent, labor, buildout, and ramp compare with expectations?", "Would you sign the same agreement again under the same terms?"]),
        ("Questions to Ask Lender/CPA/Attorney", ["What obligations survive if the business underperforms?", "How much cash cushion remains after launch?", "Which terms should be reviewed before signing or borrowing?"]),
        ("Recommended Next Steps", build_condition_lines(report_data)),
        ("Important Note", [RISK_NOTE, "PressureTest is not legal, tax, accounting, lending, or investment advice."]),
        ("Profile Snapshot", build_profile_lines(report_data)),
    ]

    if report_data.get("fdd_translation_triggered"):
        sections.insert(2, ("FDD Translation Risk", [FDD_TRANSLATION_DEFINITION]))

    for title, items in sections:
        y, page_no = _ensure_space(c, y, 120, width, height, page_no)
        y = _draw_section_header(c, title, left, y, usable_width)
        y, page_no = _draw_bullets(c, items, left, y, usable_width, width, height, page_no)
        y -= 10

    if report_data.get("final_rationale"):
        y, page_no = _ensure_space(c, y, 120, width, height, page_no)
        y = _draw_section_header(c, "Why This Recommendation Exists", left, y, usable_width)
        c.setFillColor(black)
        y = _draw_wrapped_text(c, report_data["final_rationale"], left, y, usable_width)

    _draw_footer(c, width, page_no)
    c.save()

    pdf = buffer.getvalue()
    buffer.close()
    return pdf


def _inject_local_styles() -> None:
    st.markdown(
        """
        <style>
            .rr-note {
                font-size: 0.92rem;
                line-height: 1.55;
                color: #5B6577;
            }
            .rr-shell {
                background: #FFFFFF;
                border: 1px solid #D8DEE8;
                border-radius: 16px;
                padding: 1.15rem;
                box-shadow: 0 18px 42px rgba(15, 23, 42, .06);
                margin: 1rem 0;
            }
            .rr-recommendation {
                background: linear-gradient(135deg, #111827 0%, #263244 100%);
                color: #F8FAFC;
                border-radius: 16px;
                padding: 1.25rem;
                box-shadow: 0 22px 55px rgba(17, 24, 39, .22);
                margin: 1rem 0;
            }
            .rr-recommendation h2 {
                margin: .2rem 0 .45rem 0;
                color: #F8FAFC;
                font-size: 1.55rem;
            }
            .rr-recommendation p {
                margin: 0;
                color: #E5E7EB;
                line-height: 1.55;
            }
            .rr-section-grid {
                display: grid;
                grid-template-columns: repeat(2, minmax(0, 1fr));
                gap: .85rem;
                margin: 1rem 0;
            }
            .rr-form-wrap {
                background: #FFFBEB;
                border: 1px solid #FDE68A;
                border-radius: 16px;
                padding: 1.15rem;
                margin: 1rem 0;
                box-shadow: 0 14px 34px rgba(180, 83, 9, .10);
            }
            .rr-form-title {
                color: #111827;
                font-size: 1.25rem;
                font-weight: 850;
                margin-bottom: .3rem;
            }
            .rr-form-copy {
                color: #526071;
                line-height: 1.5;
                margin-bottom: .75rem;
            }
            @media (max-width: 760px) {
                .rr-section-grid { grid-template-columns: 1fr; }
                .rr-shell, .rr-recommendation, .rr-form-wrap { border-radius: 12px; padding: .9rem; }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _render_decision_critical_issues(report_data: dict) -> None:
    issues = list(report_data.get("decision_critical_issues", []))
    st.markdown("### Decision-Critical Issues")
    for issue in issues:
        st.markdown(
            f"""
            <div class="rc-card" style="border-left:4px solid #B45309;">
                {risk_badge(str(issue.get("label", "Needs Verification")))}
                <div class="rc-card-title">{str(issue.get("title", ""))}</div>
                <div class="rc-card-body"><strong>Why it matters:</strong> {str(issue.get("why", ""))}</div>
                <div class="rc-card-body"><strong>What to verify next:</strong> {str(issue.get("verify", ""))}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def _render_paid_review_form(report_data: dict) -> None:
    st.markdown(
        """
        <div class="rr-form-wrap">
            <div class="rc-kicker">Manual paid review</div>
            <div class="rr-form-title">Want a second set of eyes?</div>
            <div class="rr-form-copy">
                Request a Reviewed Franchise Opportunity Report — starting at $299.
                PressureTest can check your assumptions, highlight red flags, and give you a clearer question list before you sign, borrow, lease, or invest.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    with st.form("paid_review_request_form"):
        c1, c2 = st.columns(2)
        with c1:
            name = st.text_input("Name", value=st.session_state.get("full_name", ""))
            email = st.text_input("Email", value=st.session_state.get("email", ""))
            franchise_brand = st.text_input("Franchise brand", value=report_data.get("franchise_name", ""))
            stage = st.selectbox("Stage", ["Early research", "FDD received", "Discovery day", "Lease/site review", "Financing", "Close to signing", "Other"])
        with c2:
            capital_at_risk = st.selectbox("Capital at risk", ["Not sure", "Under $100k", "$100k-$250k", "$250k-$500k", "$500k-$1M", "$1M+"])
            fdd_received = st.selectbox("FDD received?", ["Not sure", "Yes", "No", "Not yet"])
            signed_anything = st.selectbox("Signed anything?", ["No", "Yes", "Pending", "Not sure"])
            preferred_contact = st.selectbox("Preferred contact method", ["Email", "Phone", "Text"])
        review_scope = st.text_area("What do you want reviewed?", placeholder="Examples: FDD, local market assumptions, lease exposure, debt pressure, buildout estimate, spouse/partner concerns")
        submitted = st.form_submit_button("Request Paid Review", type="primary", use_container_width=True)
    if submitted:
        save_paid_review_request(
            {
                "name": name,
                "email": email,
                "franchise_brand": franchise_brand,
                "stage": stage,
                "capital_at_risk": capital_at_risk,
                "fdd_received": fdd_received,
                "signed_anything": signed_anything,
                "review_scope": review_scope,
                "preferred_contact": preferred_contact,
            }
        )
        st.success("Paid review request saved for manual follow-up.")


def _render_beta_feedback_form() -> None:
    st.markdown("### Beta Feedback")
    with st.form("beta_feedback_form"):
        c1, c2 = st.columns(2)
        with c1:
            changed_decision = st.radio("Would this have changed your decision?", ["Not sure", "Yes", "No"], horizontal=True)
            made_slow_down = st.radio("Did this make you slow down?", ["Not sure", "Yes", "No"], horizontal=True)
            would_pay_299 = st.radio("Would you pay $299 for a reviewed version?", ["Not sure", "Yes", "No"], horizontal=True)
            would_show_to_advisor = st.radio("Would you show this to your spouse, lender, CPA, attorney, or business partner?", ["Not sure", "Yes", "No"], horizontal=True)
        with c2:
            missing_question = st.text_area("What question is missing?")
            too_soft = st.text_area("What felt too soft?")
            too_harsh = st.text_area("What felt too harsh?")
        most_useful = st.text_area("What part was most useful?")
        confusing = st.text_area("What part was confusing?")
        submitted = st.form_submit_button("Send Beta Feedback", use_container_width=True)
    if submitted:
        save_beta_feedback(
            {
                "changed_decision": changed_decision,
                "made_slow_down": made_slow_down,
                "missing_question": missing_question,
                "too_soft": too_soft,
                "too_harsh": too_harsh,
                "would_pay_299": would_pay_299,
                "would_show_to_advisor": would_show_to_advisor,
                "most_useful": most_useful,
                "confusing": confusing,
            }
        )
        st.success("Beta feedback saved.")


def render_report_screen() -> None:
    render_beta_styles()
    _inject_local_styles()
    report_data = _collect_report_data()
    pdf_bytes = _create_pdf(report_data)
    st.session_state["report_generated"] = True

    open_shell()

    render_page_header(
        eyebrow="Step 7 of 7 — Report",
        title="Franchise Pressure-Test Report",
        subtitle="The report is the product: a cautious decision memo focused on what matters before you sign, borrow, lease, or invest.",
        wide=True,
    )

    st.markdown(
        f"""
        <div class="rr-recommendation">
            <div class="rc-kicker" style="color:#FCD34D;">Recommendation</div>
            <h2>{html.escape(str(report_data["recommendation"]))}</h2>
            <p>{html.escape(build_decision_headline(report_data))}</p>
            <div class="rc-chip-row">
                <span class="rc-chip">{html.escape(str(report_data["assessment_type"]))}</span>
                <span class="rc-chip">Decision memo</span>
                <span class="rc-chip">Shareable</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(f'<div class="pt-risk-note">{risk_badge(report_data["risk_label"])} {RISK_NOTE}</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3, gap="large")
    with col1:
        render_card(
            label="Recommendation",
            title=report_data["recommendation"],
            body="The current recommendation based on the completed work and recorded signals.",
            navy=True,
        )
    with col2:
        render_card(
            label="Main risk",
            title=report_data["top_risk"],
            body="The biggest unresolved issue that still matters to the decision.",
            soft=True,
        )
    with col3:
        render_card(
            label="Final call",
            title=report_data["final_choice"],
            body="The decision currently recorded in the workflow.",
        )

    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)
    _render_decision_critical_issues(report_data)

    st.markdown('<div class="rr-section-grid">', unsafe_allow_html=True)
    render_bullet_panel("Top Risks", "What appears most exposed", build_risk_lines(report_data))
    render_bullet_panel("Missing Evidence", "What should be verified", build_condition_lines(report_data))
    render_bullet_panel(
        "Questions to Ask",
        "Franchisor and franchisees",
        [
            "Which similar-market units support these assumptions?",
            "How did local rent, labor, buildout, and ramp compare with expectations?",
            "What risks have caused recent franchisees to miss plan?",
        ],
    )
    render_bullet_panel(
        "Recommended Next Steps",
        "Before moving forward",
        build_condition_lines(report_data),
    )
    st.markdown('</div>', unsafe_allow_html=True)

    render_section_intro(
        title="Download the decision memo",
        body="Export a printable report with recommendation, Decision-Critical Issues, risk labels, missing evidence, FDD Translation Risk, advisor questions, and next steps.",
    )

    st.download_button(
        label="Download PDF Report",
        data=pdf_bytes,
        file_name="pressuretest_report.pdf",
        mime="application/pdf",
        type="primary",
        use_container_width=True,
    )

    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="rr-note">{build_executive_summary_text(report_data)}</div>', unsafe_allow_html=True)

    if report_data.get("fdd_translation_triggered"):
        render_section_intro(
            title="FDD Translation Risk",
            body=FDD_TRANSLATION_DEFINITION,
        )

    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)
    _render_paid_review_form(report_data)
    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)
    _render_beta_feedback_form()

    close_shell()
