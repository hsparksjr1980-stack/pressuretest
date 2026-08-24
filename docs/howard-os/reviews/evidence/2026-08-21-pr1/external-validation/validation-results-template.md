# PR #1 External Authenticated Validation

## Environment

- Tested commit: `c1f56938fc6d9a0a242965e6a52d4e2107c87e81`
- Branch: `franchise-beta-ux-report-trust-pass`
- Operating system:
- Python version:
- Streamlit version:
- Supabase SDK version:
- Supabase environment: non-production (do not record URL, key, password, or user email)
- Desktop viewport: `1440x900`
- Mobile viewport: `390x844`

## Preflight

- [ ] `pip install -r requirements.txt` passed.
- [ ] `python -c "import supabase, streamlit"` passed.
- [ ] `python -m compileall -q app.py app_files workflows` passed.
- [ ] Streamlit bound to `127.0.0.1:8502`.
- [ ] Browser console/runtime output contains no exposed secrets.

## Authenticated Flow Results

| Step | Desktop | Mobile | Notes |
| --- | --- | --- | --- |
| Login screen configured |  |  |  |
| Non-production sign-in |  |  |  |
| Profile to Start Here |  |  |  |
| Quick Assessment and four FDD fields |  |  |  |
| Full Review, deeper notes, retained state |  |  |  |
| Report sections and download action |  |  |  |
| Error state and recovery |  |  |  |
| Logout blocks workspace |  |  |  |

Use only `PASS` or `FAIL` in the Desktop and Mobile columns.

## Required Screenshots

- [ ] `desktop-01-login.png`
- [ ] `desktop-02-start-quick.png`
- [ ] `desktop-03-start-full.png`
- [ ] `desktop-04-report.png`
- [ ] `mobile-01-login.png`
- [ ] `mobile-02-start-quick.png`
- [ ] `mobile-03-start-full.png`
- [ ] `mobile-04-report.png`

Before retaining screenshots, confirm they contain no credentials, tokens,
customer data, browser chrome with sensitive account information, or production
identifiers.

## Errors

Record sanitized runtime or browser-console errors here. Write `None` if there
were no errors.

## Recommendation

Choose exactly one:

- `APPROVE` — every required flow step passed at both viewports and all eight
  screenshots were inspected and accepted.
- `REVISE` — any required step failed, evidence is missing, or an unresolved
  security, authentication, data, mobile, or runtime issue remains.

Final recommendation:
