# workflows/startup/state.py

from __future__ import annotations

from typing import Final

import streamlit as st


STARTUP_STATE_DEFAULTS: Final[dict[str, object]] = {
    "startup_concept_problem": "",
    "startup_target_customer": "",
    "startup_target_customer_clarity": "",
    "startup_customer_urgency": "",
    "startup_market_demand_signal": "",
    "startup_demand_validation_method": "",
    "startup_competition_alternatives": "",
    "startup_pricing_assumptions": "",
    "startup_pricing_validation": "",
    "startup_sales_cycle": "",
    "startup_cost_estimate": 0,
    "startup_monthly_burn_estimate": 0,
    "startup_cash_available": 0,
    "startup_runway_months": 0,
    "startup_revenue_ramp_assumptions": "",
    "startup_pricing_confidence": "",
    "startup_gross_margin_assumptions": "",
    "startup_owner_salary_expectations": "",
    "startup_debt_payment_obligations": "",
    "startup_slow_ramp_plan": "",
    "startup_customer_acquisition_approach": "",
    "startup_marketing_execution_plan": "",
    "startup_founder_operator_involvement": "",
    "startup_founder_time_commitment": "",
    "startup_labor_staffing_needs": "",
    "startup_vendor_supplier_dependency": "",
    "startup_physical_location_risk": "",
    "startup_legal_regulatory_exposure": "",
    "startup_execution_complexity": "",
    "startup_launch_timeline": "",
    "startup_launch_readiness": "",
    "startup_top_risks_open_questions": "",
}


def initialize_startup_state() -> None:
    """Initialize startup-only session-state keys without touching franchise state."""
    for key, default_value in STARTUP_STATE_DEFAULTS.items():
        st.session_state.setdefault(key, default_value)


def get_startup_answer(key: str) -> object:
    initialize_startup_state()
    return st.session_state.get(key, STARTUP_STATE_DEFAULTS.get(key, ""))
