# pdf_report_engine.py

from __future__ import annotations

import io
import os
from typing import Any

from reportlab.lib.colors import HexColor, black
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas

from report_templates import (
    build_condition_lines,
    build_decision_headline,
    build_executive_summary_text,
    build_profile_lines,
    build_risk_lines,
    build_strength_lines,
    money,
    safe_text,
)

NAVY = HexColor("#0B1730")
BLUE = HexColor("#2563EB")
ORANGE = HexColor("#F97316")
GREEN = HexColor("#16A34A")
RED = HexColor("#DC2626")
AMBER = HexColor("#D97706")
SLATE = HexColor("#5B6577")
LIGHT_SLATE = HexColor("#94A3B8")
BORDER = HexColor("#E2E8F0")
SOFT = HexColor("#F8FAFC")
WHITE = HexColor("#FFFFFF")


def _get_logo_path() -> str:
    base = os.path.dirname(os.path.abspath(__file__))
    for name in ("logo.png", "logo.jpeg", "logo.jpg"):
        path = os.path.join(base, name)
        if os.path.exists(path):
            return path
    return os.path.join(base, "logo.png")


def _score_band(score: float | None) -> str:
    if score is None:
        return "neutral"
    if score >= 78:
        return "strong"
    if score >= 58:
        return "mixed"
    return "weak"


def _band_color(score: float | None) -> HexColor:
    band = _score_band(score)
    if band == "strong":
        return GREEN
    if band == "mixed":
        return AMBER
    if band == "weak":
        return RED
    return LIGHT_SLATE


def _wrap_lines(text: str, max_width: float, font_name: str, font_size: int) -> list[str]:
    text = safe_text(text, "")
    words = text.split()
    if not words:
        return [""]
    lines: list[str] = []
    current = words[0]
    for word in words[1:]:
        candidate = f"{current} {word}"
        if stringWidth(candidate, font_name, font_size) <= max_width:
            current = candidate
        else:
            lines.append(current)
            current = word
    lines.append(current)
    return lines


