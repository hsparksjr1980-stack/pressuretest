<<<<<<< HEAD
# app.py — PressureTest Phase 1 production shell
# Plug-and-play replacement for the current Streamlit entry point.
=======

# app.py
>>>>>>> fec65288cb896b4679e84e61241f185fa625e150

from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable
from typing import Final

import streamlit as st

from app_state import initialize_app_state, reset_assessment_state
<<<<<<< HEAD
from branding import APP_PRODUCT, FIT_PAGE_LABEL
from buildout_tracker_ui import render_buildout_tracker
from calculators_ui import render_calculators
from brand_territory_ui import render_brand_territory
=======
from branding import APP_PRODUCT, APP_TAGLINE, FIT_PAGE_LABEL
from buildout_tracker_ui import render_buildout_tracker
>>>>>>> fec65288cb896b4679e84e61241f185fa625e150
from decision_engine import build_decision_packet
from deal_model_ui import render_deal_model
from deal_workspace_ui import render_deal_workspace
from execution_report_ui import render_execution_report
from final_decision_ui import render_final_decision
from financial_model_ui import render_financial_model
from free_report_ui import render_free_report
<<<<<<< HEAD
from local_state_io import export_json_bytes, import_json_bytes, load_demo_state
from opportunity_fit_ui import render_opportunity_fit
from overview_ui import render_overview
from page_config import DEFAULT_PAGE, PAGES, SIDEBAR_PAGES, get_page_config, get_section_helper, is_pro_page
=======
from nav_ui import render_page_nav
from opportunity_fit_ui import render_opportunity_fit
from overview_ui import render_overview
from page_config import DEFAULT_PAGE, PAGES, SIDEBAR_PAGES, get_page_config, is_pro_page
>>>>>>> fec65288cb896b4679e84e61241f185fa625e150
from paywall_ui import render_paywall
from phase0_ui import render_phase_0
from phase1_ui import render_phase_1
from phase_gate import guard_page_or_warn
from plans_support_ui import render_plans_support
from post_discovery_ui import render_post_discovery
<<<<<<< HEAD
from premium_components import esc, inject_premium_css
from premium_home_ui import render_premium_home
from profile_ui import render_profile_setup
from report_ui import render_report_screen
from seo_resources_ui import render_seo_resources
from shared_ui import render_compact_brand_bar, render_sidebar_branding, render_pressuretest_boundary_notice
=======
from profile_ui import render_profile_setup
from report_ui import render_report_screen
from shared_ui import render_compact_brand_bar, render_sidebar_branding
>>>>>>> fec65288cb896b4679e84e61241f185fa625e150
from theme import apply_theme
from ui_styles import inject_global_styles
from welcome_ui import render_welcome

<<<<<<< HEAD
=======

>>>>>>> fec65288cb896b4679e84e61241f185fa625e150
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
]

