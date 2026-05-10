# phase_gate.py

from __future__ import annotations

from typing import Final

import streamlit as st

from page_config import FREE_PAGES, PRO_PAGES


PRO_UNLOCK_DECISION_KEY: Final[str] = "move_forward"
PREMIUM_ACCESS_KEY: Final[str] = "premium_access"
DEV_OVERRIDE_KEY: Final[str] = "dev_pro_access"

PRO_UNLOCK_DECISION_MESSAGE: Final[str] = (
<<<<<<< HEAD
    "Execution tools are designed for users who have decided to move forward. "
    "Finish Final Decision first, then upgrade when you are ready to manage the actual deal."
)
PRO_PREMIUM_REQUIRED_MESSAGE: Final[str] = (
    "This section is part of PressureTest Pro. Free gives you the assessment and decision summary; "
    "Pro unlocks the execution workspace, scenario planning, and lender-ready outputs."
)
UNKNOWN_PAGE_MESSAGE: Final[str] = "This section is not available."

FREE_POSITIONING: Final[dict[str, object]] = {
    "headline": "Free helps you decide whether the opportunity deserves more diligence.",
    "summary": (
        "Use the free workflow to organize the opportunity, test operator fit, review concept assumptions, "
        "run a baseline financial model, and generate a decision summary."
    ),
    "includes": [
        "Guided diligence assessment",
        "Operator fit and concept validation",
        "Baseline financial reality check",
        "Free report and decision summary",
    ],
}

PRO_POSITIONING: Final[dict[str, object]] = {
    "headline": "Pro helps you manage execution risk after the deal becomes real.",
    "summary": (
        "Upgrade when you need to turn the diligence file into a working execution plan: scenarios, lender prep, "
        "lease and buildout tracking, launch sequencing, and exportable operating packets."
    ),
    "includes": [
        "Deal workspace and assumption tracking",
        "Scenario planning and working-capital review",
        "Buildout and launch readiness tracking",
        "Execution report for partners, lenders, and internal review",
    ],
}

=======
    "Pro pages unlock only after you choose Move Forward in Final Decision."
)
PRO_PREMIUM_REQUIRED_MESSAGE: Final[str] = "This page requires Pro access."
UNKNOWN_PAGE_MESSAGE: Final[str] = "This section is not available."

>>>>>>> fec65288cb896b4679e84e61241f185fa625e150

def _has_dev_override() -> bool:
    return bool(st.session_state.get(DEV_OVERRIDE_KEY, False))


def _has_premium_access() -> bool:
    return bool(st.session_state.get(PREMIUM_ACCESS_KEY, False)) or _has_dev_override()


def _has_pro_unlock_decision() -> bool:
    return bool(st.session_state.get(PRO_UNLOCK_DECISION_KEY, False)) or _has_dev_override()


<<<<<<< HEAD
def has_execution_access() -> bool:
    """Paid access check for post-decision execution tools."""
    return _has_premium_access()


def has_completed_forward_decision() -> bool:
    """Workflow readiness check for Pro positioning and CTA language."""
    return _has_pro_unlock_decision()


=======
>>>>>>> fec65288cb896b4679e84e61241f185fa625e150
def is_free_page(page_name: str) -> bool:
    return page_name in FREE_PAGES


def is_pro_page(page_name: str) -> bool:
    return page_name in PRO_PAGES


def get_unlock_failure_reason(page_name: str) -> str | None:
    if is_free_page(page_name):
        return None

    if is_pro_page(page_name):
        if not _has_pro_unlock_decision():
            return PRO_UNLOCK_DECISION_MESSAGE

        if not _has_premium_access():
            return PRO_PREMIUM_REQUIRED_MESSAGE

        return None

    return UNKNOWN_PAGE_MESSAGE


def is_page_unlocked(page_name: str) -> tuple[bool, str | None]:
    reason = get_unlock_failure_reason(page_name)
    return reason is None, reason


def guard_page_or_warn(page_name: str) -> bool:
    unlocked, reason = is_page_unlocked(page_name)
    if unlocked:
        return True

    if reason:
        st.warning(reason)
    else:
        st.warning(UNKNOWN_PAGE_MESSAGE)

    return False
