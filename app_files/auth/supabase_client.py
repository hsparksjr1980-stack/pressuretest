from __future__ import annotations

import os
from functools import lru_cache
from typing import Any

import streamlit as st
try:
    from dotenv import load_dotenv
except ModuleNotFoundError:
    def load_dotenv() -> None:
        return None

try:
    from supabase import Client, create_client
except ModuleNotFoundError:
    Client = Any
    create_client = None

load_dotenv()


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
    return bool(url and anon_key and create_client is not None)


@lru_cache(maxsize=1)
def get_supabase_client() -> Client:
    url, anon_key = get_supabase_settings()
    if not url or not anon_key or create_client is None:
        raise SupabaseConfigurationError(
            "Supabase is not configured. Add SUPABASE_URL and SUPABASE_ANON_KEY "
            "to Streamlit secrets or environment variables and install auth dependencies."
        )
    return create_client(url, anon_key)


def auth_response_user(response: Any) -> Any | None:
    return getattr(response, "user", None)


def auth_response_session(response: Any) -> Any | None:
    return getattr(response, "session", None)
