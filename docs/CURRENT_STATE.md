# Current PressureTest State

## Current Focus

PressureTest is currently focused on **PressureTest: Franchise**.

The active beta product is the **7-step Franchise Beta workflow**:

1. Start Here
2. Operator Fit
3. Opportunity Review
4. Financial Reality
5. Commitment Review
6. Final Decision
7. Report

Startup and Acquisition are future placeholders only. They should not be described as active workflows.

## Current Milestone

**Franchise Beta Modern UI + Trust Pass**

The milestone goal is not to make the app bigger. The goal is to make the correct Franchise Beta workflow feel modern, polished, credible, mobile-ready, and report-focused before private beta users go through it.

## Product Direction

Positioning: **Stress-test a franchise before you sign, borrow, lease, or invest.**

PressureTest exists to slow the decision down and help the user ask:

- What actually matters here?
- What is missing?
- What has not been verified?
- What assumptions am I making?
- What would make this harder to unwind?
- What should I ask before signing, borrowing, leasing, or investing?

PressureTest is not anti-franchise or pro-franchise. It is pro-diligence.

## Active Product Rules

- Quick Assessment is the default path.
- Full Review is a depth toggle within the same Franchise workflow, not a separate product.
- The same data model and report are used for both depths.
- Users should be able to switch from Quick Assessment to Full Review without losing answers.
- The report is the core product artifact.
- Paid review remains manual.
- Stripe is not part of this phase.
- Native iOS and Android apps are not part of this phase.
- The current requirement is mobile-ready web.

## UI Quality Bar

Design target: modern underwriting tool + guided decision memo.

The app should not feel like a default Streamlit app, a basic questionnaire, a school project, a generic form builder, or a rough prototype.

The app should feel:

- Clean
- Serious
- Modern
- Calm
- Premium enough to trust
- Easy to complete
- Report-focused

The first screen should clearly communicate:

- PressureTest: Franchise
- Stress-test a franchise before you invest.
- Quick Assessment is the default path.
- Full Review is a deeper version of the same workflow.
- The report is the main artifact.

## Core Report Concepts

**Decision-Critical Issues** are a core report concept. They are the 3-5 issues most likely to change the decision, trigger a pause, or require verification before further commitment.

Each Decision-Critical Issue should include:

- Issue title
- Risk label
- Why it matters
- What to verify next

**FDD Translation Risk** is a named PressureTest concept. The FDD is important, but it is often system-wide. It may not prove the model works in the user's specific market, rent structure, labor market, buildout environment, supply chain, customer-demand profile, brand-awareness conditions, operator situation, or financing pressure.

Risk labels:

- Low Concern
- Needs Verification
- Material Risk
- Stop and Review

Low Concern does not mean safe or recommended. It only means low concern based on the information provided.

## Product Voice

The voice should be:

- Cautious
- Fair
- Direct
- Practical
- Skeptical but not cynical
- Calm, not alarmist
- Clear, not academic
- Helpful, not salesy
- Founder-led, but not overly personal
- Serious enough for someone risking real money

PressureTest should not present itself as legal, tax, accounting, lending, or investment advice.

## Current Stack

- Python
- Streamlit
- Local file capture for beta feedback and manual paid review requests
- Next.js marketing site in `website/`

## Current Risks / Weaknesses

- Some legacy modules still exist in the repo but are not active Franchise Beta scope.
- Financial Reality remains a long screen and should continue to be simplified over time.
- Mobile readiness should be checked manually at 390px, 430px, and 768px during beta passes.
