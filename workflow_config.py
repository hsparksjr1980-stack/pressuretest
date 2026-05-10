# workflow_config.py

from __future__ import annotations

from typing import Final


DEFAULT_WORKFLOW: Final[str] = "franchise"

WORKFLOW_CONFIG: Final[dict[str, dict[str, object]]] = {
    "franchise": {
        "label": "Franchise Opportunity",
        "short_label": "Franchise",
        "description": "Evaluate a franchise system, operator fit, financial pressure, and execution readiness.",
        "status": "Available now",
        "enabled": True,
        "entry_page": "Overview",
    },
    "acquisition": {
        "label": "Existing Business Acquisition",
        "short_label": "Acquisition",
        "description": "Evaluate an operating business, seller claims, transition risk, and post-close execution realities.",
        "status": "Workflow in progress",
        "enabled": False,
        "entry_page": "Workflow Placeholder",
    },
    "startup": {
        "label": "New Business / Startup",
        "short_label": "Startup",
        "description": "Evaluate a new concept, launch assumptions, capital pressure, market validation, and execution readiness.",
        "status": "Workflow in progress",
        "enabled": False,
        "entry_page": "Workflow Placeholder",
    },
}

VALID_WORKFLOWS: Final[set[str]] = set(WORKFLOW_CONFIG.keys())


def get_workflow_config(workflow_type: str | None) -> dict[str, object]:
    if workflow_type not in WORKFLOW_CONFIG:
        workflow_type = DEFAULT_WORKFLOW
    return WORKFLOW_CONFIG[workflow_type]


def get_workflow_label(workflow_type: str | None) -> str:
    return str(get_workflow_config(workflow_type)["label"])
