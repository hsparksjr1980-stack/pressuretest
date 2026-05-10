from __future__ import annotations

import streamlit as st

from decision_engine import build_decision_packet
from local_state_io import export_json_bytes, import_json_bytes, load_demo_state
from premium_components import hero, info_card, metric_card


def _go(page: str) -> None:
    st.session_state["current_page"] = page
    st.rerun()


def _completion_pct() -> int:
    flags = [
        "profile_complete",
        "brand_analysis_done",
        "phase_0_complete",
        "phase_1_complete",
        "financial_model_done",
        "phase_2_complete",
        "phase_3_complete",
    ]
    return round(sum(bool(st.session_state.get(f)) for f in flags) / len(flags) * 100)


def _next_step() -> tuple[str, str]:
    if not st.session_state.get("brand_analysis_done"):
        return "Brand & Territory Snapshot", "Add the brand website and target territory so the assessment can surface more specific pressure points."
    if not st.session_state.get("phase_0_complete"):
        return "Franchise Fit", "Start with fit, risk tolerance, capital comfort, and operator reality."
    if not st.session_state.get("phase_1_complete"):
        return "Concept Validation", "Pressure test the business model before brand excitement drives the decision."
    if not st.session_state.get("financial_model_done"):
        return "Financial Model", "Validate the economics, runway, and assumptions that must hold up."
    if not st.session_state.get("phase_2_complete"):
        return "Post-Discovery", "Convert Discovery Day information into conditions, gaps, and no-go risks."
    if not st.session_state.get("phase_3_complete"):
        return "Final Decision", "Make the call explicit: proceed, pause, renegotiate, or walk away."
    return "Report", "Package the decision signal, supporting evidence, and remaining conditions."


def _path_step(label: str, active: bool = False) -> str:
    cls = "pt-path-step pt-path-step-active" if active else "pt-path-step"
    return f'<span class="{cls}">{label}</span>'


def _current_stage_label() -> str:
    next_page, _ = _next_step()
    if next_page == "Brand & Territory Snapshot":
        return "1. Brand Context"
    if next_page == "Franchise Fit":
        return "2. Operator Fit"
    if next_page in {"Concept Validation", "Opportunity Fit & Recommendations"}:
        return "3. Opportunity Review"
    if next_page == "Financial Model":
        return "4. Financial Reality"
    if next_page == "Post-Discovery":
        return "5. Commitment Review"
    if next_page == "Final Decision":
        return "6. Final Decision"
    return "7. Report"


def render_premium_home() -> None:
    hero(
        "Decision cockpit for franchise diligence.",
        "A guided assessment workflow that helps prospective owners separate franchise sales momentum from operational, financial, and lifestyle reality.",
    )

    current_stage = _current_stage_label()
    path_html = "".join(
        [
            _path_step("1. Brand Context", current_stage == "1. Brand Context"),
            _path_step("2. Operator Fit", current_stage == "2. Operator Fit"),
            _path_step("3. Opportunity Review", current_stage == "3. Opportunity Review"),
            _path_step("4. Financial Reality", current_stage == "4. Financial Reality"),
            _path_step("5. Commitment Review", current_stage == "5. Commitment Review"),
            _path_step("6. Final Decision", current_stage == "6. Final Decision"),
            _path_step("7. Report", current_stage == "7. Report"),
        ]
    )
    st.markdown(f'<div class="pt-path">{path_html}</div>', unsafe_allow_html=True)

    packet = build_decision_packet()
    score = packet.get("weighted_score", 0)
    confidence = packet.get("confidence", "Low")
    recommendation = packet.get("recommendation", "Not enough data")
    next_page, next_reason = _next_step()

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("Completion", f"{_completion_pct()}%", "Current browser session")
    with c2:
        metric_card("Decision score", str(score), "Updates as evidence improves")
    with c3:
        metric_card("Confidence", str(confidence), "Based on completed inputs")
    with c4:
        metric_card("Current signal", str(recommendation), "Not final until locked")

    st.markdown("### Recommended next move")
    left, right = st.columns([2, 1])
    with left:
        info_card(next_page, next_reason, "next best action")
    with right:
        if st.button(f"Open {next_page}", type="primary", use_container_width=True):
            _go(next_page)
        if st.button("Load demo scenario", use_container_width=True):
            load_demo_state()
            st.rerun()

    st.markdown("### Guided workflow")
    a, b, c = st.columns(3)
    with a:
        info_card("Brand & Territory", "Add the brand website, target market, and competitor context so the assessment starts with local operating reality.", "context")
    with b:
        info_card("Operator Fit", "Assess whether the business fits your lifestyle, downside tolerance, available capital, and expected role as an owner.", "fit")
    with c:
        info_card("Opportunity Review", "Evaluate the concept, market maturity, franchisor support, operational complexity, and hidden execution risks.", "pressure test")

    d, e, f = st.columns(3)
    with d:
        info_card("Financial Reality", "Model revenue, margins, buildout, rent, debt, and runway to see what has to be true for the deal to work.", "economics")
    with e:
        info_card("Final Decision", "Turn the evidence into a clear decision: proceed, proceed with conditions, pause, renegotiate, or walk away.", "decision")
    with f:
        info_card("Execution Tools", "Deal workspace, lender/lease tracking, buildout planning, and launch tools are intentionally preview-only until paid access is connected.", "coming later")

    st.markdown("### Save or reload a session")
    s1, s2 = st.columns(2)
    with s1:
        st.download_button(
            "Download local assessment JSON",
            data=export_json_bytes(),
            file_name="pressuretest_assessment.json",
            mime="application/json",
            use_container_width=True,
        )
    with s2:
        uploaded = st.file_uploader("Import assessment JSON", type=["json"], label_visibility="collapsed")
        if uploaded is not None:
            ok, message = import_json_bytes(uploaded.getvalue())
            if ok:
                st.success(message)
                st.rerun()
            else:
                st.error(message)
