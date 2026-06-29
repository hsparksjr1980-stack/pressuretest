from __future__ import annotations

import streamlit as st

from branding import APP_PRODUCT
from franchise_beta import render_beta_styles, render_depth_toggle
from shared_ui import render_brand_header, render_pressuretest_boundary_notice
from workflow_config import DEFAULT_WORKFLOW


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
    st.session_state["workflow_type"] = DEFAULT_WORKFLOW
    st.session_state["current_page"] = "Start Here"
    st.rerun()


def render_welcome() -> None:
    render_beta_styles()
    render_brand_header(APP_PRODUCT, "PressureTest: Franchise")
    render_pressuretest_boundary_notice(compact=True)

    st.markdown(
        """
        <div class="pt-hero">
            <div class="rc-eyebrow" style="color:#FCD34D;">PressureTest: Franchise</div>
            <h1>Stress-test a franchise before you invest.</h1>
            <p>
                A caution-first decision workflow that helps you identify missing evidence,
                material risk, and the questions to ask before you sign, borrow, lease, or invest.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    render_depth_toggle()

    st.markdown(
        """
        <div class="pt-mini-grid">
            <div class="pt-mini-card"><strong>Decision-Critical Issues</strong><span>The few issues most likely to change the decision or trigger a pause.</span></div>
            <div class="pt-mini-card"><strong>FDD Translation Risk</strong><span>Whether system-wide information actually fits your market, costs, and financing pressure.</span></div>
            <div class="pt-mini-card"><strong>Shareable report</strong><span>A guided decision memo you can review with a spouse, lender, CPA, attorney, or partner.</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3, gap="large")
    with c1:
        _info_card(
            "What you'll get",
            "A first-pass risk read",
            "Quick Assessment focuses on the core questions most likely to reveal missing evidence or decision pressure.",
        )
    with c2:
        _info_card(
            "What you'll get",
            "A deeper diligence path",
            "Full Review opens Go Deeper sections without creating a second workflow or losing your answers.",
        )
    with c3:
        _info_card(
            "What you'll get",
            "A decision memo",
            "The report leads with recommendation, Decision-Critical Issues, risk labels, missing evidence, and next steps.",
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
            st.session_state["workflow_type"] = DEFAULT_WORKFLOW
            st.session_state.setdefault("current_page", "Start Here")
            st.rerun()
        st.caption("Use this only after importing or resuming saved local progress.")
