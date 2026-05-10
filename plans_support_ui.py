from __future__ import annotations

from dataclasses import dataclass

import streamlit as st

from branding import APP_PRODUCT
<<<<<<< HEAD
from paywall_logic import (
    FREE_PLAN_ID,
    PLAN_DEFINITIONS,
    PRO_PLAN_ID,
    SERVICE_PRICES,
    format_money,
    has_forward_decision,
    set_checkout_selection,
)
from premium_components import esc, tier_card, upgrade_strip
=======
>>>>>>> fec65288cb896b4679e84e61241f185fa625e150
from ui_styles import close_shell, open_shell, render_page_header, render_section_intro


@dataclass(frozen=True)
<<<<<<< HEAD
class AdvisoryOffer:
    title: str
    price: int
    subtitle: str
    bullets: tuple[str, ...]
    cta_label: str
    best_for: str
    badge: str = ""


ADVISORY_OFFERS: tuple[AdvisoryOffer, ...] = (
    AdvisoryOffer(
        title="Opportunity Review",
        price=SERVICE_PRICES["Opportunity Review"],
        subtitle="Pressure test the deal before you commit.",
        bullets=(
            "Focused review of the opportunity",
            "Financial and assumption pressure test",
            "Key risks and missing diligence items",
            "Clear next-step guidance",
        ),
        cta_label="Add Opportunity Review",
        best_for="Best for users who are still evaluating whether the deal deserves more work.",
    ),
    AdvisoryOffer(
        title="Execution Game Plan",
        price=SERVICE_PRICES["Execution Game Plan"],
        subtitle="Know what to do next and in what order.",
        bullets=(
            "Prioritized post-decision actions",
            "Site, lease, lender, bid, and buildout sequencing",
            "Launch-readiness pressure points",
            "Common early mistakes to avoid",
        ),
        cta_label="Add Execution Game Plan",
        best_for="Best for users who have decided to move forward and need sequencing discipline.",
        badge="Post-decision",
    ),
    AdvisoryOffer(
        title="Business Plan & Funding Prep",
        price=SERVICE_PRICES["Business Plan & Funding Prep"],
        subtitle="Turn the deal into a structured plan for lender or partner review.",
        bullets=(
            "Financial model refinement",
            "Business plan structure",
            "Sources and uses alignment",
            "Risk and assumptions summary",
        ),
        cta_label="Add Funding Prep",
        best_for="Best for users preparing a more formal funding or partner package.",
        badge="Structured deliverable",
    ),
)
=======
class OfferCard:
    title: str
    price: str
    subtitle: str
    bullets: list[str]
    cta_label: str
    kind: str
    badge: str = ""
    best_for: str = ""


PRO_PRICE_DEFAULT = "$99 one-time"
OPPORTUNITY_REVIEW_PRICE_DEFAULT = "$350"
EXECUTION_GAME_PLAN_PRICE_DEFAULT = "$550"
BUSINESS_PLAN_FUNDING_PREP_PRICE_DEFAULT = "$1,000 flat"

APP_TIER_OFFERS: list[OfferCard] = [
    OfferCard(
        title="Free",
        price="$0",
        subtitle="Evaluate the opportunity before you commit.",
        bullets=[
            "Overview",
            "Reality Check",
            "Concept Validation",
            "Opportunity Fit & Recommendations",
            "Financial Model (Pre-Discovery)",
            "Post-Discovery Review",
            "Final Decision",
        ],
        cta_label="Start Free",
        kind="tier",
    ),
    OfferCard(
        title="Pro",
        price=PRO_PRICE_DEFAULT,
        subtitle="Build, validate, and execute the actual deal.",
        bullets=[
            "Deal Workspace",
            "Deal Model",
            "Buildout & Launch Tracker",
            "For users who choose to move forward",
        ],
        cta_label="Upgrade to Pro",
        kind="tier",
        badge="For active deals",
    ),
]

