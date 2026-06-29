# PressureTest Workflow

This workflow defines how changes should be planned, implemented, tested, documented, and committed for PressureTest.

## Source of Truth

Before writing code, align with:

- `README.md`
- `docs/CURRENT_STATE.md`
- `docs/ROADMAP.md`
- `docs/SYSTEM_RULES.md`

The current source of truth is **PressureTest: Franchise** and the **Franchise Beta UX + Report Trust Pass** milestone.

## Implementation Rules

- Keep Franchise as the only active product workflow.
- Treat Startup and Acquisition as future placeholders only.
- Keep the 7-step Franchise Beta path intact.
- Keep Quick Assessment as the default.
- Keep Full Review as a depth toggle within the same workflow.
- Preserve one data model and one report.
- Do not add Stripe, native apps, AI agent layers, Pro tools, or new product areas.
- Make targeted, testable changes instead of broad rewrites.

## Required Testing

For code changes:

- Run Python syntax checks for edited modules.
- Start the Streamlit app locally and verify no immediate startup errors.
- Smoke test the affected Franchise Beta path.
- Check mobile-ready behavior at 390px, 430px, and 768px when UI changes are made.

For docs-only changes:

- Verify the docs do not describe Startup or Acquisition as active scope.
- Verify the docs do not imply Stripe or native apps are part of Phase 1.
- Verify run and smoke-test instructions are current.

## Beta Smoke Test

Test:

- Quick Assessment completion
- Full Review depth toggle
- Report generation
- Decision-Critical Issues
- FDD Translation Risk
- Risk labels
- Paid review request form
- Beta feedback form
- Mobile responsiveness

## Commit Discipline

- Review `git status --short` and diffs before committing.
- Stage intentional files explicitly.
- Commit code and documentation updates together for this milestone.
- Use an intent-based commit message.
