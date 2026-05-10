from __future__ import annotations

import json
from copy import deepcopy
from datetime import datetime
from typing import Any

import streamlit as st

EXCLUDED_PREFIXES = ("FormSubmitter:",)
EXCLUDED_KEYS = {"confirm_reset_assessment", "toast_message", "toast_type"}


def serializable_state() -> dict[str, Any]:
    data: dict[str, Any] = {}
    for key, value in st.session_state.items():
        if key in EXCLUDED_KEYS or any(str(key).startswith(prefix) for prefix in EXCLUDED_PREFIXES):
            continue
        try:
            json.dumps(value)
        except TypeError:
            continue
        data[str(key)] = deepcopy(value)
    return data


def export_json_bytes() -> bytes:
    payload = {
        "product": "PressureTest Franchise",
        "exported_at": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "version": "phase1-local-preview",
        "state": serializable_state(),
    }
    return json.dumps(payload, indent=2, sort_keys=True).encode("utf-8")


def import_json_bytes(raw: bytes) -> tuple[bool, str]:
    try:
        payload = json.loads(raw.decode("utf-8"))
    except Exception as exc:
        return False, f"Could not read JSON file: {exc}"

    state = payload.get("state") if isinstance(payload, dict) else None
    if not isinstance(state, dict):
        return False, "This does not look like a PressureTest export."

    for key, value in state.items():
        st.session_state[key] = value
    return True, "Assessment loaded into this browser session."


def load_demo_state() -> None:
    st.session_state.update(
        {
            "auth_complete": True,
            "profile_complete": True,
            "full_name": "Demo Operator",
            "email": "demo@example.com",
            "city_state": "St. Louis, MO",
            "franchise_name": "Sample Coffee Concept",
            "units_considered": "1",
            "ownership_style": "Owner-operator",
            "signed_anything": False,
            "assessment_started": True,
            "brand_analysis_done": True,
            "brand_website": "https://example.com/sample-coffee",
            "territory_competitor_count": 14,
            "territory_notes": "Suburban drive-thru corridor with heavy national coffee competition and a new-market brand presence.",
            "brand_territory_analysis": {
                "brand_name": "Sample Coffee Concept",
                "website": "https://example.com/sample-coffee",
                "territory": "St. Louis, MO",
                "category": "Coffee / Beverage",
                "signals": {
                    "summary": "This appears to be a coffee / beverage concept being evaluated for St. Louis, MO. The first-pass read should focus on local demand, competitor density, ramp assumptions, and whether the franchisor has proven support in markets similar to the target territory.",
                    "signals": {"labor": "High", "buildout": "High", "competition": "Elevated", "owner_dependency": "Moderate–High", "ramp": "High"},
                    "competition_level": "Elevated",
                    "found_claims": [],
                    "found_operations": ["drive-thru", "training", "site selection"],
                    "market_notes": "Suburban drive-thru corridor with heavy national coffee competition and a new-market brand presence."
                },
                "pressure_points": [
                    "Competition density appears elevated; the unit may need stronger local awareness, site quality, and differentiation than the base sales story implies.",
                    "Daypart and staffing discipline matter more than the brand story.",
                    "Drive-thru throughput, local awareness, and repeat frequency can determine whether the model works.",
                    "COGS and approved-supplier economics should be pressure-tested against the local market."
                ],
                "diligence_questions": [
                    "How many open units does the franchisor have in markets similar to St. Louis, MO, not just in its core market?",
                    "What did first-year revenue, labor, COGS, and occupancy look like for newer units versus mature units?",
                    "What are the actual approved-vendor costs in this region after freight, markups, and minimums?"
                ],
                "website_snapshot": {"scrape_status": "Demo scenario loaded."},
                "chatgpt_prompt": "Demo prompt",
                "analysis_notes": ""
            },
            "phase_0_complete": True,
            "phase_1_complete": True,
            "financial_model_done": True,
            "phase_2_complete": False,
            "phase_3_complete": False,
            "premium_access": False,
            "dev_pro_access": True,
        }
    )
