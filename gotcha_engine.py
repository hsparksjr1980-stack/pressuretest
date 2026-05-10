
from __future__ import annotations

import html
from typing import Any

import streamlit as st


SEVERITY_ORDER = {"high": 3, "medium": 2, "low": 1}


def _safe_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _num(key: str, default: float = 0.0) -> float:
    value = st.session_state.get(key, default)
    try:
        return float(value)
    except (TypeError, ValueError):
        return float(default)


def _text(key: str) -> str:
    return _safe_text(st.session_state.get(key, ""))


def _score(key: str, default: int = 3) -> int:
    value = st.session_state.get(key, default)
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _answer_is(key: str, values: set[str]) -> bool:
    return _safe_text(st.session_state.get(key, "")).lower() in {v.lower() for v in values}


def _note_contains(*terms: str) -> bool:
    haystack = " ".join(
        [
            _text("cv_risk_notes"),
            _text("cv_verification_notes"),
            _text("pd_biggest_concern"),
            _text("pd_conditions_notes"),
            _text("fd_required_conditions"),
            _text("fd_reasons_to_stop"),
        ]
    ).lower()
    return any(term.lower() in haystack for term in terms)


def _add(items: list[dict[str, Any]], *, gotcha_id: str, pages: list[str], severity: str, category: str,
         title: str, message: str, action: str) -> None:
    items.append(
        {
            "id": gotcha_id,
            "pages": pages,
            "severity": severity,
            "category": category,
            "title": title,
            "message": message,
            "action": action,
        }
    )


def build_gotcha_moments(page: str = "all") -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []

    support_confidence = _score("cv_support_confidence_score", 3)
    market_confidence = _score("cv_market_confidence_score", 3)
    economic_confidence = _score("cv_economic_confidence_score", 3)
    discipline_confidence = _score("cv_decision_discipline_score", 3)

    fdd_cogs = _num("fdd_cogs_pct", 0.0)
    actual_cogs = _num("actual_cogs_pct", 0.0)
    cogs_gap = actual_cogs - fdd_cogs
    local_cost_env = _text("local_cost_env").lower()

    weak_support_answers = sum(
        1
        for key in ["cv_q20", "cv_q21", "cv_q23", "cv_q24"]
        if _answer_is(key, {"No", "Somewhat"})
    )
    weak_market_answers = sum(
        1
        for key in ["cv_q1", "cv_q5", "cv_q6", "cv_q13", "cv_q29"]
        if _answer_is(key, {"No", "Somewhat"})
    )

    if support_confidence <= 2 or _answer_is("cv_q20", {"No"}) or _note_contains("marketing", "local marketing", "ad spend"):
        _add(
            items,
            gotcha_id="marketing_support_gap",
            pages=["overview", "concept_validation", "final_decision"],
            severity="high",
            category="franchisor_reality",
            title="Franchisor marketing may not create local demand",
            message=(
                "You may be expecting the system to generate customers for you. In practice, especially outside core markets, "
                "the owner often carries much more of the local marketing burden than expected."
            ),
            action="Pressure test who is really responsible for local awareness, traffic generation, and repeat demand in your market.",
        )

    if cogs_gap >= 2.0 or local_cost_env in {"above average", "high", "very high"}:
        severity = "high" if cogs_gap >= 4.0 else "medium"
        _add(
            items,
            gotcha_id="cogs_gap_vs_fdd",
            pages=["overview", "financial_model", "post_discovery", "final_decision"],
            severity=severity,
            category="economics",
            title="Your real COGS may be higher than the FDD suggests",
            message=(
                f"Your current model shows COGS at {actual_cogs:.1f}% versus {fdd_cogs:.1f}% in the FDD. "
                "That kind of gap can quietly erase margin if you are using system averages instead of your actual market conditions."
            ),
            action="Rebuild the model using your real supplier, freight, and market-specific costs instead of relying on the headline FDD range.",
        )

    if weak_market_answers >= 2 or market_confidence <= 2 or _answer_is("cv_q6", {"No", "Somewhat"}):
        _add(
            items,
            gotcha_id="culture_market_fit_gap",
            pages=["overview", "concept_validation", "final_decision"],
            severity="high",
            category="market_fit",
            title="Brand success in one market does not prove fit in your area",
            message=(
                "A concept can work well in its home markets and still miss the preferences, habits, or buying patterns of your local area. "
                "You may be underwriting brand strength when you still need local proof."
            ),
            action="Validate local demand, demographic fit, and consumer behavior before treating core-market success as transferable.",
        )

    if weak_support_answers >= 2 or (support_confidence <= 3 and _answer_is("cv_q19", {"Somewhat", "No"})):
        _add(
            items,
            gotcha_id="outer_market_test_case",
            pages=["overview", "concept_validation", "post_discovery", "final_decision"],
            severity="high",
            category="franchisor_reality",
            title="You may be an outer-market test case",
            message=(
                "Franchisors often optimize systems, vendors, and support around their core footprint. "
                "If support, standards, or operating clarity feel uneven, you may be helping prove the system in your market instead of stepping into a polished one."
            ),
            action="Treat market expansion risk explicitly. Ask what is truly proven in your geography versus what still depends on adaptation.",
        )

    if _answer_is("cv_q23", {"No", "Somewhat"}) or _note_contains("technology", "tech", "inventory", "integration", "reporting", "system", "systems"):
        _add(
            items,
            gotcha_id="systems_not_ready",
            pages=["overview", "concept_validation", "financial_model", "post_discovery", "final_decision"],
            severity="high",
            category="systems",
            title="The system may not be ready for your market yet",
            message=(
                "Technology, reporting, inventory, and operating tools can look clean in the sales process but break down when the market, vendors, or workflow differ from the core system."
            ),
            action="Verify whether pricing, inventory, reporting, and integrations are already built for your situation or whether you will be solving gaps yourself.",
        )

    if economic_confidence <= 2 or _answer_is("cv_q29", {"No", "Somewhat"}) or _answer_is("pd_q21", {"No"}):
        _add(
            items,
            gotcha_id="thin_margin_for_error",
            pages=["overview", "financial_model", "post_discovery", "final_decision"],
            severity="high",
            category="economics",
            title="This deal may only work if too many things go right",
            message=(
                "If the economics weaken materially when COGS rise, ramp slows, or support is thinner than expected, then the model may not have a real margin of safety."
            ),
            action="Test slower ramp, higher costs, and weaker support. A deal that only works in the upside case is still a weak deal.",
        )

    if discipline_confidence <= 2 or _answer_is("fd_q15", {"No", "Somewhat"}) or _answer_is("fd_q17", {"No", "Somewhat"}):
        _add(
            items,
            gotcha_id="forcing_the_fit",
            pages=["overview", "final_decision"],
            severity="medium",
            category="decision_quality",
            title="You may be trying to make the deal fit",
            message=(
                "When too many conditions are still open, but the decision momentum remains high, the risk is not just a weak deal. "
                "It is a weak decision process."
            ),
            action="Write down the exact conditions that must be true before committing, and keep walk-away discipline intact.",
        )

    deduped: list[dict[str, Any]] = []
    seen: set[str] = set()
    for item in sorted(items, key=lambda x: (-SEVERITY_ORDER.get(x["severity"], 0), x["title"])):
        if item["id"] in seen:
            continue
        seen.add(item["id"])
        deduped.append(item)

    if page == "all":
        return deduped
    return [item for item in deduped if page in item["pages"]]


