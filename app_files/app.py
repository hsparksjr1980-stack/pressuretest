# app.py

from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable
from typing import Final

import streamlit as st

from app_state import initialize_app_state, reset_assessment_state
from branding import APP_PRODUCT, FIT_PAGE_LABEL
from buildout_tracker_ui import render_buildout_tracker
from decision_engine import build_decision_packet
from deal_model_ui import render_deal_model
from deal_workspace_ui import render_deal_workspace
from execution_report_ui import render_execution_report
from final_decision_ui import render_final_decision
from financial_model_ui import render_financial_model
from free_report_ui import render_free_report
from opportunity_fit_ui import render_opportunity_fit
from overview_ui import render_overview
from page_config import DEFAULT_PAGE, PAGES, SIDEBAR_PAGES, get_page_config, is_pro_page
from paywall_ui import render_paywall
from phase0_ui import render_phase_0
from phase1_ui import render_phase_1
from phase_gate import guard_page_or_warn
from plans_support_ui import render_plans_support
from post_discovery_ui import render_post_discovery
from profile_ui import render_profile_setup
from report_ui import render_report_screen
from shared_ui import render_compact_brand_bar, render_sidebar_branding
from theme import apply_theme
from ui_styles import inject_global_styles
from welcome_ui import render_welcome
from workflow_config import DEFAULT_WORKFLOW, WORKFLOW_CONFIG, get_workflow_config
from workflow_placeholder_ui import render_workflow_placeholder
from workflows.startup.concept_validation_ui import render_startup_concept_validation
from workflows.startup.financial_assumptions_ui import render_startup_financial_assumptions
from workflows.startup.market_pressure_ui import render_startup_market_pressure_test
from workflows.startup.overview_ui import render_startup_overview
from workflows.startup.page_config import STARTUP_DEFAULT_PAGE, STARTUP_PAGES
from workflows.startup.readiness_report_ui import render_startup_readiness_report


PageRenderer = Callable[[], None]

RESET_KEYS_TO_KEEP: Final[list[str]] = [
    "auth_complete",
    "profile_complete",
    "full_name",
    "email",
    "city_state",
    "franchise_name",
    "units_considered",
    "ownership_style",
    "signed_anything",
    "premium_access",
    "dev_pro_access",
    "workflow_type",
]

PAGE_RENDERERS: Final[dict[str, PageRenderer]] = {
    "Overview": render_overview,
    FIT_PAGE_LABEL: render_phase_0,
    "Concept Validation": render_phase_1,
    "Opportunity Fit & Recommendations": render_opportunity_fit,
    "Financial Model": render_financial_model,
    "Free Report": render_free_report,
    "Post-Discovery": render_post_discovery,
    "Final Decision": render_final_decision,
    "Report": render_report_screen,
    "Plans & Support": render_plans_support,
    "Deal Workspace": render_deal_workspace,
    "Deal Model": render_deal_model,
    "Buildout & Launch Tracker": render_buildout_tracker,
    "Execution Report": render_execution_report,
    "Paywall": render_paywall,
}

STARTUP_PAGE_RENDERERS: Final[dict[str, PageRenderer]] = {
    "Startup Overview": render_startup_overview,
    "Startup Concept Validation": render_startup_concept_validation,
    "Startup Market Pressure Test": render_startup_market_pressure_test,
    "Startup Financial Assumptions": render_startup_financial_assumptions,
    "Startup Readiness Report": render_startup_readiness_report,
}


def configure_app() -> None:
    st.set_page_config(page_title=APP_PRODUCT, layout="wide")
    apply_theme()
    initialize_app_state()
    inject_global_styles()


def _current_workflow() -> str:
    workflow_type = st.session_state.get("workflow_type", DEFAULT_WORKFLOW)
    if workflow_type not in WORKFLOW_CONFIG:
        workflow_type = DEFAULT_WORKFLOW
    st.session_state["workflow_type"] = workflow_type
    return workflow_type