class ExecutivePdf:
    def __init__(self, title: str, subtitle: str = "") -> None:
        self.buffer = io.BytesIO()
        self.c = canvas.Canvas(self.buffer, pagesize=LETTER)
        self.width, self.height = LETTER
        self.left = 50
        self.right = 50
        self.usable_width = self.width - self.left - self.right
        self.y = self.height - 52
        self.page_no = 1
        self.title = title
        self.subtitle = subtitle

    def finish(self) -> bytes:
        self._footer()
        self.c.save()
        pdf = self.buffer.getvalue()
        self.buffer.close()
        return pdf

    def _footer(self) -> None:
        self.c.setStrokeColor(BORDER)
        self.c.line(self.left, 34, self.width - self.right, 34)
        self.c.setFont("Helvetica", 8)
        self.c.setFillColor(SLATE)
        self.c.drawString(self.left, 22, "PressureTest - educational diligence report")
        self.c.drawRightString(self.width - self.right, 22, f"Page {self.page_no}")

    def new_page(self) -> None:
        self._footer()
        self.c.showPage()
        self.page_no += 1
        self.y = self.height - 56

    def ensure(self, needed: float) -> None:
        if self.y - needed < 58:
            self.new_page()

    def cover_header(self, report_data: dict[str, Any]) -> None:
        logo_path = _get_logo_path()
        if os.path.exists(logo_path):
            try:
                logo = ImageReader(logo_path)
                self.c.drawImage(
                    logo,
                    self.left,
                    self.y - 14,
                    width=228,
                    height=58,
                    preserveAspectRatio=True,
                    mask="auto",
                )
            except Exception:
                pass

        self.c.setFont("Helvetica-Bold", 21)
        self.c.setFillColor(NAVY)
        self.c.drawRightString(self.width - self.right, self.y + 4, self.title)
        self.y -= 24
        self.c.setFont("Helvetica", 9)
        self.c.setFillColor(SLATE)
        self.c.drawRightString(self.width - self.right, self.y, f"Prepared on {report_data.get('report_date', '-')}")
        if self.subtitle:
            self.y -= 13
            self.c.drawRightString(self.width - self.right, self.y, self.subtitle)
        self.y -= 22
        self.c.setStrokeColor(ORANGE)
        self.c.setLineWidth(2)
        self.c.line(self.left, self.y, self.width - self.right, self.y)
        self.y -= 24

    def title_card(self, report_data: dict[str, Any]) -> None:
        self.c.setFillColor(SOFT)
        self.c.setStrokeColor(BORDER)
        self.c.roundRect(self.left, self.y - 92, self.usable_width, 88, 12, fill=1, stroke=1)

        self.c.setFillColor(NAVY)
        self.c.setFont("Helvetica-Bold", 15)
        self.c.drawString(self.left + 14, self.y - 22, safe_text(report_data.get("franchise_name"), "Opportunity"))
        self.c.setFont("Helvetica", 9)
        self.c.setFillColor(SLATE)
        self.c.drawString(self.left + 14, self.y - 41, build_decision_headline(report_data)[:105])
        self.c.drawString(self.left + 14, self.y - 61, f"Client: {safe_text(report_data.get('full_name'))}")
        self.c.drawString(self.left + 14, self.y - 77, f"Location: {safe_text(report_data.get('city_state'))}")
        self.c.drawRightString(self.width - self.right - 14, self.y - 77, f"Ownership: {safe_text(report_data.get('ownership_style'))}")
        self.y -= 116

    def section(self, title: str) -> None:
        self.ensure(38)
        self.c.setStrokeColor(BORDER)
        self.c.line(self.left, self.y + 5, self.width - self.right, self.y + 5)
        self.c.setFont("Helvetica-Bold", 12)
        self.c.setFillColor(NAVY)
        self.c.drawString(self.left, self.y - 10, title)
        self.y -= 30

    def paragraph(self, text: str, font_size: int = 10, leading: int = 14) -> None:
        self.c.setFont("Helvetica", font_size)
        self.c.setFillColor(black)
        for line in _wrap_lines(text, self.usable_width, "Helvetica", font_size):
            self.ensure(leading + 4)
            self.c.drawString(self.left, self.y, line)
            self.y -= leading
        self.y -= 6

    def bullets(self, items: list[str], width: float | None = None, font_size: int = 10) -> None:
        line_width = width or self.usable_width
        for item in items:
            for idx, line in enumerate(_wrap_lines(f"- {item}", line_width, "Helvetica", font_size)):
                self.ensure(18)
                self.c.setFont("Helvetica", font_size)
                self.c.setFillColor(black)
                self.c.drawString(self.left + (0 if idx == 0 else 10), self.y, line)
                self.y -= 14
        self.y -= 6

    def metric_box(self, x: float, y: float, w: float, h: float, label: str, value: str, score: float | None = None) -> None:
        accent = _band_color(score)
        self.c.setFillColor(WHITE)
        self.c.setStrokeColor(BORDER)
        self.c.roundRect(x, y - h, w, h, 10, fill=1, stroke=1)
        self.c.setFillColor(accent)
        self.c.roundRect(x + 10, y - 16, 42, 6, 3, fill=1, stroke=0)
        self.c.setFillColor(SLATE)
        self.c.setFont("Helvetica", 7.5)
        self.c.drawString(x + 10, y - 30, label.upper()[:28])
        self.c.setFillColor(NAVY)
        self.c.setFont("Helvetica-Bold", 13)
        value_lines = _wrap_lines(value, w - 20, "Helvetica-Bold", 13)
        self.c.drawString(x + 10, y - 49, value_lines[0][:34])

    def metric_grid(self, items: list[tuple[str, str, float | None]], columns: int = 3) -> None:
        if not items:
            return
        gap = 12
        box_w = (self.usable_width - gap * (columns - 1)) / columns
        box_h = 60
        for i, (label, value, score) in enumerate(items):
            if i % columns == 0:
                self.ensure(box_h + 18)
                row_y = self.y
            x = self.left + (i % columns) * (box_w + gap)
            self.metric_box(x, row_y, box_w, box_h, label, value, score)
            if i % columns == columns - 1 or i == len(items) - 1:
                self.y -= box_h + 16

    def key_value_table(self, rows: dict[str, str]) -> None:
        for label, value in rows.items():
            self.ensure(20)
            self.c.setFillColor(SLATE)
            self.c.setFont("Helvetica", 9)
            self.c.drawString(self.left, self.y, label)
            self.c.setFillColor(NAVY)
            self.c.setFont("Helvetica-Bold", 9)
            self.c.drawRightString(self.width - self.right, self.y, safe_text(value))
            self.y -= 17
        self.y -= 6

    def disclaimer_box(self) -> None:
        text = (
            "Boundary: PressureTest is an educational diligence and planning tool. It does not provide legal, financial, "
            "tax, accounting, or investment advice, does not recommend investments, and does not guarantee outcomes. "
            "Users should independently validate assumptions and consult qualified professionals before making commitments."
        )
        self.ensure(78)
        self.c.setFillColor(SOFT)
        self.c.setStrokeColor(BORDER)
        self.c.roundRect(self.left, self.y - 72, self.usable_width, 68, 10, fill=1, stroke=1)
        self.c.setFillColor(SLATE)
        self.c.setFont("Helvetica", 8.5)
        y = self.y - 20
        for line in _wrap_lines(text, self.usable_width - 24, "Helvetica", 8.5):
            self.c.drawString(self.left + 12, y, line)
            y -= 12
        self.y -= 86