def render_gotcha_section(*, page: str, title: str = "Gotcha moments", max_items: int = 3) -> None:
    items = build_gotcha_moments(page=page)[:max_items]
    if not items:
        return

    st.markdown(
        f"""
        <div class="rc-section-title">{html.escape(title)}</div>
        <div class="rc-section-body">These are the places where the deal may be weaker than it first appears.</div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

    for item in items:
        color = {
            "high": "#dc2626",
            "medium": "#d97706",
            "low": "#2563eb",
        }.get(item["severity"], "#6b7280")
        bg = {
            "high": "rgba(220,38,38,0.06)",
            "medium": "rgba(217,119,6,0.07)",
            "low": "rgba(37,99,235,0.06)",
        }.get(item["severity"], "rgba(107,114,128,0.06)")

        st.markdown(
            f"""
            <div style="border:1px solid {color}; background:{bg}; border-radius:18px; padding:1rem 1rem 0.95rem 1rem; margin-bottom:0.8rem;">
                <div style="font-size:0.72rem; font-weight:800; letter-spacing:0.08em; text-transform:uppercase; color:{color}; margin-bottom:0.35rem;">
                    {html.escape(item['severity'])} severity · {html.escape(item['category'].replace('_', ' '))}
                </div>
                <div style="font-size:1.0rem; font-weight:800; color:#111827; margin-bottom:0.35rem;">
                    {html.escape(item['title'])}
                </div>
                <div style="font-size:0.96rem; line-height:1.6; color:#374151; margin-bottom:0.55rem;">
                    {html.escape(item['message'])}
                </div>
                <div style="font-size:0.9rem; line-height:1.55; color:#4b5563;">
                    <strong>What to verify:</strong> {html.escape(item['action'])}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def build_gotcha_snapshot(max_items: int = 3) -> list[str]:
    return [item["title"] for item in build_gotcha_moments(page="all")[:max_items]]
