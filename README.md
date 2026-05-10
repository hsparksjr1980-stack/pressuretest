# PressureTest

## Current Version

```text
v0.5.0-dev
```

Current development phase:

```text
Phase 3B — Startup Assessment State + Questions
```

PressureTest is a Streamlit app for evaluating franchise opportunities and early-stage startup concepts through structured operational diligence workflows.

The platform now supports:
- franchise diligence workflow (primary production workflow)
- startup workflow shell with startup assessment-state capture
- acquisition workflow placeholder architecture

---

## Workflow Status

### Franchise Workflow
Status:
```text
Production workflow
```

Includes:
- scoring
- financial modeling
- reports
- execution tooling
- gated Pro workflow

### Startup Workflow
Status:
```text
Assessment-state MVP
```

Currently includes:
- isolated startup workflow routing
- startup-only navigation
- startup assessment questions
- startup session-state persistence
- startup assessment summary page

Not yet implemented:
- startup scoring
- startup calculations
- startup recommendations
- generated startup reports
- startup persistence/database layer

### Acquisition Workflow
Status:
```text
Placeholder only
```

---

## Startup Workflow Pages

```text
Startup Overview
Startup Concept Validation
Startup Market Pressure Test
Startup Financial Assumptions
Startup Readiness Report
```

The Startup Readiness Report currently summarizes entered answers only.

It does not generate:
- scores
- recommendations
- calculations
- advisory conclusions

---

## Architecture Notes

The repo now contains isolated workflow boundaries:

```text
/workflows
    /franchise
    /startup
    /acquisition
```

Shared platform architecture includes:
- centralized workflow config
- workflow-aware routing
- isolated startup state handling
- shared risk taxonomy foundation
- startup-only navigation registry

Franchise workflow logic remains isolated from startup workflow state.

---

## Core Constraints

Current implementation intentionally avoids:
- shared scoring engines between workflows
- startup financial modeling
- startup advisory outputs
- acquisition workflow logic
- database persistence
- production auth/payment infrastructure

The current startup workflow is intentionally scoped as:

```text
workflow shell + assessment-state capture
```

not:

```text
full startup diligence engine
```

---

## Run Locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

---

## Advisory Boundary

PressureTest is an educational diligence and operational planning platform.

It is not:
- legal advice
- tax advice
- accounting advice
- lending advice
- investment advice

Users should independently validate assumptions and consult qualified professionals before making business decisions.
