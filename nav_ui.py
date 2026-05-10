import streamlit as st
<<<<<<< HEAD

from page_config import PAGES, PRO_PAGES
from phase_gate import is_page_unlocked

OUTCOME_LABELS = {
    "Overview": "Decision Cockpit",
    "Brand & Territory Snapshot": "Brand Context",
    "Franchise Fit": "Operator Fit",
    "Concept Validation": "Concept Validation",
    "Opportunity Fit & Recommendations": "Recommendation Signal",
    "Financial Model": "Financial Reality",
    "Free Report": "First Report",
    "Post-Discovery": "Discovery Review",
    "Final Decision": "Final Decision",
    "Report": "Decision Report",
    "Plans & Support": "Support Options",
    "Deal Workspace": "Deal Workspace",
    "Deal Model": "Deal Model",
    "Buildout & Launch Tracker": "Buildout Tracker",
    "Execution Report": "Execution Report",
}


def get_display_label(page: str, unlocked: bool) -> str:
    status_icon = "✓" if unlocked else "Locked"
    pro_suffix = " — Pro" if page in PRO_PAGES else ""
    return f"{status_icon} {OUTCOME_LABELS.get(page, page)}{pro_suffix}"
=======
from page_config import PAGES, PRO_PAGES
from phase_gate import is_page_unlocked


def get_display_label(page: str, unlocked: bool) -> str:
    status_icon = "✅" if unlocked else "🔒"
    pro_suffix = " — Pro" if page in PRO_PAGES else ""
    return f"{status_icon} {page}{pro_suffix}"
>>>>>>> fec65288cb896b4679e84e61241f185fa625e150


def render_page_nav(pages, current_page):
    idx = pages.index(current_page)
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        if idx > 0:
            if st.button("← Back", key=f"back_{current_page}"):
                st.session_state["current_page"] = pages[idx - 1]
                st.rerun()

    with col2:
        labels = []
        for page in PAGES:
            unlocked, _ = is_page_unlocked(page)
            labels.append(get_display_label(page, unlocked))
        st.caption(" | ".join(labels))

    with col3:
        if idx < len(pages) - 1:
            next_page = pages[idx + 1]
            unlocked, reason = is_page_unlocked(next_page)
            if st.button("Next →", key=f"next_{current_page}", disabled=not unlocked):
                st.session_state["current_page"] = next_page
                st.rerun()
            if not unlocked and reason:
                st.caption(reason)
