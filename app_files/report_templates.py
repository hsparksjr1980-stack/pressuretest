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
