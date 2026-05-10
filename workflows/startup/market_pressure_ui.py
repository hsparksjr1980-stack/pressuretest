# workflows/startup/market_pressure_ui.py

from __future__ import annotations

import streamlit as st

from workflows.startup.state import initialize_startup_state


def _section_intro(title: str, body: str) -> None:
    st.markdown(
        f"""
        <div class="pt-card" style="margin:.5rem 0 1rem 0;">
            <div class="pt-eyebrow">Market pressure</div>
            <h2 style="margin:.15rem 0 .45rem 0;">{title}</h2>
            <p style="margin:0; line-height:1.6; color:#475569;">{body}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_startup_market_pressure_test() -> None:
    initialize_startup_state()

    st.markdown(
        """
        <div class="pt-card" style="background:#0B1730; color:#F8FAFC; padding:1.35rem 1.45rem; margin:.4rem 0 1rem 0;">
            <div class="pt-eyebrow" style="color:#CBD5E1;">Startup workflow assessment</div>
            <h1 style="margin:.2rem 0 .55rem 0; color:#F8FAFC; line-height:1.1;">Startup Market Pressure Test</h1>
            <p style="max-width:860px; margin:0; color:#E2E8F0; line-height:1.6; font-size:1rem;">
                Review how customers will be reached, how the launch will be executed, and where operating pressure
                may appear before the concept has stable traction.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    _section_intro(
        "Customer acquisition and sales motion",
        "Clarify how the first customers will actually find, evaluate, and commit to the offer.",
    )

    st.text_area(
        "Customer acquisition approach",
        key="startup_customer_acquisition_approach",
        placeholder="Describe channels, outreach, referrals, partnerships, content, local sales, paid ads, or direct sales.",
        height=120,
    )

    col1, col2 = st.columns(2)
    with col1:
        st.selectbox(
            "Sales cycle expectation",
            [
                "",
                "Same day / impulse",
                "Under 2 weeks",
                "2-8 weeks",
                "More than 2 months",
                "Unknown",
            ],
            key="startup_sales_cycle",
        )
    with col2:
        st.selectbox(
            "Marketing execution readiness",
            [
                "",
                "Clear repeatable plan",
                "Several channels identified",
                "Early ideas only",
                "Mostly untested",
                "Not defined yet",
            ],
            key="startup_marketing_execution_plan",
        )

    _section_intro(
        "Operating dependencies",
        "Identify the practical dependencies that may slow launch or make early delivery harder than expected.",
    )

    col3, col4 = st.columns(2)
    with col3:
        st.selectbox(
            "Labor/staffing needs",
            [
                "",
                "Founder-only at launch",
                "Contractor support needed",
                "Part-time staff needed",
                "Full team needed early",
                "Still unclear",
            ],
            key="startup_labor_staffing_needs",
        )
    with col4:
        st.selectbox(
            "Vendor/supplier dependency",
            [
                "",
                "Low dependency",
                "Some outside vendors needed",
                "Critical supplier/platform dependency",
                "Vendor path not validated",
            ],
            key="startup_vendor_supplier_dependency",
        )

    col5, col6 = st.columns(2)
    with col5:
        st.selectbox(
            "Physical location / buildout risk",
            [
                "",
                "No physical location needed",
                "Light setup only",
                "Lease/location likely needed",
                "Buildout or permitting likely",
                "Still unclear",
            ],
            key="startup_physical_location_risk",
        )
    with col6:
        st.selectbox(
            "Legal/regulatory exposure",
            [
                "",
                "Low / standard setup",
                "Some permits or compliance review needed",
                "Material regulatory complexity possible",
                "Unknown / needs review",
            ],
            key="startup_legal_regulatory_exposure",
        )

    _section_intro(
        "Launch execution",
        "Capture the timing and complexity of getting from idea to first real operating test.",
    )

    col7, col8 = st.columns(2)
    with col7:
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
    with col8:
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

    st.text_area(
        "Launch timeline and key milestones",
        key="startup_launch_timeline",
        placeholder="Describe the next 30, 60, and 90 day milestones or the sequence needed before launch.",
        height=110,
    )

    st.caption("Inputs support startup readiness scoring only. No forecasting or professional advice is generated.")
