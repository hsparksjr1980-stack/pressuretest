# workflows/startup/financial_assumptions_ui.py

from __future__ import annotations

import streamlit as st

from workflows.startup.state import initialize_startup_state


def _section_intro(title: str, body: str) -> None:
    st.markdown(
        f"""
        <div class="pt-card" style="margin:.5rem 0 1rem 0;">
            <div class="pt-eyebrow">Financial assumptions</div>
            <h2 style="margin:.15rem 0 .45rem 0;">{title}</h2>
            <p style="margin:0; line-height:1.6; color:#475569;">{body}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_startup_financial_assumptions() -> None:
    initialize_startup_state()

    st.markdown(
        """
        <div class="pt-card" style="background:#0B1730; color:#F8FAFC; padding:1.35rem 1.45rem; margin:.4rem 0 1rem 0;">
            <div class="pt-eyebrow" style="color:#CBD5E1;">Startup workflow assessment</div>
            <h1 style="margin:.2rem 0 .55rem 0; color:#F8FAFC; line-height:1.1;">Startup Financial Assumptions</h1>
            <p style="max-width:860px; margin:0; color:#E2E8F0; line-height:1.6; font-size:1rem;">
                Capture the financial assumptions that create early startup pressure. These inputs support a simple
                MVP readiness signal only; no advanced forecasting or full financial model is generated.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    _section_intro(
        "Capital and runway",
        "Document the basic cash, cost, and burn assumptions that determine how much time the launch path may have.",
    )

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.number_input("Startup cost estimate", min_value=0, step=1000, key="startup_cost_estimate")
    with col2:
        st.number_input("Monthly burn estimate", min_value=0, step=500, key="startup_monthly_burn_estimate")
    with col3:
        st.number_input("Cash available for launch/ramp", min_value=0, step=1000, key="startup_cash_available")
    with col4:
        st.number_input("Estimated runway months", min_value=0, step=1, key="startup_runway_months")

    _section_intro(
        "Revenue and pricing assumptions",
        "Capture the early revenue logic without turning this into a full financial model.",
    )

    st.text_area(
        "Revenue ramp assumptions",
        key="startup_revenue_ramp_assumptions",
        placeholder="Describe when revenue is expected to start, what drives it, and what assumptions are still untested.",
        height=110,
    )

    col5, col6 = st.columns(2)
    with col5:
        st.selectbox(
            "Pricing confidence",
            [
                "",
                "High - tested with paying customers",
                "Moderate - validated in conversations",
                "Low - internal estimate only",
                "Not validated yet",
            ],
            key="startup_pricing_confidence",
        )
    with col6:
        st.text_area(
            "Gross margin assumptions",
            key="startup_gross_margin_assumptions",
            placeholder="Describe expected margin, cost of goods/services, delivery cost, or uncertainty around unit economics.",
            height=100,
        )

    _section_intro(
        "Owner compensation and fixed obligations",
        "Identify fixed pressure that may reduce flexibility during early ramp.",
    )

    col7, col8 = st.columns(2)
    with col7:
        st.selectbox(
            "Owner salary expectations",
            [
                "",
                "No salary needed during launch",
                "Minimal draw needed",
                "Market salary needed quickly",
                "Still unclear",
            ],
            key="startup_owner_salary_expectations",
        )
    with col8:
        st.selectbox(
            "Debt/payment obligations",
            [
                "",
                "No fixed debt/payment obligations",
                "Manageable fixed obligations",
                "Material fixed obligations",
                "Still unclear",
            ],
            key="startup_debt_payment_obligations",
        )

    st.text_area(
        "Fallback plan if revenue ramps slower than expected",
        key="startup_slow_ramp_plan",
        placeholder="Describe cost controls, extra runway, alternate income, delayed hiring, smaller launch scope, or other fallback options.",
        height=120,
    )

    st.caption("Financial inputs are used for MVP readiness review only. No advanced financial modeling, forecasting, or advisory output is generated.")
