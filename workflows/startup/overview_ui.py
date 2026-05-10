# workflows/startup/overview_ui.py

from __future__ import annotations

import streamlit as st

from workflows.startup.state import initialize_startup_state


def _section_intro(title: str, body: str) -> None:
    st.markdown(
        f"""
        <div class="pt-card" style="margin:.5rem 0 1rem 0;">
            <div class="pt-eyebrow">Startup workflow</div>
            <h2 style="margin:.15rem 0 .45rem 0;">{title}</h2>
            <p style="margin:0; line-height:1.6; color:#475569;">{body}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_startup_overview() -> None:
    initialize_startup_state()

    st.markdown(
        """
        <div class="pt-card" style="background:#0B1730; color:#F8FAFC; padding:1.35rem 1.45rem; margin:.4rem 0 1rem 0;">
            <div class="pt-eyebrow" style="color:#CBD5E1;">Startup workflow assessment</div>
            <h1 style="margin:.2rem 0 .55rem 0; color:#F8FAFC; line-height:1.1;">Startup Overview</h1>
            <p style="max-width:860px; margin:0; color:#E2E8F0; line-height:1.6; font-size:1rem;">
                Start with the operator role, customer need, and basic concept clarity. These answers are saved in
                startup-only session state and carry across the workflow.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    _section_intro(
        "Founder/operator fit",
        "Clarify who will actually carry the early operating load and how much time the launch path may require.",
    )

    col1, col2 = st.columns(2)
    with col1:
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
    with col2:
        st.selectbox(
            "Founder time commitment",
            [
                "",
                "Less than 10 hours/week",
                "10-20 hours/week",
                "20-40 hours/week",
                "Full-time plus launch intensity",
                "Still unclear",
            ],
            key="startup_founder_time_commitment",
        )

    _section_intro(
        "Problem and customer clarity",
        "Document the customer problem in plain language and define who specifically feels it.",
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

    col3, col4 = st.columns(2)
    with col3:
        st.selectbox(
            "Target customer clarity",
            [
                "",
                "Clearly defined buyer/user",
                "Defined but broad",
                "Several possible segments",
                "Still unclear",
            ],
            key="startup_target_customer_clarity",
        )
    with col4:
        st.selectbox(
            "Customer urgency",
            [
                "",
                "High urgency / active pain",
                "Moderate urgency",
                "Low urgency / nice-to-have",
                "Not validated yet",
            ],
            key="startup_customer_urgency",
        )

    st.caption("No startup recommendations are generated from this page. Inputs support later readiness review only.")