def build_executive_report_pdf(report_data: dict[str, Any]) -> bytes:
    pdf = ExecutivePdf("Executive Diligence Report", "Decision summary and next-step operating risks")
    pdf.cover_header(report_data)
    pdf.title_card(report_data)

    pdf.section("Executive Summary")
    pdf.paragraph(build_executive_summary_text(report_data))

    pdf.section("Decision Snapshot")
    pdf.metric_grid(
        [
            ("Recommendation", safe_text(report_data.get("recommendation")), report_data.get("overall_score_value")),
            ("Final Call", safe_text(report_data.get("final_choice")), report_data.get("overall_score_value")),
            ("Overall Score", safe_text(report_data.get("overall_score_display")), report_data.get("overall_score_value")),
        ]
    )

    pdf.section("Section Scores")
    score_items = []
    for label, item in report_data.get("scores", {}).items():
        score_items.append((label, safe_text(item.get("display") if isinstance(item, dict) else item), item.get("value") if isinstance(item, dict) else None))
    pdf.metric_grid(score_items)

    pdf.section("Main Pressure Points")
    pdf.bullets(build_risk_lines(report_data))

    pdf.section("What Looks Stronger")
    pdf.bullets(build_strength_lines(report_data))

    pdf.section("Required Conditions Before Proceeding")
    pdf.bullets(build_condition_lines(report_data))

    pdf.section("Financial Snapshot")
    pdf.key_value_table(report_data.get("financial_snapshot", {}))

    pdf.section("Next-Step Checklist")
    pdf.bullets(report_data.get("next_steps", []))

    if report_data.get("final_rationale"):
        pdf.section("Recorded Decision Rationale")
        pdf.paragraph(report_data["final_rationale"])

    pdf.section("Profile Snapshot")
    pdf.bullets(build_profile_lines(report_data))

    pdf.disclaimer_box()
    return pdf.finish()


def build_free_snapshot_pdf(report_data: dict[str, Any]) -> bytes:
    pdf = ExecutivePdf("Free Pressure Snapshot", "Early signal for franchise and small-business diligence")
    pdf.cover_header(report_data)
    pdf.title_card(report_data)

    pdf.section("Early Executive Summary")
    pdf.paragraph(build_executive_summary_text(report_data))

    pdf.section("Current Signals")
    score_items = []
    for label, item in report_data.get("scores", {}).items():
        if label in {"Franchise Fit", "Concept Validation", "Financial Model", "Brand & Territory"}:
            score_items.append((label, safe_text(item.get("display") if isinstance(item, dict) else item), item.get("value") if isinstance(item, dict) else None))
    pdf.metric_grid(score_items)

    pdf.section("Primary Pressure Points")
    pdf.bullets(build_risk_lines(report_data)[:5])

    pdf.section("Recommended Next Moves")
    pdf.bullets(report_data.get("next_steps", [])[:5])

    pdf.disclaimer_box()
    return pdf.finish()