ADVISORY_OFFERS: list[OfferCard] = [
    OfferCard(
        title="Opportunity Review",
        price=OPPORTUNITY_REVIEW_PRICE_DEFAULT,
        subtitle="Pressure test the deal before you commit.",
        bullets=[
            "Focused review of the opportunity",
            "Financial and assumption pressure test",
            "Key risks and what may be missing",
            "Clear next-step guidance",
        ],
        cta_label="Book Review",
        kind="service",
        best_for="Best for: I’m looking at this and want help evaluating it.",
    ),
    OfferCard(
        title="Execution Game Plan",
        price=EXECUTION_GAME_PLAN_PRICE_DEFAULT,
        subtitle="Know what to do next and in what order.",
        bullets=[
            "Prioritized next steps",
            "Site / lease / lender / bid / buildout sequencing",
            "What to focus on first",
            "Common early mistakes to avoid",
        ],
        cta_label="Get the Plan",
        kind="service",
        best_for="Best for: I’ve decided to move forward and need to know what to do next.",
    ),
    OfferCard(
        title="Business Plan & Funding Prep",
        price=BUSINESS_PLAN_FUNDING_PREP_PRICE_DEFAULT,
        subtitle="Turn your deal into a clear, structured plan.",
        bullets=[
            "Financial model refinement",
            "Business plan structure",
            "Sources & Uses alignment",
            "Funding readiness support",
            "Risk / assumptions summary",
        ],
        cta_label="Start Plan",
        kind="service",
        badge="Structured deliverable",
        best_for="Best for: I need to turn this into a structured plan for lenders or partners.",
    ),
]
>>>>>>> fec65288cb896b4679e84e61241f185fa625e150


def _inject_page_styles() -> None:
    st.markdown(
        """
        <style>
<<<<<<< HEAD
            .ps-section-wrap { margin-top: 0.35rem; margin-bottom: 1.05rem; }
            .ps-section-title { font-size: 1.55rem; font-weight: 800; line-height: 1.15; color: #0B1730; margin-bottom: 0.25rem; }
            .ps-section-copy { font-size: 0.98rem; line-height: 1.55; color: #5B6577; max-width: 820px; }
            .ps-badge { display: inline-block; padding: 0.30rem 0.60rem; border-radius: 999px; background: rgba(249, 115, 22, 0.10); border: 1px solid rgba(249, 115, 22, 0.18); color: #C2410C; font-size: 0.72rem; font-weight: 800; margin-bottom: 0.7rem; }
            .ps-kicker { font-size: 0.72rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: #6B7280; margin-bottom: 0.45rem; }
            .ps-title { font-size: 1.25rem; font-weight: 800; line-height: 1.15; color: #0F172A; margin-bottom: 0.18rem; }
            .ps-price { font-size: 1.4rem; font-weight: 800; line-height: 1.1; color: #0B1730; margin-bottom: 0.4rem; }
            .ps-subtitle { font-size: 0.96rem; line-height: 1.5; color: #5B6577; margin-bottom: 0.75rem; }
            .ps-best-for { margin-top: 0.8rem; padding-top: 0.75rem; border-top: 1px solid #EEF2F7; font-size: 0.9rem; line-height: 1.45; color: #475569; }
            .ps-note { margin-top: 0.55rem; font-size: 0.84rem; line-height: 1.45; color: #64748B; }
            .ps-compare { border:1px solid rgba(15,23,42,.10); border-radius:24px; background:#fff; padding:1rem; box-shadow:0 14px 36px rgba(15,23,42,.05); }
            .ps-compare-row { display:grid; grid-template-columns:1.15fr 1fr 1fr; gap:1rem; padding:.72rem 0; border-bottom:1px solid #EEF2F7; font-size:.92rem; color:#334155; }
            .ps-compare-row:last-child { border-bottom:0; }
            .ps-compare-head { font-weight:850; color:#0B1220; }
=======
            .ps-section-wrap {
                margin-top: 0.35rem;
                margin-bottom: 1.05rem;
            }

            .ps-section-title {
                font-size: 1.55rem;
                font-weight: 800;
                line-height: 1.15;
                color: #0B1730;
                margin-bottom: 0.25rem;
            }

            .ps-section-copy {
                font-size: 0.98rem;
                line-height: 1.55;
                color: #5B6577;
                max-width: 780px;
            }

            .ps-badge {
                display: inline-block;
                padding: 0.30rem 0.60rem;
                border-radius: 999px;
                background: rgba(249, 115, 22, 0.10);
                border: 1px solid rgba(249, 115, 22, 0.18);
                color: #C2410C;
                font-size: 0.72rem;
                font-weight: 800;
                margin-bottom: 0.7rem;
            }

            .ps-kicker {
                font-size: 0.72rem;
                font-weight: 700;
                letter-spacing: 0.08em;
                text-transform: uppercase;
                color: #6B7280;
                margin-bottom: 0.45rem;
            }

            .ps-title {
                font-size: 1.25rem;
                font-weight: 800;
                line-height: 1.15;
                color: #0F172A;
                margin-bottom: 0.18rem;
            }

            .ps-price {
                font-size: 1.4rem;
                font-weight: 800;
                line-height: 1.1;
                color: #0B1730;
                margin-bottom: 0.4rem;
            }

            .ps-subtitle {
                font-size: 0.96rem;
                line-height: 1.5;
                color: #5B6577;
                margin-bottom: 0.75rem;
            }

            .ps-best-for {
                margin-top: 0.8rem;
                padding-top: 0.75rem;
                border-top: 1px solid #EEF2F7;
                font-size: 0.9rem;
                line-height: 1.45;
                color: #475569;
            }

            .ps-note {
                margin-top: 0.55rem;
                font-size: 0.84rem;
                line-height: 1.45;
                color: #64748B;
            }
>>>>>>> fec65288cb896b4679e84e61241f185fa625e150
        </style>
        """,
        unsafe_allow_html=True,
    )


