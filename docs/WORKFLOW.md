# PressureTest Workflow

This workflow defines how changes should be planned, implemented, tested, and committed for PressureTest.
It is aligned with current source-of-truth docs:

- `docs/SYSTEM_RULES.md`
- `docs/CURRENT_STATE.md`
- `docs/ROADMAP.md`
- `docs/CHANGELOG.md`

The goals are stability, clarity, reduced overwhelm, and disciplined iteration.

## 1) Implementation Approach

### Start from source-of-truth docs first

Before writing or editing code, confirm that planned changes align with:

- product direction (operator-first, practical, non-hype)
- UX principles (clarity over complexity, reduce overwhelm, progressive disclosure)
- engineering principles (small, testable, modular updates)
- current release scope (v1.7 priorities and out-of-scope constraints)

### Implement in small, testable slices

- Prefer targeted changes over broad rewrites.
- Keep each change scoped to a single clear outcome.
- Preserve existing visual language and component patterns unless explicitly approved.
- Reuse existing shared utilities before adding new abstractions.

### Respect app stability first

- Stabilize app/nav/report flow before adding optional enhancements.
- Avoid introducing large new dependencies unless clearly justified.
- Avoid changing multiple high-risk flows in a single pass.

## 2) Requirement: Explain Changed Files Before Editing

Before any edit, explicitly list:

- which files will be changed
- why each file needs to change
- what will not be changed in that step

This is mandatory for both docs and code work. No silent edits.

## 3) Scope Limiting Rules

### Keep work inside agreed scope

- Do not add adjacent “nice-to-have” work during an implementation pass.
- If a new issue is discovered, log it separately and continue the scoped task unless it blocks execution.
- Treat roadmap out-of-scope items as deferred by default.

### One objective per change set

Each change set should map to one primary objective (for example: "centralize Free/Pro copy", "assessment template POC", "nav stabilization").

### Protect low-risk rollout

- Start with one lower-risk page for new patterns.
- Validate behavior before expanding pattern to additional pages.
- Prefer proof-of-concept integration before broad migration.

## 4) Testing Expectations

### Baseline checks for every change

- Syntax/compile checks for edited Python modules.
- Lint checks for edited files (or closest available equivalent).
- Run app startup (`streamlit run app.py`) and verify no immediate import/runtime errors.

### Feature-path verification

For user-facing changes, verify the specific path touched:

- page renders
- key input interactions still function
- next-step/navigation behavior is intact
- no obvious regression in tone/compliance boundary messaging

### Proportional testing discipline

- Docs-only changes: verify formatting/readability and link/path references.
- UI/component changes: verify affected page path manually.
- Flow/state changes: verify entry, transition, and exit states.

## 5) Commit Discipline

### Commit quality bar

- Keep commits focused and reviewable.
- Commit message should reflect intent, not just file names.
- Avoid mixing unrelated changes in one commit.
- Separate stabilization fixes from feature/pattern work when feasible.

### Recommended commit structure

- Commit 1: stabilization/fix (if needed)
- Commit 2: scoped feature/pattern change
- Commit 3: docs/update notes (if separate)

### Commit only what is intentional

- Review status and diff before committing.
- Do not include accidental local artifacts.
- Do not include unrelated untracked files.

## 6) Cursor Staging Rules

When staging in Cursor/git:

- Stage files explicitly by path when possible (avoid blind all-file staging).
- Confirm staged diff matches the stated scope.
- If unrelated files are modified, leave them unstaged unless intentionally part of the task.
- For multi-step work, stage and commit in logical chunks.

Recommended flow:

1. `git status --short`
2. `git diff` (and `git diff --staged` if applicable)
3. stage only scoped files
4. commit with intent-based message
5. `git status` verification

## 7) Push and Integration Rules

- Push only after local checks pass for the scoped change.
- If remote has diverged, prefer rebase with explicit conflict resolution.
- Never force push shared branches unless explicitly approved.

## 8) Workflow Guardrails for PressureTest Tone and UX

Any implementation should preserve:

- blunt but fair, operator-focused tone
- no hype / no fear tactics
- practical "what to validate next" guidance
- cautionary framing (not legal, tax, lending, accounting, investment advice)
- reduced cognitive overload and clear next-step progression

If a change weakens these principles, revise before merge.
