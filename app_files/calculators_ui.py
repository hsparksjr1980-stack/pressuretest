from __future__ import annotations

import streamlit as st

from calculators_logic import (
    RampInputs,
    StaffingInputs,
    WorkingCapitalInputs,
    calculate_ramp,
    calculate_staffing_pressure,
    calculate_working_capital,
    money,
    pct,
)
from premium_components import esc, hero, metric_card, upgrade_strip


def _download_markdown(filename: str, title: str, lines: list[str]) -> None:
    body = "\n".join([f"# {title}", "", *lines, "", "---", "PressureTest is an educational diligence-support platform. This export is not legal, tax, accounting, financial, or investment advice."])
    st.download_button(
        "Download calculator summary",
        data=body.encode("utf-8"),
        file_name=filename,
        mime="text/markdown",
        use_container_width=True,
    )


def _render_context_note() -> None:
    st.markdown(
        """
        <div class="pt-note">
        These calculators are designed for early diligence. Use them to identify pressure points and questions to validate with qualified professionals, franchisors, lenders, landlords, accountants, and operators.
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_working_capital_calculator() -> None:
    st.markdown("### Working Capital Runway Calculator")
    st.caption("Estimate how long available cash can absorb early operating pressure before the unit stabilizes.")
    c1, c2 = st.columns(2)
    with c1:
        starting_cash = st.number_input("Available working capital", min_value=0.0, value=100000.0, step=5000.0)
        monthly_fixed = st.number_input("Monthly fixed costs", min_value=0.0, value=35000.0, step=1000.0)
        monthly_payroll = st.number_input("Monthly payroll", min_value=0.0, value=30000.0, step=1000.0)
        owner_draw = st.number_input("Monthly owner draw", min_value=0.0, value=6000.0, step=500.0)
    with c2:
        revenue = st.number_input("Expected monthly revenue during ramp", min_value=0.0, value=60000.0, step=2500.0)
        margin = st.slider("Gross margin %", min_value=5, max_value=95, value=55, step=1)
        ramp_months = st.slider("Ramp period to test", min_value=3, max_value=24, value=9, step=1)

    result = calculate_working_capital(WorkingCapitalInputs(starting_cash, monthly_fixed, monthly_payroll, owner_draw, revenue, margin, ramp_months))
    m1, m2, m3 = st.columns(3)
    with m1:
        metric_card("Monthly cash burn", money(result.monthly_cash_burn), "Estimated operating cash gap during ramp.")
    with m2:
        runway = "No burn" if result.runway_months >= 99 else f"{result.runway_months:.1f} months"
        metric_card("Runway", runway, "Approximate months before working capital is depleted.")
    with m3:
        metric_card("Suggested buffer", money(result.minimum_buffer), "Conservative buffer based on tested ramp period.")
    st.markdown(f"**Pressure level:** {result.pressure_level}")
    st.write(result.interpretation)
    _download_markdown(
        "pressuretest-working-capital-summary.md",
        "PressureTest Working Capital Summary",
        [
            f"- Monthly cash burn: {money(result.monthly_cash_burn)}",
            f"- Runway: {runway}",
            f"- Suggested buffer: {money(result.minimum_buffer)}",
            f"- Pressure level: {result.pressure_level}",
            f"- Interpretation: {result.interpretation}",
        ],
    )


def render_ramp_timeline_calculator() -> None:
    st.markdown("### Franchise Ramp Timeline Calculator")
    st.caption("Estimate how long it may take to reach a target monthly revenue level and how much cash the ramp may consume.")
    c1, c2 = st.columns(2)
    with c1:
        starting_revenue = st.number_input("Starting monthly revenue", min_value=0.0, value=25000.0, step=2500.0, key="ramp_start_rev")
        target_revenue = st.number_input("Target monthly revenue", min_value=0.0, value=100000.0, step=5000.0, key="ramp_target_rev")
        growth = st.slider("Monthly revenue growth %", min_value=0, max_value=50, value=12, step=1)
    with c2:
        fixed_costs = st.number_input("Fixed monthly costs", min_value=0.0, value=50000.0, step=2500.0, key="ramp_fixed")
        margin = st.slider("Gross margin %", min_value=5, max_value=95, value=55, step=1, key="ramp_margin")
        starting_cash = st.number_input("Available cash", min_value=0.0, value=125000.0, step=5000.0, key="ramp_cash")

    result = calculate_ramp(RampInputs(target_revenue, starting_revenue, growth, fixed_costs, margin, starting_cash))
    m1, m2, m3 = st.columns(3)
    with m1:
        metric_card("Months to target", f"{result.months_to_target}", "Capped at 60 months for sanity checking.")
    with m2:
        metric_card("Cash low point", money(result.projected_cash_low_point), "Lowest projected cash position before target is reached.")
    with m3:
        metric_card("Cash consumed", money(result.cumulative_cash_needed), "Cumulative projected operating gap during ramp.")
    st.markdown(f"**Pressure level:** {result.pressure_level}")
    st.write(result.interpretation)
    _download_markdown(
        "pressuretest-ramp-timeline-summary.md",
        "PressureTest Ramp Timeline Summary",
        [
            f"- Months to target: {result.months_to_target}",
            f"- Cash low point: {money(result.projected_cash_low_point)}",
            f"- Cash consumed: {money(result.cumulative_cash_needed)}",
            f"- Pressure level: {result.pressure_level}",
            f"- Interpretation: {result.interpretation}",
        ],
    )


def render_staffing_pressure_calculator() -> None:
    st.markdown("### Staffing Cost Pressure Calculator")
    st.caption("Estimate whether staffing assumptions are likely to create margin pressure at a given revenue level.")
    c1, c2 = st.columns(2)
    with c1:
        hourly_rate = st.number_input("Average hourly wage", min_value=0.0, value=17.0, step=0.5)
        weekly_hours = st.number_input("Weekly hours per employee", min_value=0.0, value=32.0, step=1.0)
        employees = st.number_input("Hourly employee count", min_value=0, value=8, step=1)
        load = st.slider("Payroll tax / benefits load %", min_value=0, max_value=50, value=14, step=1)
    with c2:
        manager_salary = st.number_input("Monthly manager salary", min_value=0.0, value=5500.0, step=250.0)
        revenue = st.number_input("Expected monthly revenue", min_value=0.0, value=90000.0, step=2500.0, key="staff_rev")
        labor_target = st.slider("Target labor cost % of revenue", min_value=5, max_value=60, value=30, step=1)

    result = calculate_staffing_pressure(StaffingInputs(hourly_rate, weekly_hours, int(employees), load, manager_salary, revenue, labor_target))
    m1, m2, m3 = st.columns(3)
    with m1:
        metric_card("Monthly staff cost", money(result.monthly_staff_cost), "Hourly labor, payroll load, and manager salary.")
    with m2:
        metric_card("Labor % of revenue", pct(result.labor_pct_of_revenue), "Compared against target labor percentage.")
    with m3:
        gap_label = money(result.monthly_gap) if result.monthly_gap >= 0 else f"({money(abs(result.monthly_gap))})"
        metric_card("Monthly target gap", gap_label, "Positive means labor is above target.")
    st.markdown(f"**Pressure level:** {result.pressure_level}")
    st.write(result.interpretation)
    _download_markdown(
        "pressuretest-staffing-pressure-summary.md",
        "PressureTest Staffing Pressure Summary",
        [
            f"- Monthly staff cost: {money(result.monthly_staff_cost)}",
            f"- Labor percent of revenue: {pct(result.labor_pct_of_revenue)}",
            f"- Target labor cost: {money(result.target_labor_cost)}",
            f"- Monthly target gap: {money(result.monthly_gap)}",
            f"- Pressure level: {result.pressure_level}",
            f"- Interpretation: {result.interpretation}",
        ],
    )


def render_calculators() -> None:
    hero(
        "Franchise Diligence Calculators",
        "Use the first calculator cluster to test working capital, ramp timing, and staffing pressure before treating the opportunity as financeable or operationally ready.",
        "Free diligence tools",
    )
    _render_context_note()
    tab1, tab2, tab3 = st.tabs(["Working capital", "Ramp timeline", "Staffing pressure"])
    with tab1:
        render_working_capital_calculator()
    with tab2:
        render_ramp_timeline_calculator()
    with tab3:
        render_staffing_pressure_calculator()

    upgrade_strip(
        "Pro turns calculator results into an execution workspace.",
        "Free calculators surface pressure points. Pro is positioned for scenario comparison, saved assumptions, lender-ready exports, and execution tracking once the user is ready to manage the actual deal.",
    )
