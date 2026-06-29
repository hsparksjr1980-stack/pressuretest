from __future__ import annotations

import csv
import html
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import streamlit as st


QUICK_ASSESSMENT_COPY = (
    "Best if you want a first-pass read before spending more time or money. "
    "Takes about 10-15 minutes and produces an initial pressure-test report."
)
FULL_REVIEW_COPY = (
    "Best if you are closer to signing, borrowing, leasing, or investing. "
    "Includes deeper diligence questions and produces a more complete report."
)

RISK_LABELS = ("Low Concern", "Needs Verification", "Material Risk", "Stop and Review")

RISK_NOTE = (
    "Risk labels are based only on the information provided. Low Concern does not mean safe "
    "or recommended. It means this area does not currently appear to be a primary concern "
    "based on the answers entered."
)

FDD_TRANSLATION_DEFINITION = (
    "The FDD is important, but it is often system-wide. It may not prove the model works in "
    "your specific market, rent structure, labor market, buildout environment, supply chain, "
    "customer-demand profile, brand-awareness conditions, operator situation, or financing pressure."
)

DATA_DIR = Path("data")
BETA_FEEDBACK_JSONL = DATA_DIR / "beta_feedback.jsonl"
BETA_FEEDBACK_CSV = DATA_DIR / "beta_feedback.csv"
PAID_REVIEW_JSONL = DATA_DIR / "paid_review_requests.jsonl"
PAID_REVIEW_CSV = DATA_DIR / "paid_review_requests.csv"


def get_assessment_depth() -> str:
    depth = str(st.session_state.get("assessment_depth", "quick")).lower()
    if depth not in {"quick", "full"}:
        depth = "quick"
    st.session_state["assessment_depth"] = depth
    return depth


def is_full_review() -> bool:
    return get_assessment_depth() == "full"


def assessment_type_label() -> str:
    return "Full Review" if is_full_review() else "Quick Assessment"


