# workflows/startup/page_config.py

from __future__ import annotations

from dataclasses import dataclass
from typing import Final


@dataclass(frozen=True)
class StartupPageConfig:
    name: str
    section: str


STARTUP_PAGE_CONFIGS: Final[list[StartupPageConfig]] = [
    StartupPageConfig("Startup Overview", "Startup Workflow"),
    StartupPageConfig("Startup Concept Validation", "Startup Workflow"),
    StartupPageConfig("Startup Market Pressure Test", "Startup Workflow"),
    StartupPageConfig("Startup Financial Assumptions", "Startup Workflow"),
    StartupPageConfig("Startup Readiness Report", "Startup Output"),
]

STARTUP_DEFAULT_PAGE: Final[str] = "Startup Overview"
STARTUP_PAGES: Final[list[str]] = [page.name for page in STARTUP_PAGE_CONFIGS]
STARTUP_PAGE_CONFIG_MAP: Final[dict[str, StartupPageConfig]] = {
    page.name: page for page in STARTUP_PAGE_CONFIGS
}


def get_startup_page_config(page_name: str) -> StartupPageConfig:
    return STARTUP_PAGE_CONFIG_MAP[page_name]


def is_startup_page(page_name: str) -> bool:
    return page_name in STARTUP_PAGE_CONFIG_MAP
