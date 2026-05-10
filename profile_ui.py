from __future__ import annotations

import streamlit as st

from shared_ui import render_brand_header
<<<<<<< HEAD
from ui_styles import close_shell, open_shell, render_action_banner, render_card, render_section_intro
=======
from ui_styles import (
    close_shell,
    open_shell,
    render_card,
    render_section_intro,
)
>>>>>>> fec65288cb896b4679e84e61241f185fa625e150

UNITS_OPTIONS = ["1", "2-3", "4+"]
OWNERSHIP_OPTIONS = [
    "Owner-Operator",
    "Manager-Led",
    "Investor / Semi-Absentee",
]
<<<<<<< HEAD
TIMELINE_OPTIONS = [
    "Exploring",
    "In conversations",
    "Discovery scheduled",
    "Near decision",
    "Already committed",
]
CAPITAL_OPTIONS = [
    "Under $100k",
    "$100k-$250k",
    "$250k-$500k",
    "$500k+",
    "Not sure yet",
]
=======
>>>>>>> fec65288cb896b4679e84e61241f185fa625e150


def _get_index(options: list[str], value: str, default: str) -> int:
    selected = value if value in options else default
    return options.index(selected)


def _complete_profile() -> None:
    st.session_state["profile_complete"] = True
<<<<<<< HEAD
    st.session_state["assessment_started"] = True
=======
>>>>>>> fec65288cb896b4679e84e61241f185fa625e150
    st.session_state["current_page"] = "Overview"
    st.rerun()


def render_profile_setup() -> None:
    open_shell()

    render_brand_header(
<<<<<<< HEAD
        "PressureTest",
        "A structured diligence workspace for prospective operators.",
    )

    render_section_intro(
        title="Set up the opportunity in two minutes.",
        body=(
            "This is not account onboarding. It is the operating context needed to make the first assessment pages useful. "
            "Keep it approximate and update it later as diligence improves."
        ),
    )

    render_action_banner(
        eyebrow="First-run setup",
        title="The goal is a quick pressure snapshot, not a perfect file.",
        body="Add enough context to route the workflow. The deeper validation happens in the assessment pages.",
        chips=["2 minutes", "Editable later", "Diligence context"],
    )

=======
        "PressureTest: Franchise",
        "Stress-test a franchise before you invest.",
    )

    render_section_intro(
        title="Set up your profile before starting the evaluation.",
        body=(
            "Provide a few basics so the assessment can guide your decision flow "
            "with better context."
        ),
    )

>>>>>>> fec65288cb896b4679e84e61241f185fa625e150
    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

    info_col_1, info_col_2 = st.columns(2, gap="large")

    with info_col_1:
<<<<<<< HEAD
        st.text_input("Full name", key="full_name", placeholder="Your name")
        st.text_input("Email", key="email", placeholder="you@example.com")
        st.text_input("City / state", key="city_state", placeholder="City, State")
        st.selectbox(
            "Current stage",
            TIMELINE_OPTIONS,
            index=_get_index(TIMELINE_OPTIONS, st.session_state.get("diligence_stage", "Exploring"), "Exploring"),
            key="diligence_stage",
        )

    with info_col_2:
        st.text_input("Franchise or concept name", key="franchise_name", placeholder="Concept being evaluated")
        st.selectbox(
            "Units considered",
            UNITS_OPTIONS,
            index=_get_index(UNITS_OPTIONS, st.session_state.get("units_considered", "1"), "1"),
            key="units_considered",
        )
        st.selectbox(
            "Ownership style",
            OWNERSHIP_OPTIONS,
            index=_get_index(OWNERSHIP_OPTIONS, st.session_state.get("ownership_style", "Owner-Operator"), "Owner-Operator"),
            key="ownership_style",
        )
        st.selectbox(
            "Estimated available capital",
            CAPITAL_OPTIONS,
            index=_get_index(CAPITAL_OPTIONS, st.session_state.get("capital_range", "Not sure yet"), "Not sure yet"),
            key="capital_range",
        )
=======
        st.text_input(
            "Full Name",
            value=st.session_state.get("full_name", ""),
            key="full_name",
            placeholder="Enter your full name",
        )
        st.text_input(
            "Email",
            value=st.session_state.get("email", ""),
            key="email",
            placeholder="Enter your email",
        )
        st.text_input(
            "City / State",
            value=st.session_state.get("city_state", ""),
            key="city_state",
            placeholder="City, State",
        )

    with info_col_2:
        st.text_input(
            "Franchise or Concept Name",
            value=st.session_state.get("franchise_name", ""),
            key="franchise_name",
            placeholder="Enter franchise or concept name",
        )
        st.selectbox(
            "Units Considered",
            UNITS_OPTIONS,
            index=_get_index(
                UNITS_OPTIONS,
                st.session_state.get("units_considered", "1"),
                "1",
            ),
            key="units_considered",
        )
        st.selectbox(
            "Ownership Style",
            OWNERSHIP_OPTIONS,
            index=_get_index(
                OWNERSHIP_OPTIONS,
                st.session_state.get("ownership_style", "Owner-Operator"),
                "Owner-Operator",
            ),
            key="ownership_style",
        )
>>>>>>> fec65288cb896b4679e84e61241f185fa625e150

    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

    render_card(
<<<<<<< HEAD
        label="Commitment check",
        title="Do not treat momentum as diligence.",
        body=(
            "Mark this if you have signed documents, paid deposits, accepted financing terms, or otherwise materially committed. "
            "The app will keep this visible because post-commitment pressure is different from pre-commitment diligence."
        ),
        soft=True,
=======
        label="Commitment Check",
        title="Current process status",
        body=(
            "Indicate whether you have already signed documents or made a material "
            "commitment in the process."
        ),
>>>>>>> fec65288cb896b4679e84e61241f185fa625e150
    )

    st.checkbox(
        "I have already signed something or materially committed in the process",
<<<<<<< HEAD
=======
        value=bool(st.session_state.get("signed_anything", False)),
>>>>>>> fec65288cb896b4679e84e61241f185fa625e150
        key="signed_anything",
    )

    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

    action_col_1, action_col_2 = st.columns([1, 1], gap="large")
<<<<<<< HEAD
    with action_col_1:
        if st.button("Continue to decision cockpit", key="profile_setup_continue", use_container_width=True, type="primary"):
            _complete_profile()
    with action_col_2:
        st.caption("Next: PressureTest will point you to the first assessment step and show what is still unresolved.")
=======

    with action_col_1:
        if st.button(
            "Continue",
            key="profile_setup_continue",
            use_container_width=True,
            type="primary",
        ):
            _complete_profile()

    with action_col_2:
        st.caption("You can update these details later.")
>>>>>>> fec65288cb896b4679e84e61241f185fa625e150

    close_shell()
