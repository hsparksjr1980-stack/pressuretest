# Architecture

## Verified Application Structure

```text
root app.py
  -> imports app_files.app.main()

app_files/app.py
  -> Streamlit app shell
  -> authentication gate
  -> local persistence controls
  -> seven-step Franchise Beta routing

website/
  -> Next.js marketing website
```

## Active Streamlit Source

`app_files/` is active modular source. It includes:

- `app.py`: Streamlit app shell and routing.
- `page_config.py`: Franchise Beta page registry.
- `auth/`: Supabase authentication helpers and UI.
- `persistence/`: local JSON session save/load/list/delete.
- `report_ui.py`: report screen.
- Page modules such as `overview_ui.py`, `phase0_ui.py`, `phase1_ui.py`, `financial_model_ui.py`, `post_discovery_ui.py`, and `final_decision_ui.py`.

## Marketing Source

`website/` is the authoritative Next.js marketing website source.

## Mixed or Legacy Areas

The repository contains historical modules and similarly named files. Agents must prove the active code path before editing. Examples include:

- Root `app.py` versus `app_files/app.py`.
- Legacy page aliases in `app_files/page_config.py`.
- `workflows/startup/` and `workflows/acquisition/`, which exist in the repository while current routing forces the franchise workflow.
- Duplicate or copy-suffixed modules in `app_files/`.

## Data and Persistence

Current persistence is local JSON session storage under `data/sessions/`, created by `app_files/persistence/storage.py`.

## Authentication

Current authentication code uses Supabase if `SUPABASE_URL` and `SUPABASE_ANON_KEY` are configured in Streamlit secrets or environment variables.

## TODO

- Confirm deployment host and production environment variables.
- Confirm whether any production data exists outside this local repository.

