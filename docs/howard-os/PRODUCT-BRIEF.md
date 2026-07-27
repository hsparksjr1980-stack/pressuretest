# PressureTest Product Brief

## Product

PressureTest is currently implemented as a Streamlit diligence product with a separate Next.js marketing website.

Current code facts:

- The active Streamlit workflow is `PressureTest: Franchise`.
- Root `app.py` launches `app_files.app.main()`.
- `workflow_config.py` defines `DEFAULT_WORKFLOW = "franchise"` and only the franchise workflow in `WORKFLOW_CONFIG`.
- `app_files/page_config.py` defines a seven-step Franchise Beta path: Start Here, Operator Fit, Opportunity Review, Financial Reality, Commitment Review, Final Decision, Report.
- The website homepage currently positions the product as `PressureTest: Franchise`.

## Product Promise

PressureTest helps prospective franchise operators organize diligence, test assumptions, identify operational pressure points, and prepare for ownership decisions before signing, borrowing, leasing, or investing.

## Advisory Boundary

PressureTest is educational diligence software. It must not present itself as legal, tax, accounting, lending, or investment advice.

## Current Product Owner

Howard Sparks is product owner and final approver.

## Operating Goal

Run one approved product task and one approved marketing task per weekly cycle, with routine execution handled by agents and a consolidated Saturday approval package for Howard.

## TODO

- Confirm the intended public version name after reconciling stale existing docs.
- Confirm whether Startup and Acquisition should remain present only as future placeholders.

