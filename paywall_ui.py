# paywall_ui.py

from __future__ import annotations

import html
<<<<<<< HEAD

import streamlit as st

from paywall_logic import (
    FREE_PLAN_ID,
    PLAN_DEFINITIONS,
    PRO_PLAN_ID,
    activate_selected_plan,
    format_money,
    has_forward_decision,
    reset_checkout_selection,
)
from premium_components import esc, upgrade_strip
from ui_styles import close_shell, open_shell, render_card, render_page_header, render_section_intro


=======
from typing import Final

import streamlit as st

from ui_styles import close_shell, open_shell, render_card, render_page_header, render_section_intro


PLAN_UNLOCKS: Final[dict[str, list[str]]] = {
    "free": [
        "Core assessment workflow",
        "Free report access",
    ],
    "pro": [
        "Deal Workspace",
        "Deal Model",
        "Buildout & Launch Tracker",
        "Execution Report",
    ],
}


def _money(value: int | float) -> str:
    return f"${float(value):,.0f}"


>>>>>>> fec65288cb896b4679e84e61241f185fa625e150
def _inject_local_styles() -> None:
    st.markdown(
        """
        <style>
<<<<<<< HEAD
            .pw-box { background: #ffffff; border: 1px solid #e5e7eb; border-radius: 20px; box-shadow: 0 8px 24px rgba(17, 24, 39, 0.06); padding: 1.2rem; }
            .pw-row { display: flex; justify-content: space-between; gap: 1rem; padding: 0.55rem 0; border-bottom: 1px solid #f3f4f6; color: #374151; font-size: 0.95rem; }
            .pw-row:last-child { border-bottom: none; }
            .pw-total { font-size: 1.28rem; font-weight: 800; color: #111827; padding-top: 0.8rem; }
            .pw-note { font-size: 0.92rem; line-height: 1.6; color: #4b5563; }
            .pw-risk-boundary { border:1px solid rgba(15,23,42,.10); border-radius:20px; background:#fff; padding:1rem; margin:.75rem 0; }
            .pw-risk-boundary h4 { margin:.1rem 0 .35rem 0; color:#0B1220; font-size:1rem; }
            .pw-risk-boundary p { margin:0; color:#475569; line-height:1.45; font-size:.92rem; }
=======
            .pw-box {
                background: #ffffff;
                border: 1px solid #e5e7eb;
                border-radius: 20px;
                box-shadow: 0 8px 24px rgba(17, 24, 39, 0.06);
                padding: 1.2rem;
            }

            .pw-row {
                display: flex;
                justify-content: space-between;
                gap: 1rem;
                padding: 0.55rem 0;
                border-bottom: 1px solid #f3f4f6;
                color: #374151;
                font-size: 0.95rem;
            }

            .pw-row:last-child {
                border-bottom: none;
            }

            .pw-total {
                font-size: 1.28rem;
                font-weight: 800;
                color: #111827;
                padding-top: 0.8rem;
            }

            .pw-note {
                font-size: 0.92rem;
                line-height: 1.6;
                color: #4b5563;
            }
>>>>>>> fec65288cb896b4679e84e61241f185fa625e150
        </style>
        """,
        unsafe_allow_html=True,
    )


def _ensure_checkout_state() -> None:
<<<<<<< HEAD
    st.session_state.setdefault("selected_plan_id", FREE_PLAN_ID)
=======
    st.session_state.setdefault("selected_plan_id", "free")
>>>>>>> fec65288cb896b4679e84e61241f185fa625e150
    st.session_state.setdefault("selected_service_ids", [])
    st.session_state.setdefault("cart_items", [])
    st.session_state.setdefault("cart_subtotal", 0.0)
    st.session_state.setdefault("checkout_ready", False)
    st.session_state.setdefault("subscription_status", "free")
    st.session_state.setdefault("purchased_services", [])
    st.session_state.setdefault("checkout_complete", False)


def _complete_checkout() -> None:
<<<<<<< HEAD
    activate_selected_plan()
=======
    selected_plan_id = str(st.session_state.get("selected_plan_id", "free"))
    selected_service_ids = list(st.session_state.get("selected_service_ids", []))

    st.session_state["subscription_status"] = "active" if selected_plan_id == "pro" else "free"
    st.session_state["premium_access"] = selected_plan_id == "pro"
    st.session_state["purchased_services"] = selected_service_ids
    st.session_state["checkout_complete"] = True

    if selected_plan_id == "pro":
        st.session_state["move_forward"] = True
        st.session_state["current_page"] = "Deal Workspace"
    else:
        st.session_state["current_page"] = "Overview"

