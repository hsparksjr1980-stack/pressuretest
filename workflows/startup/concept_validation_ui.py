# workflows/startup/concept_validation_ui.py

from __future__ import annotations

import streamlit as st

from workflows.startup.state import initialize_startup_state


def _section_intro(title: str, body: str) -> None:
    st.markdown(
        f"""
        <div class="pt-card" style="margin:.5rem 0 1rem 0;">
            <div class="pt-eyebrow">Startup validation</div>
            <h2 style="margin:.15rem 0 .45rem 0;">{title}</h2>
            <p style="margin:0; line-height:1.6; color:#475569;">{body}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_startup_concept_validation() -> None:
    initialize_startup_state()

    st.markdown(
        """
        <div class="pt-card" style="background:#0B1730; color:#F8FAFC; padding:1.35rem 1.45rem; margin:.4rem 0 1rem 0;">
            <div class="pt-eyebrow" style="color:#CBD5E1;">Startup workflow assessment</div>
            <h1 style="margin:.2rem 0 .55rem 0; color:#F8FAFC; line-height:1.1;">Startup Concept Validation</h1>
            <p style="max-width:860px; margin:0; color:#E2E8F0; line-height:1.6; font-size:1rem;">
                Pressure-test whether the customer problem, demand evidence, alternatives, and pricing assumptions
                are specific enough to support the next validation step.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    _section_intro(
        "Demand evidence",
        "Separate a promising idea from evidence that customers may actually change behavior, spend time, or pay.",
    )

    st.text_area(
        "What evidence suggests this problem matters enough for customers to act?",
        key="startup_market_demand_signal",
        placeholder="Examples: customer conversations, preorders, waitlist interest, inbound demand, manual sales, usage data.",
        height=120,
    )
    st.selectbox(
        "Demand validation method",
        [
            "",
            "Customer interviews only",
            "Waitlist or signups",
            "Preorders or paid pilot",
            "Active usage or repeat demand",
            "Not validated yet",
        ],
        key="startup_demand_validation_method",
    )

    _section_intro(
        "Competition and alternatives",
        "Clarify what customers do today. A startup usually competes with existing habits, manual workarounds, or doing nothing.",
    )

    st.text_area(
        "What alternatives or competitors does the customer use today?",
        key="startup_competition_alternatives",
        placeholder="Describe competitors, substitutes, manual workarounds, internal tools, or the status quo.",
        height=110,
    )

    _section_intro(
        "Pricing validation",
        "Document the pricing assumption and whether any real customer has reacted to it.",
    )

    st.text_area(
        "What pricing assumptions are you currently using?",
        key="startup_pricing_assumptions",
        placeholder="Describe price point, pricing model, expected willingness to pay, or early pricing tests.",
        height=110,
    )
    st.selectbox(
        "Pricing validation status",
        [
            "",
            "No pricing tested yet",
            "Customer feedback only",
            "Verbal willingness to pay",
            "Paid test or deposit",
            "Repeat paid behavior",
        ],
        key="startup_pricing_validation",
    )

    st.text_area(
        "Top risks or open questions for the concept",
        key="startup_top_risks_open_questions",
        placeholder="List the biggest unknowns that still need validation.",
        height=120,
    )

    st.caption("Inputs support startup readiness scoring only. No investment or professional advice is generated.")