def _render_section_heading(title: str, body: str) -> None:
    st.markdown(
        f"""
        <div class="ps-section-wrap">
<<<<<<< HEAD
            <div class="ps-section-title">{esc(title)}</div>
            <div class="ps-section-copy">{esc(body)}</div>
=======
            <div class="ps-section-title">{title}</div>
            <div class="ps-section-copy">{body}</div>
>>>>>>> fec65288cb896b4679e84e61241f185fa625e150
        </div>
        """,
        unsafe_allow_html=True,
    )


<<<<<<< HEAD
def _go_to_checkout(plan_id: str, services: list[str] | None = None) -> None:
    set_checkout_selection(plan_id, services or [])
    st.session_state["current_page"] = "Paywall"
    st.rerun()


def _render_positioning_strip() -> None:
    if has_forward_decision():
        upgrade_strip(
            "You have a forward decision on file.",
            "This is where Pro starts to make sense: managing assumptions, lender items, buildout steps, launch readiness, and execution risk after the opportunity moves from evaluation to action.",
        )
    else:
        upgrade_strip(
            "Start free. Upgrade only when execution risk becomes the problem.",
            "PressureTest keeps the free path focused on evaluating the opportunity. Pro is intentionally positioned for post-decision execution planning, not for casual browsing.",
        )


