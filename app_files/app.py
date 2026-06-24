# app.py

from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable
from typing import Final
from uuid import uuid4

import streamlit as st

from app_state import initialize_app_state, reset_assessment_state
from auth import ensure_authenticated, get_authenticated_user_id, render_auth_sidebar_summary
from branding import APP_PRODUCT
from decision_engine import build_decision_packet
from final_decision_ui import render_final_decision
from financial_model_ui import render_financial_model
from opportunity_fit_ui import render_opportunity_fit
from overview_ui import render_overview
from page_config import DEFAULT_PAGE, PAGES, SIDEBAR_PAGES, get_page_config, normalize_page_name
from persistence import apply_session_to_state, delete_session, list_sessions, load_session, save_session
from phase0_ui import render_phase_0
from phase1_ui import render_phase_1
from phase_gate import guard_page_or_warn
from post_discovery_ui import render_post_discovery
from profile_ui import render_profile_setup
from report_ui import render_report_screen
from shared_ui import render_compact_brand_bar, render_sidebar_branding
from theme import apply_theme
from ui_styles import inject_global_styles
from welcome_ui import render_welcome
from workflow_config import DEFAULT_WORKFLOW, get_workflow_config


PageRenderer = Callable[[], None]

RESET_KEYS_TO_KEEP: Final[list[str]] = [
    "auth_complete",
    "is_authenticated",
    "auth_user_id",
    "auth_email",
    "auth_access_token",
    "auth_refresh_token",
    "profile_complete",
    "full_name",
    "email",
    "city_state",
    "franchise_name",
    "units_considered",
    "ownership_style",
    "signed_anything",
    "workflow_type",
    "active_session_id",
]

PAGE_RENDERERS: Final[dict[str, PageRenderer]] = {
    "Start Here": render_overview,
    "Operator Fit": render_phase_0,
    "Opportunity Review": render_phase_1,
    "Financial Reality": render_financial_model,
    "Commitment Review": render_post_discovery,
    "Final Decision": render_final_decision,
    "Report": render_report_screen,
}

RECOMMENDATION_LABELS: Final[dict[str, str]] = {
    "Proceed": "Move Forward",
    "Do Not Proceed": "Walk Away",
    "Proceed with Conditions": "Proceed Only If Conditions Are Met",
}


def _recommendation_label(value: object) -> str:
    return RECOMMENDATION_LABELS.get(str(value), str(value or "Not enough data"))


def configure_app() -> None:
    st.set_page_config(page_title=APP_PRODUCT, layout="wide")
    apply_theme()
    initialize_app_state()
    inject_global_styles()


def _current_workflow() -> str:
    st.session_state["workflow_type"] = DEFAULT_WORKFLOW
    return DEFAULT_WORKFLOW


def _normalize_page(page_name: str | None = None) -> str:
    page = normalize_page_name(page_name or st.session_state.get("current_page"))
    if page in PAGES:
        return page
    return DEFAULT_PAGE


def _local_session_user_id() -> str:
    auth_user_id = get_authenticated_user_id()
    if auth_user_id:
        return auth_user_id
    session_id = str(st.session_state.get("active_session_id") or uuid4())
    st.session_state["active_session_id"] = session_id
    return session_id


def ensure_required_state() -> None:
    st.session_state.setdefault("auth_complete", False)
    st.session_state.setdefault("is_authenticated", False)
    st.session_state.setdefault("auth_user_id", "")
    st.session_state.setdefault("auth_email", "")
    st.session_state.setdefault("profile_complete", False)
    st.session_state.setdefault("workflow_type", DEFAULT_WORKFLOW)
    st.session_state.setdefault("active_session_id", str(uuid4()))
    st.session_state["workflow_type"] = DEFAULT_WORKFLOW
    st.session_state["current_page"] = _normalize_page()


def render_gates() -> bool:
    if not ensure_authenticated():
        return False
    if not st.session_state["auth_complete"]:
        render_welcome()
        return False
    if not st.session_state["profile_complete"]:
        render_profile_setup()
        return False
    return True


