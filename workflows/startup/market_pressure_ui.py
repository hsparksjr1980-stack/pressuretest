# workflows/startup/market_pressure_ui.py

from __future__ import annotations

import streamlit as st


def render_startup_market_pressure_test() -> None:
    st.markdown(
        """
        <div class="pt-card">
            <div class="pt-eyebrow">Startup workflow MVP shell</div>
            <h1 style="margin:.2rem 0 .55rem 0;">Startup Market Pressure Test</h1>
            <p style="margin:0; line-height:1.6; color:#475569;">
                This page will later help evaluate market demand, customer access, competition, and early revenue
                validation pressure. Phase 3A only wires the startup workflow shell and navigation path.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.info("Market pressure questions will be added in Phase 3B. No scoring is active yet.")
