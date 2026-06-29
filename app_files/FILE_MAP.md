# PressureTest File Map

Current active product scope: **PressureTest: Franchise**.

Startup and Acquisition directories may exist as legacy or placeholder architecture, but they are not active workflows in this phase.

## Active Franchise Beta Files

- `app.py` — Streamlit app shell, beta navigation, workflow routing
- `app_state.py` — session defaults, assessment depth, reset handling
- `page_config.py` — 7-step Franchise Beta page configuration
- `franchise_beta.py` — assessment depth, risk labels, Decision-Critical Issues, FDD Translation Risk, paid review and beta feedback storage helpers
- `overview_ui.py` — Start Here
- `phase0_ui.py` — Operator Fit
- `phase1_ui.py` — Opportunity Review
- `financial_model_ui.py` — Financial Reality
- `post_discovery_ui.py` — Commitment Review
- `final_decision_ui.py` — Final Decision
- `report_ui.py` — Franchise Pressure-Test Report, PDF export, manual paid review CTA, beta feedback
- `report_templates.py` — report text helpers
- `decision_engine.py` — decision packet aggregation
- `ui_styles.py` and `theme.py` — shared visual styling

## Manual Capture Files

- `data/paid_review_requests.csv` and `data/paid_review_requests.jsonl` — created locally when paid review requests are submitted
- `data/beta_feedback.csv` and `data/beta_feedback.jsonl` — created locally when beta feedback is submitted

## Deferred / Placeholder Areas

- Startup workflow: future placeholder only
- Acquisition workflow: future placeholder only
- Stripe: not part of this phase
- Native iOS / Android: not part of this phase
- Pro tools: not part of this phase
