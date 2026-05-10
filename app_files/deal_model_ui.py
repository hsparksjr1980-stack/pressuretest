from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Any

import streamlit as st

from branding import APP_PRODUCT
from ui_styles import close_shell, open_shell, render_page_header, render_section_intro


@dataclass(frozen=True)
class ScenarioMetric:
    label: str
    key: str
    kind: str = "currency"


DEFAULT_SCENARIO_TEMPLATE: dict[str, Any] = {
    "scenario_name": "Base Case",
    "notes": "",
    "is_working_model": True,
    "concept_name": "",
    "units": 1,
    "ownership_style": "Owner-Operator",
    "square_feet": 1800,
    "franchise_fee": 50000.0,
    "buildout_cost": 250000.0,
    "equipment_cost": 90000.0,
    "furniture_fixtures_signage": 30000.0,
    "tech_pos_setup": 12000.0,
    "inventory_opening": 10000.0,
    "professional_fees": 8000.0,
    "permits_licenses": 5000.0,
    "training_travel": 7000.0,
    "preopening_payroll": 18000.0,
    "marketing_opening": 12000.0,
    "working_capital_reserve": 60000.0,
    "contingency": 25000.0,
    "owner_cash": 150000.0,
    "sba_loan": 350000.0,
    "conventional_loan": 0.0,
    "investor_equity": 0.0,
    "landlord_ti": 0.0,
    "seller_note": 0.0,
    "other_funding": 0.0,
    "interest_rate": 10.5,
    "term_years": 10,
    "interest_only_months": 0,
    "month_1_sales": 45000.0,
    "month_2_sales": 55000.0,
    "month_3_sales": 65000.0,
    "stabilized_monthly_sales": 90000.0,
    "ramp_months": 9,
    "cogs_percent": 28.0,
    "labor_percent": 24.0,
    "occupancy_cost_monthly": 12000.0,
    "royalty_percent": 6.0,
    "marketing_percent": 2.0,
    "insurance_monthly": 1200.0,
    "utilities_monthly": 1800.0,
    "software_monthly": 700.0,
    "other_fixed_costs_monthly": 3500.0,
    "buildout_months": 4,
    "open_delay_months": 0,
    "owner_salary_start_month": 10,
    "owner_salary_monthly": 6000.0,
    "minimum_cash_buffer": 30000.0,
    "sales_downside_percent": 15.0,
    "buildout_overrun_percent": 10.0,
    "labor_overrun_percent": 5.0,
}

SCENARIO_PRESETS: dict[str, dict[str, Any]] = {
    "Base Case": {},
    "Conservative Case": {
        "scenario_name": "Conservative Case",
        "stabilized_monthly_sales": 80000.0,
        "sales_downside_percent": 20.0,
        "working_capital_reserve": 80000.0,
    },
    "SBA Case": {
        "scenario_name": "SBA Case",
        "owner_cash": 120000.0,
        "sba_loan": 420000.0,
        "interest_rate": 11.0,
    },
}

COMPARE_METRICS: list[ScenarioMetric] = [
    ScenarioMetric("Startup cash required", "owner_cash_required"),
    ScenarioMetric("Total uses", "total_uses"),
    ScenarioMetric("Monthly debt service", "monthly_debt_service"),
    ScenarioMetric("Break-even sales", "break_even_sales"),
    ScenarioMetric("12-month low cash", "year1_low_cash"),
    ScenarioMetric("Time to owner pay", "months_to_owner_pay", "months"),
    ScenarioMetric("Funding gap", "funding_gap"),
    ScenarioMetric("Stressed low cash", "stressed_low_cash"),
    ScenarioMetric("Breaks first", "breaks_first", "text"),
]

TOP_METRICS: list[ScenarioMetric] = [
    ScenarioMetric("Startup cash", "owner_cash_required"),
    ScenarioMetric("Debt service", "monthly_debt_service"),
    ScenarioMetric("Break-even sales", "break_even_sales"),
    ScenarioMetric("12-mo low cash", "year1_low_cash"),
]


