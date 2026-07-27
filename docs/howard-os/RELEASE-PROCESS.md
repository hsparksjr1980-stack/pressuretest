# Release Process

## Branching

Agents should create isolated task branches from the current approved base. Use clear branch names that identify product or marketing scope.

## Pull Requests

Every task branch should open or update a pull request before Howard review.

## Validation

Website validation:

```bash
cd website
npm run lint
npm run typecheck
npm run build
```

Python validation:

- Run syntax/import checks for edited modules.
- Run the closest available app startup or path-specific checks.
- There is no committed Python test runner currently confirmed.

## Howard Approval Gates

No merge, deployment, publication, spending, or consequential action without Howard approval.

## Saturday Approval Package

Agents consolidate:

- What changed.
- Why it changed.
- Validation results.
- Screenshots or artifacts when relevant.
- Known risks.
- Required Howard decisions.

## TODO

- Confirm production deployment provider.
- Confirm release branch protection rules.
- Confirm required GitHub checks after first CI run.

