# Decision Log

## 2026-07-27 - Install Howard OS Initial Operating System

Decision: install repository-level agent instructions, Howard OS docs, GitHub task templates, pull request template, and CI workflow.

Rationale: PressureTest needs a weekly operating cadence that agents can execute without routine Howard involvement, while preserving Howard approval for consequential actions.

Boundaries:

- No product behavior changes.
- No application logic changes.
- No authentication or persistence changes.
- No database schema changes.
- No pricing, monetization, publication, deployment, merge, or push.

## Standing Decisions

- Howard is product owner and final approver.
- Agents handle routine execution after a task is approved.
- Saturday approval package is the normal approval checkpoint.
- One product task and one marketing task maximum per weekly cycle.

## 2026-08-01 - Post-Approval Audit Found No Actionable Approval

Decision status: no explicit Howard approval was found for an exact
current-cycle product pull request or versioned marketing deliverable.

Action: no merge, deployment, publication, sending, spending, or stage advance
was performed. Product and marketing remain `BLOCKED` because the weekly cycle
and eligible task records are absent. Live GitHub verification was also blocked
by invalid local authentication and an unreachable API.

Required decision: Howard should define the weekly cycle and explicitly approve
up to one eligible product issue and one eligible marketing issue. Until then,
historical pull request #1 and all unpublished work remain unchanged.

## 2026-08-08 - Post-Approval Audit Found No Actionable Approval

Decision status: no explicit Howard approval was found for an exact
current-cycle product task, branch, pull request, or versioned marketing
deliverable. The 2026-08-08 Saturday package requests no consequential release
approval.

Action: no merge, deployment, publication, sending, spending, or stage advance
was performed. Product and marketing remain `BLOCKED` before `PROPOSED`.
Historical pull request #1 and all unpublished work remain unchanged.

Verification note: live GitHub state could not be revalidated because the
configured `gh` credential is invalid. This is an additional release blocker,
not evidence of approval.

Required decision: Howard should define the weekly cycle and explicitly approve
up to one fully specified, eligible product issue and one fully specified,
eligible marketing issue through the required Monday selection reviews.

## 2026-08-15 - Post-Approval Audit Found No Actionable Approval

Decision status: no explicit Howard approval was found for an exact
current-cycle product task, branch, pull request, or versioned marketing
deliverable. The 2026-08-15 Saturday package requests no consequential release
approval.

Action: no merge, deployment, publication, sending, scheduling, promotion,
spending, or stage advance was performed. Product and marketing remain
`BLOCKED` before `PROPOSED`; historical pull request #1 remains unchanged.

Verification note: live GitHub state could not be revalidated because the
configured credential is invalid. This is an additional verification blocker,
not evidence of approval.

Required decision: Howard should define the weekly cycle and explicitly approve
up to one fully specified, eligible product issue and one fully specified,
eligible marketing issue through the required Monday selection reviews.

## 2026-08-22 - Post-Approval Audit Found No Actionable Approval

Decision status: the Saturday package explicitly requests no merge, deployment,
publication, or sending approval and directs Howard not to approve a
consequential release action. No separate explicit approval is recorded.

Action: no merge, deployment, publication, sending, scheduling, promotion,
spending, or release-stage advance was performed. Product remains `FIXES` /
`BLOCKED`; marketing remains `BLOCKED` before `PROPOSED`.

Mismatch: the package records PR head `c1f5693`, while the later branch-capture
audit records `bc07adf` as the complete target after two more fixes. Live GitHub
state could not be confirmed because the configured credential is invalid.

Required decision: after external authenticated validation and independent
approval at exact head `bc07adf`, Howard must explicitly approve that exact PR
version before merge. Marketing requires selection of one exact eligible task
before any deliverable or publication approval can exist.
