"""PressureTest calculator logic.

These calculators are intentionally conservative planning tools. They do not
provide legal, tax, financial, accounting, or investment advice.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class WorkingCapitalInputs:
    starting_cash: float
    monthly_fixed_costs: float
    monthly_payroll: float
    owner_draw: float
    expected_monthly_revenue: float
    gross_margin_pct: float
    ramp_months: int


@dataclass(frozen=True)
class WorkingCapitalResult:
    monthly_cash_burn: float
    runway_months: float
    minimum_buffer: float
    pressure_level: str
    interpretation: str


@dataclass(frozen=True)
class RampInputs:
    target_monthly_revenue: float
    starting_monthly_revenue: float
    monthly_growth_rate_pct: float
    fixed_monthly_costs: float
    gross_margin_pct: float
    starting_cash: float


@dataclass(frozen=True)
class RampResult:
    months_to_target: int
    projected_cash_low_point: float
    cumulative_cash_needed: float
    pressure_level: str
    interpretation: str


@dataclass(frozen=True)
class StaffingInputs:
    hourly_rate: float
    weekly_hours: float
    employee_count: int
    payroll_tax_benefit_load_pct: float
    manager_salary_monthly: float
    monthly_revenue: float
    labor_target_pct: float


@dataclass(frozen=True)
class StaffingResult:
    monthly_staff_cost: float
    labor_pct_of_revenue: float
    target_labor_cost: float
    monthly_gap: float
    pressure_level: str
    interpretation: str


def _level_from_ratio(value: float, moderate: float, high: float) -> str:
    if value >= high:
        return "High pressure"
    if value >= moderate:
        return "Moderate pressure"
    return "Lower pressure"


def calculate_working_capital(inputs: WorkingCapitalInputs) -> WorkingCapitalResult:
    gross_profit = inputs.expected_monthly_revenue * (inputs.gross_margin_pct / 100)
    monthly_cash_burn = max(0.0, inputs.monthly_fixed_costs + inputs.monthly_payroll + inputs.owner_draw - gross_profit)
    runway_months = 99.0 if monthly_cash_burn <= 0 else inputs.starting_cash / monthly_cash_burn
    minimum_buffer = max(0.0, monthly_cash_burn * max(3, min(inputs.ramp_months, 12)))

    if runway_months < 6:
        level = "High pressure"
        interpretation = "Cash runway is thin for a ramp period. Delay, slower revenue, or staffing pressure could force outside capital or owner concessions."
    elif runway_months < 12:
        level = "Moderate pressure"
        interpretation = "Runway may be workable, but the plan depends on disciplined spend control and realistic ramp assumptions."
    else:
        level = "Lower pressure"
        interpretation = "Runway appears more durable, assuming the revenue and margin assumptions hold up under validation."

    return WorkingCapitalResult(monthly_cash_burn, runway_months, minimum_buffer, level, interpretation)


def calculate_ramp(inputs: RampInputs) -> RampResult:
    revenue = max(0.0, inputs.starting_monthly_revenue)
    target = max(revenue, inputs.target_monthly_revenue)
    monthly_growth = max(0.0, inputs.monthly_growth_rate_pct) / 100
    cash = inputs.starting_cash
    low_point = cash
    cumulative_need = 0.0
    months = 0

    while revenue < target and months < 60:
        gross_profit = revenue * (inputs.gross_margin_pct / 100)
        monthly_gap = inputs.fixed_monthly_costs - gross_profit
        cash -= monthly_gap
        low_point = min(low_point, cash)
        cumulative_need += max(0.0, monthly_gap)
        revenue = revenue * (1 + monthly_growth) if monthly_growth > 0 else revenue
        months += 1
        if monthly_growth <= 0 and revenue < target:
            months = 60
            break

    pressure_ratio = cumulative_need / max(inputs.starting_cash, 1.0)
    level = _level_from_ratio(pressure_ratio, 0.45, 0.75)
    if months >= 60:
        interpretation = "The ramp does not reach the target within five years under the current assumptions. Revisit growth rate, pricing, demand, and fixed costs."
    elif level == "High pressure":
        interpretation = "The ramp consumes a large share of available cash before reaching the target revenue level. Validate timing and contingency capital."
    elif level == "Moderate pressure":
        interpretation = "The ramp is plausible but sensitive to slower sales growth, payroll timing, and delayed break-even."
    else:
        interpretation = "The ramp has more breathing room, provided local demand and gross margin assumptions are independently validated."

    return RampResult(months, low_point, cumulative_need, level, interpretation)


def calculate_staffing_pressure(inputs: StaffingInputs) -> StaffingResult:
    hourly_monthly = inputs.hourly_rate * inputs.weekly_hours * 4.333 * inputs.employee_count
    load = 1 + max(0.0, inputs.payroll_tax_benefit_load_pct) / 100
    monthly_staff_cost = hourly_monthly * load + inputs.manager_salary_monthly
    labor_pct = (monthly_staff_cost / inputs.monthly_revenue * 100) if inputs.monthly_revenue > 0 else 0.0
    target_labor_cost = inputs.monthly_revenue * (inputs.labor_target_pct / 100)
    gap = monthly_staff_cost - target_labor_cost

    ratio = labor_pct / max(inputs.labor_target_pct, 1.0)
    level = _level_from_ratio(ratio, 1.1, 1.3)
    if level == "High pressure":
        interpretation = "Labor appears materially above the target level. The model may require higher sales, leaner scheduling, or revised owner-role assumptions."
    elif level == "Moderate pressure":
        interpretation = "Labor is close enough to require active scheduling discipline and validation against real operating hours."
    else:
        interpretation = "Labor appears within target range, subject to local wage conditions, absenteeism, manager coverage, and training time."

    return StaffingResult(monthly_staff_cost, labor_pct, target_labor_cost, gap, level, interpretation)


def money(value: float) -> str:
    return f"${value:,.0f}"


def pct(value: float) -> str:
    return f"{value:.1f}%"
