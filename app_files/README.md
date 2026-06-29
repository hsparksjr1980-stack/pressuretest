# PressureTest App Files

This folder contains the Streamlit implementation for **PressureTest: Franchise**.

The active beta product is the 7-step Franchise Beta workflow:

1. Start Here
2. Operator Fit
3. Opportunity Review
4. Financial Reality
5. Commitment Review
6. Final Decision
7. Report

Startup and Acquisition code may exist in the repo as legacy or placeholder architecture, but they are not active product scope for this phase.

## Current Milestone

**Franchise Beta UX + Report Trust Pass**

Implementation priorities:

- Quick Assessment is the default path.
- Full Review is a depth toggle inside the same workflow.
- Go Deeper sections hold detail without creating a separate workflow.
- The report is the core artifact.
- Decision-Critical Issues and FDD Translation Risk are core report concepts.
- Paid review remains manual.
- Beta feedback remains after the report and is stored locally for review.
- The app should be mobile-ready web, not a native app.

## Run Locally

From the repo root:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Local Review Data

Manual paid review requests and beta feedback are written to local files under `data/` when submitted. These are prototype-friendly review stores, not production CRM or billing integrations.

## Advisory Boundary

PressureTest is a diligence-support tool. It is not legal, tax, accounting, lending, or investment advice.
