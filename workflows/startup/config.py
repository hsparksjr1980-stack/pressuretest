# workflows/startup/config.py

from __future__ import annotations

from typing import Final


STARTUP_WORKFLOW_CONFIG: Final[dict[str, object]] = {
    "key": "startup",
    "label": "New Business / Startup",
    "short_label": "Startup",
    "description": "Evaluate a new concept, launch assumptions, capital pressure, market validation, and execution readiness.",
    "status": "Workflow in progress",
    "enabled": False,
    "placeholder": True,
    "default_page": "Workflow Placeholder",
}
