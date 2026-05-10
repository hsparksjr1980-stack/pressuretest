# workflows/startup/state.py

from __future__ import annotations

from typing import Final

import streamlit as st


STARTUP_STATE_DEFAULTS: Final[dict[str, object]] = {
    "startup_concept_problem": "",
    "startup_target_customer": "",
    "startup_market_demand_signal": "",
    "startup_pricing_assumptions": "",
    "startup_cost_estimate": 0,
    "startup_monthly_burn_estimate": 0,
    "startup_cash_available": 0,
    "startup_customer_acquisition_approach": "",
    "startup_founder_operator_involvement": "",
    "startup_execution_complexity": "",
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
