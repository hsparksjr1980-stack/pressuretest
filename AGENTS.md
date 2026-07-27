# PressureTest Agent Operating Rules

This repository uses the Howard OS operating model. Agents are expected to complete approved weekly work autonomously while preserving Howard Sparks as product owner and final approver.

## Current Source Map

- `website/` is the authoritative Next.js marketing website source. Use `website/package.json` for website commands.
- Root `app.py` is the Streamlit launcher. It adds the repository root and `app_files/` to `sys.path`, then runs `app_files.app.main()`.
- `app_files/` is active modular source for the Streamlit product application. It contains the active app shell, page modules, authentication package, local persistence package, UI helpers, report code, and supporting logic.
- `workflows/` contains workflow module code and configuration. Current app routing forces `DEFAULT_WORKFLOW = "franchise"` from `workflow_config.py`; Startup and Acquisition are present as historical or placeholder areas unless a task proves an active code path.
- `docs/` contains existing product documentation. Some existing docs are stale relative to current code; verify facts against code before relying on them.
- `.github/` contains workflow and issue/PR templates for operating cadence once installed.

When multiple similarly named files exist, agents must determine the active code path before editing. Do not edit an uncertain or non-authoritative source merely because a file name appears related.

## Autonomy Mandate

Once Howard approves a weekly product or marketing task, agents must independently:

1. Read relevant operating records and prior decisions.
2. Plan the work.
3. Inspect relevant code and content.
4. Create and manage an isolated branch.
5. Implement the product change or create the marketing deliverable.
6. Make reasonable decisions within approved scope.
7. Run available validation and quality checks.
8. Diagnose and correct ordinary failures.
9. Perform or request independent review.
10. Address ordinary review findings.
11. Update documentation and issue status.
12. Commit and push the task branch.
13. Open or update the pull request.
14. Prepare the Saturday approval package.

Howard is not the daily project manager, task coordinator, technical troubleshooter, editor, QA operator, or branch manager.

## Howard Approval Required

Ask Howard before:

- Merging into `main`.
- Deploying to production.
- Publishing or sending marketing material.
- Spending money or adding a paid service.
- Changing pricing, monetization, or the approved business model.
- Materially expanding or changing product scope.
- Making a material authentication or security architecture change.
- Migrating, deleting, exposing, or materially changing production data.
- Using customer information publicly.
- Making unapproved legal, regulatory, financial, profitability, failure-rate, or comparative claims.
- Accepting a material risk that cannot be corrected during the weekly cycle.
- Choosing between conflicting product directions.
- Continuing when the task cannot be completed without materially changing acceptance criteria.

Do not ask Howard for routine implementation choices, internal names, ordinary refactors, minor brand-consistent wording, lint/build/test corrections, small design choices within standards, or ordinary review corrections.

## Weekly Limit

Each weekly cycle may complete at most:

- One approved product task.
- One approved marketing task.

Supporting bug fixes needed to complete those two tasks are allowed. Additional ideas belong in the proposed backlog.

## Task Eligibility

Product work may begin only from a GitHub issue with:

- Labels: `product`, `ready`.
- Clear acceptance criteria.
- Defined out-of-scope items.
- Identified risk level.
- Current weekly cycle.

Marketing work may begin only from a GitHub issue with:

- Labels: `marketing`, `ready`.
- Defined audience.
- Defined objective.
- Defined deliverable.
- Defined channel.
- Claims and compliance requirements.
- Current weekly cycle.

## Validation

For website changes, run from `website/`:

- `npm run lint`
- `npm run typecheck`
- `npm run build`

For Streamlit/Python changes, run the closest available syntax, import, app-start, and path-specific checks. There is no committed Python test runner in the current repository.

## Security

Never inspect, print, commit, or reveal local secrets. Keep `.streamlit/secrets.toml`, `.streamlit/secrets*.toml`, `.env`, and `.env.*` ignored. Preserve `!.env.example`.

