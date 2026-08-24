# PR #1 Branch Capture Audit — 2026-08-21

## Decision

Do not merge the local historical branches into pull request #1. Deploy the
Streamlit validation environment from branch
`franchise-beta-ux-report-trust-pass` at current reviewed commit
`bc07adf53fbb6733404e635bcd4f92454d90645a`. The original assessment-depth
audit baseline was `c1f56938fc6d9a0a242965e6a52d4e2107c87e81`.

PR #1 remains `REVISE` pending the documented external authenticated desktop
and mobile evidence. Nothing was merged to `main` or deployed by this audit.

## Sole Active Validation Branch Designation

Effective 2026-08-21, `franchise-beta-ux-report-trust-pass` is the sole active
PressureTest Streamlit validation, recovery-fix, and review-deployment branch.
All such work must use its current reviewed head, beginning with
`c1f56938fc6d9a0a242965e6a52d4e2107c87e81` and now including the validated
button-routing recovery through `bc07adf53fbb6733404e635bcd4f92454d90645a`.

The historical UI, phase, auth, setup, archive, and independent-review branches
are inactive/superseded for product validation. `main` remains the protected
production integration branch, not the pre-merge validation branch. Remote
history remains intact.

Existing non-production Supabase credentials remain the approved validation
credentials. Do not rotate or replace them without a clear security issue, and
never print, commit, upload, log, document, or capture them in screenshots.

## Authoritative Product Code

- `main` at `dfc88899cb5bfe9e101d2ed04ef9229fcd8f9819` and PR #1 share product
  baseline `c2888a8310f5544a6a69c6647ffeece1bceedc49`.
- The eight commits on `main` after that baseline change Howard OS records,
  repository/CI configuration, and the Next.js marketing website. They do not
  change `app.py`, `app_files/`, `workflows/`, `requirements.txt`, or
  `workflow_config.py`.
- PR #1 is five commits ahead of the shared product baseline and changes only
  the authoritative active Streamlit files `app_files/overview_ui.py` and
  `app_files/report_ui.py` relative to current `main`.
- Therefore the PR branch contains current baseline product code plus the
  intended Franchise Beta UX/report changes, without omitting a later product
  fix from `main`.

## Recovery Commit

Commit `c1f56938fc6d9a0a242965e6a52d4e2107c87e81` fully captures the validated
recovery fix. Its only change is making `_assessment_depth()` a non-mutating
getter in `app_files/overview_ui.py`, removing the post-widget session-state
write that caused `StreamlitAPIException`.

The isolated validation snapshot's `overview_ui.py` and `report_ui.py` match
the files at `c1f5693` byte-for-byte. The saved recovery patch describes the
same one-function change and contains no additional product work.

## Local and Historical Branches

| Branch/ref | Relationship to authoritative validation branch | Decision |
| --- | --- | --- |
| `main` / `origin/main` (`dfc8889`) | Diverged after the shared product baseline; later differences are operating records, CI/repository configuration, and marketing website files | Do not merge for Streamlit validation; no active product code is missing |
| `origin/phase-1-franchise-beta` (`c2888a8`) | Ancestor and exact product baseline for PR #1 | Already included |
| `origin/franchise-beta-ui-trust-pass` (`b2e1d04`) | Divergent alternate implementation changing auth, persistence, app shell, routing, workflow config, and many UI files | Do not merge; regression risk |
| local `franchise-beta-ui-trust-pass`, `phase-1-franchise-beta`, and `codex/archive-local-main-before-reconcile` (`b2e1d04`) | Same divergent historical snapshot despite misleading local names | Do not deploy or merge |
| `origin/phase-4b-supabase-auth` (`768e327`) | Historical auth-only line predating later integrated auth/persistence work | Do not merge; current baseline already contains the integrated successor |
| `codex/independent-review-2026-07-30` (`7c0b78a`) | Documentation/review branch; working tree has Howard OS records only | No product code to capture |

## Stranded Work Check

- No tracked or untracked changes exist under `app.py`, `app_files/`,
  `workflows/`, `requirements.txt`, or `workflow_config.py` in the current
  working tree.
- No relevant product change exists only on the local review branch.
- The local recovery patch is duplicate evidence of commit `c1f5693`, not
  stranded product code.
- The temporary validation snapshot matches commit `c1f5693` for both PR files.

## Validation Specification Alignment

The documented external validation specification names branch
`franchise-beta-ux-report-trust-pass` and commit
`c1f56938fc6d9a0a242965e6a52d4e2107c87e81`. The product code to deploy does
not differ from that specification.

Repository records do not identify or verify the branch currently selected in
the external Streamlit deployment console. Before starting validation, confirm
the Streamlit app is explicitly configured to the branch and commit above. Do
not validate `main`, `franchise-beta-ui-trust-pass`, or a local branch with a
similar name.

## Safe Next Step

It is safe to proceed with authenticated Streamlit validation using
non-production Supabase credentials only after the deployed app reports or is
otherwise verified at exact commit `c1f5693`. PR #1 remains open and `REVISE`;
this audit does not authorize merge to production, deployment to production,
publication, pricing changes, customer contact, spending, or production
credential use.

## Local Branch Deletion Audit

No local branch was deleted. These branches have zero commits unique relative
to all `origin/*` refs and are safe deletion candidates after Howard confirms:

- `codex/archive-local-main-before-reconcile` at `b2e1d04`.
- `phase-1-franchise-beta` at `b2e1d04`.
- `franchise-beta-ui-trust-pass` at `b2e1d04`.
- `codex/setup-reconcile` at `ac0ab79`.

Keep local `main`. Keep `codex/independent-review-2026-07-30`: it is the current
branch, contains commit `7c0b78a` not reachable from any `origin/*` ref, and
owns the current uncommitted Howard OS review records.
