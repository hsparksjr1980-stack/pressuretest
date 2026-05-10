from __future__ import annotations

import streamlit as st

from branding import APP_PRODUCT
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

<<<<<<< HEAD
WORKFLOW_STEPS: list[tuple[str, str, str]] = [
    ("Operator Fit", "Franchise Fit", "Test time demand, downside tolerance, and owner-role fit."),
    ("Brand Context", "Brand & Territory Snapshot", "Add brand, territory, and local-market context."),
    ("Concept Validation", "Concept Validation", "Pressure-test demand, unit economics claims, and operating complexity."),
    ("Financial Reality", "Financial Model", "Model startup cost, runway, ramp, and margin pressure."),
    ("Decision Output", "Free Report", "Package a first summary of open risks and next steps."),
]


def _go_to(page_name: str) -> None:
    st.session_state["current_page"] = page_name
    st.rerun()


def _recommended_next_step() -> tuple[str, str]:
    if not st.session_state.get("phase_0_complete"):
        return "Franchise Fit", "Start with operator fit before spending more time on brand story or economics."
    if not st.session_state.get("brand_analysis_done"):
        return "Brand & Territory Snapshot", "Add brand and territory context so the rest of the workflow is less generic."
    if not st.session_state.get("phase_1_complete"):
        return "Concept Validation", "Pressure-test the concept before momentum makes weak assumptions feel settled."
    if not st.session_state.get("financial_model_done"):
        return "Financial Model", "Check economics, ramp, and capital pressure before treating the opportunity as viable."
    if not st.session_state.get("free_report_generated"):
        return "Free Report", "Package the current signal into a usable first diligence summary."
    if not st.session_state.get("phase_2_complete"):
        return "Post-Discovery", "Use discovery answers to convert unknowns into conditions, gaps, or no-go issues."
    return "Final Decision", "Bring the evidence together and decide whether to proceed, pause, renegotiate, or walk away."


def _profile_summary() -> list[str]:
    fields = [
        ("Operator", st.session_state.get("full_name")),
        ("Concept", st.session_state.get("franchise_name")),
        ("Market", st.session_state.get("city_state")),
        ("Units", st.session_state.get("units_considered")),
        ("Ownership style", st.session_state.get("ownership_style")),
        ("Stage", st.session_state.get("diligence_stage")),
        ("Capital range", st.session_state.get("capital_range")),
    ]
    return [f"{label}: {value}" for label, value in fields if value]


def _step_done(page_name: str) -> bool:
    completion_map = {
        "Franchise Fit": bool(st.session_state.get("phase_0_complete")),
        "Brand & Territory Snapshot": bool(st.session_state.get("brand_analysis_done")),
        "Concept Validation": bool(st.session_state.get("phase_1_complete")),
        "Financial Model": bool(st.session_state.get("financial_model_done")),
        "Free Report": bool(st.session_state.get("free_report_generated")),
    }
    return completion_map.get(page_name, False)


def _workflow_status() -> list[str]:
    return [f"{label}: {'Complete' if _step_done(page) else 'Open'}" for label, page, _ in WORKFLOW_STEPS]


def _completion_count() -> int:
    return sum(1 for _, page, _ in WORKFLOW_STEPS if _step_done(page))


def _overview_snapshot() -> dict[str, str]:
    completed = _completion_count()
    signed = bool(st.session_state.get("signed_anything"))

    if completed == 0:
        return {
            "signal": "Not enough evidence yet",
            "signal_explainer": "The opportunity may still be interesting, but the current file does not support a decision.",
            "top_risk": "Assumption risk",
            "top_risk_explainer": "Early enthusiasm can hide unknowns around owner role, capital need, ramp, and local execution.",
            "stance": "Start the pressure snapshot",
            "stance_explainer": "Complete operator fit first, then add brand context and financial pressure testing.",
        }

    if signed and completed < 4:
        return {
            "signal": "Commitment pressure present",
            "signal_explainer": "You flagged that something may already be signed or materially committed.",
            "top_risk": "Reduced optionality",
            "top_risk_explainer": "After commitment, unresolved assumptions become execution risks instead of diligence questions.",
            "stance": "Document gaps now",
            "stance_explainer": "Use the remaining pages to identify what must be validated quickly.",
        }

    if not st.session_state.get("financial_model_done"):
        return {
            "signal": "Developing",
            "signal_explainer": "You have some early signal, but economics have not been pressure-tested yet.",
            "top_risk": "Untested financial reality",
            "top_risk_explainer": "A concept can look strong and still fail the working-capital, ramp, or margin test.",
            "stance": "Keep validating",
            "stance_explainer": "Move through concept validation and financial modeling before forming a decision view.",
        }

    return {
        "signal": "Usable diligence file forming",
        "signal_explainer": "Enough of the workflow is complete to start summarizing risks and conditions.",
        "top_risk": "Execution discipline",
        "top_risk_explainer": "The remaining issue is whether the assumptions can survive launch, staffing, buildout, and cash-pressure realities.",
        "stance": "Prepare decision output",
        "stance_explainer": "Generate the report, then use final decision pages for proceed / pause / walk-away discipline.",
    }


