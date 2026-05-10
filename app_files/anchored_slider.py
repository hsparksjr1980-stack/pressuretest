from __future__ import annotations

import streamlit as st


def anchored_slider(
    label: str,
    *,
    key: str,
    value: int = 3,
    min_value: int = 1,
    max_value: int = 5,
    anchors: dict[int, str] | None = None,
    help: str | None = None,
) -> int:
    """Render a 1-5 slider with plain-English anchor descriptions.

    This keeps the numeric output unchanged while making each score easier
    for users to interpret consistently.
    """
    if not st.session_state.get("_anchored_slider_css_loaded"):
        st.markdown("""
        <style>
        .pt-slider-guide { display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.5rem; margin: -0.35rem 0 0.35rem 0; }
        .pt-slider-guide div { border: 1px solid rgba(15, 23, 42, 0.10); border-radius: 0.75rem; padding: 0.45rem 0.55rem; background: rgba(248, 250, 252, 0.88); min-height: 58px; }
        .pt-slider-guide strong { display: block; font-size: 0.72rem; color: #0f172a; margin-bottom: 0.15rem; }
        .pt-slider-guide span { display: block; font-size: 0.72rem; line-height: 1.15rem; color: #475569; }
        .pt-slider-selected { font-size: 0.78rem; line-height: 1.2rem; color: #334155; background: rgba(241, 245, 249, 0.72); border-left: 3px solid #334155; border-radius: 0.35rem; padding: 0.4rem 0.55rem; margin: 0.15rem 0 0.95rem 0; }
        </style>
        """, unsafe_allow_html=True)
        st.session_state["_anchored_slider_css_loaded"] = True

    anchors = anchors or {
        1: "Very low / weak",
        2: "Some concerns",
        3: "Mixed / uncertain",
        4: "Generally strong",
        5: "Very strong / validated",
    }

    selected = st.slider(
        label,
        min_value=min_value,
        max_value=max_value,
        value=int(value),
        key=key,
        help=help,
    )

    st.markdown(
        f"""
        <div class="pt-slider-guide">
            <div><strong>1</strong><span>{anchors.get(1, '')}</span></div>
            <div><strong>3</strong><span>{anchors.get(3, '')}</span></div>
            <div><strong>5</strong><span>{anchors.get(5, '')}</span></div>
        </div>
        <div class="pt-slider-selected"><strong>Selected {selected}:</strong> {anchors.get(int(selected), '')}</div>
        """,
        unsafe_allow_html=True,
    )
    return int(selected)
