# /Users/howardsparks/Desktop/pressuretest/report_templates.py

from __future__ import annotations

from decision_engine import build_decision_packet


def build_decision_headline(report_data: dict) -> str:
    choice = report_data.get("final_choice", "Not recorded")
    recommendation = report_data.get("recommendation", "No recommendation yet")
    score = report_data.get("overall_score_display", "—")
    return f"{recommendation} · Final call: {choice} · Overall score: {score}"


def build_executive_summary_text(report_data: dict) -> str:
    recommendation = report_data.get("recommendation", "No recommendation yet")
    final_choice = report_data.get("final_choice", "Not recorded")
    top_risk = report_data.get("top_risk", "Not enough evidence yet")
    top_strength = report_data.get("top_strength", "No clear strength identified yet")
    concept = report_data.get("franchise_name") or "the opportunity"

    return (
        f"PressureTest currently reads {concept} as {recommendation.lower()}. "
        f"The recorded final call is {final_choice.lower()}. "
        f"The main reason to keep leaning in is {top_strength.lower()}. "
        f"The main reason to stay cautious is {top_risk.lower()}. "
        f"This report should be used as a structured decision memo, not as a guarantee of outcome. "
        f"The goal is to make the next move clearer, identify the conditions that still matter, "
        f"and reduce the odds of committing on weak assumptions."
    )


def build_profile_lines(report_data: dict) -> list[str]:
    return [
        f"Client: {report_data.get('full_name') or '—'}",
        f"Email: {report_data.get('email') or '—'}",
        f"Location: {report_data.get('city_state') or '—'}",
        f"Concept: {report_data.get('franchise_name') or '—'}",
        f"Units considered: {report_data.get('units_considered') or '—'}",
        f"Ownership style: {report_data.get('ownership_style') or '—'}",
    ]


def build_strength_lines(report_data: dict) -> list[str]:
    strengths = list(report_data.get("strengths", []))
    return strengths or ["No clear strengths have been captured yet."]


def build_risk_lines(report_data: dict) -> list[str]:
    risks = list(report_data.get("risks", []))
    return risks or ["No major risks have been captured yet."]


def build_condition_lines(report_data: dict) -> list[str]:
    conditions = list(report_data.get("conditions", []))
    return conditions or ["No explicit proceed conditions have been recorded yet."]


def build_score_lines(report_data: dict) -> list[str]:
    lines: list[str] = []
    for label, item in report_data.get("scores", {}).items():
        lines.append(f"{label}: {item.get('display', '—')}")
    lines.append(f"Overall: {report_data.get('overall_score_display', '—')}")
    return lines


def build_stress_test_report_text(pressure_test_result: dict) -> str:
    packet = build_decision_packet()
    lines = [
        "PressureTest — Deal Stress Test Report",
        "",
        f"Master verdict: {packet.get('master_verdict', 'Not available')}",
        f"Decision action: {packet.get('decision_action') or 'Not locked'}",
        "",
        "Top risk flags:",
    ]
    lines.extend([f"- {flag}" for flag in packet.get("risk_flags", [])] or ["- No major risk flags captured yet."])
    lines.extend(
        [
            "",
            "Pressure test output:",
            f"- Stressed revenue: ${pressure_test_result['stressed_revenue']:,.0f}",
            f"- Stressed margin: {pressure_test_result['stressed_margin_pct'] * 100:.1f}%",
            f"- Stressed buildout: ${pressure_test_result['stressed_buildout']:,.0f}",
            f"- Annual cash after fixed costs: ${pressure_test_result['annual_cash_after_fixed']:,.0f}",
            f"- Ending cash: ${pressure_test_result['ending_cash']:,.0f}",
            f"- What breaks first: {pressure_test_result['breaks_first']}",
        ]
    )
    return "\n".join(lines)
<<<<<<< HEAD

# Compatibility helpers for PDF report engine
def money(value):
    try:
        return "${:,.0f}".format(float(value or 0))
    except Exception:
        return "$0"

def pct(value):
    try:
        return "{:.1f}%".format(float(value or 0))
    except Exception:
        return "0.0%"

def number(value):
    try:
        return "{:,.0f}".format(float(value or 0))
    except Exception:
        return "0"

# More compatibility helpers for PDF report engine
def safe_text(value, fallback="Not provided"):
    if value is None:
        return fallback
    text = str(value).strip()
    return text if text else fallback

def safe_list(value):
    if value is None:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, tuple):
        return list(value)
    return [value]

def score_label(score):
    try:
        score = float(score or 0)
    except Exception:
        score = 0
    if score >= 80:
        return "Strong"
    if score >= 60:
        return "Moderate"
    if score >= 40:
        return "Needs Review"
    return "High Pressure"

def risk_label(value):
    text = str(value or "").strip()
    return text if text else "Review Needed"

# Compatibility collector for current UI/report modules
def collect_report_data():
    try:
        import streamlit as st
        state = dict(st.session_state)
    except Exception:
        state = {}

    def pick(*keys, default=None):
        for key in keys:
            value = state.get(key)
            if value not in (None, "", [], {}):
                return value
        return default

    return {
        "operator_name": pick("operator_name", "name", default="Operator"),
        "business_name": pick("business_name", "concept_name", "franchise_name", default="Opportunity"),
        "industry": pick("industry", "business_category", default="Not provided"),
        "investment_range": pick("investment_range", "total_investment", default="Not provided"),
        "fit_score": pick("fit_score", "pressure_score", "overall_score", default=0),
        "risk_level": pick("risk_level", "pressure_level", default="Review Needed"),
        "summary": pick("summary", "executive_summary", default="This report summarizes the current diligence inputs and pressure points identified so far."),
        "pressure_points": pick("pressure_points", "risks", "top_risks", default=[]),
        "next_steps": pick("next_steps", "recommendations", default=[]),
        "assumptions": state,
    }

def get_report_data():
    return collect_report_data()

def build_report_data():
    return collect_report_data()

def build_executive_summary(data=None):
    data = data or collect_report_data()
    return data.get("summary", "This report summarizes the current diligence review.")

def build_pressure_points(data=None):
    data = data or collect_report_data()
    points = data.get("pressure_points") or []
    return points if isinstance(points, list) else [points]

def build_next_steps(data=None):
    data = data or collect_report_data()
    steps = data.get("next_steps") or []
    return steps if isinstance(steps, list) else [steps]

def build_assumptions_summary(data=None):
    data = data or collect_report_data()
    return data.get("assumptions", {})

def __getattr__(name):
    def fallback(*args, **kwargs):
        if "data" in name or "collect" in name:
            return collect_report_data()
        if "summary" in name:
            return build_executive_summary()
        if "point" in name or "risk" in name:
            return build_pressure_points()
        if "step" in name or "recommend" in name:
            return build_next_steps()
        if "assumption" in name:
            return build_assumptions_summary()
        return ""
    return fallback
=======
>>>>>>> fec65288cb896b4679e84e61241f185fa625e150
