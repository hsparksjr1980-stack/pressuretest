# /Users/howardsparks/Desktop/pressuretest/final_decision_ui.py

from __future__ import annotations

import streamlit as st

<<<<<<< HEAD
from decision_engine import build_decision_packet
=======
>>>>>>> fec65288cb896b4679e84e61241f185fa625e150
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
<<<<<<< HEAD
        subtitle="Make the call after the evidence is on the table. The goal is not to sell yourself on the deal — it is to decide whether the opportunity survives pressure.",
=======
        subtitle="Make the call only after the earlier work is complete. This page should clarify whether to proceed, pause, or walk away.",
>>>>>>> fec65288cb896b4679e84e61241f185fa625e150
        wide=True,
    )

    snapshot = _decision_snapshot()
<<<<<<< HEAD
    decision_packet = build_decision_packet()
    base_score = decision_packet.get("base_score", decision_packet.get("weighted_score"))
    final_score = decision_packet.get("final_score", base_score)
    brand_adjustment = decision_packet.get("brand_intelligence_adjustment", 0) or 0
    brand_level = decision_packet.get("brand_intelligence_level", "Low / Unknown")
    brand_signals = decision_packet.get("brand_intelligence_signals", []) or []
    brand_note = decision_packet.get("brand_intelligence_note", "")
=======
>>>>>>> fec65288cb896b4679e84e61241f185fa625e150

    render_action_banner(
        eyebrow="Decision state",
        title=str(snapshot["stance"]),
        body=str(snapshot["stance_body"]),
<<<<<<< HEAD
        chips=["Blunt read", "Risk", "Conditions", "Not legal advice"],
=======
        chips=["Decision", "Risk", "Conditions"],
>>>>>>> fec65288cb896b4679e84e61241f185fa625e150
    )

    col1, col2, col3 = st.columns(3, gap="large")

<<<<<<< HEAD
    def _fmt_score(value: object) -> str:
        try:
            return f"{float(value):.0f}/100"
        except Exception:
            return "—"

    with col1:
        render_card(
            label="Base diligence score",
            title=_fmt_score(base_score),
            body="Built from the core assessment, financial review, guardrails, and user-entered diligence inputs.",
=======
    with col1:
        render_card(
            label="Current stance",
            title=str(snapshot["stance"]),
            body=str(snapshot["stance_body"]),
>>>>>>> fec65288cb896b4679e84e61241f185fa625e150
            navy=True,
        )

    with col2:
<<<<<<< HEAD
        adj_display = f"{int(brand_adjustment):+d} pts" if isinstance(brand_adjustment, (int, float)) else "0 pts"
        render_card(
            label="Brand / territory adjustment",
            title=adj_display,
            body=f"Risk level: {brand_level}. This reflects AI/manual brand notes, closure signals, market fit, and territory pressure.",
=======
        render_card(
            label="Main unresolved risk",
            title=str(snapshot["top_risk"]),
            body=str(snapshot["top_risk_body"]),
>>>>>>> fec65288cb896b4679e84e61241f185fa625e150
            soft=True,
        )

    with col3:
        render_card(
<<<<<<< HEAD
            label="Final PressureTest score",
            title=_fmt_score(final_score),
            body=f"Recommendation: {decision_packet.get('recommendation', 'Review required')}. The final call includes brand intelligence when available.",
        )

    # Blunt decision read: make the score interpretable instead of just numeric.
    blunt_items = []
    try:
        fs = float(final_score or 0)
    except Exception:
        fs = 0
    if fs < 55:
        blunt_items.append("This does not currently survive the pressure test. Treat the default answer as no unless the facts materially improve.")
    elif fs < 70:
        blunt_items.append("This is not a clean yes. The burden of proof is on the deal, not on you to rationalize it.")
    elif fs < 82:
        blunt_items.append("The deal may be viable, but only if the open conditions are specific, measurable, and resolved before signing.")
    else:
        blunt_items.append("The current signal is comparatively stronger, but strong scores do not replace FDD review, operator validation, lender review, or legal review.")
    if brand_adjustment < 0:
        blunt_items.append("Brand and territory research reduced the score. Do not ignore closure, expansion, competition, or market-fit signals just because the concept is attractive.")
    blunt_items.append("PressureTest is an operating diligence tool. It is not legal, tax, lending, accounting, or investment advice.")
    render_bullet_panel(
        label="Blunt read",
        title="What the score is really saying",
        items=blunt_items,
    )

    if brand_adjustment < 0 or brand_signals:
        st.markdown('<div class="rc-gap-sm"></div>', unsafe_allow_html=True)
        render_bullet_panel(
            label="Brand intelligence carried forward",
            title="Signals affecting the final decision",
            items=[str(x) for x in brand_signals[:6]],
            empty_text=brand_note or "No brand intelligence signals have been generated yet.",
        )
    elif not st.session_state.get("brand_territory_analysis"):
        st.info("Brand/territory intelligence has not been generated yet. The final decision is currently based only on the core assessment. Add a Brand & Territory Snapshot to include closure, expansion, and territory signals in the score.")

=======
            label="Decision discipline",
            title="Proceed only on explicit terms",
            body="Do not use optimism, momentum, or sunk time as a substitute for evidence.",
        )

>>>>>>> fec65288cb896b4679e84e61241f185fa625e150
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
<<<<<<< HEAD
            str(decision_packet.get("summary") or _default_rationale(selected_option)),
=======
            _default_rationale(selected_option),
>>>>>>> fec65288cb896b4679e84e61241f185fa625e150
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
<<<<<<< HEAD
            "\n".join([str(x) for x in decision_packet.get("conditions", snapshot["conditions"])]) if selected_option == "Proceed with Conditions" else "",
=======
            "\n".join(snapshot["conditions"]) if selected_option == "Proceed with Conditions" else "",
>>>>>>> fec65288cb896b4679e84e61241f185fa625e150
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
<<<<<<< HEAD
            items=[str(item) for item in decision_packet.get("conditions", snapshot["conditions"])],
=======
            items=[str(item) for item in snapshot["conditions"]],
>>>>>>> fec65288cb896b4679e84e61241f185fa625e150
            empty_text="No conditions listed yet.",
        )

        render_bullet_panel(
            label="Use this page well",
            title="Decision quality rules",
            items=[
<<<<<<< HEAD
                "Do not let sunk cost, excitement, or broker/franchisor pressure force a yes.",
                "Treat unresolved assumptions as risk.",
                "Write down the exact reason for your decision.",
                "Use conditions when the answer is not a clean yes — and walk if the conditions are not met.",
=======
                "Do not let sunk cost force a yes.",
                "Treat unresolved assumptions as risk.",
                "Write down the exact reason for your decision.",
                "Use conditions when the answer is not a clean yes.",
>>>>>>> fec65288cb896b4679e84e61241f185fa625e150
            ],
        )

    close_shell()