def _render_tier_comparison() -> None:
    free = PLAN_DEFINITIONS[FREE_PLAN_ID]
    pro = PLAN_DEFINITIONS[PRO_PLAN_ID]

    _render_section_heading(
        "Free vs Pro",
        "The boundary is simple: Free helps you decide whether the opportunity deserves more diligence. Pro helps you manage the work after you decide to move forward.",
    )

    st.markdown('<div class="pt-tier-grid">', unsafe_allow_html=True)
    col1, col2 = st.columns(2, gap="large")
    with col1:
        tier_card(
            title=free.name,
            price="$0",
            body=free.positioning,
            features=free.includes,
            badge="Assessment",
        )
        if st.button("Continue Free Assessment", key="plans_continue_free", use_container_width=True, type="primary"):
            st.session_state["current_page"] = "Overview"
            st.rerun()
    with col2:
        tier_card(
            title=pro.name,
            price=format_money(pro.price),
            body=pro.positioning,
            features=pro.includes,
            badge="Execution Workspace",
            pro=True,
        )
        pro_cta = "Upgrade to Pro" if has_forward_decision() else "Preview Pro Checkout"
        if st.button(pro_cta, key="plans_upgrade_pro", use_container_width=True):
            _go_to_checkout(PRO_PLAN_ID)
    st.markdown('</div>', unsafe_allow_html=True)


def _render_comparison_table() -> None:
    rows = [
        ("Primary question", "Should I keep investigating?", "How do I avoid execution mistakes?"),
        ("Best stage", "Early diligence", "Post-decision planning"),
        ("Financial view", "Baseline model", "Scenario planning and capital pressure"),
        ("Output", "Free report", "Execution packet and workspace outputs"),
        ("Workflow", "Assessment", "Ongoing deal management"),
    ]
    html_rows = "".join(
        f"""
        <div class="ps-compare-row">
          <div>{esc(label)}</div>
          <div>{esc(free)}</div>
          <div>{esc(pro)}</div>
        </div>
        """
        for label, free, pro in rows
    )
    st.markdown(
        f"""
        <div class="ps-compare">
          <div class="ps-compare-row ps-compare-head">
            <div>Boundary</div><div>Free</div><div>Pro</div>
          </div>
          {html_rows}
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_advisory_offer(offer: AdvisoryOffer, button_key: str) -> None:
    with st.container(border=True):
        if offer.badge:
            st.markdown(f'<div class="ps-badge">{esc(offer.badge)}</div>', unsafe_allow_html=True)

        st.markdown(
            f"""
            <div class="ps-kicker">Optional support</div>
            <div class="ps-title">{esc(offer.title)}</div>
            <div class="ps-price">{esc(format_money(offer.price))}</div>
            <div class="ps-subtitle">{esc(offer.subtitle)}</div>
=======
def _render_offer_card(offer: OfferCard, button_key: str, primary: bool = False) -> None:
    with st.container(border=True):
        if offer.badge:
            st.markdown(f'<div class="ps-badge">{offer.badge}</div>', unsafe_allow_html=True)

        st.markdown(
            f"""
            <div class="ps-kicker">{"App Tier" if offer.kind == "tier" else "Advisory Offer"}</div>
            <div class="ps-title">{offer.title}</div>
            <div class="ps-price">{offer.price}</div>
            <div class="ps-subtitle">{offer.subtitle}</div>
>>>>>>> fec65288cb896b4679e84e61241f185fa625e150
            """,
            unsafe_allow_html=True,
        )

        for bullet in offer.bullets:
            st.markdown(f"- {bullet}")

<<<<<<< HEAD
        st.markdown(f'<div class="ps-best-for">{esc(offer.best_for)}</div>', unsafe_allow_html=True)

        if st.button(offer.cta_label, key=button_key, use_container_width=True):
            _go_to_checkout(FREE_PLAN_ID, [offer.title])
=======
        if offer.best_for:
            st.markdown(f'<div class="ps-best-for">{offer.best_for}</div>', unsafe_allow_html=True)

        if st.button(
            offer.cta_label,
            key=button_key,
            use_container_width=True,
            type="primary" if primary else "secondary",
        ):
            if offer.title == "Free":
                st.session_state["current_page"] = "Overview"
                st.rerun()
            elif offer.title == "Pro":
                st.session_state["current_page"] = "Plans & Support"
                st.rerun()
            else:
                st.session_state["selected_support_offer"] = offer.title
                st.success(f"{offer.title} selected. Connect this button to booking or checkout next.")


def _render_app_tiers() -> None:
    _render_section_heading(
        "App Tiers",
        "Choose the workflow that fits your stage. Start with evaluation. Upgrade when you are actively moving the deal forward.",
    )

    col1, col2 = st.columns(2, gap="large")

    with col1:
        _render_offer_card(APP_TIER_OFFERS[0], "plans_free_cta", primary=True)

    with col2:
        _render_offer_card(APP_TIER_OFFERS[1], "plans_pro_cta")
>>>>>>> fec65288cb896b4679e84e61241f185fa625e150


def _render_advisory_support() -> None:
    _render_section_heading(
<<<<<<< HEAD
        "Optional support",
        "Support is separate from Pro access. Use it when you need a sharper review, a sequenced execution plan, or a more structured funding package.",
    )

    col1, col2, col3 = st.columns(3, gap="large")
    columns = (col1, col2, col3)
    for index, offer in enumerate(ADVISORY_OFFERS):
        with columns[index]:
            _render_advisory_offer(offer, f"service_{index}_{offer.title}")
=======
        "Advisory & Support",
        "Optional focused support for the moment you are in: evaluating the opportunity, moving forward, or preparing for lenders or partners.",
    )

    col1, col2, col3 = st.columns(3, gap="large")

    with col1:
        _render_offer_card(ADVISORY_OFFERS[0], "service_opportunity_review")

    with col2:
        _render_offer_card(ADVISORY_OFFERS[1], "service_execution_game_plan")

    with col3:
        _render_offer_card(ADVISORY_OFFERS[2], "service_business_plan_funding_prep")
