# workflows/startup/financial_assumptions_ui.py

from __future__ import annotations

import streamlit as st

from workflows.startup.state import initialize_startup_state


def render_startup_financial_assumptions() -> None:
    initialize_startup_state()

    st.markdown(
        """
        <div class="pt-card">
            <div class="pt-eyebrow">Startup workflow assessment</div>
            <h1 style="margin:.2rem 0 .55rem 0;">Startup Financial Assumptions</h1>
            <p style="margin:0; line-height:1.6; color:#475569;">
                Capture basic financial assumptions for later review. These are simple inputs only; Phase 3B does not
                calculate runway, score readiness, or generate recommendations.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        st.number_input(
            "Startup cost estimate",
            min_value=0,
            step=1000,
            key="startup_cost_estimate",
        )
    with col2:
        st.number_input(
            "Monthly burn estimate",
            min_value=0,
            step=500,
            key="startup_monthly_burn_estimate",
        )
    with col3:
        st.number_input(
            "Cash available for launch/ramp",
            min_value=0,
            step=1000,
            key="startup_cash_available",
        )

    st.caption("No startup financial calculations are performed in Phase 3B.")
