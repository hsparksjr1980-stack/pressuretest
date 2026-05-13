# app_files/auth/auth_service.py

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import streamlit as st

from .supabase_client import auth_response_session, auth_response_user, get_supabase_client, is_supabase_configured


@dataclass(frozen=True)
class AuthResult:
    success: bool
    message: str = ""
    user_id: str | None = None
    email: str | None = None


def _get_attr_or_item(value: Any, key: str, default: Any = None) -> Any:
    if value is None:
        return default
    if isinstance(value, dict):
        return value.get(key, default)
    return getattr(value, key, default)


def _persist_auth_state(user: Any | None, session: Any | None = None) -> AuthResult:
    user_id = _get_attr_or_item(user, "id")
    email = _get_attr_or_item(user, "email")
    access_token = _get_attr_or_item(session, "access_token")
    refresh_token = _get_attr_or_item(session, "refresh_token")

    if not user_id:
        return AuthResult(False, "Authentication succeeded but no user ID was returned.")

    st.session_state["is_authenticated"] = True
    st.session_state["auth_user_id"] = str(user_id)
    st.session_state["auth_email"] = str(email or "")
    st.session_state["auth_access_token"] = str(access_token or "")
    st.session_state["auth_refresh_token"] = str(refresh_token or "")
    st.session_state["auth_complete"] = True

    if email and not st.session_state.get("email"):
        st.session_state["email"] = str(email)

    return AuthResult(True, "Authenticated.", user_id=str(user_id), email=str(email or ""))


def clear_auth_state() -> None:
    for key in (
        "is_authenticated",
        "auth_user_id",
        "auth_email",
        "auth_access_token",
        "auth_refresh_token",
    ):
        st.session_state.pop(key, None)
    st.session_state["is_authenticated"] = False
    st.session_state["auth_complete"] = False


def restore_auth_session() -> AuthResult:
    if not is_supabase_configured():
        clear_auth_state()
        return AuthResult(False, "Supabase is not configured.")

    access_token = st.session_state.get("auth_access_token")
    refresh_token = st.session_state.get("auth_refresh_token")
    if not access_token or not refresh_token:
        clear_auth_state()
        return AuthResult(False, "No existing auth session.")

    try:
        client = get_supabase_client()
        response = client.auth.set_session(str(access_token), str(refresh_token))
        return _persist_auth_state(auth_response_user(response), auth_response_session(response))
    except Exception as exc:
        clear_auth_state()
        return AuthResult(False, f"Could not restore session: {exc}")


def sign_up(email: str, password: str) -> AuthResult:
    if not email or not password:
        return AuthResult(False, "Email and password are required.")
    if not is_supabase_configured():
        return AuthResult(False, "Supabase is not configured.")

    try:
        response = get_supabase_client().auth.sign_up({"email": email, "password": password})
        user = auth_response_user(response)
        session = auth_response_session(response)
        if session:
            return _persist_auth_state(user, session)
        user_id = _get_attr_or_item(user, "id")
        return AuthResult(
            True,
            "Account created. Check your email if confirmation is required, then sign in.",
            user_id=str(user_id) if user_id else None,
            email=email,
        )
    except Exception as exc:
        return AuthResult(False, f"Signup failed: {exc}")


def sign_in(email: str, password: str) -> AuthResult:
    if not email or not password:
        return AuthResult(False, "Email and password are required.")
    if not is_supabase_configured():
        return AuthResult(False, "Supabase is not configured.")

    try:
        response = get_supabase_client().auth.sign_in_with_password({"email": email, "password": password})
        return _persist_auth_state(auth_response_user(response), auth_response_session(response))
    except Exception as exc:
        return AuthResult(False, f"Login failed: {exc}")


def sign_out() -> AuthResult:
    try:
        if is_supabase_configured() and st.session_state.get("is_authenticated"):
            get_supabase_client().auth.sign_out()
    except Exception:
        pass
    clear_auth_state()
    return AuthResult(True, "Signed out.")


def get_current_user() -> dict[str, str] | None:
    if not is_authenticated():
        return None
    return {
        "id": str(st.session_state.get("auth_user_id") or ""),
        "email": str(st.session_state.get("auth_email") or ""),
    }


def get_authenticated_user_id() -> str | None:
    user_id = st.session_state.get("auth_user_id")
    return str(user_id) if user_id else None


def is_authenticated() -> bool:
    return bool(st.session_state.get("is_authenticated") and st.session_state.get("auth_user_id"))
