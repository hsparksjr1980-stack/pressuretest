
# PressureTest Roadmap

# v1.7 Scope (Audit-Aligned, Limited Release)

v1.7 is intentionally constrained to five high-ROI improvements. The goal is to stabilize core user flow, reduce overwhelm, and improve consistency before adding net-new features.

## 1) Stabilize app/nav/report flow files

### Objective
Eliminate flow instability and conflicting behaviors in core routing, navigation, and report rendering.

### In Scope
- Stabilize app orchestration and page handoff behavior.
- Resolve inconsistent navigation/state/report pathways.
- Standardize report entry points and expected user progression.

### Success Criteria
- One clear navigation path through core pages.
- Report flow behavior is predictable and consistent.
- No conflicting implementations active in app/nav/report flow files.

## 2) Centralize Free/Pro boundary copy and logic

### Objective
Use one source of truth for boundary messaging and unlock behavior.

### In Scope
- Consolidate Free/Pro copy into a shared source.
- Standardize gating logic and unlock checks across pages.
- Keep tone aligned with system rules: direct, practical, no hype, no fear tactics.

### Success Criteria
- Boundary language is consistent across all gated surfaces.
- Unlock behavior is consistent regardless of entry point.
- Reduced duplication of paywall/gating logic.

## 3) Create reusable assessment page template

### Objective
Create a shared template pattern for assessment-style pages to improve consistency and maintainability.

### In Scope
- Define common assessment scaffold (header, progress, section grouping, scoring summary, next-step CTA).
- Apply shared structure to core assessment experiences.
- Reduce repeated per-page implementation patterns.

### Success Criteria
- Core assessment pages follow one consistent interaction pattern.
- Shared template reduces repeated logic and layout drift.
- Faster iteration for future assessment refinements.

## 4) Reduce onboarding text density with progressive disclosure

### Objective
Lower cognitive load in early user flow by chunking content and revealing detail as needed.

### In Scope
- Break large onboarding/assessment content into smaller guided steps.
- Replace dense static text blocks with staged disclosure patterns.
- Improve clarity of “what to do next” at each step.

### Success Criteria
- Early flow feels lighter and easier to complete.
- Fewer walls of text in onboarding-adjacent pages.
- Clear next action visible at each major step.

## 5) Standardize shared UI primitives

### Objective
Use one consistent set of reusable UI primitives for cards, spacing, typography, and status/pill elements.

### In Scope
- Align core pages to a shared primitive system.
- Reduce page-specific style drift where practical.
- Improve visual consistency while preserving current brand direction.

### Success Criteria
- Page-to-page UI feels cohesive and deliberate.
- Reduced duplicate component/style patterns.
- Improved maintainability for future UX updates.

## Explicitly Out of Scope for v1.7

- New major feature modules (deal workspace, buildout tracker, vendor tracking, etc.)
- SEO/content expansion initiatives
- Broader platform expansion beyond core diligence flow stabilization

## v1.7 Release Principle

Stability and consistency first. v1.7 is a foundation release to reduce overwhelm, improve trust, and make subsequent feature work lower risk.