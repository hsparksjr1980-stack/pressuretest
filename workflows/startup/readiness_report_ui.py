# workflows/startup/readiness_report_ui.py

from __future__ import annotations

import streamlit as st

from workflows.startup.scoring import build_startup_scorecard
from workflows.startup.state import get_startup_answer, initialize_startup_state


def _answer_value(key: str) -> object:
    value = get_startup_answer(key)
    return "Not answered yet" if value in (None, "") else value


def _display_answer(label: str, key: str) -> None:
    st.markdown(f"**{label}**")
    st.write(_answer_value(key))


def _display_list(title: str, items: list[str], empty_text: str = "No items available yet.") -> None:
    st.subheader(title)
    if not items:
        st.caption(empty_text)
        return
    for item in items:
        st.markdown(f"- {item}")


def _section_card(title: str, body: str) -> None:
    st.markdown(
        f"""
        <div class="pt-card" style="margin:.75rem 0 1rem 0;">
            <h3 style="margin:.1rem 0 .45rem 0;">{title}</h3>
            <p style="margin:0; line-height:1.6; color:#475569;">{body}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _capital_observation() -> str:
    startup_cost = int(get_startup_answer("startup_cost_estimate") or 0)
    monthly_burn = int(get_startup_answer("startup_monthly_burn_estimate") or 0)
    cash_available = int(get_startup_answer("startup_cash_available") or 0)

    if not any([startup_cost, monthly_burn, cash_available]):
        return "Capital and burn assumptions have not been entered yet. This may require further validation before launch planning feels grounded."
    if monthly_burn <= 0:
        return "Monthly burn is not yet defined. This commonly creates pressure because runway cannot be reviewed clearly without a burn assumption."

    simple_runway = cash_available / monthly_burn
    if simple_runway >= 12:
        return "Based on the entered cash and burn assumptions, runway appears less compressed. Startup cost assumptions should still be validated against vendor quotes and launch timing."
    if simple_runway >= 6:
        return "Based on the entered cash and burn assumptions, runway appears moderate. This may still require validation against launch delays, customer ramp, and operating surprises."
    return "Based on the entered cash and burn assumptions, runway appears tight. This may indicate higher liquidity pressure and should be validated before relying on the current launch plan."


def render_startup_readiness_report() -> None:
    initialize_startup_state()
    scorecard = build_startup_scorecard()

    st.markdown(
        """
        <div class="pt-card" style="background:#0B1730; color:#F8FAFC; padding:1.35rem 1.45rem; margin:.4rem 0 1rem 0;">
            <div class="pt-eyebrow" style="color:#CBD5E1;">Startup readiness report</div>
            <h1 style="margin:.2rem 0 .55rem 0; color:#F8FAFC; line-height:1.1;">MVP readiness signal</h1>
            <p style="max-width:860px; margin:0; color:#E2E8F0; line-height:1.6; font-size:1rem;">
                This page organizes the startup answers and MVP scoring signal into a structured readiness view.
                It is not a final recommendation and does not provide legal, tax, accounting, lending, or investment advice.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("Startup Readiness Signal")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Overall signal", scorecard["overall_signal"])
    with col2:
        st.metric("MVP score", f"{scorecard['total_score']} / {scorecard['max_score']}")
    with col3:
        st.metric("Completion signal", f"{scorecard['score_percent']}%")

    _section_card(
        "How to read this signal",
        "This MVP signal reflects the completeness and relative strength of entered startup assumptions. It may indicate areas that deserve more validation, but it should not be treated as a decision, prediction, or professional advisory conclusion.",
    )

    st.subheader("Key Risk Areas")
    for item in scorecard["categories"]:
        st.markdown(f"**{item['risk_category']}** — {item['score']} / 4")
        st.caption(f"{item['detail']} This should be validated with customer, operational, and capital evidence where practical.")

    _display_list(
        "Strongest Signals",
        scorecard["strongest_signals"],
        "No stronger signals are available yet. More complete answers may clarify this section.",
    )
    _display_list(
        "Weakest Assumptions",
        scorecard["weakest_assumptions"],
        "No weak assumptions are available yet. More complete answers may clarify this section.",
    )

    st.subheader("Execution Pressure Areas")
    _section_card(
        "Execution complexity",
        f"Current input: {_answer_value('startup_execution_complexity')}. Higher complexity commonly creates pressure around launch timing, coordination, vendor dependency, and founder capacity.",
    )
    _section_card(
        "Customer acquisition pressure",
        f"Current input: {_answer_value('startup_customer_acquisition_approach')}. This may require further validation through customer interviews, small demand tests, and evidence of repeatable acquisition channels.",
    )

    st.subheader("Founder/Operator Considerations")
    _section_card(
        "Founder involvement",
        f"Current input: {_answer_value('startup_founder_operator_involvement')}. Operator involvement should be validated against the actual time, decision load, and launch coordination required by the concept.",
    )

    st.subheader("Capital & Runway Observations")
    _section_card("Capital pressure", _capital_observation())
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        _display_answer("Startup cost estimate", "startup_cost_estimate")
    with col_b:
        _display_answer("Monthly burn estimate", "startup_monthly_burn_estimate")
    with col_c:
        _display_answer("Cash available", "startup_cash_available")

    _display_list("Questions to Validate Next", scorecard["next_validation_questions"])

    st.subheader("Next Validation Steps")
    validation_steps = [
        "Interview target customers to confirm the problem is urgent enough to act on.",
        "Test pricing assumptions with real customer conversations or small paid experiments.",
        "Run a demand test before assuming repeatable acquisition.",
        "Validate launch assumptions against vendor timelines, founder capacity, and operating bottlenecks.",
        "Review customer acquisition cost assumptions before scaling spend.",
        "Pressure-test runway sufficiency against delays and slower-than-expected revenue ramp.",
        "Identify operational bottlenecks that could block launch or early delivery quality.",
    ]
    for step in validation_steps:
        st.markdown(f"- {step}")

    st.subheader("Final Readiness Summary")
    _section_card(
        "Operator-focused summary",
        f"Current startup signal: {scorecard['overall_signal']}. The strongest areas may provide a useful foundation, while the weakest assumptions may require further validation before the concept is treated as operationally ready. This summary is intentionally cautious and based only on the answers entered in the startup workflow.",
    )

    st.markdown("---")
    with st.expander("Entered answers"):
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

        st.markdown("### Open questions")
        _display_answer("Top risks / open questions", "startup_top_risks_open_questions")

    st.caption("No advanced financial model, forecasting engine, PDF/export system, or generated investment recommendation is active in Phase 3D.")
