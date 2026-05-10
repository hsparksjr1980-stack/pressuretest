# PressureTest Phase 1 Production Shell

This folder is a plug-and-play Phase 1 version of your current Streamlit app.

## What changed

- New premium `app.py` entry point
- New cockpit-style Home page
- New premium CSS/components
- Local JSON export/import instead of paid database storage
- Pro preview access enabled without Stripe/paywall plumbing
- Demo scenario loader
- Clean `.gitignore`

## How to run

```bash
cd pressuretest_phase1
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Important

This still uses your existing page modules and logic. It is meant to make the current prototype feel more like a real product without adding paid storage, auth, or payment systems yet.

## Later Phase 2

- Supabase or Postgres storage
- Auth with Clerk/Auth0/Supabase Auth
- Stripe checkout
- Real PDF report engine
- Admin dashboard
- Automated tests


## Advisory Boundary
PressureTest is a blunt operating and diligence screen. It is not legal, tax, lending, accounting, or investment advice. Users should validate findings with qualified advisors before signing franchise, lease, loan, or other binding documents.
