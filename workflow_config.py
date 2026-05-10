# workflow_config.py

from __future__ import annotations

from typing import Final

from workflows.acquisition.config import ACQUISITION_WORKFLOW_CONFIG
from workflows.franchise.config import FRANCHISE_WORKFLOW_CONFIG
from workflows.startup.config import STARTUP_WORKFLOW_CONFIG


DEFAULT_WORKFLOW: Final[str] = "franchise"

WORKFLOW_CONFIG: Final[dict[str, dict[str, object]]] = {
    "franchise": dict(FRANCHISE_WORKFLOW_CONFIG),
    "acquisition": dict(ACQUISITION_WORKFLOW_CONFIG),
    "startup": dict(STARTUP_WORKFLOW_CONFIG),
}

VALID_WORKFLOWS: Final[set[str]] = set(WORKFLOW_CONFIG.keys())


def get_workflow_config(workflow_type: str | None) -> dict[str, object]:
    if workflow_type not in WORKFLOW_CONFIG:
        workflow_type = DEFAULT_WORKFLOW
    return WORKFLOW_CONFIG[workflow_type]


def get_workflow_label(workflow_type: str | None) -> str:
    return str(get_workflow_config(workflow_type)["label"])


def is_placeholder_workflow(workflow_type: str | None) -> bool:
    return bool(get_workflow_config(workflow_type).get("placeholder", True))


def get_workflow_default_page(workflow_type: str | None) -> str:
    return str(get_workflow_config(workflow_type).get("default_page", "Overview"))