def ensure_required_state() -> None:
    st.session_state.setdefault("auth_complete", False)
    st.session_state.setdefault("profile_complete", False)
    st.session_state.setdefault("premium_access", False)
    st.session_state.setdefault("dev_pro_access", True)
    st.session_state.setdefault("workflow_type", DEFAULT_WORKFLOW)

    workflow_type = _current_workflow()
    current_page = st.session_state.get("current_page", DEFAULT_PAGE)

    if workflow_type == "startup":
        if current_page not in STARTUP_PAGES:
            current_page = STARTUP_DEFAULT_PAGE
    elif current_page not in PAGES:
        current_page = DEFAULT_PAGE

    st.session_state["current_page"] = current_page


def render_gates() -> bool:
    if not st.session_state["auth_complete"]:
        render_welcome()
        return False

    if not st.session_state["profile_complete"]:
        render_profile_setup()
        return False

    return True


def _recommended_page() -> tuple[str, str]:
    if not st.session_state.get("phase_0_complete"):
        return FIT_PAGE_LABEL, "Start with fit: time demand, ownership reality, and downside exposure."
    if not st.session_state.get("phase_1_complete"):
        return "Concept Validation", "Pressure-test whether the concept itself deserves more time."
    if not st.session_state.get("financial_model_done"):
        return "Financial Model", "Run the economics before treating momentum as proof."
    if not st.session_state.get("phase_2_complete"):
        return "Post-Discovery", "Tighten the unknowns before you call this investable."
    if not st.session_state.get("phase_3_complete"):
        return "Final Decision", "Turn the evidence into a clear go, no-go, or conditions-based call."
    return "Report", "Review the final signal and unresolved conditions."


def _go_to(page_name: str) -> None:
    st.session_state["current_page"] = page_name
    st.rerun()


def _render_workflow_sidebar(workflow_type: str) -> bool:
    workflow_config = get_workflow_config(workflow_type)
    st.sidebar.caption("Active workflow")
    st.sidebar.info(f"{workflow_config['label']}\n\n{workflow_config['status']}")

    if workflow_type == "franchise":
        return True

    st.sidebar.caption("This workflow path is staged for future expansion.")
    if st.sidebar.button("Switch to Franchise workflow", use_container_width=True):
        st.session_state["workflow_type"] = "franchise"
        st.session_state["current_page"] = DEFAULT_PAGE
        st.rerun()
    return False


def _render_startup_sidebar() -> None:
    workflow_config = get_workflow_config("startup")
    st.sidebar.caption("Active workflow")
    st.sidebar.info(f"{workflow_config['label']}\n\n{workflow_config['status']}")
    st.sidebar.caption("Startup workflow shell")
    st.sidebar.markdown("---")
    st.sidebar.caption("Startup navigation")

    current_page = st.session_state.get("current_page", STARTUP_DEFAULT_PAGE)
    for page_name in STARTUP_PAGES:
        label = page_name + (" •" if current_page == page_name else "")
        if st.sidebar.button(label, key=f"startup_nav_{page_name}", use_container_width=True):
            _go_to(page_name)

    st.sidebar.markdown("---")
    if st.sidebar.button("Switch to Franchise workflow", use_container_width=True):
        st.session_state["workflow_type"] = "franchise"
        st.session_state["current_page"] = DEFAULT_PAGE
        st.rerun()


