# workflows/startup/config.py

from __future__ import annotations

from typing import Final


STARTUP_WORKFLOW_CONFIG: Final[dict[str, object]] = {
    "key": "startup",
    "label": "New Business / Startup",
    "short_label": "Startup",
    "description": "Evaluate a new concept, launch assumptions, capital pressure, market validation, and execution readiness.",
    "status": "MVP workflow shell in progress",
    "enabled": True,
    "placeholder": False,
    "default_page": "Startup Overview",
    "entry_page": "Startup Overview",
}
