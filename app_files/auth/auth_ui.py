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
    with st.form("auth_login_form"):
        email = st.text_input("Email", key="auth_login_email")
        password = st.text_input("Password", type="password", key="auth_login_password")
        submitted = st.form_submit_button("Log in", type="primary", use_container_width=True)

    if submitted:
        result = sign_in(email.strip(), password)
        if result.success:
            st.success("Logged in.")
            st.rerun()
        else:
            st.error(result.message)


def _render_signup_form() -> None:
    with st.form("auth_signup_form"):
        email = st.text_input("Email", key="auth_signup_email")
        password = st.text_input("Password", type="password", key="auth_signup_password")
        confirm_password = st.text_input("Confirm password", type="password", key="auth_signup_confirm_password")
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


def render_auth_screen() -> None:
    render_brand_header(APP_PRODUCT, APP_TAGLINE)
    render_pressuretest_boundary_notice(compact=True)

    st.markdown(
        """
        <div class="pt-card" style="background:#0B1730; color:#F8FAFC; padding:1.35rem 1.45rem; margin:.4rem 0 1rem 0;">
            <div class="pt-eyebrow" style="color:#CBD5E1;">Secure access</div>
            <h1 style="margin:.2rem 0 .55rem 0; color:#F8FAFC; line-height:1.1;">Sign in to PressureTest.</h1>
            <p style="max-width:820px; margin:0; color:#E2E8F0; line-height:1.6; font-size:1rem;">
                Authentication protects your workspace and gives the app a stable user identity for future cloud persistence.
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