def render_sidebar() -> None:
    render_sidebar_branding()

    workflow_type = _current_workflow()

    if workflow_type == "startup":
        _render_startup_sidebar()
        return

    if not _render_workflow_sidebar(workflow_type):
        return

    is_paid_pro = bool(st.session_state.get("premium_access", False))
    has_dev_pro = bool(st.session_state.get("dev_pro_access", False))
    pro_enabled = is_paid_pro or has_dev_pro

    plan_label = "Pro" if pro_enabled else "Core"
    plan_subtext = "Developer override enabled" if has_dev_pro and not is_paid_pro else (
        "Execution tools unlocked" if pro_enabled else "Core workflow only"
    )
    st.sidebar.caption("Your plan")
    st.sidebar.info(f"{plan_label}\n\n{plan_subtext}")

    packet = build_decision_packet()
    next_page, next_reason = _recommended_page()
    risks = packet.get("risks") or packet.get("key_risks") or []
    top_risk = risks[0] if risks else "No meaningful risk signal yet. Complete more of the workflow."

    st.sidebar.caption("Decision pulse")
    st.sidebar.write(f"**{packet.get('recommendation', 'Not enough data')}**")
    st.sidebar.caption(f"Weighted score: {packet.get('weighted_score', 0)} · Confidence: {packet.get('confidence', 'Unknown')}")
    st.sidebar.caption(f"Biggest unresolved risk: {top_risk}")

    if st.sidebar.button(f"Go to: {next_page}", use_container_width=True, type="primary"):
        _go_to(next_page)

    st.sidebar.caption(next_reason)
    st.sidebar.markdown("---")
    st.sidebar.caption("Workflow navigation")

    current_page = st.session_state["current_page"]
    grouped_pages: dict[str, list[str]] = defaultdict(list)
    for page_name in SIDEBAR_PAGES:
        grouped_pages[get_page_config(page_name).section].append(page_name)

    for section_name, section_pages in grouped_pages.items():
        with st.sidebar.expander(section_name, expanded=current_page in section_pages):
            for page_name in section_pages:
                locked = is_pro_page(page_name) and not pro_enabled
                label = page_name + (" 🔒" if locked else " •" if current_page == page_name else "")
                if st.button(label, key=f"nav_{page_name}", use_container_width=True, disabled=locked):
                    _go_to(page_name)

    st.sidebar.markdown("---")
    st.sidebar.caption("Developer access")

    dev_enabled = st.sidebar.checkbox(
        "Enable Pro dev access",
        value=bool(st.session_state.get("dev_pro_access", False)),
        key="sidebar_dev_pro_access",
    )
    st.session_state["dev_pro_access"] = bool(dev_enabled)

    render_reset_controls()


def render_reset_controls() -> None:
    with st.sidebar.expander("Reset assessment"):
        st.caption("This clears assessment progress and keeps your basic profile info.")
        confirm_reset = st.checkbox(
            "I understand this will reset my assessment progress.",
            key="confirm_reset_assessment",
        )
        if st.button("Reset now", type="secondary", disabled=not confirm_reset, use_container_width=True):
            reset_assessment_state(keys_to_keep=RESET_KEYS_TO_KEEP)
            st.session_state["current_page"] = DEFAULT_PAGE
            st.session_state["confirm_reset_assessment"] = False
            st.rerun()


def get_current_page() -> str:
    page = st.session_state.get("current_page", DEFAULT_PAGE)
    workflow_type = _current_workflow()
    if workflow_type == "startup":
        return page if page in STARTUP_PAGES else STARTUP_DEFAULT_PAGE
    if page not in PAGES:
        return DEFAULT_PAGE
    return page


def render_current_page(page: str) -> None:
    render_compact_brand_bar()

    workflow_type = _current_workflow()

    if workflow_type == "startup":
        renderer = STARTUP_PAGE_RENDERERS.get(page, render_startup_overview)
        renderer()
        return

    if workflow_type != "franchise":
        render_workflow_placeholder()
        return

    renderer = PAGE_RENDERERS.get(page)
    if renderer is None:
        st.error(f'No renderer is registered for page "{page}".')
        return

    renderer()


def render_prev_next_buttons(page: str) -> None:
    workflow_type = _current_workflow()

    if workflow_type == "startup":
        visible_pages = list(STARTUP_PAGES)
    elif workflow_type == "franchise":
        visible_pages = list(PAGES)
    else:
        return

    if page not in visible_pages:
        return

    current_index = visible_pages.index(page)
    prev_page = visible_pages[current_index - 1] if current_index > 0 else None
    next_page = visible_pages[current_index + 1] if current_index < len(visible_pages) - 1 else None

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

    if _current_workflow() == "franchise" and not guard_page_or_warn(page):
        st.stop()

    render_current_page(page)
    render_prev_next_buttons(page)


if __name__ == "__main__":
    main()