def _inject_local_styles() -> None:
    st.markdown(
        """
        <style>
            .dm-toolbar {
                background: #FFFFFF;
                border: 1px solid #E2E8F0;
                border-radius: 18px;
                padding: 1rem 1rem 0.9rem 1rem;
                margin-bottom: 1rem;
                box-shadow: 0 8px 24px rgba(15, 23, 42, 0.04);
            }
            .dm-band {
                background: linear-gradient(135deg, #0B1730, #13213A);
                color: white;
                border-radius: 18px;
                padding: 1rem 1.1rem;
                margin-bottom: 1rem;
            }
            .dm-band-kicker {
                font-size: 0.72rem;
                font-weight: 700;
                letter-spacing: 0.08em;
                text-transform: uppercase;
                opacity: 0.85;
                margin-bottom: 0.35rem;
            }
            .dm-band-title {
                font-size: 1.35rem;
                font-weight: 800;
                line-height: 1.15;
                margin-bottom: 0.25rem;
            }
            .dm-band-body {
                font-size: 0.96rem;
                line-height: 1.55;
                opacity: 0.96;
            }
            .dm-note {
                font-size: 0.9rem;
                line-height: 1.5;
                color: #5B6577;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def status_band(value: str) -> str:
    normalized = value.strip().lower()
    if normalized in {"ready", "strong", "good", "complete", "on track"}:
        return "green"
    if normalized in {"blocked", "critical", "weak", "not ready"}:
        return "red"
    return "yellow"


def status_card(title: str, value: str, body: str = "") -> None:
    band = status_band(value)
    palette = {
        "green": {"bg": "#ECFDF3", "border": "#A7F3D0", "text": "#065F46", "pill": "#10B981"},
        "yellow": {"bg": "#FFFBEB", "border": "#FDE68A", "text": "#92400E", "pill": "#F59E0B"},
        "red": {"bg": "#FEF2F2", "border": "#FECACA", "text": "#991B1B", "pill": "#EF4444"},
    }
    colors = palette[band]
    st.markdown(
        f"""
        <div style="
            background: {colors['bg']};
            border: 1px solid {colors['border']};
            border-radius: 18px;
            padding: 0.95rem 1rem;
            margin-bottom: 0.75rem;
            min-height: 180px;
        ">
            <div style="
                width: 44px;
                height: 6px;
                border-radius: 999px;
                background: {colors['pill']};
                margin-bottom: 0.6rem;
            "></div>
            <div style="
                font-size: 0.75rem;
                font-weight: 700;
                letter-spacing: 0.08em;
                text-transform: uppercase;
                color: #6B7280;
                margin-bottom: 0.35rem;
            ">
                {title}
            </div>
            <div style="
                font-size: 1.15rem;
                font-weight: 800;
                color: {colors['text']};
                margin-bottom: 0.25rem;
                line-height: 1.2;
            ">
                {value}
            </div>
            <div style="
                font-size: 0.93rem;
                line-height: 1.5;
                color: #475569;
            ">
                {body}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _currency(value: float | int | None) -> str:
    if value is None:
        return "—"
    return f"${value:,.0f}"


def _months(value: float | int | None) -> str:
    if value is None:
        return "—"
    return f"{value:.1f} mo"


def _format_metric(value: Any, kind: str) -> str:
    if kind == "currency":
        return _currency(value)
    if kind == "months":
        return _months(value)
    return str(value)


def _scenario_store() -> list[dict[str, Any]]:
    if "deal_model_scenarios" not in st.session_state:
        scenarios: list[dict[str, Any]] = []
        for preset_name in ["Base Case", "Conservative Case", "SBA Case"]:
            base = deepcopy(DEFAULT_SCENARIO_TEMPLATE)
            base.update(SCENARIO_PRESETS[preset_name])
            scenarios.append(base)
        st.session_state["deal_model_scenarios"] = scenarios
        st.session_state["deal_model_active_index"] = 0
        st.session_state["deal_model_compare_names"] = [s["scenario_name"] for s in scenarios[:2]]
    return st.session_state["deal_model_scenarios"]


def _active_index() -> int:
    scenarios = _scenario_store()
    idx = int(st.session_state.get("deal_model_active_index", 0))
    if idx < 0 or idx >= len(scenarios):
        idx = 0
        st.session_state["deal_model_active_index"] = idx
    return idx


def _active_scenario() -> dict[str, Any]:
    return _scenario_store()[_active_index()]


def _scenario_names() -> list[str]:
    return [s["scenario_name"] for s in _scenario_store()]


def _rename_duplicates() -> None:
    seen: dict[str, int] = {}
    for scenario in _scenario_store():
        base_name = scenario["scenario_name"].strip() or "Scenario"
        count = seen.get(base_name, 0)
        scenario["scenario_name"] = base_name if count == 0 else f"{base_name} {count + 1}"
        seen[base_name] = count + 1


def _scenario_key(scenario: dict[str, Any], field: str) -> str:
    safe_name = scenario["scenario_name"].lower().replace(" ", "_").replace("-", "_")
    return f"deal_model_{safe_name}_{field}"


def _bind_number_input(
    scenario: dict[str, Any],
    field: str,
    label: str,
    *,
    min_value: float = 0.0,
    step: float = 1000.0,
    integer: bool = False,
) -> None:
    key = _scenario_key(scenario, field)
    if key not in st.session_state:
        default = scenario.get(field, 0)
        st.session_state[key] = int(default) if integer else float(default)

    if integer:
        st.number_input(label, min_value=int(min_value), step=int(step), key=key)
        scenario[field] = int(st.session_state[key])
    else:
        st.number_input(label, min_value=float(min_value), step=float(step), key=key)
        scenario[field] = float(st.session_state[key])


def _add_scenario_from_current() -> None:
    current = deepcopy(_active_scenario())
    current["scenario_name"] = f"{current['scenario_name']} Copy"
    current["is_working_model"] = False
    _scenario_store().append(current)
    _rename_duplicates()
    st.session_state["deal_model_active_index"] = len(_scenario_store()) - 1


def _add_blank_scenario() -> None:
    scenario = deepcopy(DEFAULT_SCENARIO_TEMPLATE)
    scenario["scenario_name"] = f"Scenario {len(_scenario_store()) + 1}"
    scenario["is_working_model"] = False
    _scenario_store().append(scenario)
    st.session_state["deal_model_active_index"] = len(_scenario_store()) - 1


def _delete_active_scenario() -> None:
    scenarios = _scenario_store()
    if len(scenarios) <= 1:
        return
    idx = _active_index()
    scenarios.pop(idx)
    st.session_state["deal_model_active_index"] = max(0, min(idx, len(scenarios) - 1))


def _set_working_model(active_name: str) -> None:
    for scenario in _scenario_store():
        scenario["is_working_model"] = scenario["scenario_name"] == active_name


def _monthly_debt_service(loan_amount: float, annual_rate: float, term_years: int) -> float:
    if loan_amount <= 0 or annual_rate <= 0 or term_years <= 0:
        return 0.0
    r = annual_rate / 100 / 12
    n = term_years * 12
    return loan_amount * (r * (1 + r) ** n) / ((1 + r) ** n - 1)


def _scenario_outputs(s: dict[str, Any]) -> dict[str, Any]:
    total_uses = sum(
        float(s[k]) for k in [
            "franchise_fee","buildout_cost","equipment_cost","furniture_fixtures_signage","tech_pos_setup",
            "inventory_opening","professional_fees","permits_licenses","training_travel","preopening_payroll",
            "marketing_opening","working_capital_reserve","contingency",
        ]
    )
    total_sources = sum(
        float(s[k]) for k in [
            "owner_cash","sba_loan","conventional_loan","investor_equity","landlord_ti","seller_note","other_funding",
        ]
    )
    loan_amount = float(s["sba_loan"]) + float(s["conventional_loan"])
    debt_service = _monthly_debt_service(loan_amount, float(s["interest_rate"]), int(s["term_years"]))
    stabilized_sales = float(s["stabilized_monthly_sales"])
    variable_pct = (
        float(s["cogs_percent"]) + float(s["labor_percent"]) + float(s["royalty_percent"]) + float(s["marketing_percent"])
    ) / 100
    fixed_monthly = (
        float(s["occupancy_cost_monthly"]) + float(s["insurance_monthly"]) + float(s["utilities_monthly"])
        + float(s["software_monthly"]) + float(s["other_fixed_costs_monthly"]) + debt_service
    )
    contribution_margin_pct = 1 - variable_pct
    break_even_sales = fixed_monthly / contribution_margin_pct if contribution_margin_pct > 0 else 0.0
    owner_cash_required = max(total_uses - (total_sources - float(s["owner_cash"])), 0.0)
    funding_gap = total_uses - total_sources

    monthly_points = [float(s["month_1_sales"]), float(s["month_2_sales"]), float(s["month_3_sales"])]
    ramp_months = max(int(s["ramp_months"]), 3)
    if ramp_months > 3:
        last = monthly_points[-1]
        target = stabilized_sales
        steps = ramp_months - 3
        for i in range(steps):
            monthly_points.append(last + (target - last) * ((i + 1) / steps))
    while len(monthly_points) < 12:
        monthly_points.append(stabilized_sales)

    cash = float(s["working_capital_reserve"])
    lowest_cash = cash
    months_to_owner_pay = None
    for i, sales in enumerate(monthly_points[:12], start=1):
        variable = sales * variable_pct
        pre_owner_cash = sales - variable - fixed_monthly
        owner_pay = float(s["owner_salary_monthly"]) if i >= int(s["owner_salary_start_month"]) else 0.0
        if months_to_owner_pay is None and owner_pay > 0:
            months_to_owner_pay = float(i)
        cash += pre_owner_cash - owner_pay
        lowest_cash = min(lowest_cash, cash)

    stressed_sales = stabilized_sales * (1 - float(s["sales_downside_percent"]) / 100)
    stressed_buildout = float(s["buildout_cost"]) * (1 + float(s["buildout_overrun_percent"]) / 100)
    stressed_labor_pct = float(s["labor_percent"]) * (1 + float(s["labor_overrun_percent"]) / 100)
    stressed_fixed = fixed_monthly + (stressed_buildout - float(s["buildout_cost"])) / max(int(s["buildout_months"]), 1)
    stressed_variable = stressed_sales * (
        float(s["cogs_percent"]) + stressed_labor_pct + float(s["royalty_percent"]) + float(s["marketing_percent"])
    ) / 100
    stressed_monthly_cash = stressed_sales - stressed_variable - stressed_fixed
    stressed_low_cash = float(s["working_capital_reserve"]) + stressed_monthly_cash * 12

    if funding_gap > 0:
        breaks_first = "Funding gap"
    elif stressed_low_cash < float(s["minimum_cash_buffer"]):
        breaks_first = "Cash buffer"
    elif break_even_sales > stabilized_sales:
        breaks_first = "Sales ramp"
    else:
        breaks_first = "Execution discipline"

    return {
        "total_uses": total_uses,
        "total_sources": total_sources,
        "funding_gap": funding_gap,
        "owner_cash_required": owner_cash_required,
        "monthly_debt_service": debt_service,
        "break_even_sales": break_even_sales,
        "year1_low_cash": lowest_cash,
        "months_to_owner_pay": months_to_owner_pay,
        "stressed_low_cash": stressed_low_cash,
        "breaks_first": breaks_first,
    }


def _top_watchout(outputs: dict[str, Any], scenario: dict[str, Any]) -> str:
    if outputs["funding_gap"] > 0:
        return "Funding still does not fully cover uses."
    if outputs["stressed_low_cash"] < 0:
        return "The downside case runs out of cash."
    if outputs["break_even_sales"] > scenario["stabilized_monthly_sales"]:
        return "Break-even sales are above stabilized sales."
    return "Main risk has shifted from structure to execution."


def _render_toolbar() -> None:
    scenarios = _scenario_store()
    names = _scenario_names()
    active_idx = _active_index()

    st.markdown('<div class="dm-toolbar">', unsafe_allow_html=True)

    top_left, top_mid, top_right = st.columns([1.5, 1.2, 1.3], gap="large")
    with top_left:
        selected_name = st.selectbox("Working scenario", options=names, index=active_idx, key="deal_model_active_name")
        st.session_state["deal_model_active_index"] = names.index(selected_name)
    with top_mid:
        st.multiselect(
            "Compare scenarios",
            options=names,
            default=st.session_state.get("deal_model_compare_names", names[:2]),
            max_selections=4,
            key="deal_model_compare_names",
        )
    with top_right:
        st.toggle("Show deltas", value=st.session_state.get("deal_model_show_deltas", True), key="deal_model_show_deltas")
        st.toggle("Compare mode", value=st.session_state.get("deal_model_compare_mode", True), key="deal_model_compare_mode")

    b1, b2, b3, b4 = st.columns(4, gap="small")
    with b1:
        if st.button("New Scenario", use_container_width=True):
            _add_blank_scenario()
            st.rerun()
    with b2:
        if st.button("Duplicate Scenario", use_container_width=True):
            _add_scenario_from_current()
            st.rerun()
    with b3:
        if st.button("Delete Scenario", use_container_width=True, disabled=len(scenarios) <= 1):
            _delete_active_scenario()
            st.rerun()
    with b4:
        if st.button("Mark as Working Model", use_container_width=True):
            _set_working_model(_scenario_names()[_active_index()])
            st.rerun()

    active = _active_scenario()
    active["scenario_name"] = st.text_input(
        "Scenario name",
        value=active["scenario_name"],
        key=f"scenario_name_{_active_index()}",
    ).strip() or "Scenario"
    active["notes"] = st.text_area(
        "Scenario notes",
        value=active.get("notes", ""),
        key=f"scenario_notes_{_active_index()}",
        height=80,
        placeholder="What is different about this model?",
    )

    _rename_duplicates()
    st.markdown("</div>", unsafe_allow_html=True)


def _render_status_band(outputs: dict[str, Any]) -> None:
    working = next((s["scenario_name"] for s in _scenario_store() if s.get("is_working_model")), _active_scenario()["scenario_name"])
    count = len(_scenario_store())
    watchout = _top_watchout(outputs, _active_scenario())
    st.markdown(
        f"""
        <div class="dm-band">
            <div class="dm-band-kicker">Deal model</div>
            <div class="dm-band-title">Working scenario: {working}</div>
            <div class="dm-band-body">Scenarios saved: {count} · Main watchout: {watchout}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_metric_strip(compare_names: list[str]) -> None:
    selected = [s for s in _scenario_store() if s["scenario_name"] in compare_names] or [_active_scenario()]
    outputs = {s["scenario_name"]: _scenario_outputs(s) for s in selected}
    cols = st.columns(len(TOP_METRICS), gap="large")
    base_name = selected[0]["scenario_name"]
    for col, metric in zip(cols, TOP_METRICS):
        value = outputs[base_name][metric.key]
        with col:
            st.metric(metric.label, _format_metric(value, metric.kind))


def _render_inputs() -> None:
    s = _active_scenario()
    tabs = st.tabs(["Capital & Uses", "Funding", "Revenue", "Costs", "Stress"])

    with tabs[0]:
        c1, c2 = st.columns(2, gap="large")
        with c1:
            _bind_number_input(s, "franchise_fee", "Franchise fee", step=5000.0)
            _bind_number_input(s, "buildout_cost", "Buildout cost", step=10000.0)
            _bind_number_input(s, "equipment_cost", "Equipment cost", step=5000.0)
            _bind_number_input(s, "furniture_fixtures_signage", "Furniture / fixtures / signage", step=5000.0)
            _bind_number_input(s, "working_capital_reserve", "Working capital reserve", step=5000.0)
        with c2:
            _bind_number_input(s, "tech_pos_setup", "Tech / POS setup", step=1000.0)
            _bind_number_input(s, "inventory_opening", "Opening inventory", step=1000.0)
            _bind_number_input(s, "professional_fees", "Professional fees", step=1000.0)
            _bind_number_input(s, "preopening_payroll", "Pre-opening payroll", step=1000.0)
            _bind_number_input(s, "contingency", "Contingency", step=5000.0)

    with tabs[1]:
        c1, c2 = st.columns(2, gap="large")
        with c1:
            _bind_number_input(s, "owner_cash", "Owner cash", step=5000.0)
            _bind_number_input(s, "sba_loan", "SBA loan", step=5000.0)
            _bind_number_input(s, "conventional_loan", "Conventional loan", step=5000.0)
            _bind_number_input(s, "investor_equity", "Investor equity", step=5000.0)
        with c2:
            _bind_number_input(s, "landlord_ti", "Landlord TI", step=5000.0)
            _bind_number_input(s, "seller_note", "Seller note", step=5000.0)
            _bind_number_input(s, "other_funding", "Other funding", step=5000.0)
            _bind_number_input(s, "interest_rate", "Interest rate %", step=0.25)
            _bind_number_input(s, "term_years", "Loan term (years)", min_value=1, step=1, integer=True)

    with tabs[2]:
        c1, c2 = st.columns(2, gap="large")
        with c1:
            _bind_number_input(s, "month_1_sales", "Month 1 sales", step=5000.0)
            _bind_number_input(s, "month_2_sales", "Month 2 sales", step=5000.0)
            _bind_number_input(s, "month_3_sales", "Month 3 sales", step=5000.0)
        with c2:
            _bind_number_input(s, "stabilized_monthly_sales", "Stabilized monthly sales", step=5000.0)
            _bind_number_input(s, "ramp_months", "Ramp months", min_value=3, step=1, integer=True)
            _bind_number_input(s, "owner_salary_start_month", "Owner salary starts month", min_value=1, step=1, integer=True)
            _bind_number_input(s, "owner_salary_monthly", "Owner salary monthly", step=500.0)

    with tabs[3]:
        c1, c2 = st.columns(2, gap="large")
        with c1:
            _bind_number_input(s, "cogs_percent", "COGS %", step=0.5)
            _bind_number_input(s, "labor_percent", "Labor %", step=0.5)
            _bind_number_input(s, "royalty_percent", "Royalty %", step=0.5)
            _bind_number_input(s, "marketing_percent", "Marketing %", step=0.5)
        with c2:
            _bind_number_input(s, "occupancy_cost_monthly", "Occupancy monthly", step=500.0)
            _bind_number_input(s, "insurance_monthly", "Insurance monthly", step=100.0)
            _bind_number_input(s, "utilities_monthly", "Utilities monthly", step=100.0)
            _bind_number_input(s, "other_fixed_costs_monthly", "Other fixed costs monthly", step=250.0)

    with tabs[4]:
        c1, c2 = st.columns(2, gap="large")
        with c1:
            _bind_number_input(s, "sales_downside_percent", "Sales downside %", step=1.0)
            _bind_number_input(s, "buildout_overrun_percent", "Buildout overrun %", step=1.0)
        with c2:
            _bind_number_input(s, "labor_overrun_percent", "Labor overrun %", step=1.0)
            _bind_number_input(s, "minimum_cash_buffer", "Minimum cash buffer", step=1000.0)


def _render_comparison_table(compare_names: list[str]) -> None:
    selected = [s for s in _scenario_store() if s["scenario_name"] in compare_names] or [_active_scenario()]
    outputs = {s["scenario_name"]: _scenario_outputs(s) for s in selected}
    rows: list[dict[str, Any]] = []
    base_name = selected[0]["scenario_name"]
    base_outputs = outputs[base_name]
    for metric in COMPARE_METRICS:
        row = {"Metric": metric.label}
        for scenario in selected:
            val = outputs[scenario["scenario_name"]][metric.key]
            display = _format_metric(val, metric.kind)
            if st.session_state.get("deal_model_show_deltas", True) and metric.kind != "text":
                base_val = base_outputs[metric.key]
                if isinstance(val, (int, float)) and isinstance(base_val, (int, float)) and scenario["scenario_name"] != base_name:
                    if metric.kind == "currency":
                        display = f"{display} ({val - base_val:+,.0f})"
                    else:
                        display = f"{display} ({val - base_val:+.1f})"
            row[scenario["scenario_name"]] = display
        rows.append(row)
    st.dataframe(rows, use_container_width=True, hide_index=True)


def _interpretation_cards(outputs: dict[str, Any]) -> tuple[tuple[str,str,str], tuple[str,str,str], tuple[str,str,str]]:
    if outputs["funding_gap"] > 0:
        now = ("Now", "Blocked", "Close the funding gap before treating this model as executable.")
    elif outputs["break_even_sales"] > _active_scenario()["stabilized_monthly_sales"]:
        now = ("Now", "Caution", "Break-even sales are above the stabilized case.")
    else:
        now = ("Now", "Ready", "The current structure is directionally workable.")

    next_step = ("Next", "In Progress", "Compare this case against one conservative case and one funding alternative.")

    if outputs["stressed_low_cash"] < 0:
        watch = ("Watch", "Critical", "The downside case runs out of cash.")
    elif outputs["monthly_debt_service"] > 10000:
        watch = ("Watch", "Caution", "Debt service may be too heavy for the early ramp.")
    else:
        watch = ("Watch", "On Track", "Main risk shifts from structure to execution.")
    return now, next_step, watch


def render_deal_model() -> None:
    open_shell()
    _inject_local_styles()
    _scenario_store()

    render_page_header(
        eyebrow=APP_PRODUCT,
        title="Deal Model",
        subtitle="Compare multiple structures, pressure-test assumptions, and decide which version of the deal is actually workable.",
        wide=True,
    )
    render_section_intro(
        title="Scenario comparison engine",
        body="Use this page to compare funding structures, buildout assumptions, revenue ramps, and downside resilience before you treat a model as decision-ready.",
    )

    _render_toolbar()

    compare_names = st.session_state.get("deal_model_compare_names", _scenario_names()[:2])
    active_outputs = _scenario_outputs(_active_scenario())

    _render_status_band(active_outputs)
    _render_metric_strip(compare_names)

    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

    left, right = st.columns([1.2, 1], gap="large")
    with left:
        _render_inputs()
    with right:
        st.markdown("### Comparison")
        _render_comparison_table(compare_names)
        st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3, gap="medium")
        now, next_step, watch = _interpretation_cards(active_outputs)
        with c1:
            status_card(*now)
        with c2:
            status_card(*next_step)
        with c3:
            status_card(*watch)

    close_shell()
