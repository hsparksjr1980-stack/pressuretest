from __future__ import annotations

from dataclasses import dataclass

import streamlit as st

from branding import APP_PRODUCT
from ui_styles import close_shell, open_shell, render_page_header, render_section_intro


@dataclass(frozen=True)
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


def _inject_page_styles() -> None:
    st.markdown(
        """
        <style>
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
        </style>
        """,
        unsafe_allow_html=True,
    )


def _render_section_heading(title: str, body: str) -> None:
    st.markdown(
        f"""
        <div class="ps-section-wrap">
            <div class="ps-section-title">{title}</div>
            <div class="ps-section-copy">{body}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


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
            """,
            unsafe_allow_html=True,
        )

        for bullet in offer.bullets:
            st.markdown(f"- {bullet}")

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


def _render_advisory_support() -> None:
    _render_section_heading(
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

    st.markdown(
        """
        <div class="ps-note">
            Business Plan & Funding Prep is a structured business plan and funding prep package. It is not full SBA packaging, guaranteed approval, legal advice, or financial advice.
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
        subtitle="Use the app to evaluate the deal. Add support only when you need a clearer review, a forward plan, or a structured lender-ready package.",
        wide=True,
    )

    render_section_intro(
        title="Simple structure, clear progression",
        body="Free helps you evaluate. Pro helps you execute. Advisory support is there when you want a sharper review, a practical next-step plan, or a structured lender-ready package.",
    )

    st.markdown('<div class="rc-gap-sm"></div>', unsafe_allow_html=True)

    _render_app_tiers()

    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

    _render_advisory_support()

    close_shell()
