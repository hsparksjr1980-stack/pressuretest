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
    "Move Forward",
    "Proceed Only If Conditions Are Met",
    "Walk Away",
]

LEGACY_OPTION_MAP = {
    "Proceed": "Move Forward",
    "Proceed with Conditions": "Proceed Only If Conditions Are Met",
    "Pause": "Proceed Only If Conditions Are Met",
    "Do Not Proceed": "Walk Away",
}


def _normalize_final_choice(value: object) -> str:
    choice = str(value or "Proceed Only If Conditions Are Met")
    return LEGACY_OPTION_MAP.get(choice, choice if choice in FINAL_OPTIONS else "Proceed Only If Conditions Are Met")


def _decision_snapshot() -> dict[str, object]:
    phase_0 = bool(st.session_state.get("phase_0_complete", False))
    phase_1 = bool(st.session_state.get("phase_1_complete", False))
    financial = bool(st.session_state.get("financial_model_done", False))
    phase_2 = bool(st.session_state.get("phase_2_complete", False))

    completed = sum([phase_0, phase_1, financial, phase_2])

    if completed <= 1:
        return {
            "stance": "Too early to commit",
            "stance_body": "Based on the information provided, there is not enough completed work to make a reliable decision.",
            "top_risk": "Decision made before enough evidence",
            "top_risk_body": "This may indicate risk because fit, opportunity quality, and economics have not all been pressure-tested.",
            "conditions": [
                "Complete Operator Fit",
                "Complete Opportunity Review",
                "Pressure-test the economics",
            ],
            "default_option": "Proceed Only If Conditions Are Met",
        }

    if not financial:
        return {
            "stance": "Needs economic validation",
            "stance_body": "Based on the information provided, the economics are not complete enough to support a cleaner recommendation.",
            "top_risk": "Weak or untested economics",
            "top_risk_body": "This should be verified because a concept can look promising and still fail under the numbers.",
            "conditions": [
                "Finish Financial Reality",
                "Test downside assumptions",
                "Confirm capital and cash-flow tolerance",
            ],
            "default_option": "Proceed Only If Conditions Are Met",
        }

    if not phase_2:
        return {
            "stance": "Close, but not decision-ready",
            "stance_body": "Based on the information provided, discovery gaps and unresolved assumptions may still change the recommendation.",
            "top_risk": "Unresolved conditions",
            "top_risk_body": "Outstanding items may materially change the real risk, cost, or operating burden.",
            "conditions": [
                "Complete Commitment Review",
                "Resolve major unknowns",
                "List explicit move-forward or walk-away conditions",
            ],
            "default_option": "Proceed Only If Conditions Are Met",
        }

    return {
        "stance": "Ready for a final call",
        "stance_body": "Based on the information provided, there is enough completed work to choose a disciplined decision posture.",
        "top_risk": "Execution risk",
        "top_risk_body": "This should be verified because sequencing, capital discipline, and operator readiness still matter.",
        "conditions": [
            "Confirm final assumptions",
            "Document non-negotiables",
            "Move forward only if required conditions remain true",
        ],
        "default_option": "Proceed Only If Conditions Are Met",
    }


def _default_rationale(selected_option: str) -> str:
    defaults = {
        "Move Forward": "Based on the information provided, the evidence appears strong enough to continue diligence while still verifying assumptions.",
        "Proceed Only If Conditions Are Met": "Based on the information provided, the opportunity may remain viable only if specific risks are resolved first.",
        "Walk Away": "Based on the information provided, the current risk profile appears too unresolved to continue without major changes.",
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
        subtitle="Make the call only after the earlier work is complete. The goal is a disciplined decision posture, not a sales-style yes/no.",
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
            title="Use evidence, not momentum",
            body="Do not use optimism, pressure, or sunk time as a substitute for verified evidence.",
        )

    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

    left, right = st.columns([1.1, 1], gap="large")

    with left:
        render_section_intro(
            title="Make the call",
            body="Choose the option that best matches the evidence, then write the reasoning in plain English.",
        )

        saved_choice = _normalize_final_choice(st.session_state.get("final_decision_choice", str(snapshot["default_option"])))
        default_index = FINAL_OPTIONS.index(saved_choice)

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
            "\n".join(snapshot["conditions"]) if selected_option == "Proceed Only If Conditions Are Met" else "",
        )
        conditions_text = st.text_area(
            "Required conditions before moving forward",
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
            title="What must be true before moving forward",
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
                "Use conditions when the answer is not clean.",
            ],
        )

    close_shell()