def _render_workflow_cards() -> None:
    for label, page, body in WORKFLOW_STEPS:
        done = _step_done(page)
        status = "Complete" if done else "Open"
        cols = st.columns([.18, .62, .2])
        with cols[0]:
            st.markdown(f"<div class='pt-pill'>{status}</div>", unsafe_allow_html=True)
        with cols[1]:
            st.markdown(f"**{label}**  \n{body}")
        with cols[2]:
            if st.button("Open", key=f"overview_open_{page}", use_container_width=True):
                _go_to(page)
        st.markdown("<hr style='margin:.55rem 0; border:none; border-top:1px solid #E5E7EB;' />", unsafe_allow_html=True)



# Local compatibility override for older positional render_card calls
def render_card(*args, soft=False, **kwargs):
    import streamlit as st

    title = kwargs.get("title", args[0] if len(args) > 0 else "")
    value = kwargs.get("value", args[1] if len(args) > 1 else "")
    body = kwargs.get("body", args[2] if len(args) > 2 else kwargs.get("content", ""))

    bg = "#F8FAFC" if soft else "#FFFFFF"
    border = "#E5E7EB"

    st.markdown(
        f"""
        <div style="background:{bg}; border:1px solid {border}; border-radius:14px; padding:18px; margin:10px 0;">
            <div style="font-size:0.85rem; color:#64748B; font-weight:600; margin-bottom:6px;">{title}</div>
            <div style="font-size:1.25rem; color:#0F172A; font-weight:700; margin-bottom:6px;">{value}</div>
            <div style="font-size:0.95rem; color:#475569; line-height:1.5;">{body}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


=======

def _recommended_next_step() -> tuple[str, str]:
    if not st.session_state.get("phase_0_complete"):
        return (
            "Franchise Fit",
            "Start by testing whether the ownership model, time demand, and downside fit you.",
        )
    if not st.session_state.get("phase_1_complete"):
        return (
            "Concept Validation",
            "Pressure-test the concept before you give more weight to momentum or brand story.",
        )
    if not st.session_state.get("financial_model_done"):
        return (
            "Financial Model",
            "Check the economics before treating the opportunity as investable.",
        )
    if not st.session_state.get("phase_2_complete"):
        return (
            "Post-Discovery",
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
        ("Franchise Fit", st.session_state.get("phase_0_complete", False)),
        ("Concept Validation", st.session_state.get("phase_1_complete", False)),
        ("Financial Model", st.session_state.get("financial_model_done", False)),
        ("Post-Discovery", st.session_state.get("phase_2_complete", False)),
        ("Final Decision", st.session_state.get("phase_3_complete", False)),
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


>>>>>>> fec65288cb896b4679e84e61241f185fa625e150
def render_overview() -> None:
    open_shell()

    render_page_header(
        eyebrow=APP_PRODUCT,
<<<<<<< HEAD
        title="Decision Cockpit",
        subtitle="Start with the next step that improves decision quality. Keep assumptions visible until they are validated.",
=======
        title="Overview",
        subtitle="Use this page to see what matters now, where the risk is, and what to do next.",
>>>>>>> fec65288cb896b4679e84e61241f185fa625e150
        wide=True,
    )

    next_step, next_reason = _recommended_next_step()
<<<<<<< HEAD
    completed = _completion_count()

    render_action_banner(
        eyebrow="Recommended next action",
        title=next_step,
        body=next_reason,
        chips=[f"{completed}/{len(WORKFLOW_STEPS)} core steps complete", "Guided flow", "Operator-focused"],
    )

    if st.button(f"Continue: {next_step}", type="primary", use_container_width=True, key="overview_continue_next"):
        _go_to(next_step)

    snapshot = _overview_snapshot()
    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3, gap="large")
    with col1:
        render_card("Current signal", snapshot["signal"], snapshot["signal_explainer"], soft=True)
    with col2:
        render_card("Biggest unresolved risk", snapshot["top_risk"], snapshot["top_risk_explainer"], soft=True)
    with col3:
        render_card("Current stance", snapshot["stance"], snapshot["stance_explainer"], navy=True)

    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

    left, right = st.columns([1.2, .8], gap="large")
    with left:
        render_section_intro(
            title="Core assessment path",
            body="This replaces a phase-heavy starting experience with a clearer first-run path.",
        )
        _render_workflow_cards()
        render_gotcha_section(page="overview", title="Watchouts to resolve", max_items=3)

    with right:
        render_bullet_panel(
            label="Opportunity profile",
            title="Current setup",
            items=_profile_summary(),
            empty_text="Complete first-run setup to personalize the workflow.",
        )
        render_bullet_panel(
            label="Progress",
            title="Assessment status",
            items=_workflow_status(),
        )
        render_bullet_panel(
            label="Decision discipline",
            title="How to use this page",
            items=[
                "Do not skip economics because the brand story feels strong.",
                "Treat unanswered assumptions as open risk, not neutral information.",
                "Use the report only after the core steps have enough evidence.",
=======

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
                "Focus first on fit, then concept, then economics.",
                "Treat unanswered assumptions as risk, not as neutral.",
                "Use the final decision only after the earlier pages are complete.",
>>>>>>> fec65288cb896b4679e84e61241f185fa625e150
            ],
        )

    close_shell()
