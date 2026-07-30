# Current Status

## Verified Repository Facts

- Current Streamlit entry point: root `app.py`.
- Active Streamlit implementation: `app_files/app.py` and supporting modules in `app_files/`.
- Active workflow config: `workflow_config.py`.
- Active workflow: `franchise`.
- Marketing website source: `website/`.
- Website package manager: npm, with `website/package-lock.json`.
- Website framework: Next.js with App Router files under `website/src/app`.
- Existing website scripts before Howard OS setup: `dev`, `build`, `start`, `lint`.
- Authentication implementation exists under `app_files/auth/` and uses Supabase settings from Streamlit secrets or environment variables when configured.
- Local JSON persistence exists under `app_files/persistence/` and writes session data under `data/sessions/`.
- No `.github/` directory existed before this setup.
- No `AGENTS.md` existed before this setup.

## Documentation Mismatches Found

Existing docs contain stale or conflicting references:

- `README.md` describes Phase 4A persistence foundation and says no auth yet, while current code includes Supabase auth modules.
- `docs/CURRENT_STATE.md` repeats content and still describes broader active product areas.
- `website/README.md` is still the default create-next-app README.

Treat this file and `AGENTS.md` as the operating source for repository facts until older docs are reconciled.

## Current Operating State

- Howard OS initial setup was merged to `main` in pull request #2.
- As of the 2026-07-30 independent-review run, no current weekly cycle dates
  are defined and GitHub has no open product or marketing issues.
- No product or marketing task is recorded at `AGENT REVIEW`, so neither task
  is eligible to move to `FIXES` or `RELEASE READY`.
- Historical remote branches remain, including `codex/setup-reconcile`,
  `franchise-beta-ui-trust-pass`, `franchise-beta-ux-report-trust-pass`,
  `phase-1-franchise-beta`, `phase-4a-session-ui`, and
  `phase-4b-supabase-auth`. They were not treated as current-cycle work.
- Pull request #1, `Franchise Beta UX + Report Trust Pass`, remains open, but
  it has no eligible current-cycle issue or recorded `AGENT REVIEW` stage.
- Pull request #2, `Install PressureTest Howard OS autonomous workflow`, is
  closed and represented in `main` history.
- The detailed review gate record is in
  `docs/howard-os/reviews/2026-07-30-independent-review.md`.

## TODO

- Reconcile legacy README and docs with current Franchise Beta positioning in a future approved docs task.
- Confirm CI requirements after the first GitHub Actions run.
- Define the current weekly cycle and create at most one eligible `product`,
  `ready` issue and one eligible `marketing`, `ready` issue before starting
  weekly execution.
