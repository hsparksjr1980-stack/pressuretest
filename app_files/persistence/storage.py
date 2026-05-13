# app_files/persistence/storage.py

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Final
from uuid import uuid4

import streamlit as st

from persistence.models import SavedSession, SavedSessionMetadata, utc_now_iso

DATA_DIR: Final[Path] = Path(__file__).resolve().parents[2] / "data" / "sessions"
PROFILE_KEYS: Final[set[str]] = {
    "full_name",
    "email",
    "city_state",
    "franchise_name",
    "units_considered",
    "ownership_style",
    "signed_anything",
}
EXCLUDED_STATE_KEYS: Final[set[str]] = {
    "confirm_reset_assessment",
    "toast_message",
    "toast_type",
}


def _ensure_data_dir() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def _safe_session_id(raw_value: str | None = None) -> str:
    candidate = raw_value or str(uuid4())
    safe = re.sub(r"[^a-zA-Z0-9_-]", "-", candidate).strip("-")
    return safe or str(uuid4())


def _session_path(session_id: str) -> Path:
    return DATA_DIR / f"{_safe_session_id(session_id)}.json"


def _json_safe(value: Any) -> Any:
    try:
        json.dumps(value)
        return value
    except TypeError:
        return str(value)


def export_session_state() -> dict[str, Any]:
    """Export JSON-safe Streamlit session state without UI-only transient keys."""
    exported: dict[str, Any] = {}
    for key, value in st.session_state.items():
        if key in EXCLUDED_STATE_KEYS:
            continue
        exported[key] = _json_safe(value)
    return exported


def _profile_from_state(state: dict[str, Any]) -> dict[str, Any]:
    return {key: state.get(key) for key in PROFILE_KEYS if key in state}


def save_session(user_id: str, data: dict[str, Any] | None = None, label: str | None = None) -> SavedSession:
    """Save a local JSON session snapshot.

    user_id is currently used as the local session identifier. This can later map to a real user/account id.
    """
    _ensure_data_dir()
    session_id = _safe_session_id(user_id)
    state = dict(data or export_session_state())
    existing = load_session(session_id, default_none=True)
    now = utc_now_iso()

    session = SavedSession(
        session_id=session_id,
        label=label or str(state.get("email") or state.get("full_name") or session_id),
        workflow_type=str(state.get("workflow_type") or "franchise"),
        profile=_profile_from_state(state),
        state=state,
        created_at=existing.created_at if existing else now,
        updated_at=now,
    )

    _session_path(session_id).write_text(json.dumps(session.to_dict(), indent=2, sort_keys=True), encoding="utf-8")
    return session


def load_session(user_id: str, default_none: bool = False) -> SavedSession | None:
    _ensure_data_dir()
    path = _session_path(user_id)
    if not path.exists():
        return None if default_none else None
    payload = json.loads(path.read_text(encoding="utf-8"))
    return SavedSession.from_dict(payload)


def apply_session_to_state(session: SavedSession) -> None:
    for key, value in session.state.items():
        st.session_state[key] = value


def list_sessions() -> list[SavedSessionMetadata]:
    _ensure_data_dir()
    sessions: list[SavedSessionMetadata] = []
    for path in sorted(DATA_DIR.glob("*.json")):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
            session = SavedSession.from_dict(payload)
            sessions.append(
                SavedSessionMetadata(
                    session_id=session.session_id,
                    label=session.label,
                    workflow_type=session.workflow_type,
                    created_at=session.created_at,
                    updated_at=session.updated_at,
                )
            )
        except (json.JSONDecodeError, OSError, TypeError, ValueError):
            continue
    return sorted(sessions, key=lambda item: item.updated_at, reverse=True)


def delete_session(user_id: str) -> bool:
    _ensure_data_dir()
    path = _session_path(user_id)
    if not path.exists():
        return False
    path.unlink()
    return True