def _recommended_page() -> tuple[str, str]:
    if not st.session_state.get("phase_0_complete"):
        return "Operator Fit", "Start with fit, time demand, and downside exposure."
    if not st.session_state.get("phase_1_complete"):
        return "Opportunity Review", "Review the opportunity before treating momentum as evidence."
    if not st.session_state.get("financial_model_done"):
        return "Financial Reality", "Run the numbers before relying on sales pressure."
    if not st.session_state.get("phase_2_complete"):
        return "Commitment Review", "Tighten the unknowns before commitment."
    if not st.session_state.get("phase_3_complete"):
        return "Final Decision", "Turn the evidence into a clear decision posture."
    return "Report", "Review the report, open risks, missing evidence, and next steps."


def _go_to(page_name: str) -> None:
    st.session_state["current_page"] = _normalize_page(page_name)
    st.rerun()


def _session_default_label() -> str:
    workflow_label = get_workflow_config(DEFAULT_WORKFLOW)["label"]
    profile_name = st.session_state.get("franchise_name") or st.session_state.get("full_name") or "Untitled"
    return f"{profile_name} — {workflow_label}"


def _session_option_label(session_id: str, metadata_lookup: dict[str, object]) -> str:
    metadata = metadata_lookup[session_id]
    label = getattr(metadata, "label", "Untitled session")
    updated_at = str(getattr(metadata, "updated_at", ""))
    return f"{label} · Franchise · {updated_at[:10]}"


def _restore_saved_session(session_id: str) -> None:
    session = load_session(session_id)
    if session is None:
        st.sidebar.error("Saved session could not be found.")
        return
    auth_keys = {
        "is_authenticated": st.session_state.get("is_authenticated", False),
        "auth_user_id": st.session_state.get("auth_user_id", ""),
        "auth_email": st.session_state.get("auth_email", ""),
        "auth_access_token": st.session_state.get("auth_access_token", ""),
        "auth_refresh_token": st.session_state.get("auth_refresh_token", ""),
    }
    apply_session_to_state(session)
    st.session_state.update(auth_keys)
    st.session_state["active_session_id"] = session.session_id
    st.session_state["workflow_type"] = DEFAULT_WORKFLOW
    st.session_state["current_page"] = _normalize_page(st.session_state.get("current_page"))
    st.sidebar.success("Session loaded.")
    st.rerun()


def render_persistence_controls() -> None:
    with st.sidebar.expander("Saved sessions", expanded=False):
        st.caption("Local JSON saves for this app instance.")
        label = st.text_input(
            "Session name",
            value=str(st.session_state.get("session_save_label") or _session_default_label()),
            key="session_save_label",
        )
        if st.button("Save current session", use_container_width=True, type="primary"):
            session_id = _local_session_user_id()
            st.session_state["active_session_id"] = session_id
            saved = save_session(user_id=session_id, label=label.strip() or _session_default_label())
            st.sidebar.success(f"Saved: {saved.label}")

        sessions = list_sessions()
        if not sessions:
            st.caption("No saved sessions yet.")
            return

        metadata_lookup = {session.session_id: session for session in sessions}
        selected_session_id = st.selectbox(
            "Prior sessions",
            options=[session.session_id for session in sessions],
            format_func=lambda value: _session_option_label(value, metadata_lookup),
            key="selected_saved_session_id",
        )
        left, right = st.columns(2)
        with left:
            if st.button("Load", use_container_width=True):
                _restore_saved_session(selected_session_id)
        with right:
            confirm_delete = st.checkbox("Confirm delete", key="confirm_delete_saved_session")
            if st.button("Delete", disabled=not confirm_delete, use_container_width=True):
                deleted = delete_session(selected_session_id)
                if deleted and st.session_state.get("active_session_id") == selected_session_id:
                    st.session_state["active_session_id"] = str(uuid4())
                st.session_state["confirm_delete_saved_session"] = False
                st.sidebar.success("Deleted saved session." if deleted else "Saved session was not found.")
                st.rerun()


