# workflows/franchise/config.py

from __future__ import annotations

from typing import Final


FRANCHISE_WORKFLOW_CONFIG: Final[dict[str, object]] = {
    "key": "franchise",
    "label": "Franchise Opportunity",
    "short_label": "Franchise",
    "description": "Evaluate a franchise system, operator fit, financial pressure, and execution readiness.",
    "status": "Available now",
    "enabled": True,
    "placeholder": False,
    "default_page": "Overview",
}
