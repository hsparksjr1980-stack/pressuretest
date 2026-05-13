# PressureTest

## Current Version

```text
v0.6.0-dev
```

Current development phase:

```text
Phase 4A — Persistence Foundation
```

PressureTest is a workflow-based diligence and operational planning platform built on Streamlit.

The platform currently supports:
- franchise diligence workflow
- startup readiness workflow
- workflow-aware routing architecture
- startup MVP scoring and reporting
- local persistence foundation
- acquisition workflow placeholder architecture

---

# Platform Progression

## Phase 1
```text
Workflow selection foundation
```

Added:
- workflow selector
- franchise/startup/acquisition routing
- placeholder workflow architecture

---

## Phase 2
```text
Workflow Architecture & Shared Engine Foundation
```

Added:
- centralized workflow config
- isolated workflow modules
- shared risk taxonomy
- config-driven workflow routing

---

## Phase 3A
```text
Startup Workflow Shell
```

Added:
- startup workflow registry
- startup-only navigation
- startup page shell architecture

---

## Phase 3B
```text
Startup Assessment State + Questions
```

Added:
- startup-only assessment state
- startup question persistence
- startup readiness summary foundation

---

## Phase 3C
```text
Startup Scoring MVP
```

Added:
- startup scoring engine
- startup readiness signals
- startup validation prompts
- startup risk summaries

---

## Phase 3D
```text
Startup Readiness Report Enhancements
```

Added:
- structured readiness report
- execution pressure sections
- founder/operator considerations
- capital/runway observations
- validation checklist sections

---

## Phase 3E
```text
Startup Workflow UX + Question Depth Polish
```

Added:
- deeper startup diligence questions
- improved startup workflow UX consistency
- expanded market and operational pressure coverage
- expanded startup financial assumption capture
- expanded startup readiness reporting

---

## Phase 4A (Current)
```text
Persistence Foundation
```

Added:
- persistence package structure
- persistence models
- local JSON storage layer
- session serialization helpers
- workflow-aware session snapshots
- save/load/list/delete persistence primitives

Current persistence architecture:

```text
app_files/persistence/
    __init__.py
    models.py
    storage.py
```

Local session storage path:

```text
/data/sessions/
```

Current persistence scope:
- local JSON snapshots only
- no auth yet
- no cloud sync yet
- no database yet
- no API layer yet

---

# Current Workflow Status

## Franchise Workflow
Status:
```text
Primary production workflow
```

Includes:
- franchise scoring
- financial modeling
- reporting
- execution planning
- paywall/pro workflow logic

## Startup Workflow
Status:
```text
Startup readiness MVP
```

Includes:
- startup workflow routing
- startup assessment persistence
- startup scoring MVP
- startup readiness reporting
- expanded startup diligence questions
- startup operational pressure analysis
- startup capital/runway observations

Not yet implemented:
- advanced startup financial modeling
- forecasting engine
- startup PDF export
- production persistence/auth
- startup database layer

## Acquisition Workflow
Status:
```text
Placeholder only
```

---

# Current Architecture

Current platform structure:

```text
UI Layer (Streamlit)
    ↓
Workflow + State Layer
    ↓
Persistence Layer
    ↓
Local JSON Storage
```

Current workflow module structure:

```text
/workflows
    /franchise
    /startup
    /acquisition
```

Persistence structure:

```text
/app_files/persistence
```

Shared architecture includes:
- centralized workflow config
- workflow-aware routing
- isolated workflow state
- startup scoring engine
- startup readiness reporting
- shared risk taxonomy
- local persistence abstraction

---

# Current Constraints

PressureTest intentionally does NOT yet include:
- Postgres/Supabase
- authentication system
- multi-user tenancy
- billing backend
- API services
- cloud persistence
- background jobs
- advanced forecasting engine
- enterprise infrastructure

The platform is currently transitioning from:

```text
prototype workflow application
```

toward:

```text
persistent multi-workflow diligence platform
```

---

# Run Locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=. streamlit run app.py
```

---

# Advisory Boundary

PressureTest is an educational diligence and operational planning platform.

It does not provide:
- investment advice
- legal advice
- tax advice
- accounting advice
- lending advice

Users should independently validate assumptions and consult qualified professionals before making business decisions.
