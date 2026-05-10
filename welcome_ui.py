from __future__ import annotations

import streamlit as st

from branding import APP_PRODUCT, APP_TAGLINE
from shared_ui import render_brand_header, render_pressuretest_boundary_notice


def _info_card(label: str, title: str, body: str) -> None:
    st.markdown(
        f"""
        <div class="pt-card" style="height:100%;">
            <div class="pt-eyebrow">{label}</div>
            <h3 style="margin:.2rem 0 .4rem 0;">{title}</h3>
            <p style="margin:0; line-height:1.55; color:#475569;">{body}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _start_assessment() -> None:
    st.session_state["auth_complete"] = True
    st.session_state["profile_complete"] = False
    st.session_state["assessment_started"] = True
    st.session_state["current_page"] = "Overview"
    st.rerun()


def render_welcome() -> None:
    render_brand_header(APP_PRODUCT, APP_TAGLINE)
    render_pressuretest_boundary_notice(compact=True)

    st.markdown(
        """
        <div class="pt-card" style="background:#0B1730; color:#F8FAFC; padding:1.35rem 1.45rem; margin:.4rem 0 1rem 0;">
            <div class="pt-eyebrow" style="color:#CBD5E1;">Franchise diligence workspace</div>
            <h1 style="margin:.2rem 0 .55rem 0; color:#F8FAFC; line-height:1.1;">Pressure-test the opportunity before you commit.</h1>
            <p style="max-width:820px; margin:0; color:#E2E8F0; line-height:1.6; font-size:1rem;">
                Build a quick operating profile, identify the next diligence step, and start a structured review of fit,
                concept risk, economics, and execution pressure.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3, gap="large")
    with c1:
        _info_card(
            "Step 1",
            "Create a quick profile",
            "Capture the concept, market, ownership role, and commitment status so the workflow starts with context.",
        )
    with c2:
        _info_card(
            "Step 2",
            "Run the pressure snapshot",
            "Start with operator fit and early assumptions before going deeper into concept validation and economics.",
        )
    with c3:
        _info_card(
            "Step 3",
            "Build a usable report",
            "Turn answers into a decision summary, open questions, and next steps you can review with advisors.",
        )

    st.markdown("<div style='height:.5rem;'></div>", unsafe_allow_html=True)

    left, right = st.columns([1.2, .8], gap="large")
    with left:
        if st.button("Start assessment", type="primary", use_container_width=True, key="welcome_start_assessment"):
            _start_assessment()
        st.caption("No recommendation, guarantee, or legal/financial advice. This is a structured diligence workflow.")

    with right:
        if st.button("Continue saved session", use_container_width=True, key="welcome_continue_saved"):
            st.session_state["auth_complete"] = True
            st.session_state["profile_complete"] = True
            st.session_state.setdefault("current_page", "Overview")
            st.rerun()
        st.caption("Use this only after importing or resuming saved local progress.")
