# lead_capture_store.py

from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

LEADS_DIR = Path("data")
LEADS_JSONL = LEADS_DIR / "leads.jsonl"
LEADS_CSV = LEADS_DIR / "leads.csv"

CSV_FIELDS = [
    "captured_at",
    "email",
    "full_name",
    "city_state",
    "franchise_name",
    "lead_source",
    "asset_name",
    "diligence_stage",
    "capital_range",
    "ownership_style",
    "units_considered",
    "consent",
]


def _safe_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _ensure_store() -> None:
    LEADS_DIR.mkdir(parents=True, exist_ok=True)
    if not LEADS_CSV.exists():
        with LEADS_CSV.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
            writer.writeheader()


def normalize_email(email: str) -> str:
    return _safe_text(email).lower()


def build_lead_record(*, session_state: Any, lead_source: str, asset_name: str, consent: bool) -> dict[str, str]:
    return {
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "email": normalize_email(session_state.get("email", "")),
        "full_name": _safe_text(session_state.get("full_name", "")),
        "city_state": _safe_text(session_state.get("city_state", "")),
        "franchise_name": _safe_text(session_state.get("franchise_name", "")),
        "lead_source": _safe_text(lead_source),
        "asset_name": _safe_text(asset_name),
        "diligence_stage": _safe_text(session_state.get("diligence_stage", "")),
        "capital_range": _safe_text(session_state.get("capital_range", "")),
        "ownership_style": _safe_text(session_state.get("ownership_style", "")),
        "units_considered": _safe_text(session_state.get("units_considered", "")),
        "consent": "yes" if consent else "no",
    }


def save_lead_record(record: dict[str, str]) -> None:
    """Append a lead record to local JSONL and CSV stores.

    This is intentionally simple for the prototype. In production, replace this
    with HubSpot, Customer.io, ConvertKit, Postgres, or another CRM endpoint.
    """
    _ensure_store()
    with LEADS_JSONL.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
    with LEADS_CSV.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writerow({field: record.get(field, "") for field in CSV_FIELDS})
