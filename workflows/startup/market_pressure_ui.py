# workflows/startup/market_pressure_ui.py

from __future__ import annotations

import streamlit as st

from workflows.startup.state import initialize_startup_state


def render_startup_market_pressure_test() -> None:
    initialize_startup_state()

    st.markdown(
        """
        <div class="pt-card">
            <div class="pt-eyebrow">Startup workflow assessment</div>
            <h1 style="margin:.2rem 0 .55rem 0;">Startup Market Pressure Test</h1>
            <p style="margin:0; line-height:1.6; color:#475569;">
                Capture how you plan to reach customers and how complex the early execution path looks. These inputs
                are stored only in startup-specific session state.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.text_area(
        "Customer acquisition approach",
        key="startup_customer_acquisition_approach",
        placeholder="Describe how customers will find, evaluate, and buy from the business.",
        height=120,
    )
    st.selectbox(
        "Execution complexity",
        [
            "",
            "Low - few moving parts",
            "Moderate - some operating complexity",
            "High - many dependencies or unknowns",
            "Very high - complex launch path",
        ],
        key="startup_execution_complexity",
    )
    st.selectbox(
        "Launch readiness",
        [
            "",
            "Idea only",
            "Early validation started",
            "Prototype or offer drafted",
            "Ready for first customers",
            "Already launched",
        ],
        key="startup_launch_readiness",
    )

    st.caption("No startup scoring or recommendations are generated in Phase 3B.")
