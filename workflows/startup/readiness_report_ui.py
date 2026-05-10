# workflows/startup/readiness_report_ui.py

from __future__ import annotations

import streamlit as st

from workflows.startup.scoring import build_startup_scorecard
from workflows.startup.state import get_startup_answer, initialize_startup_state


def _display_answer(label: str, key: str) -> None:
    value = get_startup_answer(key)
    if value in (None, ""):
        value = "Not answered yet"
    st.markdown(f"**{label}**")
    st.write(value)


def _display_list(title: str, items: list[str]) -> None:
    st.subheader(title)
    if not items:
        st.caption("No items available yet.")
        return
    for item in items:
        st.markdown(f"- {item}")


def render_startup_readiness_report() -> None:
    initialize_startup_state()
    scorecard = build_startup_scorecard()

    st.markdown(
        """
        <div class="pt-card">
            <div class="pt-eyebrow">Startup readiness MVP signal</div>
            <h1 style="margin:.2rem 0 .55rem 0;">Startup Readiness Report</h1>
            <p style="margin:0; line-height:1.6; color:#475569;">
                This page summarizes entered startup answers and displays a simple MVP readiness signal. It is not a
                final recommendation and does not provide legal, tax, accounting, lending, or investment advice.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Overall signal", scorecard["overall_signal"])
    with col2:
        st.metric("MVP score", f"{scorecard['total_score']} / {scorecard['max_score']}")
    with col3:
        st.metric("Completion signal", f"{scorecard['score_percent']}%")

    st.caption("MVP readiness signal only. This is not a generated recommendation or advisory conclusion.")

    st.subheader("Scoring summary")
    for item in scorecard["categories"]:
        st.markdown(f"**{item['risk_category']}** — {item['score']} / 4")
        st.caption(item["detail"])

    _display_list("Top risks", scorecard["top_risks"])
    _display_list("Strongest signals", scorecard["strongest_signals"])
    _display_list("Weakest assumptions", scorecard["weakest_assumptions"])
    _display_list("Next validation questions", scorecard["next_validation_questions"])

    st.markdown("---")
    st.subheader("Entered answers")

    st.markdown("### Concept and customer")
    _display_answer("Problem / customer need", "startup_concept_problem")
    _display_answer("Target customer", "startup_target_customer")
    _display_answer("Founder/operator involvement", "startup_founder_operator_involvement")

    st.markdown("### Validation and market pressure")
    _display_answer("Market demand signal", "startup_market_demand_signal")
    _display_answer("Pricing assumptions", "startup_pricing_assumptions")
    _display_answer("Customer acquisition approach", "startup_customer_acquisition_approach")
    _display_answer("Execution complexity", "startup_execution_complexity")
    _display_answer("Launch readiness", "startup_launch_readiness")

    st.markdown("### Financial assumptions entered")
    _display_answer("Startup cost estimate", "startup_cost_estimate")
    _display_answer("Monthly burn estimate", "startup_monthly_burn_estimate")
    _display_answer("Cash available for launch/ramp", "startup_cash_available")

    st.markdown("### Open questions")
    _display_answer("Top risks / open questions", "startup_top_risks_open_questions")

    st.caption("No advanced financial model, generated investment recommendation, or professional advice logic is active in Phase 3C.")
