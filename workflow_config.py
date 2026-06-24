# workflow_config.py

from __future__ import annotations

from typing import Final

DEFAULT_WORKFLOW: Final[str] = "franchise"

WORKFLOW_CONFIG: Final[dict[str, dict[str, object]]] = {
    "franchise": {
        "label": "PressureTest: Franchise",
        "status": "Active private beta workflow.",
        "default_page": "Start Here",
        "placeholder": False,
    }
}

VALID_WORKFLOWS: Final[set[str]] = {"franchise"}


def get_workflow_config(workflow_type: str | None) -> dict[str, object]:
    return WORKFLOW_CONFIG[DEFAULT_WORKFLOW]


def get_workflow_label(workflow_type: str | None) -> str:
    return str(get_workflow_config(workflow_type)["label"])


def is_placeholder_workflow(workflow_type: str | None) -> bool:
    return workflow_type != DEFAULT_WORKFLOW


def get_workflow_default_page(workflow_type: str | None) -> str:
    return str(get_workflow_config(workflow_type).get("default_page", "Start Here"))
