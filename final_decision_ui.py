# /Users/howardsparks/Desktop/pressuretest/final_decision_ui.py

from __future__ import annotations

import streamlit as st

from branding import APP_PRODUCT
from ui_styles import (
    close_shell,
    open_shell,
    render_action_banner,
    render_bullet_panel,
    render_card,
    render_page_header,
    render_section_intro,
)


FINAL_OPTIONS = [
    "Proceed",
    "Proceed with Conditions",
    "Pause",
    "Do Not Proceed",
]


def _decision_snapshot() -> dict[str, object]:
    phase_0 = bool(st.session_state.get("phase_0_complete", False))
    phase_1 = bool(st.session_state.get("phase_1_complete", False))
    financial = bool(st.session_state.get("financial_model_done", False))
    phase_2 = bool(st.session_state.get("phase_2_complete", False))

    completed = sum([phase_0, phase_1, financial, phase_2])

    if completed <= 1:
        return {
            "stance": "Too early to commit",
            "stance_body": "You do not yet have enough completed work to make a confident go / no-go call.",
            "top_risk": "Decision made before enough evidence",
            "top_risk_body": "The biggest risk right now is forcing a conclusion before fit, concept, and economics have been pressure-tested.",
            "conditions": [
                "Complete Franchise Fit",
                "Complete Concept Validation",
                "Pressure-test the economics",
            ],
            "default_option": "Pause",
        }

    if not financial:
        return {
            "stance": "Needs economic validation",
            "stance_body": "You may have directional signal, but the economics are not complete enough to support a confident recommendation.",
            "top_risk": "Weak or untested economics",
            "top_risk_body": "A concept that looks promising can still be the wrong deal if the numbers do not hold up.",
            "conditions": [
                "Finish the Financial Model",
                "Test downside assumptions",
                "Confirm capital and cash-flow tolerance",
            ],
            "default_option": "Pause",
        }

    if not phase_2:
        return {
            "stance": "Close, but not decision-ready",
            "stance_body": "The deal is starting to take shape, but discovery gaps and unresolved assumptions can still change the recommendation.",
            "top_risk": "Unresolved conditions",
            "top_risk_body": "Outstanding discovery items may materially change the real risk, cost, or operating burden.",
            "conditions": [
                "Complete Post-Discovery Review",
                "Resolve major unknowns",
                "List explicit proceed / walk-away conditions",
            ],
            "default_option": "Proceed with Conditions",
        }

    return {
        "stance": "Ready for a final call",
        "stance_body": "You have enough completed work to make a more disciplined final recommendation.",
        "top_risk": "Execution risk",
        "top_risk_body": "Even a good decision can fail if sequencing, capital discipline, or operator readiness are weak.",
        "conditions": [
            "Confirm final assumptions",
            "Document your non-negotiables",
            "Proceed only if conditions remain true",
        ],
        "default_option": "Proceed with Conditions",
    }


def _default_rationale(selected_option: str) -> str:
    defaults = {
        "Proceed": "The evidence is strong enough to move forward without major open conditions.",
        "Proceed with Conditions": "The opportunity may work, but only if specific risks are resolved first.",
        "Pause": "More work is needed before making a high-confidence decision.",
        "Do Not Proceed": "The current evidence suggests the opportunity is not strong enough to justify moving forward.",
    }
    return defaults[selected_option]


def _save_final_decision(selected_option: str, rationale: str, conditions_text: str) -> None:
    st.session_state["final_decision_choice"] = selected_option
    st.session_state["final_decision_rationale"] = rationale.strip()
    st.session_state["final_decision_conditions"] = conditions_text.strip()
    st.session_state["phase_3_complete"] = True


def render_final_decision() -> None:
    open_shell()

    render_page_header(
        eyebrow=APP_PRODUCT,
        title="Final Decision",
        subtitle="Make the call only after the earlier work is complete. This page should clarify whether to proceed, pause, or walk away.",
        wide=True,
    )

    snapshot = _decision_snapshot()

    render_action_banner(
        eyebrow="Decision state",
        title=str(snapshot["stance"]),
        body=str(snapshot["stance_body"]),
        chips=["Decision", "Risk", "Conditions"],
    )

    col1, col2, col3 = st.columns(3, gap="large")

    with col1:
        render_card(
            label="Current stance",
            title=str(snapshot["stance"]),
            body=str(snapshot["stance_body"]),
            navy=True,
        )

    with col2:
        render_card(
            label="Main unresolved risk",
            title=str(snapshot["top_risk"]),
            body=str(snapshot["top_risk_body"]),
            soft=True,
        )

    with col3:
        render_card(
            label="Decision discipline",
            title="Proceed only on explicit terms",
            body="Do not use optimism, momentum, or sunk time as a substitute for evidence.",
        )

    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

    left, right = st.columns([1.1, 1], gap="large")

    with left:
        render_section_intro(
            title="Make the call",
            body="Choose the option that best matches the evidence, then write the reasoning in plain English.",
        )

        saved_choice = st.session_state.get("final_decision_choice", str(snapshot["default_option"]))
        default_index = FINAL_OPTIONS.index(saved_choice) if saved_choice in FINAL_OPTIONS else FINAL_OPTIONS.index(str(snapshot["default_option"]))

        selected_option = st.radio(
            "Final recommendation",
            options=FINAL_OPTIONS,
            index=default_index,
            key="final_decision_choice_radio",
        )

        rationale_default = st.session_state.get(
            "final_decision_rationale",
            _default_rationale(selected_option),
        )
        rationale = st.text_area(
            "Why this recommendation exists",
            value=rationale_default,
            key="final_decision_rationale_input",
            height=140,
            placeholder="State the reasoning clearly and directly.",
        )

        conditions_default = st.session_state.get(
            "final_decision_conditions",
            "\n".join(snapshot["conditions"]) if selected_option == "Proceed with Conditions" else "",
        )
        conditions_text = st.text_area(
            "Required conditions before proceeding",
            value=conditions_default,
            key="final_decision_conditions_input",
            height=120,
            placeholder="List explicit conditions, thresholds, or must-resolve items.",
        )

        if st.button("Save Final Decision", type="primary", use_container_width=True):
            _save_final_decision(selected_option, rationale, conditions_text)
            st.success("Final decision saved.")

    with right:
        render_bullet_panel(
            label="Required conditions",
            title="What must be true before you move forward",
            items=[str(item) for item in snapshot["conditions"]],
            empty_text="No conditions listed yet.",
        )

        render_bullet_panel(
            label="Use this page well",
            title="Decision quality rules",
            items=[
                "Do not let sunk cost force a yes.",
                "Treat unresolved assumptions as risk.",
                "Write down the exact reason for your decision.",
                "Use conditions when the answer is not a clean yes.",
            ],
        )

    close_shell()
