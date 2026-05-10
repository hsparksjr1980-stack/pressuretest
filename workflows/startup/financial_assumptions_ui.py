# workflows/startup/financial_assumptions_ui.py

from __future__ import annotations

import streamlit as st


def render_startup_financial_assumptions() -> None:
    st.markdown(
        """
        <div class="pt-card">
            <div class="pt-eyebrow">Startup workflow MVP shell</div>
            <h1 style="margin:.2rem 0 .55rem 0;">Startup Financial Assumptions</h1>
            <p style="margin:0; line-height:1.6; color:#475569;">
                This page will later capture startup cost, monthly burn, runway, pricing, and customer acquisition
                assumptions. Phase 3A only provides the routed page shell. No calculations are active yet.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.info("Financial assumption questions and calculations are planned for later Phase 3 steps.")
