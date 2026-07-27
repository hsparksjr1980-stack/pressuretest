# Security Rules

## Secret Handling

Agents must never inspect, print, reveal, stage, commit, or upload local secrets.

Protected local files include:

- `.streamlit/secrets.toml`
- `.streamlit/secrets*.toml`
- `.env`
- `.env.*`

The repository may include `!.env.example` as a safe template exception.

## Approval Required

Howard approval is required before:

- Material authentication changes.
- Security architecture changes.
- Production data migration, deletion, exposure, or material change.
- Adding paid services or new external services.
- Using customer information publicly.

## Current Auth Facts

The code includes Supabase auth helpers under `app_files/auth/`. Supabase settings are read from Streamlit secrets or environment variables. This setup task does not change that behavior.

## Current Persistence Facts

The code includes local JSON persistence under `app_files/persistence/`, writing session files under `data/sessions/`. This setup task does not change that behavior.

## TODO

- Confirm production secret storage and deployment environment.
- Confirm whether repository scanning is enabled in GitHub.

