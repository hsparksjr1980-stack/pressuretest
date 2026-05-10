# report_templates.py

from __future__ import annotations

from datetime import datetime
from typing import Any



def safe_text(value: Any, fallback: str = "-") -> str:
    if value is None:
        return fallback
    text = str(value).strip()
    return text if text else fallback


def safe_score(value: Any) -> str:
    if value is None:
        return "-"
    try:
        return f"{float(value):.1f}"
    except Exception:
        return safe_text(value)


def score_value(value: Any) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except Exception:
        return None


def money(value: Any) -> str:
    try:
        return f"${float(value):,.0f}"
    except Exception:
        return "-"


def pct(value: Any) -> str:
    try:
        return f"{float(value):,.1f}%"
    except Exception:
        return "-"


def parse_conditions(raw: str | None) -> list[str]:
    if not raw:
        return []
    return [line.strip("-• ").strip() for line in str(raw).splitlines() if line.strip()]


def derive_final_choice() -> str:
    import streamlit as st

    explicit = st.session_state.get("final_decision_choice")
    if explicit:
        return safe_text(explicit)
    if st.session_state.get("move_forward", False):
        return "Proceed"
    if st.session_state.get("walk_away", False):
        return "Do Not Proceed"
    return "Not recorded"


def build_decision_headline(report_data: dict) -> str:
    choice = report_data.get("final_choice", "Not recorded")
    recommendation = report_data.get("recommendation", "No recommendation yet")
    score = report_data.get("overall_score_display", "-")
    return f"{recommendation} | Final call: {choice} | Overall score: {score}"


def build_executive_summary_text(report_data: dict) -> str:
    recommendation = safe_text(report_data.get("recommendation"), "No recommendation yet")
    final_choice = safe_text(report_data.get("final_choice"), "Not recorded")
    top_risk = safe_text(report_data.get("top_risk"), "not enough evidence yet")
    top_strength = safe_text(report_data.get("top_strength"), "no clear strength identified yet")
    concept = safe_text(report_data.get("franchise_name"), "the opportunity")

    return (
        f"PressureTest currently reads {concept} as: {recommendation}. "
        f"The recorded decision posture is: {final_choice}. "
        f"The strongest current support is: {top_strength}. "
        f"The most important unresolved pressure point is: {top_risk}. "
        "This document is an educational diligence summary, not legal, financial, tax, accounting, or investment advice. "
        "Use it to organize questions, validate assumptions independently, and prepare next-step discussions with qualified professionals."
    )


def build_profile_lines(report_data: dict) -> list[str]:
    return [
        f"Client: {safe_text(report_data.get('full_name'))}",
        f"Email: {safe_text(report_data.get('email'))}",
        f"Location: {safe_text(report_data.get('city_state'))}",
        f"Concept: {safe_text(report_data.get('franchise_name'))}",
        f"Units considered: {safe_text(report_data.get('units_considered'))}",
        f"Ownership style: {safe_text(report_data.get('ownership_style'))}",
    ]


def build_strength_lines(report_data: dict) -> list[str]:
    strengths = [safe_text(x) for x in report_data.get("strengths", []) if safe_text(x) != "-"]
    return strengths or ["No clear strengths have been captured yet."]


def build_risk_lines(report_data: dict) -> list[str]:
    risks = [safe_text(x) for x in report_data.get("risks", []) if safe_text(x) != "-"]
    return risks or ["No major risks have been captured yet."]


def build_condition_lines(report_data: dict) -> list[str]:
    conditions = [safe_text(x) for x in report_data.get("conditions", []) if safe_text(x) != "-"]
    return conditions or ["No explicit proceed conditions have been recorded yet."]


def build_score_lines(report_data: dict) -> list[str]:
    lines: list[str] = []
    for label, item in report_data.get("scores", {}).items():
        if isinstance(item, dict):
            lines.append(f"{label}: {item.get('display', '-')}")
        else:
            lines.append(f"{label}: {safe_score(item)}")
    lines.append(f"Overall: {report_data.get('overall_score_display', '-')}")
    return lines


def _add_unique(target: list[str], item: Any) -> None:
    text = safe_text(item, "")
    if text and text not in target:
        target.append(text)


def _derive_strengths(packet: dict, scores: dict[str, Any]) -> list[str]:
    strengths: list[str] = []
    for item in packet.get("strengths", []) or []:
        _add_unique(strengths, item)

    score_rules = [
        ("Franchise Fit", "Personal fit and ownership readiness look directionally workable."),
        ("Brand & Territory", "Brand and territory review has enough structure to support deeper diligence."),
        ("Concept Validation", "The concept has enough evidence to remain under consideration."),
        ("Financial Model", "The current economics appear more grounded than purely aspirational."),
        ("Post-Discovery", "Discovery work has converted some unknowns into specific follow-up items."),
        ("Pressure Test", "The opportunity appears less fragile under stress than an unsupported deal."),
    ]
    for label, sentence in score_rules:
        value = score_value(scores.get(label))
        if value is not None and value >= 58:
            _add_unique(strengths, sentence)
    return strengths[:8]


def _derive_risks(packet: dict, scores: dict[str, Any]) -> list[str]:
    risks: list[str] = []
    for key in ("risk_flags", "key_risks", "risks", "conditions"):
        for item in packet.get(key, []) or []:
            _add_unique(risks, item)

    score_rules = [
        ("Franchise Fit", "Fit, time demand, downside tolerance, or operator readiness may not align with the opportunity."),
        ("Brand & Territory", "Brand or territory assumptions may still be too thin to support a confident decision."),
        ("Concept Validation", "The concept may be less durable or less differentiated than it first appears."),
        ("Financial Model", "The economics may be too thin under current assumptions or may need a larger working-capital cushion."),
        ("Post-Discovery", "Important diligence questions may remain unresolved after discovery."),
        ("Pressure Test", "The opportunity may break down when revenue, margin, buildout, or ramp assumptions are stressed."),
    ]
    for label, sentence in score_rules:
        value = score_value(scores.get(label))
        if value is not None and value < 58:
            _add_unique(risks, sentence)
    return risks[:10]


