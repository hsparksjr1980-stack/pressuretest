# workflows/startup/readiness_report_ui.py

from __future__ import annotations

import streamlit as st


def render_startup_readiness_report() -> None:
    st.markdown(
        """
        <div class="pt-card">
            <div class="pt-eyebrow">Startup workflow MVP shell</div>
            <h1 style="margin:.2rem 0 .55rem 0;">Startup Readiness Report</h1>
            <p style="margin:0; line-height:1.6; color:#475569;">
                This page is a placeholder for the future startup readiness output. Phase 3A only creates the
                routed page shell. No startup scoring, calculations, report generation, or recommendations are active.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.info("Startup readiness reporting is planned for a later Phase 3 step.")
