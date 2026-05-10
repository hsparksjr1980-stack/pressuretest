# workflows/startup/overview_ui.py

from __future__ import annotations

import streamlit as st


def render_startup_overview() -> None:
    st.markdown(
        """
        <div class="pt-card">
            <div class="pt-eyebrow">Startup workflow MVP shell</div>
            <h1 style="margin:.2rem 0 .55rem 0;">Startup Overview</h1>
            <p style="margin:0; line-height:1.6; color:#475569;">
                This workflow path is being staged for new business and startup diligence. Phase 3A adds the
                startup navigation shell only. Startup questions, scoring, financial calculations, and readiness
                reports will be added in later Phase 3 steps.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.info("Next planned step: add startup assessment questions and session state in Phase 3B.")
