# PressureTest

PressureTest is a Streamlit app for evaluating whether a franchise opportunity is worth pursuing, financing, and negotiating.

The product is organized as a guided decision flow. Users move from a welcome/profile gate into a multi-phase assessment, generate decision outputs, and optionally unlock Pro execution tools.

## What the app does

The app helps a user answer three questions:

1. Is this the right operator and opportunity?
2. Does the deal make sense financially and operationally?
3. Should the user move forward, move forward with conditions, or walk away?

The current repo already contains the core assessment flow, report views, and Pro execution pages.

## Core flow

```text
Welcome
  -> Profile
  -> Overview
  -> PressureTest
  -> Concept Validation
  -> Opportunity Fit & Recommendations
  -> Financial Model
  -> Free Report
  -> Post-Discovery
  -> Final Decision
  -> Report
  -> Plans & Support
  -> Pro execution tools
```

### Free pages

- Overview
- PressureTest
- Concept Validation
- Opportunity Fit & Recommendations
- Financial Model
- Free Report
- Plans & Support
- Post-Discovery
- Final Decision
- Report

### Pro pages

- Deal Workspace
- Deal Model
- Buildout & Launch Tracker
- Execution Report

Pro pages are gated by two conditions in the current implementation:

- the user chooses **Move Forward** in Final Decision
- the session has Pro access enabled

A developer override is also present in session state.

## Tech stack

- Python
- Streamlit
- pandas
- numpy
- reportlab

## Quickstart

### 1. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the app

```bash
streamlit run app.py
```

## Project structure

```text
app.py                         # app entrypoint and page routing
app_state.py                   # session-state defaults, normalization, reset
page_config.py                 # page registry, sections, access tiers
phase_gate.py                  # free/pro access rules and page gating

welcome_ui.py                  # front door / auth shell
profile_ui.py                  # profile intake
overview_ui.py                 # overview page

phase0_*.py                    # PressureTest questions, logic, UI
phase1_*.py                    # Concept Validation questions, logic, UI
post_discovery_*.py            # Post-Discovery questions, logic, UI

financial_model_ui.py          # financial model UI
opportunity_fit_*.py           # fit/recommendation engine and UI
final_decision_ui.py           # final recommendation / decision page
decision_engine.py            # normalized decision packet builder

free_report_ui.py              # free report output
report_ui.py                   # report screen
report_templates.py            # report content helpers

plans_support_*.py             # plans/support content and UI
paywall_*.py                   # paywall logic/UI

deal_workspace_*.py            # Pro execution workspace
deal_model_*.py                # Pro deal model
buildout_tracker_*.py          # Pro buildout tracker
execution_report_ui.py         # Pro execution reporting

shared_ui.py                   # shared layout helpers
nav_ui.py                      # page navigation
theme.py                       # theme setup
ui_styles.py                   # global CSS styles
```

## Architecture at a glance

- `app.py` is the orchestrator. It configures Streamlit, initializes session state, renders the sidebar, applies gating, and dispatches to page renderers.
- `page_config.py` is the page registry and the single source of truth for page names, sections, and access tiers.
- `app_state.py` owns app/session defaults and reset behavior.
- `phase_gate.py` determines whether a page is available.
- `decision_engine.py` aggregates scores, guardrails, flags, and page outputs into one decision packet.

More detail lives in:

- `docs/app-flow.md`
- `docs/architecture.md`
- `docs/page-reference.md`
- `docs/session-state.md`
- `docs/developer-guide.md`
- `docs/limitations-roadmap.md`

## Current limitations

This repo looks like a strong prototype or internal tool, not a finished production app.

Current gaps:

- no real authentication
- no persistent database
- no payment integration
- no hardened authorization model
- no formal deployment or environment docs
- no reliable artifact/export workflow beyond current report scaffolding
- heavy reliance on Streamlit session state
- developer Pro override is enabled by default in `app_state.py`

## Cleanup recommended before sharing publicly

Remove these from the project archive:

- `.venv/`
- `.DS_Store`
- `__MACOSX/`
- other machine-specific or generated files

They increase archive size and make the repo feel less production-ready.

## Suggested next improvements

1. Replace `README.txt` with this `README.md`.
2. Move old transitional notes into a changelog or archive note.
3. Add screenshots of the main user flow.
4. Add environment-variable and deployment guidance.
5. Turn Pro access, auth, and persistence into real services.

## Advisory Boundary

PressureTest is a blunt operating and diligence screen. It is not legal, tax, lending, accounting, or investment advice. Users should validate findings with qualified advisors before signing franchise agreements or making material financial commitments.