>>>>>>> fec65288cb896b4679e84e61241f185fa625e150
    st.rerun()


def _back_to_plans() -> None:
    st.session_state["current_page"] = "Plans & Support"
    st.rerun()


def _render_basket_summary() -> None:
    cart_items = list(st.session_state.get("cart_items", []))
    subtotal = float(st.session_state.get("cart_subtotal", 0.0))

    st.markdown('<div class="pw-box">', unsafe_allow_html=True)

    if not cart_items:
        st.write("Your basket is currently empty.")
    else:
        for item in cart_items:
<<<<<<< HEAD
            description = html.escape(str(item.get("description", "")))
            st.markdown(
                f"""
                <div class="pw-row">
                    <div>
                        <strong>{html.escape(str(item["name"]))}</strong><br>
                        <span style="color:#64748B;font-size:.86rem;">{description}</span>
                    </div>
                    <div>{format_money(float(item["price"]))}</div>
=======
            st.markdown(
                f"""
                <div class="pw-row">
                    <div>{html.escape(str(item["name"]))}</div>
                    <div>{_money(float(item["price"]))}</div>
>>>>>>> fec65288cb896b4679e84e61241f185fa625e150
                </div>
                """,
                unsafe_allow_html=True,
            )

<<<<<<< HEAD
        st.markdown(f'<div class="pw-total">Total: {format_money(subtotal)}</div>', unsafe_allow_html=True)
=======
        st.markdown(
            f'<div class="pw-total">Total: {_money(subtotal)}</div>',
            unsafe_allow_html=True,
        )
>>>>>>> fec65288cb896b4679e84e61241f185fa625e150

    st.markdown("</div>", unsafe_allow_html=True)


<<<<<<< HEAD
def _render_unlock_summary(selected_plan_id: str) -> None:
    plan = PLAN_DEFINITIONS.get(selected_plan_id, PLAN_DEFINITIONS[FREE_PLAN_ID])
    includes = list(plan.includes)
    render_card(
        label="Selected access",
        title=plan.name,
        body=plan.positioning,
    )
    st.markdown('<div class="rc-gap-sm"></div>', unsafe_allow_html=True)
    for item in includes:
        st.markdown(f"- {item}")


def _render_commercial_boundary(selected_plan_id: str) -> None:
    if selected_plan_id == PRO_PLAN_ID:
        if has_forward_decision():
            title = "Pro is being used at the right stage."
            body = "You have a forward decision on file, so this upgrade is positioned around execution planning, assumption tracking, lender prep, buildout readiness, and launch risk."
        else:
            title = "Pro is best after a forward decision."
            body = "You can still preview checkout, but the intended workflow is to finish the free assessment first and upgrade once execution planning becomes the problem."
    else:
        title = "Free remains the assessment path."
        body = "Free should help the user decide whether deeper diligence is warranted. It should not try to solve post-commitment execution work."

    st.markdown(
        f"""
        <div class="pw-risk-boundary">
          <h4>{esc(title)}</h4>
          <p>{esc(body)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


=======
>>>>>>> fec65288cb896b4679e84e61241f185fa625e150
def render_paywall() -> None:
    _ensure_checkout_state()
    _inject_local_styles()

    cart_items = list(st.session_state.get("cart_items", []))
    subtotal = float(st.session_state.get("cart_subtotal", 0.0))
    checkout_ready = bool(st.session_state.get("checkout_ready", False))
<<<<<<< HEAD
    selected_plan_id = str(st.session_state.get("selected_plan_id", FREE_PLAN_ID))
=======
    selected_plan_id = str(st.session_state.get("selected_plan_id", "free"))
    unlocks = PLAN_UNLOCKS.get(selected_plan_id, [])
>>>>>>> fec65288cb896b4679e84e61241f185fa625e150

    open_shell()

    render_page_header(
        eyebrow="Checkout",
<<<<<<< HEAD
        title="Review the upgrade or support selection.",
        subtitle="This checkout screen keeps the commercial boundary clear: assessment is free; execution planning and optional support are separate paid steps.",
=======
        title="Review your basket before payment.",
        subtitle=(
            "This paywall is ready for a future payment provider. For now, it acts as a "
            "clean checkout summary and temporary entitlement handoff."
        ),
>>>>>>> fec65288cb896b4679e84e61241f185fa625e150
        wide=True,
    )

    st.markdown('<div class="rc-gap-lg"></div>', unsafe_allow_html=True)

    if bool(st.session_state.get("dev_pro_access", False)):
        st.info("Developer override is enabled. Pro pages are currently accessible without checkout.")

    if not cart_items:
<<<<<<< HEAD
        upgrade_strip(
            "No plan or support item selected.",
            "Return to Plans & Support to choose Pro access or an optional support package.",
        )
        st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)
        if st.button("Back to Plans & Support", key="paywall_back_empty", use_container_width=True, type="primary"):
            reset_checkout_selection()
            _back_to_plans()
=======
        st.warning("Your basket is empty. Go back to Plans & Support to choose a plan or services.")

        st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

        if st.button(
            "Back to Plans & Support",
            key="paywall_back_empty",
            use_container_width=True,
            type="primary",
        ):
            _back_to_plans()

>>>>>>> fec65288cb896b4679e84e61241f185fa625e150
        close_shell()
        return

    col1, col2 = st.columns([1.35, 1], gap="large")

    with col1:
        render_section_intro(
            title="Basket summary",
<<<<<<< HEAD
            body="Review what the user is buying. Pro unlocks app access; optional support items represent separate service follow-up.",
        )
        st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)
        _render_basket_summary()

        st.markdown('<div class="rc-gap-lg"></div>', unsafe_allow_html=True)
        render_section_intro(
            title="Access boundary",
            body="The product should make it obvious why the user is upgrading and what operational problem the upgrade solves.",
        )
        _render_commercial_boundary(selected_plan_id)