>>>>>>> fec65288cb896b4679e84e61241f185fa625e150

    st.markdown(
        """
        <div class="ps-note">
<<<<<<< HEAD
            Business Plan & Funding Prep is a structured planning package. It is not SBA packaging, guaranteed approval, legal advice, financial advice, tax advice, accounting advice, or an investment recommendation.
=======
            Business Plan & Funding Prep is a structured business plan and funding prep package. It is not full SBA packaging, guaranteed approval, legal advice, or financial advice.
>>>>>>> fec65288cb896b4679e84e61241f185fa625e150
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_plans_support() -> None:
    open_shell()
    _inject_page_styles()

    render_page_header(
        eyebrow=APP_PRODUCT,
        title="Plans & Support",
<<<<<<< HEAD
        subtitle="Free helps you evaluate the opportunity. Pro helps you manage execution risk after the deal becomes real.",
=======
        subtitle="Use the app to evaluate the deal. Add support only when you need a clearer review, a forward plan, or a structured lender-ready package.",
>>>>>>> fec65288cb896b4679e84e61241f185fa625e150
        wide=True,
    )

    render_section_intro(
<<<<<<< HEAD
        title="A sharper commercial boundary",
        body="PressureTest should not push users into Pro before they understand the opportunity. The upgrade makes sense when the user needs a workspace for scenarios, lender prep, buildout tracking, and launch execution.",
    )

    st.markdown('<div class="rc-gap-sm"></div>', unsafe_allow_html=True)
    _render_positioning_strip()
    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)
    _render_tier_comparison()
    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)
    _render_comparison_table()
    st.markdown('<div class="rc-gap-lg"></div>', unsafe_allow_html=True)
=======
        title="Simple structure, clear progression",
        body="Free helps you evaluate. Pro helps you execute. Advisory support is there when you want a sharper review, a practical next-step plan, or a structured lender-ready package.",
    )

    st.markdown('<div class="rc-gap-sm"></div>', unsafe_allow_html=True)

    _render_app_tiers()

    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

>>>>>>> fec65288cb896b4679e84e61241f185fa625e150
    _render_advisory_support()

    close_shell()
