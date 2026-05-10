# PressureTest

## Current Version

```text
v0.5.0-dev
```

Current development phase:

```text
Phase 3C — Startup Scoring MVP
```

PressureTest is a Streamlit app for evaluating franchise opportunities and early-stage startup concepts through structured operational diligence workflows.

The platform now supports:
- franchise diligence workflow (primary production workflow)
- startup workflow shell with startup assessment-state capture and MVP scoring
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
Scoring MVP
```

Currently includes:
- isolated startup workflow routing
- startup-only navigation
- startup assessment questions
- startup session-state persistence
- startup readiness summary page
- startup MVP readiness scoring
- startup risk-flag summaries
- startup validation-question prompts

Startup scoring currently evaluates:
- liquidity/runway pressure
- market validation
- pricing assumptions
- customer acquisition approach
- founder/operator involvement
- execution complexity
- launch readiness

Not yet implemented:
- advanced startup financial modeling
- startup generated recommendations
- startup database persistence
- acquisition workflow engine

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

The Startup Readiness Report currently provides:
- MVP startup signal
- scoring summary
- top risks
- strongest signals
- weakest assumptions
- next validation questions
- startup answer summary

The report does not provide:
- investment recommendations
- legal advice
- tax advice
- accounting advice
- lending advice
- guaranteed outcomes

---

## Architecture Notes

The repo contains isolated workflow boundaries:

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
- startup-only scoring engine

Franchise workflow logic remains isolated from startup workflow state and startup scoring.

---

## Core Constraints

Current implementation intentionally avoids:
- shared scoring engines between workflows
- advanced startup financial modeling
- generated investment recommendations
- acquisition workflow logic
- database persistence
- production auth/payment infrastructure

The current startup workflow is intentionally scoped as:

```text
startup workflow + MVP readiness scoring
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