=======
            body="Review everything selected in Plans & Support before continuing.",
        )
        st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

        _render_basket_summary()

        st.markdown('<div class="rc-gap-lg"></div>', unsafe_allow_html=True)

        render_section_intro(
            title="What happens after checkout",
            body="Platform access and advisory support are handled differently.",
        )
        st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)
>>>>>>> fec65288cb896b4679e84e61241f185fa625e150

        c1, c2 = st.columns(2, gap="medium")
        with c1:
            render_card(
<<<<<<< HEAD
                label="Free",
                title="Assessment and decision summary",
                body="Use free to evaluate whether the opportunity deserves more diligence before committing capital.",
            )
        with c2:
            render_card(
                label="Pro",
                title="Execution workspace",
                body="Use Pro to organize assumptions, scenarios, lender prep, buildout steps, and launch-readiness work.",
=======
                label="Plan unlocks",
                title="Included platform access",
                body=", ".join(unlocks) if unlocks else "No additional app unlocks.",
            )
        with c2:
            render_card(
                label="Service fulfillment",
                title="Support is recorded separately",
                body="Consulting and one-off services are saved as purchased support items.",
>>>>>>> fec65288cb896b4679e84e61241f185fa625e150
            )

    with col2:
        render_section_intro(
            title="Order summary",
<<<<<<< HEAD
            body="Temporary checkout state for future Stripe or billing-provider integration.",
        )
        st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

        _render_unlock_summary(selected_plan_id)

        st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)
        render_card(
            label="Subtotal",
            title=format_money(subtotal),
            body="Current basket total before payment-provider integration.",
        )

        st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)
        st.markdown(
            """
            <div class="pw-note">
                This is a temporary checkout flow. Later, this button can create a Stripe checkout session and activate access after payment confirmation.
=======
            body="Use this to confirm the current basket before payment.",
        )
        st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

        render_card(
            label="Selected plan",
            title=selected_plan_id.title(),
            body="Only Pro unlocks the execution-side working tools.",
        )

        st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

        render_card(
            label="Subtotal",
            title=_money(subtotal),
            body="Current basket total before provider integration.",
        )

        st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

        st.markdown(
            """
            <div class="pw-note">
                This is a temporary checkout flow. Later, this button can connect to Stripe or another billing provider.
>>>>>>> fec65288cb896b4679e84e61241f185fa625e150
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

<<<<<<< HEAD
        if st.button("Proceed to Payment", key="paywall_proceed", use_container_width=True, type="primary", disabled=not checkout_ready):
            _complete_checkout()

        if st.button("Back to Plans & Support", key="paywall_back", use_container_width=True):
=======
        if st.button(
            "Proceed to Payment",
            key="paywall_proceed",
            use_container_width=True,
            type="primary",
            disabled=not checkout_ready,
        ):
            _complete_checkout()

        if st.button(
            "Back to Plans & Support",
            key="paywall_back",
            use_container_width=True,
        ):
>>>>>>> fec65288cb896b4679e84e61241f185fa625e150
            _back_to_plans()

    close_shell()
