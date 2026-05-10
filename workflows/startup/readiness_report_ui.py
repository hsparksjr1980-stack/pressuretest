# workflows/startup/readiness_report_ui.py

from __future__ import annotations

import streamlit as st

from workflows.startup.state import get_startup_answer, initialize_startup_state


def _display_answer(label: str, key: str) -> None:
    value = get_startup_answer(key)
    if value in (None, ""):
        value = "Not answered yet"
    st.markdown(f"**{label}**")
    st.write(value)


def render_startup_readiness_report() -> None:
    initialize_startup_state()

    st.markdown(
        """
        <div class="pt-card">
            <div class="pt-eyebrow">Startup assessment summary</div>
            <h1 style="margin:.2rem 0 .55rem 0;">Startup Readiness Report</h1>
            <p style="margin:0; line-height:1.6; color:#475569;">
                This page summarizes the answers entered across the startup workflow. Phase 3B does not generate
                scores, calculations, recommendations, or advisory conclusions.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("Concept and customer")
    _display_answer("Problem / customer need", "startup_concept_problem")
    _display_answer("Target customer", "startup_target_customer")
    _display_answer("Founder/operator involvement", "startup_founder_operator_involvement")

    st.subheader("Validation and market pressure")
    _display_answer("Market demand signal", "startup_market_demand_signal")
    _display_answer("Pricing assumptions", "startup_pricing_assumptions")
    _display_answer("Customer acquisition approach", "startup_customer_acquisition_approach")
    _display_answer("Execution complexity", "startup_execution_complexity")
    _display_answer("Launch readiness", "startup_launch_readiness")

    st.subheader("Financial assumptions entered")
    _display_answer("Startup cost estimate", "startup_cost_estimate")
    _display_answer("Monthly burn estimate", "startup_monthly_burn_estimate")
    _display_answer("Cash available for launch/ramp", "startup_cash_available")

    st.subheader("Open questions")
    _display_answer("Top risks / open questions", "startup_top_risks_open_questions")

    st.caption("Summary only. No startup scoring, calculations, recommendations, or generated report logic is active in Phase 3B.")
