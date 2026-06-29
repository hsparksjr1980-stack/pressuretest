from __future__ import annotations

import streamlit as st

from branding import APP_PRODUCT
from franchise_beta import render_beta_styles, render_depth_toggle, render_pressure_check
from gotcha_engine import render_gotcha_section
from ui_styles import (
    close_shell,
    open_shell,
    render_action_banner,
    render_bullet_panel,
    render_card,
    render_page_header,
    render_section_intro,
)


def _recommended_next_step() -> tuple[str, str]:
    if not st.session_state.get("phase_0_complete"):
        return (
            "Operator Fit",
            "Start by testing whether the ownership model, time demand, and downside fit you.",
        )
    if not st.session_state.get("phase_1_complete"):
        return (
            "Opportunity Review",
            "Pressure-test the concept before you give more weight to momentum or brand story.",
        )
    if not st.session_state.get("financial_model_done"):
        return (
            "Financial Reality",
            "Check the economics before treating the opportunity as investable.",
        )
    if not st.session_state.get("phase_2_complete"):
        return (
            "Commitment Review",
            "Use discovery to tighten assumptions and surface unresolved issues.",
        )
    return (
        "Final Decision",
        "Bring the evidence together and decide whether to proceed, pause, or walk away.",
    )


def _profile_summary() -> list[str]:
    items: list[str] = []

    full_name = st.session_state.get("full_name")
    franchise_name = st.session_state.get("franchise_name")
    units = st.session_state.get("units_considered")
    ownership_style = st.session_state.get("ownership_style")

    if full_name:
        items.append(f"Profile: {full_name}")
    if franchise_name:
        items.append(f"Concept: {franchise_name}")
    if units:
        items.append(f"Units considered: {units}")
    if ownership_style:
        items.append(f"Ownership style: {ownership_style}")

    return items


def _workflow_status() -> list[str]:
    steps = [
        ("Start Here", True),
        ("Operator Fit", st.session_state.get("phase_0_complete", False)),
        ("Opportunity Review", st.session_state.get("phase_1_complete", False)),
        ("Financial Reality", st.session_state.get("financial_model_done", False)),
        ("Commitment Review", st.session_state.get("phase_2_complete", False)),
        ("Final Decision", st.session_state.get("phase_3_complete", False)),
        ("Report", st.session_state.get("report_generated", False)),
    ]
    return [f"{name}: {'Complete' if done else 'Not complete'}" for name, done in steps]


def _overview_snapshot() -> dict[str, str]:
    phase_0 = st.session_state.get("phase_0_complete", False)
    phase_1 = st.session_state.get("phase_1_complete", False)
    financial = st.session_state.get("financial_model_done", False)
    phase_2 = st.session_state.get("phase_2_complete", False)
    phase_3 = st.session_state.get("phase_3_complete", False)

    completed = sum([phase_0, phase_1, financial, phase_2, phase_3])

    if completed == 0:
        return {
            "signal": "Early",
            "signal_explainer": "You are still at the start. Use the first pages to test fit before getting attached to the opportunity.",
            "top_risk": "Not enough evidence yet",
            "top_risk_explainer": "The biggest current risk is making assumptions before you have enough signal.",
            "stance": "Too early to call",
            "stance_explainer": "Complete the early workflow before making a recommendation.",
        }

    if not financial:
        return {
            "signal": "Promising, but incomplete",
            "signal_explainer": "You have early directional signal, but the economics have not been pressure-tested yet.",
            "top_risk": "Economics still untested",
            "top_risk_explainer": "Without a financial view, a good concept can still be a bad deal.",
            "stance": "Needs pressure testing",
            "stance_explainer": "Do not move forward confidently until the numbers hold up.",
        }

    if not phase_3:
        return {
            "signal": "Developing",
            "signal_explainer": "You have enough evidence to start forming a view, but unresolved conditions may still change the decision.",
            "top_risk": "Unresolved conditions",
            "top_risk_explainer": "Discovery gaps, assumptions, or operator mismatch may still be open.",
            "stance": "Close, but not final",
            "stance_explainer": "Use the remaining pages to convert signal into a clear recommendation.",
        }

    return {
        "signal": "Built",
        "signal_explainer": "You have enough completed work to make a more grounded recommendation.",
        "top_risk": "Execution risk",
        "top_risk_explainer": "Even good decisions can fail in execution if conditions and discipline are weak.",
        "stance": "Ready for decision",
        "stance_explainer": "Review the final decision page and report before committing.",
    }


def render_overview() -> None:
    render_beta_styles()
    open_shell()

    render_page_header(
        eyebrow="PressureTest: Franchise",
        title="Stress-test a franchise before you invest.",
        subtitle="Build a report-first read on operator fit, local economics, commitment risk, missing evidence, and Decision-Critical Issues.",
        wide=True,
    )

    render_depth_toggle()
    st.markdown(
        """
        <div class="pt-mini-grid">
            <div class="pt-mini-card"><strong>What you'll get</strong><span>A clear recommendation posture based on the information provided.</span></div>
            <div class="pt-mini-card"><strong>What to verify</strong><span>Missing evidence, FDD Translation Risk, and questions for the franchisor and advisors.</span></div>
            <div class="pt-mini-card"><strong>What matters most</strong><span>Decision-Critical Issues near the top of the report.</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    render_pressure_check(
        "PressureTest is pro-diligence. It is not legal, tax, accounting, lending, or investment advice."
    )

    next_step, next_reason = _recommended_next_step()

    render_action_banner(
        eyebrow="Recommended next step",
        title=next_step,
        body=next_reason,
        chips=["Focus", "Risk", "Decision quality"],
    )

    snapshot = _overview_snapshot()

    col1, col2, col3 = st.columns(3)

    with col1:
        render_card(
            label="Current signal",
            title=snapshot["signal"],
            body=snapshot["signal_explainer"],
            soft=True,
        )

    with col2:
        render_card(
            label="Biggest unresolved risk",
            title=snapshot["top_risk"],
            body=snapshot["top_risk_explainer"],
            soft=True,
        )

    with col3:
        render_card(
            label="Current stance",
            title=snapshot["stance"],
            body=snapshot["stance_explainer"],
            navy=True,
        )

    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

    left, right = st.columns([1.15, 1], gap="large")

    with left:
        render_section_intro(
            title="What to focus on now",
            body="Do the next step that changes the decision, not just the next step in the checklist.",
        )

        render_bullet_panel(
            label="Workflow status",
            title="Progress through the evaluation",
            items=_workflow_status(),
            empty_text="No workflow data yet.",
        )

        render_gotcha_section(
            page="overview",
            title="Watchouts to resolve",
            max_items=3,
        )

    with right:
        render_bullet_panel(
            label="Profile",
            title="Current setup",
            items=_profile_summary(),
            empty_text="Complete your profile setup to personalize the workflow.",
        )

        render_bullet_panel(
            label="How to use this",
            title="Decision discipline",
            items=[
                "Quick Assessment is the default path.",
                "Full Review is a depth toggle in the same workflow, not a separate product.",
                "The report is the core product artifact.",
                "Treat unanswered assumptions as risk, not as neutral.",
                "Use the final decision and report before committing more money or signing obligations.",
            ],
        )

    close_shell()
