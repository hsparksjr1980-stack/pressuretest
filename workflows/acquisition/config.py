# workflows/acquisition/config.py

from __future__ import annotations

from typing import Final


ACQUISITION_WORKFLOW_CONFIG: Final[dict[str, object]] = {
    "key": "acquisition",
    "label": "Existing Business Acquisition",
    "short_label": "Acquisition",
    "description": "Evaluate an operating business, seller claims, transition risk, and post-close execution realities.",
    "status": "Workflow in progress",
    "enabled": False,
    "placeholder": True,
    "default_page": "Workflow Placeholder",
}
