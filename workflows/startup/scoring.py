# workflows/startup/scoring.py

from __future__ import annotations

from typing import Any, Final

from risk_taxonomy import get_risk_label
from workflows.startup.state import get_startup_answer, initialize_startup_state


STARTUP_SIGNAL_STRONGER: Final[str] = "Stronger foundation"
STARTUP_SIGNAL_NEEDS_VALIDATION: Final[str] = "Needs validation"
STARTUP_SIGNAL_HIGH_PRESSURE: Final[str] = "High pressure / high uncertainty"


def _text_present(key: str) -> bool:
    value = get_startup_answer(key)
    return isinstance(value, str) and bool(value.strip())


def _numeric_value(key: str) -> int:
    value = get_startup_answer(key)
    try:
        return int(value or 0)
    except (TypeError, ValueError):
        return 0


def _score_liquidity() -> tuple[int, str, str]:
    startup_cost = _numeric_value("startup_cost_estimate")
    monthly_burn = _numeric_value("startup_monthly_burn_estimate")
    cash_available = _numeric_value("startup_cash_available")

    if not any([startup_cost, monthly_burn, cash_available]):
        return 1, get_risk_label("liquidity_risk"), "Cash, startup cost, and burn assumptions have not been entered yet."

    if monthly_burn <= 0:
        return 2, get_risk_label("liquidity_risk"), "Monthly burn is not defined, so runway pressure is still unclear."

    months_of_burn = cash_available / monthly_burn if monthly_burn else 0
    if months_of_burn >= 12:
        return 4, get_risk_label("liquidity_risk"), "Cash entered appears to cover at least 12 months of stated burn."
    if months_of_burn >= 6:
        return 3, get_risk_label("liquidity_risk"), "Cash entered appears to cover 6 to 12 months of stated burn."
    return 1, get_risk_label("liquidity_risk"), "Cash entered appears to cover less than 6 months of stated burn."


def _score_text_signal(key: str, risk_key: str, positive_detail: str, missing_detail: str) -> tuple[int, str, str]:
    if _text_present(key):
        return 3, get_risk_label(risk_key), positive_detail
    return 1, get_risk_label(risk_key), missing_detail


def _score_choice(key: str, risk_key: str, strong_values: set[str], weak_values: set[str], missing_detail: str) -> tuple[int, str, str]:
    value = str(get_startup_answer(key) or "")
    if not value:
        return 1, get_risk_label(risk_key), missing_detail
    if value in strong_values:
        return 4, get_risk_label(risk_key), f"Current answer: {value}."
    if value in weak_values:
        return 1, get_risk_label(risk_key), f"Current answer: {value}."
    return 3, get_risk_label(risk_key), f"Current answer: {value}."


def build_startup_scorecard() -> dict[str, Any]:
    """Build a simple MVP startup readiness scorecard from startup-only answers."""
    initialize_startup_state()

    categories = {
        "liquidity_runway": _score_liquidity(),
        "market_validation": _score_text_signal(
            "startup_market_demand_signal",
            "market_risk",
            "A market-demand signal has been described.",
            "Market-demand evidence has not been described yet.",
        ),
        "revenue_pricing": _score_text_signal(
            "startup_pricing_assumptions",
            "revenue_validation_risk",
            "Pricing assumptions have been documented.",
            "Pricing assumptions have not been documented yet.",
        ),
        "customer_acquisition": _score_text_signal(
            "startup_customer_acquisition_approach",
            "revenue_validation_risk",
            "A customer acquisition approach has been documented.",
            "Customer acquisition approach is still undefined.",
        ),
        "founder_operator_fit": _score_choice(
            "startup_founder_operator_involvement",
            "execution_risk",
            {"Full-time operator"},
            {"Still undecided", ""},
            "Founder/operator involvement is not defined yet.",
        ),
        "execution_complexity": _score_choice(
            "startup_execution_complexity",
            "operational_complexity",
            {"Low - few moving parts", "Moderate - some operating complexity"},
            {"High - many dependencies or unknowns", "Very high - complex launch path"},
            "Execution complexity has not been selected yet.",
        ),
        "launch_readiness": _score_choice(
            "startup_launch_readiness",
            "execution_risk",
            {"Ready for first customers", "Already launched"},
            {"Idea only", ""},
            "Launch readiness has not been selected yet.",
        ),
    }

    scored_items = [
        {"key": key, "score": score, "risk_category": risk, "detail": detail}
        for key, (score, risk, detail) in categories.items()
    ]
    total_score = sum(item["score"] for item in scored_items)
    max_score = len(scored_items) * 4
    score_percent = round((total_score / max_score) * 100) if max_score else 0

    if score_percent >= 70:
        overall_signal = STARTUP_SIGNAL_STRONGER
    elif score_percent >= 45:
        overall_signal = STARTUP_SIGNAL_NEEDS_VALIDATION
    else:
        overall_signal = STARTUP_SIGNAL_HIGH_PRESSURE

    weakest = sorted(scored_items, key=lambda item: item["score"])[:3]
    strongest = sorted(scored_items, key=lambda item: item["score"], reverse=True)[:3]

    top_risks = [f"{item['risk_category']}: {item['detail']}" for item in weakest]
    strongest_signals = [f"{item['risk_category']}: {item['detail']}" for item in strongest if item["score"] >= 3]
    weakest_assumptions = [f"{item['risk_category']}: {item['detail']}" for item in weakest]
    next_questions = [
        "What evidence would confirm that customers have urgent enough demand to act?",
        "Which pricing assumption needs the fastest real-world validation?",
        "What operating dependency could slow launch the most?",
    ]

    return {
        "overall_signal": overall_signal,
        "total_score": total_score,
        "max_score": max_score,
        "score_percent": score_percent,
        "categories": scored_items,
        "top_risks": top_risks[:3],
        "strongest_signals": strongest_signals[:3],
        "weakest_assumptions": weakest_assumptions[:3],
        "next_validation_questions": next_questions,
    }
