# app_files/auth/auth_ui.py

from __future__ import annotations

import streamlit as st

from branding import APP_PRODUCT, APP_TAGLINE
from shared_ui import render_brand_header, render_pressuretest_boundary_notice

from .auth_service import get_current_user, is_authenticated, restore_auth_session, sign_in, sign_out, sign_up
from .supabase_client import is_supabase_configured


def _render_auth_configuration_notice() -> None:
    st.error("Supabase authentication is not configured.")
    st.caption("Add SUPABASE_URL and SUPABASE_ANON_KEY to .streamlit/secrets.toml or environment variables.")


def _render_login_form() -> None:
    st.markdown("#### Welcome back")
    st.caption("Sign in to continue your saved diligence workspace.")
    with st.form("auth_login_form"):
        email = st.text_input("Email", placeholder="you@example.com", key="auth_login_email")
        password = st.text_input("Password", type="password", placeholder="Your password", key="auth_login_password")
        submitted = st.form_submit_button("Log in", type="primary", use_container_width=True)

    if submitted:
        result = sign_in(email.strip(), password)
        if result.success:
            st.success("Logged in.")
            st.rerun()
        else:
            st.error(result.message)


def _render_signup_form() -> None:
    st.markdown("#### Create your workspace")
    st.caption("Use this to save progress, return later, and prepare for cloud persistence.")
    with st.form("auth_signup_form"):
        email = st.text_input("Email", placeholder="you@example.com", key="auth_signup_email")
        password = st.text_input("Password", type="password", placeholder="At least 8 characters", key="auth_signup_password")
        confirm_password = st.text_input("Confirm password", type="password", placeholder="Re-enter password", key="auth_signup_confirm_password")
        submitted = st.form_submit_button("Create account", type="primary", use_container_width=True)

    if submitted:
        if password != confirm_password:
            st.error("Passwords do not match.")
            return
        if len(password) < 8:
            st.error("Use a password with at least 8 characters.")
            return

        result = sign_up(email.strip(), password)
        if result.success:
            st.success(result.message or "Account created.")
            if result.user_id:
                st.rerun()
        else:
            st.error(result.message)


def _render_auth_value_card(title: str, body: str) -> None:
    st.markdown(
        f"""
        <div class="pt-card" style="height:100%; padding:1rem 1.05rem;">
            <h4 style="margin:.1rem 0 .35rem 0; color:#0F172A;">{title}</h4>
            <p style="margin:0; color:#475569; line-height:1.5; font-size:.92rem;">{body}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_auth_screen() -> None:
    render_brand_header(APP_PRODUCT, APP_TAGLINE)
    render_pressuretest_boundary_notice(compact=True)

    left, right = st.columns([1.15, .85], gap="large")

    with left:
        st.markdown(
            """
            <div class="pt-card" style="
                background:linear-gradient(135deg,#0B1730 0%,#13294B 58%,#1E3A5F 100%);
                color:#F8FAFC;
                padding:1.75rem 1.8rem;
                margin:.4rem 0 1rem 0;
                min-height:310px;
                display:flex;
                flex-direction:column;
                justify-content:space-between;
            ">
                <div>
                    <div class="pt-eyebrow" style="color:#CBD5E1;">Secure diligence workspace</div>
                    <h1 style="margin:.35rem 0 .75rem 0; color:#F8FAFC; line-height:1.05; font-size:2.35rem;">
                        Pressure-test before you commit capital.
                    </h1>
                    <p style="max-width:780px; margin:0; color:#E2E8F0; line-height:1.65; font-size:1.02rem;">
                        Sign in to save your work, resume assessments, and keep franchise or startup diligence organized as the platform moves toward cloud persistence.
                    </p>
                </div>
                <div style="display:flex; gap:.65rem; flex-wrap:wrap; margin-top:1.4rem;">
                    <span style="padding:.4rem .65rem; border-radius:999px; background:rgba(255,255,255,.10); color:#E2E8F0; font-size:.82rem;">Saved sessions</span>
                    <span style="padding:.4rem .65rem; border-radius:999px; background:rgba(255,255,255,.10); color:#E2E8F0; font-size:.82rem;">Workflow recovery</span>
                    <span style="padding:.4rem .65rem; border-radius:999px; background:rgba(255,255,255,.10); color:#E2E8F0; font-size:.82rem;">Operator-focused review</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        c1, c2, c3 = st.columns(3, gap="medium")
        with c1:
            _render_auth_value_card("Organize diligence", "Keep assessment progress and business context in one structured workspace.")
        with c2:
            _render_auth_value_card("Resume later", "Return to saved workflow state instead of starting over each session.")
        with c3:
            _render_auth_value_card("Prepare for cloud", "Authenticated user IDs are now ready for the next persistence phase.")

    with right:
        st.markdown(
            """
            <div class="pt-card" style="padding:1.2rem 1.25rem; margin:.4rem 0 1rem 0;">
                <div class="pt-eyebrow">Account access</div>
                <h3 style="margin:.25rem 0 .25rem 0; color:#0F172A;">Continue your review</h3>
                <p style="margin:0; color:#64748B; line-height:1.5; font-size:.93rem;">
                    Log in if you already created an account, or create one to start saving under a stable user identity.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if not is_supabase_configured():
            _render_auth_configuration_notice()
            return

        login_tab, signup_tab = st.tabs(["Log in", "Create account"])
        with login_tab:
            _render_login_form()
        with signup_tab:
            _render_signup_form()

    st.caption("PressureTest is an educational diligence workspace, not legal, financial, tax, or investment advice.")


def ensure_authenticated() -> bool:
    if is_authenticated():
        return True

    restore_auth_session()
    if is_authenticated():
        return True

    render_auth_screen()
    return False


def render_auth_sidebar_summary() -> None:
    if not is_authenticated():
        return

    user = get_current_user() or {}
    email = user.get("email") or "Authenticated user"

    st.sidebar.caption("Signed in")
    st.sidebar.info(email)

    if st.sidebar.button("Log out", use_container_width=True):
        sign_out()
        st.rerun()
