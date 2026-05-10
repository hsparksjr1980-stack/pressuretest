from __future__ import annotations

import streamlit as st

from branding import APP_PRODUCT, APP_TAGLINE
from shared_ui import render_brand_header, render_pressuretest_boundary_notice
from workflow_config import DEFAULT_WORKFLOW, WORKFLOW_CONFIG, get_workflow_config


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


def _render_workflow_selector() -> None:
    workflow_keys = list(WORKFLOW_CONFIG.keys())
    current_workflow = st.session_state.get("workflow_type", DEFAULT_WORKFLOW)
    if current_workflow not in WORKFLOW_CONFIG:
        current_workflow = DEFAULT_WORKFLOW

    st.markdown("<div style='height:.25rem;'></div>", unsafe_allow_html=True)
    st.markdown("### What type of opportunity are you evaluating?")
    st.caption("Choose the workflow path. Franchise is available now; other paths are staged for expansion.")

    selected_workflow = st.radio(
        "Opportunity type",
        workflow_keys,
        index=workflow_keys.index(current_workflow),
        format_func=lambda key: str(WORKFLOW_CONFIG[key]["label"]),
        horizontal=True,
        label_visibility="collapsed",
        key="welcome_workflow_selector",
    )
    st.session_state["workflow_type"] = selected_workflow

    c1, c2, c3 = st.columns(3, gap="large")
    for column, workflow_key in zip((c1, c2, c3), workflow_keys):
        config = WORKFLOW_CONFIG[workflow_key]
        selected = workflow_key == selected_workflow
        border = "rgba(249,115,22,0.38)" if selected else "rgba(17,24,39,0.08)"
        background = "rgba(249,115,22,0.06)" if selected else "#FFFFFF"
        badge_background = "rgba(249,115,22,0.12)" if selected else "rgba(100,116,139,0.10)"
        badge_color = "#C2410C" if selected else "#475569"
        with column:
            st.markdown(
                f"""
                <div class="pt-card" style="height:100%; border-color:{border}; background:{background};">
                    <div class="pt-eyebrow">Workflow</div>
                    <h3 style="margin:.2rem 0 .45rem 0;">{config['label']}</h3>
                    <p style="margin:0 0 .7rem 0; line-height:1.55; color:#475569;">{config['description']}</p>
                    <span style="
                        display:inline-block;
                        padding:.22rem .58rem;
                        border-radius:999px;
                        background:{badge_background};
                        color:{badge_color};
                        font-size:.72rem;
                        font-weight:800;
                        letter-spacing:.04em;
                        text-transform:uppercase;
                    ">{config['status']}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )


def _start_assessment() -> None:
    workflow_type = st.session_state.get("workflow_type", DEFAULT_WORKFLOW)
    workflow_config = get_workflow_config(workflow_type)

    st.session_state["auth_complete"] = True
    st.session_state["profile_complete"] = False
    st.session_state["assessment_started"] = True
    st.session_state["workflow_type"] = workflow_type if workflow_type in WORKFLOW_CONFIG else DEFAULT_WORKFLOW
    st.session_state["current_page"] = str(workflow_config.get("entry_page", "Overview"))
    st.rerun()


def render_welcome() -> None:
    render_brand_header(APP_PRODUCT, APP_TAGLINE)
    render_pressuretest_boundary_notice(compact=True)

    st.markdown(
        """
        <div class="pt-card" style="background:#0B1730; color:#F8FAFC; padding:1.35rem 1.45rem; margin:.4rem 0 1rem 0;">
            <div class="pt-eyebrow" style="color:#CBD5E1;">Opportunity diligence workspace</div>
            <h1 style="margin:.2rem 0 .55rem 0; color:#F8FAFC; line-height:1.1;">Pressure-test the opportunity before you commit.</h1>
            <p style="max-width:820px; margin:0; color:#E2E8F0; line-height:1.6; font-size:1rem;">
                Build a quick operating profile, identify the next diligence step, and start a structured review of fit,
                concept risk, economics, and execution pressure.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    _render_workflow_selector()

    st.markdown("<div style='height:.75rem;'></div>", unsafe_allow_html=True)

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
            workflow_type = st.session_state.get("workflow_type", DEFAULT_WORKFLOW)
            workflow_config = get_workflow_config(workflow_type)
            st.session_state["auth_complete"] = True
            st.session_state["profile_complete"] = True
            st.session_state["workflow_type"] = workflow_type if workflow_type in WORKFLOW_CONFIG else DEFAULT_WORKFLOW
            st.session_state.setdefault("current_page", str(workflow_config.get("entry_page", "Overview")))
            st.rerun()
        st.caption("Use this only after importing or resuming saved local progress.")
