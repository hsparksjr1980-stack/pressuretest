# workflows/startup/overview_ui.py

from __future__ import annotations

import streamlit as st

from workflows.startup.state import initialize_startup_state


def render_startup_overview() -> None:
    initialize_startup_state()

    st.markdown(
        """
        <div class="pt-card">
            <div class="pt-eyebrow">Startup workflow assessment</div>
            <h1 style="margin:.2rem 0 .55rem 0;">Startup Overview</h1>
            <p style="margin:0; line-height:1.6; color:#475569;">
                Capture the basic startup concept and operating role. These answers are saved in session state and
                will carry across the startup workflow pages.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.text_area(
        "What problem or customer need does this startup address?",
        key="startup_concept_problem",
        placeholder="Describe the problem, customer pain, or unmet need.",
        height=120,
    )
    st.text_area(
        "Who is the target customer?",
        key="startup_target_customer",
        placeholder="Describe the customer segment, buyer, user, or market niche.",
        height=100,
    )
    st.selectbox(
        "Founder/operator involvement",
        [
            "",
            "Full-time operator",
            "Part-time operator",
            "Investor/oversight role",
            "Still undecided",
        ],
        key="startup_founder_operator_involvement",
    )
