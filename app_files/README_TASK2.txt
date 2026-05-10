Task #2 - Downloadable Executive Report

Copy these files into the root of the PressureTest Streamlit app:

- pdf_report_engine.py     (new)
- report_templates.py      (full replacement)
- report_ui.py             (full replacement)
- free_report_ui.py        (full replacement)

Then run:

python -m py_compile report_templates.py pdf_report_engine.py report_ui.py free_report_ui.py
streamlit run app.py

What changes:

- Adds a reusable ReportLab PDF engine.
- Replaces the old free report PDF with a branded Free Pressure Snapshot.
- Replaces the main Report screen with an Executive Diligence Report download.
- Adds executive summary, decision snapshot, section scores, risks, strengths, conditions, financial snapshot, next-step checklist, profile snapshot, and educational boundary language.
