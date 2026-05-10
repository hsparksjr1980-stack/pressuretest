# workflows/startup/concept_validation_ui.py

from __future__ import annotations

import streamlit as st

from workflows.startup.state import initialize_startup_state


def render_startup_concept_validation() -> None:
    initialize_startup_state()

    st.markdown(
        """
        <div class="pt-card">
            <div class="pt-eyebrow">Startup workflow assessment</div>
            <h1 style="margin:.2rem 0 .55rem 0;">Startup Concept Validation</h1>
            <p style="margin:0; line-height:1.6; color:#475569;">
                Capture early evidence around the customer problem, demand signal, pricing logic, and open questions.
                These inputs are saved in session state only.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.text_area(
        "What evidence suggests this problem matters enough for customers to act?",
        key="startup_market_demand_signal",
        placeholder="Examples: customer conversations, preorders, waitlist interest, inbound demand, manual sales, usage data.",
        height=120,
    )
    st.text_area(
        "What pricing assumptions are you currently using?",
        key="startup_pricing_assumptions",
        placeholder="Describe price point, pricing model, expected willingness to pay, or early pricing tests.",
        height=110,
    )
    st.text_area(
        "Top risks or open questions for the concept",
        key="startup_top_risks_open_questions",
        placeholder="List the biggest unknowns that still need validation.",
        height=120,
    )

    st.caption("No startup scoring or recommendations are generated in Phase 3B.")
