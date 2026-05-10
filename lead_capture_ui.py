# lead_capture_ui.py

from __future__ import annotations

import re
from typing import Any

import streamlit as st

from lead_capture_store import build_lead_record, normalize_email, save_lead_record

EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


def _inject_lead_styles() -> None:
    st.markdown(
        """
        <style>
            .lc-box {
                border: 1px solid #E2E8F0;
                border-radius: 18px;
                background: #FFFFFF;
                padding: 1.1rem 1.2rem;
                box-shadow: 0 16px 40px rgba(15, 23, 42, 0.06);
                margin-bottom: .85rem;
            }
            .lc-box-muted {
                border: 1px solid #E2E8F0;
                border-radius: 18px;
                background: #F8FAFC;
                padding: 1.1rem 1.2rem;
                margin-bottom: .85rem;
            }
            .lc-label {
                font-size: .72rem;
                font-weight: 800;
                letter-spacing: .08em;
                text-transform: uppercase;
                color: #9A3412;
                margin-bottom: .3rem;
            }
            .lc-title {
                font-size: 1.12rem;
                font-weight: 800;
                line-height: 1.25;
                color: #0B1730;
                margin-bottom: .35rem;
            }
            .lc-copy {
                font-size: .94rem;
                color: #5B6577;
                line-height: 1.55;
                margin-bottom: .45rem;
            }
            .lc-list {
                margin: .4rem 0 0 1.1rem;
                color: #334155;
                font-size: .92rem;
                line-height: 1.5;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def is_valid_email(email: str) -> bool:
    return bool(EMAIL_RE.match(normalize_email(email)))


def has_lead_capture(asset_key: str) -> bool:
    captured_assets = st.session_state.get("lead_captured_assets", {})
    if isinstance(captured_assets, dict) and captured_assets.get(asset_key):
        return True
    # Preserve backward compatibility: profile email counts as captured only
    # after an explicit capture action for this asset.
    return False


def mark_lead_capture(asset_key: str) -> None:
    captured_assets = st.session_state.get("lead_captured_assets", {})
    if not isinstance(captured_assets, dict):
        captured_assets = {}
    captured_assets[asset_key] = True
    st.session_state["lead_captured_assets"] = captured_assets
    st.session_state["lead_captured"] = True


def render_lead_capture_gate(
    *,
    asset_key: str,
    asset_name: str,
    lead_source: str,
    title: str = "Send this to yourself before downloading",
    body: str = "Enter your email to unlock the download and keep a copy of this diligence output tied to your workspace.",
    button_label: str = "Unlock download",
) -> bool:
    """Render a lightweight lead capture gate.

    Returns True when the asset is unlocked for this session.
    """
    _inject_lead_styles()

    if has_lead_capture(asset_key):
        st.success(f"{asset_name} unlocked for this session.")
        return True

    st.markdown(
        f"""
        <div class="lc-box">
            <div class="lc-label">Lead capture</div>
            <div class="lc-title">{title}</div>
            <div class="lc-copy">{body}</div>
            <ul class="lc-list">
                <li>No investment, legal, tax, or financing advice.</li>
                <li>Use the output as a diligence organizer and discussion packet.</li>
                <li>You can replace this local capture with a CRM integration later.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

    default_email = normalize_email(st.session_state.get("email", ""))
    default_name = st.session_state.get("full_name", "")

    with st.form(f"lead_capture_{asset_key}"):
        full_name = st.text_input("Name", value=default_name, placeholder="Jane Operator")
        email = st.text_input("Email", value=default_email, placeholder="jane@example.com")
        consent = st.checkbox(
            "I understand this is an educational diligence tool and not legal, financial, tax, accounting, or investment advice.",
            value=True,
        )
        submitted = st.form_submit_button(button_label, type="primary", use_container_width=True)

    if submitted:
        normalized = normalize_email(email)
        if not full_name.strip():
            st.error("Enter a name before unlocking the download.")
            return False
        if not is_valid_email(normalized):
            st.error("Enter a valid email address before unlocking the download.")
            return False
        if not consent:
            st.error("Confirm the educational-use notice before unlocking the download.")
            return False

        st.session_state["full_name"] = full_name.strip()
        st.session_state["email"] = normalized
        record = build_lead_record(
            session_state=st.session_state,
            lead_source=lead_source,
            asset_name=asset_name,
            consent=consent,
        )
        save_lead_record(record)
        mark_lead_capture(asset_key)
        st.success("Download unlocked.")
        st.rerun()

    return False


def render_inline_lead_prompt(*, asset_name: str, context: str) -> None:
    _inject_lead_styles()
    st.markdown(
        f"""
        <div class="lc-box-muted">
            <div class="lc-label">Save point</div>
            <div class="lc-title">{asset_name}</div>
            <div class="lc-copy">{context}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
