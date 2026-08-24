# Validation and Recovery Sprint — 2026-08-21

## Authorization

Howard explicitly authorized the Notion task `PressureTest — Franchise Beta
end-to-end validation` as the active approved product task. The task is marked
`Approved for Codex`, `Approval Status: Approved`, and `Status: Doing` in
Notion. This one-time authorization overrides the repository's undefined weekly
cycle only for validation and recovery of pull request #1.

The prior blocker, safe non-production Supabase configuration and valid
Streamlit secrets for runtime testing, is cleared as of 2026-08-21.

## Scope and Boundaries

- Complete end-to-end runtime validation of pull request #1.
- Capture current-run desktop and mobile evidence.
- Record failures and correct only straightforward validation/recovery defects
  when safe.
- Return one final `APPROVE` or `REVISE` recommendation.
- Do not merge, deploy, publish, change pricing, contact customers, spend money,
  or use production credentials.

## Results

### Recommendation: REVISE

Pull request #1 must not advance to release review. The added Start Here depth
selector crashes on the first authenticated render because `_assessment_depth`
writes `st.session_state["assessment_depth"]` after the radio widget using that
key has been instantiated. Streamlit raises `StreamlitAPIException`, stopping
the flow.

The minimal recovery patch makes `_assessment_depth` a non-mutating getter. It
was validated in the isolated snapshot, then committed directly to pull request
#1 through the connected GitHub integration as
`c1f56938fc6d9a0a242965e6a52d4e2107c87e81`. Local Git metadata remained
read-only. The patch is also saved at
`docs/howard-os/reviews/evidence/2026-08-21-pr1/assessment-depth-session-state-fix.patch`.

A later button-routing audit reproduced two further ordinary defects. The
Opportunity Review continuation used a legacy alias that normalized back to the
same page, and incomplete Financial Reality silently selected the legacy
`Free Report` route. Commits `5aaecd72cfc6b58e78fcedb7464c7313565e8e4a`
and `bc07adf53fbb6733404e635bcd4f92454d90645a` correct those paths on the sole
active branch. The tested PR head is now `bc07adf53fbb6733404e635bcd4f92454d90645a`.

A separate free-to-paid audit confirmed that no active tier conversion exists.
The Report page's collapsed `Request Paid Review` form is a beta request capture
only; it neither grants paid access nor initiates payment or communication.
Historical Plans/Paywall modules are excluded from active routing and contain
stale prices and prototype entitlement behavior. Reactivating them would change
approved monetization scope, so no implementation was attempted without an
approved offer, price, entitlement boundary, and conversion action.

### Validation Performed

- Inspected the actual `main...origin/franchise-beta-ux-report-trust-pass`
  change set: 339 additions and 56 deletions across authoritative active files
  `app_files/overview_ui.py` and `app_files/report_ui.py` only.
- Python compile check: passed for `app.py`, `app_files/`, and `workflows/`.
- Import check: blocked at `app_files/auth/supabase_client.py` because the
  declared `supabase` dependency is absent from the local virtual environment.
- Dependency recovery: attempted installation in a temporary environment; the
  restricted network could not reach the package index.
- Streamlit AppTest, unmodified PR code: reproduced one exception on Start
  Here—post-widget mutation of `assessment_depth`.
- Streamlit AppTest, isolated minimal patch: Quick Assessment passed with zero
  exceptions; changing to Full Review passed with zero exceptions and exposed
  the deeper FDD Translation Risk notes field.
- Streamlit AppTest, isolated minimal patch, Report path: passed with zero
  exceptions; the report rendered the download action, copyable report,
  Decision-Critical Issues/FDD Translation Risk content, paid-review form, and
  beta-feedback fields.
- Streamlit AppTest, routing recovery: Opportunity Review advanced to Financial
  Reality; incomplete Financial Reality stayed on the same page across a
  rerun; completed Financial Reality exposed an explicit Commitment Review
  continuation; Commitment Review advanced to Final Decision; and every
  sidebar destination routed to its canonical page.
- GitHub Actions run `32483953509`: passed after commit `c1f5693`. The existing
  workflow validates the marketing website only (`lint`, `typecheck`, and
  production `build`); it does not provide Python or authenticated Streamlit
  coverage.
- `git diff --check`: required as the final documentation integrity check.
- No formal Python test framework is committed; no formal coverage is claimed.

### Desktop and Mobile Evidence

