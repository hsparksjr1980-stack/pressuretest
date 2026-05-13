# app_files/auth/supabase_client.py

from __future__ import annotations

import os
from functools import lru_cache
from typing import Any

import streamlit as st
from supabase import Client, create_client


class SupabaseConfigurationError(RuntimeError):
    """Raised when Supabase auth is enabled without required configuration."""


def _read_secret(name: str) -> str | None:
    try:
        value = st.secrets.get(name)
        if value:
            return str(value)
    except Exception:
        pass
    return os.getenv(name)


def get_supabase_settings() -> tuple[str | None, str | None]:
    return _read_secret("SUPABASE_URL"), _read_secret("SUPABASE_ANON_KEY")


def is_supabase_configured() -> bool:
    url, anon_key = get_supabase_settings()
    return bool(url and anon_key)


@lru_cache(maxsize=1)
def get_supabase_client() -> Client:
    url, anon_key = get_supabase_settings()
    if not url or not anon_key:
        raise SupabaseConfigurationError(
            "Supabase is not configured. Add SUPABASE_URL and SUPABASE_ANON_KEY to Streamlit secrets or environment variables."
        )
    return create_client(url, anon_key)


def auth_response_user(response: Any) -> Any | None:
    return getattr(response, "user", None)


def auth_response_session(response: Any) -> Any | None:
    return getattr(response, "session", None)
