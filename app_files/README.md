# PressureTest

## Current Version

```text
v0.5.0-dev
```

Current development phase:

```text
Phase 3D — Startup Readiness Report Enhancements
```

PressureTest is a Streamlit app for evaluating franchise opportunities and early-stage startup concepts through structured operational diligence workflows.

The platform now supports:
- franchise diligence workflow (primary production workflow)
- startup workflow shell with startup assessment-state capture and MVP scoring
- structured startup readiness reporting
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
Readiness-report MVP
```

Currently includes:
- isolated startup workflow routing
- startup-only navigation
- startup assessment questions
- startup session-state persistence
- startup MVP readiness scoring
- startup readiness report enhancements
- startup risk-flag summaries
- startup validation-question prompts
- startup readiness observations

Startup scoring currently evaluates:
- liquidity/runway pressure
- market validation
- pricing assumptions
- customer acquisition approach
- founder/operator involvement
- execution complexity
- launch readiness

Startup readiness report now includes:
- startup readiness signal
- key risk areas
- strongest signals
- weakest assumptions
- execution pressure areas
- validation questions
- founder/operator considerations
- capital and runway observations
- final readiness summary

Not yet implemented:
- advanced startup financial modeling
- startup forecasting engine
- startup PDF export
- startup generated investment recommendations
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
- structured scoring summary
- operator-focused risk observations
- startup validation checklist
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
- deterministic predictions

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
- startup readiness report layer

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
startup workflow + MVP readiness reporting
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
