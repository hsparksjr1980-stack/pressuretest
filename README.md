# PressureTest

PressureTest is currently focused on **PressureTest: Franchise**.

Positioning: **Stress-test a franchise before you sign, borrow, lease, or invest.**

The active beta product is the **7-step Franchise Beta workflow**:

1. Start Here
2. Operator Fit
3. Opportunity Review
4. Financial Reality
5. Commitment Review
6. Final Decision
7. Report

The current milestone is **Franchise Beta Modern UI + Trust Pass**. The goal is to make the correct Franchise Beta workflow feel modern, polished, credible, mobile-ready, and report-focused before private beta users go through it.

## Current Scope

- Franchise is the only active product workflow.
- Startup and Acquisition are future placeholders only.
- Quick Assessment is the default path.
- Full Review is a depth toggle inside the same Franchise workflow, not a separate product.
- The report is the core product artifact.
- Paid review remains manual. Do not build Stripe in this phase.
- Native iOS and Android apps are not part of this phase. The requirement is mobile-ready web.

## Core Report Concepts

The report should read like a cautious decision memo someone could share with a spouse, business partner, lender, CPA, attorney, franchise consultant, or potential investor.

Core report concepts:

- **Decision-Critical Issues**: the 3-5 issues most likely to change the decision, trigger a pause, or require verification before further commitment.
- **FDD Translation Risk**: the risk that system-wide FDD information may not prove the model works in the user's specific market, rent structure, labor market, buildout environment, supply chain, customer-demand profile, brand-awareness conditions, operator situation, or financing pressure.

Risk labels:

- Low Concern
- Needs Verification
- Material Risk
- Stop and Review

Low Concern does not mean safe or recommended. It means low concern based on the information provided.

## Product Voice

PressureTest should be cautious, fair, direct, practical, skeptical but not cynical, calm, clear, helpful, and pro-diligence.

PressureTest should not present itself as legal, tax, accounting, lending, or investment advice. It should help users organize diligence, identify risk signals, clarify missing evidence, and prepare better questions for professionals and stakeholders.

Use cautious language such as:

- Based on the information provided...
- This may indicate risk...
- This should be verified...
- This could materially affect the decision...
- System-wide information may not translate directly to this market...
- Local economics should be validated before further commitment...

Avoid overconfident language such as safe, approved, guaranteed, good investment, bad investment, you should buy this, or this will be profitable.

## Run Locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Open the local Streamlit URL shown in the terminal.

## Smoke Test

Use the Franchise Beta workflow and verify:

- First impression clearly communicates PressureTest: Franchise and "Stress-test a franchise before you invest."
- Quick Assessment and Full Review appear as polished selection cards.
- Quick Assessment is selected by default on Start Here.
- Full Review can be selected without losing existing answers.
- Operator Fit, Opportunity Review, Financial Reality, Commitment Review, Final Decision, and Report are reachable in order.
- Report generation shows Recommendation, Decision-Critical Issues, Top Risks, Missing Evidence, FDD Translation Risk when triggered, paid review CTA, and Beta Feedback.
- Sidebar shows useful workflow, step, progress, and risk signal information without developer-facing controls.
- Risk labels use only Low Concern, Needs Verification, Material Risk, and Stop and Review.
- Paid review request form saves manual follow-up data locally.
- Beta feedback form saves reviewable feedback locally.
- Mobile widths around 390px, 430px, and 768px have no horizontal scrolling and readable report content.

## Out of Scope

Do not add Stripe, native apps, AI agent layers, Pro tools, Startup expansion, Acquisition expansion, or new product areas during this phase.
