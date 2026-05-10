# workflows/startup/concept_validation_ui.py

from __future__ import annotations

import streamlit as st


def render_startup_concept_validation() -> None:
    st.markdown(
        """
        <div class="pt-card">
            <div class="pt-eyebrow">Startup workflow MVP shell</div>
            <h1 style="margin:.2rem 0 .55rem 0;">Startup Concept Validation</h1>
            <p style="margin:0; line-height:1.6; color:#475569;">
                This page will capture the problem, target customer, need intensity, and early validation evidence.
                Phase 3A only establishes the workflow shell; assessment questions will be added in Phase 3B.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.info("No startup scoring is active yet.")
