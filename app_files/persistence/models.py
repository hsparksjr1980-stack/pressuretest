# app_files/persistence/models.py

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Final

SCHEMA_VERSION: Final[str] = "phase_4a_local_json_v1"


@dataclass(frozen=True)
class SavedSessionMetadata:
    session_id: str
    label: str
    workflow_type: str
    created_at: str
    updated_at: str


@dataclass(frozen=True)
class SavedSession:
    session_id: str
    label: str
    workflow_type: str
    profile: dict[str, Any] = field(default_factory=dict)
    state: dict[str, Any] = field(default_factory=dict)
    schema_version: str = SCHEMA_VERSION
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "session_id": self.session_id,
            "label": self.label,
            "workflow_type": self.workflow_type,
            "profile": self.profile,
            "state": self.state,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "SavedSession":
        return cls(
            schema_version=str(payload.get("schema_version") or SCHEMA_VERSION),
            session_id=str(payload.get("session_id") or ""),
            label=str(payload.get("label") or "Untitled session"),
            workflow_type=str(payload.get("workflow_type") or "franchise"),
            profile=dict(payload.get("profile") or {}),
            state=dict(payload.get("state") or {}),
            created_at=str(payload.get("created_at") or datetime.now(timezone.utc).isoformat()),
            updated_at=str(payload.get("updated_at") or datetime.now(timezone.utc).isoformat()),
        )


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()