def _derive_next_steps(report_data: dict) -> list[str]:
    steps = [
        "Validate revenue, ramp, labor, occupancy, and working-capital assumptions with independent sources.",
        "Ask the franchisor or seller for evidence behind the assumptions that most affect break-even timing.",
        "Review lease, debt, buildout, and staffing obligations with qualified professionals before signing.",
        "Convert unresolved risks into specific questions, owners, due dates, and decision conditions.",
    ]
    if report_data.get("top_risk"):
        steps.insert(0, f"Resolve the top pressure point before proceeding: {report_data['top_risk']}")
    return steps[:6]


def _build_financial_snapshot() -> dict[str, str]:
    revenue = st.session_state.get("fdd_revenue") or st.session_state.get("annual_revenue") or 0
    selected_loan = st.session_state.get("selected_loan", 0)
    selected_rent = st.session_state.get("selected_rent", 0)
    selected_nnn = st.session_state.get("selected_nnn", 0)
    su_gap = st.session_state.get("su_gap", 0)
    lowest_cash = st.session_state.get("deal_model_lowest_cash")
    break_even = st.session_state.get("deal_model_break_even_month")
    payback = st.session_state.get("deal_model_payback")
    dscr = st.session_state.get("deal_model_dscr")

    return {
        "Estimated revenue input": money(revenue),
        "Selected loan amount": money(selected_loan),
        "Monthly rent + NNN": money(float(selected_rent or 0) + float(selected_nnn or 0)),
        "Sources / uses gap": money(su_gap),
        "Lowest modeled cash": money(lowest_cash),
        "Break-even month": safe_text(break_even),
        "Estimated payback": safe_text(payback),
        "Modeled DSCR": safe_text(dscr),
    }


def collect_report_data(report_type: str = "executive") -> dict[str, Any]:
    import streamlit as st
    from decision_engine import build_decision_packet

    packet = build_decision_packet()

    raw_scores = {
        "Franchise Fit": st.session_state.get("readiness_score"),
        "Brand & Territory": st.session_state.get("brand_territory_score"),
        "Concept Validation": st.session_state.get("concept_score") or st.session_state.get("concept_validation_score"),
        "Financial Model": st.session_state.get("financial_score"),
        "Post-Discovery": st.session_state.get("post_discovery_score"),
        "Pressure Test": st.session_state.get("pressure_test_score"),
    }

    overall_raw = packet.get("final_score", packet.get("weighted_score"))
    recommendation = packet.get("master_verdict", packet.get("recommendation", "Decision Summary"))

    base: dict[str, Any] = {
        "report_type": report_type,
        "report_date": datetime.now().strftime("%Y-%m-%d"),
        "full_name": st.session_state.get("full_name", ""),
        "email": st.session_state.get("email", ""),
        "city_state": st.session_state.get("city_state", ""),
        "franchise_name": st.session_state.get("franchise_name", ""),
        "units_considered": st.session_state.get("units_considered", ""),
        "ownership_style": st.session_state.get("ownership_style", ""),
        "recommendation": safe_text(recommendation, "Decision Summary"),
        "decision_action": safe_text(packet.get("decision_action"), "Not locked"),
        "final_choice": derive_final_choice(),
        "overall_score_display": safe_score(overall_raw),
        "overall_score_value": score_value(overall_raw),
        "scores": {
            label: {"display": safe_score(value), "value": score_value(value)}
            for label, value in raw_scores.items()
        },
        "premium_access": bool(st.session_state.get("premium_access", False)),
        "final_rationale": st.session_state.get("final_decision_rationale", ""),
        "financial_snapshot": _build_financial_snapshot(),
    }

    strengths = _derive_strengths(packet, raw_scores)
    risks = _derive_risks(packet, raw_scores)

    conditions: list[str] = []
    for item in parse_conditions(st.session_state.get("final_decision_conditions")):
        _add_unique(conditions, item)
    for item in packet.get("conditions", []) or []:
        _add_unique(conditions, item)

    base["strengths"] = strengths[:8]
    base["risks"] = risks[:10]
    base["conditions"] = conditions[:8]
    base["top_strength"] = strengths[0] if strengths else "No clear strength identified yet"
    base["top_risk"] = risks[0] if risks else "Not enough evidence yet"
    base["next_steps"] = _derive_next_steps(base)
    return base


def build_stress_test_report_text(pressure_test_result: dict) -> str:
    from decision_engine import build_decision_packet

    packet = build_decision_packet()
    lines = [
        "PressureTest - Deal Stress Test Report",
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
            f"- Stressed revenue: {money(pressure_test_result.get('stressed_revenue'))}",
            f"- Stressed margin: {pct(float(pressure_test_result.get('stressed_margin_pct', 0)) * 100)}",
            f"- Stressed buildout: {money(pressure_test_result.get('stressed_buildout'))}",
            f"- Annual cash after fixed costs: {money(pressure_test_result.get('annual_cash_after_fixed'))}",
            f"- Ending cash: {money(pressure_test_result.get('ending_cash'))}",
            f"- What breaks first: {safe_text(pressure_test_result.get('breaks_first'))}",
        ]
    )
    return "\n".join(lines)
