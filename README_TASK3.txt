PressureTest Task #3 — Lead capture architecture

Install:
1. Copy these files into the app root, replacing existing files where names match:
   - app_state.py
   - free_report_ui.py
   - report_ui.py
   - lead_capture_ui.py
   - lead_capture_store.py

2. Or apply pressuretest_task3.patch from the repository root if your local code already includes Task #1 and Task #2.

What changed:
- Adds reusable lead-capture components.
- Adds local CRM-ready lead storage in data/leads.csv and data/leads.jsonl.
- Gates Free Pressure Snapshot PDF download behind a practical email capture form.
- Gates Executive Diligence Report PDF download behind the same reusable capture flow.
- Stores per-asset capture state in st.session_state['lead_captured_assets'].

Production note:
- lead_capture_store.py is intentionally local-file based for prototype use.
- Replace save_lead_record() with a CRM, database, or email platform integration when deploying publicly.