def render_sidebar() -> None:
    render_sidebar_branding()
    render_auth_sidebar_summary()
    st.session_state["workflow_type"] = DEFAULT_WORKFLOW

    workflow_config = get_workflow_config(DEFAULT_WORKFLOW)
    st.sidebar.caption("Active workflow")
    st.sidebar.info(f"{workflow_config['label']}\n\n{workflow_config['status']}")
    st.sidebar.caption("Future workflows")
    st.sidebar.caption("Startup and Acquisition are disabled while this beta focuses on Franchise.")

    render_persistence_controls()

    packet = build_decision_packet()
    next_page, next_reason = _recommended_page()
    risks = packet.get("risks") or packet.get("key_risks") or []
    top_risk = risks[0] if risks else "No meaningful risk signal yet. Complete more of the workflow."
    recommendation = _recommendation_label(packet.get("recommendation", "Not enough data"))

    st.sidebar.caption("Decision pulse")
    st.sidebar.write(f"**{recommendation}**")
    st.sidebar.caption(f"Score: {packet.get('weighted_score', 0)} · Confidence: {packet.get('confidence', 'Unknown')}")
    st.sidebar.caption(f"Biggest unresolved risk: {top_risk}")

    if st.sidebar.button(f"Go to: {next_page}", use_container_width=True, type="primary"):
        _go_to(next_page)

    st.sidebar.caption(next_reason)
    st.sidebar.markdown("---")
    st.sidebar.caption("Franchise Beta path")

    current_page = st.session_state["current_page"]
    grouped_pages: dict[str, list[str]] = defaultdict(list)
    for page_name in SIDEBAR_PAGES:
        grouped_pages[get_page_config(page_name).section].append(page_name)

    for section_name, section_pages in grouped_pages.items():
        with st.sidebar.expander(section_name, expanded=True):
            for page_name in section_pages:
                label = page_name + (" •" if current_page == page_name else "")
                if st.button(label, key=f"nav_{page_name}", use_container_width=True):
                    _go_to(page_name)

    render_reset_controls()


def render_reset_controls() -> None:
    with st.sidebar.expander("Reset assessment"):
        st.caption("This clears assessment progress and keeps your basic profile info.")
        confirm_reset = st.checkbox("I understand this will reset my assessment progress.", key="confirm_reset_assessment")
        if st.button("Reset now", type="secondary", disabled=not confirm_reset, use_container_width=True):
            reset_assessment_state(keys_to_keep=RESET_KEYS_TO_KEEP)
            st.session_state["current_page"] = DEFAULT_PAGE
            st.session_state["confirm_reset_assessment"] = False
            st.rerun()


def get_current_page() -> str:
    return _normalize_page(st.session_state.get("current_page", DEFAULT_PAGE))


def render_current_page(page: str) -> None:
    render_compact_brand_bar()
    renderer = PAGE_RENDERERS.get(page)
    if renderer is None:
        st.error(f'No renderer is registered for page "{page}".')
        return
    renderer()


def render_prev_next_buttons(page: str) -> None:
    if page not in PAGES:
        return
    current_index = PAGES.index(page)
    prev_page = PAGES[current_index - 1] if current_index > 0 else None
    next_page = PAGES[current_index + 1] if current_index < len(PAGES) - 1 else None
    left, spacer, right = st.columns([1, 4, 1])
    with left:
        if prev_page and st.button("← Back", use_container_width=True):
            _go_to(prev_page)
    with right:
        if next_page and st.button("Next →", use_container_width=True):
            _go_to(next_page)


def main() -> None:
    configure_app()
    ensure_required_state()
    if not render_gates():
        st.stop()
    render_sidebar()
    page = get_current_page()
    if not guard_page_or_warn(page):
        st.stop()
    render_current_page(page)
    render_prev_next_buttons(page)


if __name__ == "__main__":
    main()
