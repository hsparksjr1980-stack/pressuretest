<<<<<<< HEAD
# report_ui.py

from __future__ import annotations

import streamlit as st

from branding import APP_PRODUCT
from lead_capture_ui import render_lead_capture_gate, render_inline_lead_prompt
from pdf_report_engine import build_executive_report_pdf
=======
# /Users/howardsparks/Desktop/pressuretest/report_ui.py

from __future__ import annotations

import io
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
>>>>>>> fec65288cb896b4679e84e61241f185fa625e150
from report_templates import (
    build_condition_lines,
    build_decision_headline,
    build_executive_summary_text,
<<<<<<< HEAD
    build_risk_lines,
    build_strength_lines,
    collect_report_data,
=======
    build_profile_lines,
    build_risk_lines,
    build_score_lines,
    build_strength_lines,
>>>>>>> fec65288cb896b4679e84e61241f185fa625e150
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

<<<<<<< HEAD
=======
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

    readiness = st.session_state.get("readiness_score")
    concept = st.session_state.get("concept_score") or st.session_state.get("concept_validation_score")
    financial = st.session_state.get("financial_score")
    post = st.session_state.get("post_discovery_score")
    pressure = st.session_state.get("pressure_test_score")

    overall_raw = packet.get("final_score", packet.get("weighted_score"))
    recommendation = packet.get("master_verdict", packet.get("recommendation", "Decision Summary"))
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

    data = {
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
    c.drawRightString(width - right, y + 2, "Decision Report")

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

    y, page_no = _ensure_space(c, y, 108, width, height, page_no)
    y = _draw_section_header(c, "Decision Snapshot", left, y, usable_width)

    box_w = (usable_width - 24) / 3
    _draw_metric_box(c, left, y, box_w, 62, "Recommendation", report_data["recommendation"], report_data["overall_score_value"])
    _draw_metric_box(c, left + box_w + 12, y, box_w, 62, "Final Call", report_data["final_choice"], report_data["overall_score_value"])
    _draw_metric_box(c, left + (box_w + 12) * 2, y, box_w, 62, "Overall Score", report_data["overall_score_display"], report_data["overall_score_value"])
    y -= 82

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
        ("What Looks Stronger", build_strength_lines(report_data)),
        ("Main Risks", build_risk_lines(report_data)),
        ("Required Conditions Before Proceeding", build_condition_lines(report_data)),
        ("Profile Snapshot", build_profile_lines(report_data)),
    ]

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

>>>>>>> fec65288cb896b4679e84e61241f185fa625e150

def _inject_local_styles() -> None:
    st.markdown(
        """
        <style>
            .rr-note {
                font-size: 0.92rem;
                line-height: 1.55;
                color: #5B6577;
            }
<<<<<<< HEAD
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
=======
>>>>>>> fec65288cb896b4679e84e61241f185fa625e150
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_report_screen() -> None:
    _inject_local_styles()
<<<<<<< HEAD
    report_data = collect_report_data(report_type="executive")
    pdf_bytes = build_executive_report_pdf(report_data)
=======
    report_data = _collect_report_data()
    pdf_bytes = _create_pdf(report_data)
>>>>>>> fec65288cb896b4679e84e61241f185fa625e150

    open_shell()

    render_page_header(
        eyebrow=APP_PRODUCT,
<<<<<<< HEAD
        title="Executive Diligence Report",
        subtitle="Export a cleaner operator packet with the decision posture, key risks, conditions, financial snapshot, and next-step checklist.",
=======
        title="Report",
        subtitle="Generate a cleaner decision memo with the recommendation, risks, conditions, and section findings in one printable file.",
>>>>>>> fec65288cb896b4679e84e61241f185fa625e150
        wide=True,
    )

    render_action_banner(
        eyebrow="Report posture",
        title=report_data["recommendation"],
        body=build_decision_headline(report_data),
<<<<<<< HEAD
        chips=["Printable PDF", "Decision memo", "Operator packet"],
=======
        chips=["Printable", "Decision memo", "Shareable"],
>>>>>>> fec65288cb896b4679e84e61241f185fa625e150
    )

    col1, col2, col3 = st.columns(3, gap="large")
    with col1:
        render_card(
            label="Recommendation",
            title=report_data["recommendation"],
<<<<<<< HEAD
            body="The current decision posture based on completed workflow signals.",
=======
            body="The current recommendation based on the completed work and recorded signals.",
>>>>>>> fec65288cb896b4679e84e61241f185fa625e150
            navy=True,
        )
    with col2:
        render_card(
<<<<<<< HEAD
            label="Main pressure point",
            title=report_data["top_risk"],
            body="The biggest unresolved issue to validate before committing.",
=======
            label="Main risk",
            title=report_data["top_risk"],
            body="The biggest unresolved issue that still matters to the decision.",
>>>>>>> fec65288cb896b4679e84e61241f185fa625e150
            soft=True,
        )
    with col3:
        render_card(
            label="Final call",
            title=report_data["final_choice"],
            body="The decision currently recorded in the workflow.",
        )

    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

<<<<<<< HEAD
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
=======
    render_section_intro(
        title="What the PDF now does better",
        body="The export opens with the recommendation, executive summary, section scores, main risks, proceed conditions, and a clearer memo-style layout for printing or sharing.",
    )

    left, right = st.columns([1.05, 1], gap="large")

    with left:
        render_bullet_panel(
            label="Included in the report",
            title="Core contents",
            items=[
                "Executive summary",
                "Decision snapshot",
                "Section score summary",
                "Main risks",
                "Required proceed conditions",
                "Profile snapshot",
>>>>>>> fec65288cb896b4679e84e61241f185fa625e150
            ],
        )

    with right:
<<<<<<< HEAD
        render_section_intro(
            title="Download",
            body="Use this as a discussion packet for personal review, partner conversations, lender preparation, or advisor review.",
        )
        render_inline_lead_prompt(
            asset_name="Executive Diligence Report PDF",
            context="This capture point preserves the report workflow and creates a CRM-ready handoff for serious users.",
        )
        unlocked = render_lead_capture_gate(
            asset_key="executive_diligence_report_pdf",
            asset_name="Executive Diligence Report PDF",
            lead_source="executive_report_download",
            title="Unlock the executive report download",
            body="Enter your email to save the operator packet and download the PDF.",
            button_label="Unlock Executive Report PDF",
        )
        if unlocked:
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
=======
        render_bullet_panel(
            label="Download",
            title="Export a printable PDF",
            items=[
                "Clean cover and hierarchy",
                "Print-safe spacing",
                "Board-ready decision summary",
            ],
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
>>>>>>> fec65288cb896b4679e84e61241f185fa625e150

    close_shell()