No desktop or mobile screenshot is claimed. The exact PR app could not be
exposed to the in-app browser because the managed sandbox rejected the local
Streamlit socket bind with `PermissionError: [Errno 1] Operation not permitted`.
The audit therefore names the blocker instead of presenting indirect or
fabricated screenshots.

### Required External Validation Environment

Use a disposable or approved non-production workstation, VM, Codespace, or CI
runner with all of the following:

- Sole active source branch: `franchise-beta-ux-report-trust-pass`. Do not run
  validation or fixes from historical local or remote branches.
- macOS or Linux with Python 3.11–3.13 and Git.
- Outbound HTTPS/DNS access to PyPI and the approved non-production Supabase
  project only.
- Permission to bind a loopback port such as `127.0.0.1:8502`.
- The exact PR #1 head commit
  `bc07adf53fbb6733404e635bcd4f92454d90645a` checked out on branch
  `franchise-beta-ux-report-trust-pass`.
- A fresh virtual environment populated with `pip install -r requirements.txt`;
  `python -c "import supabase, streamlit"` must pass before launch.
- Non-production `SUPABASE_URL` and `SUPABASE_ANON_KEY` supplied through an
  untracked `.streamlit/secrets.toml` or process environment. Never print,
  commit, upload, or reuse production credentials.
- Continue using the existing approved non-production Supabase credentials. Do
  not rotate or replace them unless a clear security issue is identified.
- A dedicated non-production test user whose email and password may be entered
  into that non-production Supabase project. Do not use customer information.
- A Chromium-compatible browser with desktop viewport `1440x900` and mobile
  viewport `390x844` available for current-run screenshots.

Run from the repository root:

```bash
python -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python -c "import supabase, streamlit"
.venv/bin/python -m compileall -q app.py app_files workflows
.venv/bin/streamlit run app.py --server.address 127.0.0.1 --server.port 8502 --browser.gatherUsageStats false
```

Authenticated flow to validate at both viewports:

1. Load the login screen and confirm the Supabase configuration error is absent.
2. Sign in with the dedicated non-production account; do not create or use a
   production account.
3. Complete or confirm profile setup and reach Start Here.
4. Run Quick Assessment on Start Here, complete the four FDD Translation Risk
   fields, navigate forward, and confirm no exception or broken state.
5. Return to Start Here, switch to Full Review, expand the deeper FDD notes,
   enter a harmless test note, navigate away and back, and confirm answers are
   retained.
6. Open Report and confirm Assessment Type, Decision-Critical Issues, FDD
   Translation Risk, Missing Evidence, Copyable Report, and Download Text
   Report render without error.
7. Exercise invalid/empty form submission where available and confirm errors
   are understandable and recoverable.
8. Log out and confirm the authenticated workspace is no longer accessible.

Capture current-run PNG evidence in
`docs/howard-os/reviews/evidence/2026-08-21-pr1/external-validation/` using:

- `desktop-01-login.png`
- `desktop-02-start-quick.png`
- `desktop-03-start-full.png`
- `desktop-04-report.png`
- `mobile-01-login.png`
- `mobile-02-start-quick.png`
- `mobile-03-start-full.png`
- `mobile-04-report.png`

Also save a sanitized `validation-results.md` in that folder with the tested
commit SHA, Python and Streamlit versions, viewport sizes, each flow step's
pass/fail result, observed console/runtime errors with secrets removed, and a
single `APPROVE` or `REVISE` recommendation. PR #1 stays `REVISE` unless every
required step passes and all eight screenshots are accepted as current-run
evidence.

### Notion Blockers

The active validation task was moved to `Waiting`, and three high-priority
blocker tasks were created in the existing `✅ Tasks` data source:

- `PressureTest blocker — Supabase SDK unavailable`.
- `PressureTest blocker — assessment depth crashes Start Here`.
- `PressureTest blocker — local Streamlit server cannot bind`.

The assessment-depth blocker is resolved and marked `Done`. The Supabase SDK
and local-server blockers remain `Waiting` and approved for Codex to resume
after their stated environment dependencies clear.

### Final Stage

- Product task: `FIXES` / `REVISE`.
- Pull request #1: `REVISE`.
- PR head after recovery commit: `c1f56938fc6d9a0a242965e6a52d4e2107c87e81`.
- Marketing task: unchanged and outside this sprint.
- No merge, deployment, publication, pricing change, customer contact, spend,
  or production credential use occurred.