<<<<<<< HEAD
# Home is new. All other pages reuse your existing app modules.
PAGE_RENDERERS: Final[dict[str, PageRenderer]] = {
    "Home": render_overview,
    "Overview": render_overview,
    "Brand & Territory Snapshot": render_brand_territory,
=======
PAGE_RENDERERS: Final[dict[str, PageRenderer]] = {
    "Overview": render_overview,
>>>>>>> fec65288cb896b4679e84e61241f185fa625e150
    FIT_PAGE_LABEL: render_phase_0,
    "Concept Validation": render_phase_1,
    "Opportunity Fit & Recommendations": render_opportunity_fit,
    "Financial Model": render_financial_model,
<<<<<<< HEAD
    "Calculators": render_calculators,
=======
>>>>>>> fec65288cb896b4679e84e61241f185fa625e150
    "Free Report": render_free_report,
    "Post-Discovery": render_post_discovery,
    "Final Decision": render_final_decision,
    "Report": render_report_screen,
    "Plans & Support": render_plans_support,
<<<<<<< HEAD
    "SEO Resources": render_seo_resources,
=======
>>>>>>> fec65288cb896b4679e84e61241f185fa625e150
    "Deal Workspace": render_deal_workspace,
    "Deal Model": render_deal_model,
    "Buildout & Launch Tracker": render_buildout_tracker,
    "Execution Report": render_execution_report,
    "Paywall": render_paywall,
}


def configure_app() -> None:
<<<<<<< HEAD
    st.set_page_config(page_title=APP_PRODUCT, page_icon="🧭", layout="wide")
    apply_theme()
    initialize_app_state()
    inject_global_styles()
    inject_premium_css()
=======
    st.set_page_config(page_title=APP_PRODUCT, layout="wide")
    apply_theme()
    initialize_app_state()
    inject_global_styles()
>>>>>>> fec65288cb896b4679e84e61241f185fa625e150


def ensure_required_state() -> None:
    st.session_state.setdefault("auth_complete", False)
    st.session_state.setdefault("profile_complete", False)
    st.session_state.setdefault("premium_access", False)
<<<<<<< HEAD
    # Public prototype mode: no payment plumbing and no free-user access to execution tools.
    st.session_state.setdefault("dev_pro_access", False)

    current_page = st.session_state.get("current_page", "Home")
    valid_pages = ["Home", *PAGES]
    if current_page not in valid_pages:
        current_page = "Home"
=======
    st.session_state.setdefault("dev_pro_access", True)

    current_page = st.session_state.get("current_page", DEFAULT_PAGE)
    if current_page not in PAGES:
        current_page = DEFAULT_PAGE
>>>>>>> fec65288cb896b4679e84e61241f185fa625e150
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
<<<<<<< HEAD
        return FIT_PAGE_LABEL, "Start with operator fit, downside tolerance, and ownership reality."
    if not st.session_state.get("brand_analysis_done"):
        return "Brand & Territory Snapshot", "Add brand and territory context so the workflow is less generic."
    if not st.session_state.get("phase_1_complete"):
        return "Concept Validation", "Pressure-test the concept before momentum takes over."
    if not st.session_state.get("financial_model_done"):
        return "Financial Model", "Run economics, ramp, and working-capital pressure before treating the deal as viable."
    if not st.session_state.get("free_report_generated"):
        return "Calculators", "Test working capital, ramp, and staffing pressure before packaging the report."
    if not st.session_state.get("phase_2_complete"):
        return "Post-Discovery", "Convert Discovery Day answers into conditions and gaps."
    if not st.session_state.get("phase_3_complete"):
        return "Final Decision", "Turn the evidence into a clear proceed, pause, renegotiate, or walk-away call."
    return "Report", "Package the decision signal and remaining conditions."
=======
        return (
            FIT_PAGE_LABEL,
            "Start with fit: time demand, ownership reality, and downside exposure.",
        )
    if not st.session_state.get("phase_1_complete"):
        return (
            "Concept Validation",
            "Pressure-test whether the concept itself deserves more time.",
        )
    if not st.session_state.get("financial_model_done"):
        return (
            "Financial Model",
            "Run the economics before treating momentum as proof.",
        )
    if not st.session_state.get("phase_2_complete"):
        return (
            "Post-Discovery",
            "Tighten the unknowns before you call this investable.",
        )
    if not st.session_state.get("phase_3_complete"):
        return (
            "Final Decision",
            "Turn the evidence into a clear go, no-go, or conditions-based call.",
        )
    return "Report", "Review the final signal and unresolved conditions."
>>>>>>> fec65288cb896b4679e84e61241f185fa625e150


def _go_to(page_name: str) -> None:
    st.session_state["current_page"] = page_name
    st.rerun()


<<<<<<< HEAD
def _decision_pulse_html() -> str:
    packet = build_decision_packet()
    risks = packet.get("risks") or packet.get("key_risks") or []
    top_risk = risks[0] if risks else "Complete more of the workflow to surface the top unresolved risk."
    return f"""
    <div class="pt-card" style="margin-bottom:.8rem;">
      <div class="pt-eyebrow">Decision pulse</div>
      <h3>{esc(packet.get('recommendation', 'Not enough data'))}</h3>
      <p><strong>Score:</strong> {esc(packet.get('weighted_score', 0))} · <strong>Confidence:</strong> {esc(packet.get('confidence', 'Low'))}</p>
      <div class="pt-divider"></div>
      <p><strong>Top unresolved risk</strong><br>{esc(top_risk)}</p>
    </div>
    """


=======
>>>>>>> fec65288cb896b4679e84e61241f185fa625e150
def render_sidebar() -> None:
    render_sidebar_branding()

    is_paid_pro = bool(st.session_state.get("premium_access", False))
    has_dev_pro = bool(st.session_state.get("dev_pro_access", False))
    pro_enabled = is_paid_pro or has_dev_pro

<<<<<<< HEAD
    plan_label = "Pro" if is_paid_pro else "Free Assessment"
    plan_subtext = "Core diligence workflow open. Execution tools require Pro." if not is_paid_pro else "Execution tools unlocked."

    st.sidebar.markdown(
        f"""
        <div class="pt-card" style="margin-bottom:.8rem;">
          <div class="pt-eyebrow">Workspace</div>
          <span class="pt-pill">{esc(plan_label)}</span>
          <p style="margin-top:.55rem;">{esc(plan_subtext)}</p>
=======
    plan_label = "Pro" if pro_enabled else "Core"
    plan_subtext = "Execution tools unlocked" if pro_enabled else "Core workflow only"
    if has_dev_pro and not is_paid_pro:
        plan_subtext = "Developer override enabled"

    st.sidebar.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, rgba(249,115,22,0.10), rgba(249,115,22,0.03));
            border: 1px solid rgba(249,115,22,0.18);
            border-radius: 18px;
            padding: 0.95rem 1rem 0.9rem 1rem;
            margin-bottom: 0.9rem;
            box-shadow: 0 8px 24px rgba(17, 24, 39, 0.05);
        ">
            <div style="
                font-size: 0.72rem;
                font-weight: 700;
                letter-spacing: 0.08em;
                text-transform: uppercase;
                color: #64748B;
                margin-bottom: 0.38rem;
            ">
                Your plan
            </div>
            <div style="
                display: inline-block;
                padding: 0.22rem 0.58rem;
                border-radius: 999px;
                background: rgba(249,115,22,0.10);
                border: 1px solid rgba(249,115,22,0.16);
                color: #C2410C;
                font-size: 0.7rem;
                font-weight: 800;
                letter-spacing: 0.04em;
                text-transform: uppercase;
                margin-bottom: 0.45rem;
            ">
                {plan_label}
            </div>
            <div style="
                font-size: 0.92rem;
                line-height: 1.45;
                color: #334155;
            ">
                {plan_subtext}
            </div>
>>>>>>> fec65288cb896b4679e84e61241f185fa625e150
        </div>
        """,
        unsafe_allow_html=True,
    )

<<<<<<< HEAD
    st.sidebar.markdown(_decision_pulse_html(), unsafe_allow_html=True)

    next_page, next_reason = _recommended_page()
    if st.sidebar.button(f"Next best action: {next_page}", type="primary", use_container_width=True):
        _go_to(next_page)
    st.sidebar.caption(next_reason)

    st.sidebar.markdown("---")
    if st.sidebar.button("Decision Cockpit", use_container_width=True):
        _go_to("Home")

    st.sidebar.caption("Guided diligence flow")
=======
    packet = build_decision_packet()
    next_page, next_reason = _recommended_page()
    risks = packet.get("risks") or packet.get("key_risks") or []
    top_risk = risks[0] if risks else "No meaningful risk signal yet. Complete more of the workflow."

    st.sidebar.markdown(
        f"""
        <div style="
            background: #ffffff;
            border: 1px solid rgba(17,24,39,0.08);
            border-radius: 18px;
            padding: 0.95rem 1rem 0.9rem 1rem;
            margin-bottom: 0.9rem;
            box-shadow: 0 8px 24px rgba(17, 24, 39, 0.04);
        ">
            <div style="font-size: 0.72rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: #64748B; margin-bottom: 0.35rem;">Decision pulse</div>
            <div style="font-size: 1rem; font-weight: 700; color: #0F172A; margin-bottom: 0.25rem;">{packet.get('recommendation', 'Not enough data')}</div>
            <div style="font-size: 0.88rem; line-height: 1.45; color: #475569; margin-bottom: 0.55rem;">Weighted score: {packet.get('weighted_score', 0)} · Confidence: {packet.get('confidence', 'Low')}</div>
            <div style="font-size: 0.72rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: #64748B; margin-bottom: 0.2rem;">Biggest unresolved risk</div>
            <div style="font-size: 0.84rem; line-height: 1.45; color: #475569;">{top_risk}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.sidebar.button(f"Go to: {next_page}", use_container_width=True, type="primary"):
        _go_to(next_page)

    st.sidebar.caption(next_reason)
    st.sidebar.markdown("---")
    st.sidebar.caption("Workflow")

>>>>>>> fec65288cb896b4679e84e61241f185fa625e150
    current_page = st.session_state["current_page"]
    grouped_pages: dict[str, list[str]] = defaultdict(list)
    for page_name in SIDEBAR_PAGES:
        grouped_pages[get_page_config(page_name).section].append(page_name)

    for section_name, section_pages in grouped_pages.items():
<<<<<<< HEAD
        helper = get_section_helper(section_name)
        expanded = current_page in section_pages
        with st.sidebar.expander(section_name, expanded=expanded):
            if helper:
                st.caption(helper)
=======
        with st.sidebar.expander(section_name, expanded=current_page in section_pages):
>>>>>>> fec65288cb896b4679e84e61241f185fa625e150
            for page_name in section_pages:
                locked = is_pro_page(page_name) and not pro_enabled
                label = page_name
                if locked:
<<<<<<< HEAD
                    label += "  🔒"
                elif current_page == page_name:
                    label += "  •"
                if st.button(label, key=f"nav_{page_name}", use_container_width=True, disabled=locked):
                    _go_to(page_name)
            if section_name == "Execution Tools" and not pro_enabled:
                st.caption("Pro unlocks execution-side tools after the user is ready to manage the actual deal.")
                if st.button("Compare Free vs Pro", key="nav_compare_free_pro", use_container_width=True):
                    _go_to("Plans & Support")

    st.sidebar.markdown("---")
    with st.sidebar.expander("Local save / load", expanded=False):
        st.download_button(
            "Download assessment JSON",
            data=export_json_bytes(),
            file_name="pressuretest_assessment.json",
            mime="application/json",
            use_container_width=True,
        )
        uploaded = st.file_uploader("Import JSON", type=["json"], key="sidebar_import_json")
        if uploaded is not None:
            ok, message = import_json_bytes(uploaded.getvalue())
            if ok:
                st.success(message)
                st.rerun()
            else:
                st.error(message)
        if st.button("Load demo scenario", use_container_width=True):
            load_demo_state()
            st.rerun()

    with st.sidebar.expander("Execution preview", expanded=False):
        st.caption("Execution tools are intentionally locked in the public prototype. This keeps free users in the assessment path instead of sending them into future paid sections.")
=======
                    label += " 🔒"
                elif current_page == page_name:
                    label += " •"

                if st.button(
                    label,
                    key=f"nav_{page_name}",
                    use_container_width=True,
                    disabled=locked,
                ):
                    _go_to(page_name)

    st.sidebar.markdown("---")
    st.sidebar.caption("Developer access")

    dev_enabled = st.sidebar.checkbox(
        "Enable Pro dev access",
        value=bool(st.session_state.get("dev_pro_access", False)),
        key="sidebar_dev_pro_access",
    )
    st.session_state["dev_pro_access"] = bool(dev_enabled)
>>>>>>> fec65288cb896b4679e84e61241f185fa625e150

    render_reset_controls()


def render_reset_controls() -> None:
<<<<<<< HEAD
    with st.sidebar.expander("Reset assessment", expanded=False):
        st.caption("Clears assessment progress but keeps basic profile info.")
        confirm_reset = st.checkbox("I understand this will reset progress.", key="confirm_reset_assessment")
        if st.button("Reset now", disabled=not confirm_reset, use_container_width=True):
            reset_assessment_state(keys_to_keep=RESET_KEYS_TO_KEEP)
            st.session_state["current_page"] = "Home"
=======
    with st.sidebar.expander("Reset assessment"):
        st.caption("This clears assessment progress and keeps your basic profile info.")

        confirm_reset = st.checkbox(
            "I understand this will reset my assessment progress.",
            key="confirm_reset_assessment",
        )

        reset_clicked = st.button(
            "Reset now",
            type="secondary",
            disabled=not confirm_reset,
            use_container_width=True,
        )

        if reset_clicked:
            reset_assessment_state(keys_to_keep=RESET_KEYS_TO_KEEP)
            st.session_state["current_page"] = DEFAULT_PAGE
>>>>>>> fec65288cb896b4679e84e61241f185fa625e150
            st.session_state["confirm_reset_assessment"] = False
            st.rerun()


def get_current_page() -> str:
<<<<<<< HEAD
    page = st.session_state.get("current_page", "Home")
    if page not in ["Home", *PAGES]:
        return "Home"
    return page


def _has_execution_access() -> bool:
    return bool(st.session_state.get("premium_access", False)) or bool(st.session_state.get("dev_pro_access", False))


def render_locked_execution_preview(page: str) -> None:
    render_compact_brand_bar()
    render_pressuretest_boundary_notice()
    st.markdown(
        f"""
        <div class="pt-lock-card">
          <div class="pt-eyebrow">Execution tools</div>
          <h1 style="margin:.1rem 0 .45rem 0;">{esc(page)} is part of PressureTest Pro.</h1>
          <p style="max-width:760px; line-height:1.55; color:#475569;">
            Free helps you decide whether the opportunity deserves deeper diligence. Pro is for the post-decision work: lender coordination, lease items, vendor quotes, buildout tracking, launch readiness, working-capital scenarios, and execution reporting.
          </p>
          <div class="pt-divider"></div>
          <p><strong>Access boundary:</strong> this section stays locked for free users so the assessment path remains focused on decision quality instead of execution planning.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="pt-card"><span class="pt-pill">Included later</span><h3>Deal Workspace</h3><p>Track lender, lease, contractor, landlord, vendor, and open-decision items.</p></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="pt-card"><span class="pt-pill">Included later</span><h3>Buildout & Launch</h3><p>Organize permits, quotes, payments, timelines, pre-opening tasks, and readiness risks.</p></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="pt-card"><span class="pt-pill">Included later</span><h3>Execution Report</h3><p>Package the post-commitment plan, key risks, and next actions into a clean operating memo.</p></div>', unsafe_allow_html=True)
    cta1, cta2 = st.columns([1, 1])
    with cta1:
        if st.button("Compare Free vs Pro", type="primary", use_container_width=True):
            _go_to("Plans & Support")
    with cta2:
        if st.button("Return to Decision Cockpit", use_container_width=True):
            _go_to("Home")


def render_current_page(page: str) -> None:
    if is_pro_page(page) and not _has_execution_access():
        render_locked_execution_preview(page)
        return
    renderer = PAGE_RENDERERS.get(page)
    if renderer is None:
        st.error(f'No renderer is registered for page "{page}".')
        return
    render_compact_brand_bar()
    render_pressuretest_boundary_notice()
    renderer()


def _visible_navigation_pages() -> list[str]:
    pages = ["Home", *PAGES]
    if _has_execution_access():
        return pages
    return [p for p in pages if not is_pro_page(p)]


def render_prev_next_buttons(page: str) -> None:
    visible_pages = _visible_navigation_pages()
    if page not in visible_pages:
        return
    current_index = visible_pages.index(page)
    prev_page = visible_pages[current_index - 1] if current_index > 0 else None
    next_page = visible_pages[current_index + 1] if current_index < len(visible_pages) - 1 else None
    st.markdown("---")
    left, _, right = st.columns([1, 4, 1])
    with left:
        if prev_page and st.button("← Back", use_container_width=True):
            _go_to(prev_page)
    with right:
        if next_page and st.button("Next →", type="primary", use_container_width=True):
            _go_to(next_page)
=======
    page = st.session_state.get("current_page", DEFAULT_PAGE)
    if page not in PAGES:
        return DEFAULT_PAGE
    return page


def render_current_page(page: str) -> None:
    renderer = PAGE_RENDERERS.get(page)

    if renderer is None:
        st.error(f'No renderer is registered for page "{page}".')
        return

    render_compact_brand_bar()
    renderer()


def render_prev_next_buttons(page: str) -> None:
    visible_pages = list(PAGES)

    if page not in visible_pages:
        return

    current_index = visible_pages.index(page)
    prev_page = visible_pages[current_index - 1] if current_index > 0 else None
    next_page = visible_pages[current_index + 1] if current_index < len(visible_pages) - 1 else None

    left, spacer, right = st.columns([1, 4, 1])

    with left:
        if prev_page and st.button("← Back", use_container_width=True):
            st.session_state["current_page"] = prev_page
            st.rerun()

    with right:
        if next_page and st.button("Next →", use_container_width=True):
            st.session_state["current_page"] = next_page
            st.rerun()
>>>>>>> fec65288cb896b4679e84e61241f185fa625e150


def main() -> None:
    configure_app()
    ensure_required_state()

    if not render_gates():
        st.stop()

    render_sidebar()
<<<<<<< HEAD
    page = get_current_page()

    # Home is never gated. Pro pages show a polished preview instead of dumping free users into paid tools.
    if page != "Home" and not is_pro_page(page) and not guard_page_or_warn(page):
=======

    page = get_current_page()

    if not guard_page_or_warn(page):
>>>>>>> fec65288cb896b4679e84e61241f185fa625e150
        st.stop()

    render_current_page(page)
    render_prev_next_buttons(page)
<<<<<<< HEAD
=======
    
>>>>>>> fec65288cb896b4679e84e61241f185fa625e150


if __name__ == "__main__":
    main()
