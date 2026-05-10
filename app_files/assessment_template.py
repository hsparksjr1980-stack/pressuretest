from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import streamlit as st

from premium_components import esc


@dataclass(frozen=True)
class AssessmentQuestion:
    key: str
    label: str
    kind: str = "text"  # text | textarea | select | number
    placeholder: str = ""
    help_text: str = ""
    options: Sequence[str] | None = None
    min_value: int = 0
    max_value: int = 100
    step: int = 1


@dataclass(frozen=True)
class AssessmentGroup:
    title: str
    description: str
    questions: Sequence[AssessmentQuestion]


def _is_answered(question: AssessmentQuestion) -> bool:
    value = st.session_state.get(question.key)
    if question.kind == "select":
        return value is not None and value not in ("", "Select one...")
    if question.kind == "number":
        return value is not None
    return bool(str(value or "").strip())


def _render_question(question: AssessmentQuestion) -> None:
    if question.kind == "textarea":
        st.text_area(
            question.label,
            key=question.key,
            placeholder=question.placeholder,
            help=question.help_text or None,
            height=110,
        )
        return

    if question.kind == "select":
        options = list(question.options or [])
        if not options:
            options = ["Select one..."]
        st.selectbox(
            question.label,
            options=options,
            key=question.key,
            help=question.help_text or None,
        )
        return

    if question.kind == "number":
        st.number_input(
            question.label,
            min_value=question.min_value,
            max_value=question.max_value,
            step=question.step,
            key=question.key,
            help=question.help_text or None,
        )
        return

    st.text_input(
        question.label,
        key=question.key,
        placeholder=question.placeholder,
        help=question.help_text or None,
    )


def render_assessment_template(
    *,
    section_title: str,
    context_description: str,
    groups: Sequence[AssessmentGroup],
    why_this_matters: str,
    next_step_guidance: str,
) -> None:
    st.markdown(
        f"""
        <div class="pt-card">
          <div class="pt-eyebrow">Assessment</div>
          <h3 style="margin:.1rem 0 .35rem 0;">{esc(section_title)}</h3>
          <p>{esc(context_description)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    total_questions = sum(len(group.questions) for group in groups)
    answered = sum(1 for group in groups for question in group.questions if _is_answered(question))
    progress = (answered / total_questions) if total_questions else 0.0

    metric_col, progress_col = st.columns([1, 2], gap="large")
    with metric_col:
        st.markdown(
            f"""
            <div class="pt-card">
              <div class="pt-eyebrow">Progress</div>
              <h3 style="margin:.1rem 0 .2rem 0;">{answered} of {total_questions}</h3>
              <p>Complete each section for a more reliable diligence read.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with progress_col:
        st.progress(progress)

    st.markdown('<div class="pt-divider"></div>', unsafe_allow_html=True)

    for idx, group in enumerate(groups, start=1):
        with st.expander(f"{idx}. {group.title}", expanded=(idx == 1)):
            st.caption(group.description)
            for question in group.questions:
                _render_question(question)

    st.markdown('<div class="pt-divider"></div>', unsafe_allow_html=True)

    helper_col, next_col = st.columns(2, gap="large")
    with helper_col:
        st.markdown(
            f"""
            <div class="pt-note">
              <strong>Why this matters</strong><br/>
              {esc(why_this_matters)}
            </div>
            """,
            unsafe_allow_html=True,
        )
    with next_col:
        st.markdown(
            f"""
            <div class="pt-note">
              <strong>Next step guidance</strong><br/>
              {esc(next_step_guidance)}
            </div>
            """,
            unsafe_allow_html=True,
        )