def render_depth_toggle() -> None:
    current = get_assessment_depth()
    st.markdown(
        """
        <div class="pt-depth-panel">
            <div class="pt-depth-kicker">Assessment depth</div>
            <div class="pt-depth-title">Choose how deep to go. Quick Assessment is the default.</div>
            <div class="pt-depth-copy">Full Review unlocks deeper sections in the same workflow and keeps your existing answers.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    choice = st.radio(
        "Assessment depth",
        options=["Quick Assessment", "Full Review"],
        index=1 if current == "full" else 0,
        horizontal=True,
        label_visibility="collapsed",
        captions=[QUICK_ASSESSMENT_COPY, FULL_REVIEW_COPY],
        key="assessment_depth_choice",
    )
    st.session_state["assessment_depth"] = "full" if choice == "Full Review" else "quick"


def render_pressure_check(text: str) -> None:
    st.markdown(
        f"""
        <div class="pt-pressure-check">
            <div class="pt-pressure-label">Pressure Check</div>
            <div>{html.escape(text)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_beta_styles() -> None:
    st.markdown(
        """
        <style>
            .pt-depth-panel,
            .pt-pressure-check,
            .pt-risk-note {
                border: 1px solid #D8DEE8;
                border-radius: 12px;
                background: #FFFFFF;
                padding: 1rem;
                margin: .75rem 0;
                box-shadow: 0 10px 28px rgba(15, 23, 42, .045);
            }
            .pt-depth-kicker,
            .pt-pressure-label {
                color: #9A3412;
                font-size: .72rem;
                font-weight: 800;
                letter-spacing: .08em;
                text-transform: uppercase;
                margin-bottom: .25rem;
            }
            .pt-depth-title {
                color: #0B1730;
                font-size: 1.08rem;
                font-weight: 800;
                margin-bottom: .25rem;
            }
            .pt-depth-copy,
            .pt-pressure-check,
            .pt-risk-note {
                color: #475569;
                font-size: .94rem;
                line-height: 1.5;
            }
            .pt-risk-badge {
                display: inline-block;
                border-radius: 999px;
                padding: .26rem .6rem;
                font-size: .76rem;
                font-weight: 800;
                margin-bottom: .4rem;
                border: 1px solid #CBD5E1;
            }
            .pt-risk-low { background: #ECFDF3; color: #166534; border-color: #BBF7D0; }
            .pt-risk-verify { background: #FEFCE8; color: #854D0E; border-color: #FDE68A; }
            .pt-risk-material { background: #FFF7ED; color: #9A3412; border-color: #FED7AA; }
            .pt-risk-stop { background: #FEF2F2; color: #991B1B; border-color: #FECACA; }
            @media (max-width: 760px) {
                .block-container { padding-left: 1rem; padding-right: 1rem; }
                .rc-title, .rc-title-wide { font-size: 1.75rem; line-height: 1.12; }
                .rc-card, .rc-card-soft, .rc-card-navy, .rc-bullet-panel, .rc-action-banner {
                    border-radius: 12px;
                    padding: .9rem;
                }
                div[data-testid="column"] { width: 100% !important; flex: 1 1 100% !important; }
                .stButton > button, .stDownloadButton > button { min-height: 44px; }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def risk_label_for_score(score: float | None) -> str:
    if score is None:
        return "Needs Verification"
    if score >= 78:
        return "Low Concern"
    if score >= 58:
        return "Needs Verification"
    if score >= 40:
        return "Material Risk"
    return "Stop and Review"


def risk_badge(label: str) -> str:
    css = {
        "Low Concern": "pt-risk-low",
        "Needs Verification": "pt-risk-verify",
        "Material Risk": "pt-risk-material",
        "Stop and Review": "pt-risk-stop",
    }.get(label, "pt-risk-verify")
    return f'<span class="pt-risk-badge {css}">{html.escape(label)}</span>'


def collect_fdd_translation_inputs() -> None:
    st.selectbox(
        "Is this market already proven for this franchise?",
        [
            "Not sure",
            "Yes, there are successful nearby or similar-market locations",
            "Somewhat, but the market is still developing",
            "No, this is a new or unproven market",
        ],
        key="fdd_market_proven",
    )
    st.selectbox(
        "Are the financial examples or performance claims from markets similar to yours?",
        [
            "Not sure",
            "Yes, similar market/location/cost structure",
            "Somewhat similar",
            "No, different market or unclear comparison",
        ],
        key="fdd_market_comparables",
    )
    st.selectbox(
        "Have you spoken with franchisees in markets similar to yours?",
        ["Not sure", "Yes", "No", "Not yet"],
        key="fdd_similar_franchisee_calls",
    )
    st.selectbox(
        "Are your local rent, labor, buildout, and supply costs materially different from examples you have seen?",
        ["Not sure yet", "No major difference identified", "Some differences", "Material differences"],
        key="fdd_local_cost_difference",
    )


def fdd_translation_triggered() -> bool:
    risk_values = {
        "No, this is a new or unproven market",
        "Not sure",
        "No, different market or unclear comparison",
        "No",
        "Not yet",
        "Some differences",
        "Material differences",
        "Not sure yet",
    }
    keys = (
        "fdd_market_proven",
        "fdd_market_comparables",
        "fdd_similar_franchisee_calls",
        "fdd_local_cost_difference",
    )
    return any(st.session_state.get(key) in risk_values for key in keys)


def build_decision_critical_issues(report_data: dict[str, Any]) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []

    def add(title: str, label: str, why: str, verify: str) -> None:
        if len(issues) < 5 and not any(item["title"] == title for item in issues):
            issues.append({"title": title, "label": label, "why": why, "verify": verify})

    if fdd_translation_triggered():
        add(
            "FDD Translation Risk",
            "Material Risk",
            "System-wide information may not translate directly to this market, cost structure, operator situation, or debt pressure.",
            "Validate similar-market unit performance, local rent/labor/buildout costs, and franchisee experience in markets like yours.",
        )

    if bool(st.session_state.get("signed_anything", False)):
        add(
            "Agreement or commitment already signed",
            "Stop and Review",
            "Signed documents, deposits, leases, or guarantees can make a weak decision harder to unwind.",
            "Confirm exactly what is binding, what is refundable, and what professional review is still needed.",
        )

    risks = list(report_data.get("risks", []))
    conditions = list(report_data.get("conditions", []))
    score = report_data.get("overall_score_value")
    risk_label = risk_label_for_score(score)
    for item in risks[:3]:
        add(
            str(item),
            risk_label if risk_label != "Low Concern" else "Needs Verification",
            "This appears among the top unresolved risk signals based on the answers provided.",
            "Get evidence that directly confirms or disproves this issue before committing more money or signing obligations.",
        )
    for item in conditions[:3]:
        add(
            str(item),
            "Needs Verification",
            "This condition may materially affect whether the opportunity deserves further commitment.",
            "Document the threshold, owner, and evidence needed to resolve it.",
        )

    if not issues:
        add(
            "Not enough verified evidence yet",
            "Needs Verification",
            "A low number of flagged items does not mean the opportunity is safe; it may mean the current answers are incomplete.",
            "Complete the Quick Assessment and verify the core facts behind the report.",
        )

    return issues[:5]


def _safe_text(value: Any) -> str:
    return "" if value is None else str(value).strip()


def _append_record(jsonl_path: Path, csv_path: Path, csv_fields: list[str], record: dict[str, str]) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with jsonl_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
    write_header = not csv_path.exists()
    with csv_path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=csv_fields)
        if write_header:
            writer.writeheader()
        writer.writerow({field: record.get(field, "") for field in csv_fields})


def save_paid_review_request(values: dict[str, Any]) -> None:
    fields = [
        "captured_at",
        "name",
        "email",
        "franchise_brand",
        "stage",
        "capital_at_risk",
        "fdd_received",
        "signed_anything",
        "review_scope",
        "preferred_contact",
    ]
    record = {field: _safe_text(values.get(field, "")) for field in fields}
    record["captured_at"] = datetime.now(timezone.utc).isoformat()
    _append_record(PAID_REVIEW_JSONL, PAID_REVIEW_CSV, fields, record)


def save_beta_feedback(values: dict[str, Any]) -> None:
    fields = [
        "captured_at",
        "changed_decision",
        "made_slow_down",
        "missing_question",
        "too_soft",
        "too_harsh",
        "would_pay_299",
        "would_show_to_advisor",
        "most_useful",
        "confusing",
    ]
    record = {field: _safe_text(values.get(field, "")) for field in fields}
    record["captured_at"] = datetime.now(timezone.utc).isoformat()
    _append_record(BETA_FEEDBACK_JSONL, BETA_FEEDBACK_CSV, fields, record)
