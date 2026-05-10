<<<<<<< HEAD
from __future__ import annotations

from dataclasses import dataclass
from typing import Final

import streamlit as st


FREE_PLAN_ID: Final[str] = "free"
PRO_PLAN_ID: Final[str] = "pro"

PRO_PRICE_DEFAULT: Final[int] = 99


@dataclass(frozen=True)
class PlanDefinition:
    plan_id: str
    name: str
    price: int
    positioning: str
    includes: tuple[str, ...]
    best_for: str


PLAN_DEFINITIONS: Final[dict[str, PlanDefinition]] = {
    FREE_PLAN_ID: PlanDefinition(
        plan_id=FREE_PLAN_ID,
        name="Free Assessment",
        price=0,
        positioning="Decide whether the opportunity deserves deeper diligence.",
        includes=(
            "Guided diligence workflow",
            "Operator fit and concept validation",
            "Baseline financial reality check",
            "Free report and decision summary",
        ),
        best_for="Early evaluation before signing, funding, leasing, or committing capital.",
    ),
    PRO_PLAN_ID: PlanDefinition(
        plan_id=PRO_PLAN_ID,
        name="PressureTest Pro",
        price=PRO_PRICE_DEFAULT,
        positioning="Manage execution risk once the deal becomes real.",
        includes=(
            "Deal workspace and assumption tracking",
            "Scenario planning and working-capital review",
            "Buildout and launch readiness tracking",
            "Execution report for partners, lenders, and internal review",
        ),
        best_for="Users moving forward who need a structured operating plan, not just an assessment.",
    ),
}


SERVICE_PRICES: Final[dict[str, int]] = {
    "Opportunity Review": 350,
    "Execution Game Plan": 550,
    "Business Plan & Funding Prep": 1000,
}


def format_money(value: int | float) -> str:
    return f"${float(value):,.0f}"


def has_premium_access() -> bool:
    return bool(st.session_state.get("premium_access", False)) or bool(st.session_state.get("dev_pro_access", False))


def has_forward_decision() -> bool:
    return bool(st.session_state.get("move_forward", False)) or bool(st.session_state.get("dev_pro_access", False))


def can_access_pro() -> bool:
    return bool(has_forward_decision() and has_premium_access())
=======
import streamlit as st


def has_premium_access() -> bool:
    return bool(st.session_state.get("premium_access", False))



def can_access_pro() -> bool:
    return bool(st.session_state.get("move_forward", False) and has_premium_access())

>>>>>>> fec65288cb896b4679e84e61241f185fa625e150


def dev_unlock_pro() -> None:
    st.session_state["premium_access"] = True
<<<<<<< HEAD
    st.session_state["subscription_status"] = "active"
=======

>>>>>>> fec65288cb896b4679e84e61241f185fa625e150


def lock_decision(action: str) -> None:
    st.session_state["decision_locked"] = True
    st.session_state["final_decision_action"] = action
    st.session_state["move_forward"] = action == "Move Forward"
    st.session_state["walk_away"] = action == "Walk Away"
<<<<<<< HEAD


def reset_checkout_selection() -> None:
    st.session_state["selected_plan_id"] = FREE_PLAN_ID
    st.session_state["selected_service_ids"] = []
    st.session_state["cart_items"] = []
    st.session_state["cart_subtotal"] = 0.0
    st.session_state["checkout_ready"] = False


def build_cart(selected_plan_id: str, selected_service_ids: list[str] | tuple[str, ...]) -> tuple[list[dict[str, object]], float]:
    items: list[dict[str, object]] = []

    plan = PLAN_DEFINITIONS.get(selected_plan_id, PLAN_DEFINITIONS[FREE_PLAN_ID])
    if plan.plan_id == PRO_PLAN_ID:
        items.append(
            {
                "id": plan.plan_id,
                "name": plan.name,
                "type": "plan",
                "price": plan.price,
                "description": plan.positioning,
            }
        )

    for service_id in selected_service_ids:
        price = SERVICE_PRICES.get(service_id)
        if price is None:
            continue
        items.append(
            {
                "id": service_id,
                "name": service_id,
                "type": "service",
                "price": price,
                "description": "Optional support service selected from Plans & Support.",
            }
        )

    subtotal = float(sum(float(item["price"]) for item in items))
    return items, subtotal


def set_checkout_selection(selected_plan_id: str, selected_service_ids: list[str] | tuple[str, ...] | None = None) -> None:
    services = list(selected_service_ids or [])
    cart_items, subtotal = build_cart(selected_plan_id, services)

    st.session_state["selected_plan_id"] = selected_plan_id
    st.session_state["selected_service_ids"] = services
    st.session_state["cart_items"] = cart_items
    st.session_state["cart_subtotal"] = subtotal
    st.session_state["checkout_ready"] = bool(cart_items)


def activate_selected_plan() -> None:
    selected_plan_id = str(st.session_state.get("selected_plan_id", FREE_PLAN_ID))
    selected_service_ids = list(st.session_state.get("selected_service_ids", []))

    st.session_state["subscription_status"] = "active" if selected_plan_id == PRO_PLAN_ID else "free"
    st.session_state["premium_access"] = selected_plan_id == PRO_PLAN_ID
    st.session_state["purchased_services"] = selected_service_ids
    st.session_state["checkout_complete"] = True

    if selected_plan_id == PRO_PLAN_ID:
        st.session_state["move_forward"] = True
        st.session_state["current_page"] = "Deal Workspace"
    else:
        st.session_state["current_page"] = "Overview"
=======
>>>>>>> fec65288cb896b4679e84e61241f185fa625e150
