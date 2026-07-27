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

- Howard OS initial setup is being installed on `codex/setup-reconcile`.
- This setup must not change product behavior, authentication behavior, persistence behavior, database schemas, pricing, monetization, or deployment configuration.

## TODO

- Reconcile legacy README and docs with current Franchise Beta positioning in a future approved docs task.
- Confirm CI requirements after the first GitHub Actions run.

