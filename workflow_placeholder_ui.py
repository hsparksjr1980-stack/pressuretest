# workflow_placeholder_ui.py

from __future__ import annotations

import streamlit as st

from workflow_config import DEFAULT_WORKFLOW, WORKFLOW_CONFIG, get_workflow_config


def render_workflow_placeholder() -> None:
    workflow_type = st.session_state.get("workflow_type", DEFAULT_WORKFLOW)
    config = get_workflow_config(workflow_type)

    st.markdown(
        f"""
        <div class="pt-card" style="background:#0B1730; color:#F8FAFC; padding:1.35rem 1.45rem; margin:.4rem 0 1rem 0;">
            <div class="pt-eyebrow" style="color:#CBD5E1;">{config['status']}</div>
            <h1 style="margin:.2rem 0 .55rem 0; color:#F8FAFC; line-height:1.1;">{config['label']}</h1>
            <p style="max-width:820px; margin:0; color:#E2E8F0; line-height:1.6; font-size:1rem;">
                {config['description']}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="pt-card">
            <div class="pt-eyebrow">Workflow in progress</div>
            <h3 style="margin:.2rem 0 .5rem 0;">This assessment path is being built.</h3>
            <p style="margin:0; line-height:1.6; color:#475569;">
                PressureTest currently supports the franchise opportunity workflow. Acquisition and startup workflows
                are being staged as separate diligence paths so they can be added without disrupting the existing
                franchise assessment, scoring engine, or report flow.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div style='height:.75rem;'></div>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("Switch to Franchise workflow", type="primary", use_container_width=True):
            st.session_state["workflow_type"] = "franchise"
            st.session_state["current_page"] = "Overview"
            st.rerun()
    with col2:
        st.caption("The selected workflow is saved in session state. No scoring or pricing changes have been made for this phase.")

    with st.expander("Available workflow paths"):
        for key, item in WORKFLOW_CONFIG.items():
            st.markdown(f"**{item['label']}** — {item['status']}")
