import pandas as pd


def st_session():
    import streamlit as st
    return st.session_state


def _empty_df(columns):
    return pd.DataFrame(columns=columns)


def init_workspace_state():
    defaults = {
        "funding_debt": _empty_df([
            "Bank / Lender",
            "Product (SBA/Conventional/Private)",
            "Loan Amount",
            "Rate (%)",
            "Term (years)",
            "Amort (years)",
            "Monthly Payment (est)",
            "DSCR Req",
            "Collateral / PG",
            "Status",
            "Notes",
        ]),
        "funding_equity": _empty_df([
            "Partner / Investor",
            "Equity Amount",
            "Ownership (%)",
            "Pref Return (%)",
            "Distribution Split",
            "Role (Active/Passive)",
            "Control Rights",
            "Status",
            "Notes",
        ]),
        "quotes": _empty_df([
            "Category (GC/Equipment/Signage/Arch/Permits)",
            "Vendor",
            "Quote Amount",
            "Scope Included",
            "Exclusions",
            "Contingency Included (Y/N)",
            "Timeline (weeks)",
            "Status",
            "Notes",
        ]),
        "leases": _empty_df([
            "Property / Landlord",
            "Rent (Monthly)",
            "NNN / CAM",
            "Term (years)",
            "TI Allowance",
            "Free Rent (months)",
            "Escalation (%)",
            "Deposit",
            "Exclusivity",
            "Drive-thru / Parking",
            "Status",
            "Notes",
        ]),
        "selected_loan": 0.0,
        "selected_rate": 8.5,
        "selected_term": 10.0,
        "selected_rent": 0.0,
        "selected_nnn": 0.0,
        "selected_ti": 0.0,
        "total_quotes": 0.0,
        "working_cap_override": 50000.0,
        "contingency_pct_override": 0.10,
        "su_total_uses": 0.0,
        "su_total_sources": 0.0,
        "su_gap": 0.0,
        "su_net_buildout": 0.0,
    }

    ss = st_session()
    for k, v in defaults.items():
        if k not in ss:
            ss[k] = v


def add_row(df, columns):
    if df is None or df.empty:
        return pd.DataFrame([{c: "" for c in columns}], columns=columns)

    working_df = df.copy()
    for c in columns:
        if c not in working_df.columns:
            working_df[c] = ""

    working_df = working_df[columns]
    new = pd.DataFrame([{c: "" for c in columns}], columns=columns)
    return pd.concat([working_df, new], ignore_index=True)


def delete_row(df):
    if df is None or df.empty:
        return df
    return df.iloc[:-1].copy()


def _sum_numeric(series):
    return pd.to_numeric(series, errors="coerce").fillna(0).sum()


def _safe_float(value, default=0.0):
    try:
        if value is None or value == "":
            return float(default)
        return float(value)
    except (TypeError, ValueError):
        return float(default)


def calc_monthly_debt_payment(principal, annual_rate_pct, term_years):
    principal = _safe_float(principal, 0.0)
    annual_rate_pct = _safe_float(annual_rate_pct, 0.0)
    term_years = _safe_float(term_years, 0.0)

    if principal <= 0 or term_years <= 0:
        return 0.0

    monthly_rate = annual_rate_pct / 100 / 12
    n = int(term_years * 12)

    if n <= 0:
        return 0.0

    if monthly_rate == 0:
        return principal / n

    return principal * (monthly_rate * (1 + monthly_rate) ** n) / (((1 + monthly_rate) ** n) - 1)


def calc_sources_uses(ss):
    uses_quotes = _safe_float(ss.get("total_quotes", 0.0))
    ti = _safe_float(ss.get("selected_ti", 0.0))
    net_buildout = max(uses_quotes - ti, 0.0)

    working_cap = _safe_float(ss.get("working_cap_override", 50000.0), 50000.0)
    contingency_pct = _safe_float(ss.get("contingency_pct_override", 0.10), 0.10)
    contingency = contingency_pct * net_buildout

    total_uses = net_buildout + working_cap + contingency

    debt = _safe_float(ss.get("selected_loan", 0.0))

    eq_df = ss.get("funding_equity", pd.DataFrame())
    equity = 0.0
    if isinstance(eq_df, pd.DataFrame) and not eq_df.empty and "Equity Amount" in eq_df.columns:
        equity = float(_sum_numeric(eq_df["Equity Amount"]))

    total_sources = debt + equity

    debt_payment = calc_monthly_debt_payment(
        ss.get("selected_loan", 0.0),
        ss.get("selected_rate", 8.5),
        ss.get("selected_term", 10),
    )

    selected_rent = _safe_float(ss.get("selected_rent", 0.0))
    selected_nnn = _safe_float(ss.get("selected_nnn", 0.0))
    monthly_occupancy = selected_rent + selected_nnn

    return {
        "uses_quotes": float(uses_quotes),
        "ti": float(ti),
        "net_buildout": float(net_buildout),
        "working_cap": float(working_cap),
        "contingency_pct": float(contingency_pct),
        "contingency": float(contingency),
        "total_uses": float(total_uses),
        "debt": float(debt),
        "equity": float(equity),
        "total_sources": float(total_sources),
        "gap": float(total_uses - total_sources),
        "debt_payment": float(debt_payment),
        "monthly_occupancy": float(monthly_occupancy),
    }


def _ss_float(ss, key, default=0.0):
    return _safe_float(ss.get(key, default), default)


def build_workspace_decision_pack(ss):
    """
    Pulls the most decision-relevant items from workspace + deal model state into one structure.
    """
    su = calc_sources_uses(ss)
    annual_revenue = _ss_float(ss, "deal_model_annual_revenue", 0.0)
    labor_pct = _ss_float(ss, "deal_model_labor_pct", 0.0)
    cogs_pct = _ss_float(ss, "deal_model_cogs_pct", 0.0)
    break_even_month = ss.get("deal_model_break_even_month")
    downside_break_even = ss.get("deal_model_downside_break_even_month")
    financial_verdict = ss.get("financial_verdict", "Not yet modeled")

    what_must_be_true = ss.get("deal_model_what_must_be_true")
    if not what_must_be_true:
        what_must_be_true = []
        if annual_revenue > 0:
            what_must_be_true.append(f"Annual revenue needs to reach about ${annual_revenue:,.0f}.")
        if labor_pct > 0:
            what_must_be_true.append(f"Labor needs to stay near {labor_pct * 100:,.1f}% of sales or better.")
        if cogs_pct > 0:
            what_must_be_true.append(f"COGS needs to stay near {cogs_pct * 100:,.1f}% of sales or better.")
        if break_even_month:
            what_must_be_true.append(f"Cumulative cash likely needs to turn positive by about month {break_even_month}.")
        if su.get("gap", 0.0) > 0:
            what_must_be_true.append("The remaining funding gap needs to be closed before the deal is truly executable.")

    kill_criteria = ss.get("deal_model_kill_criteria")
    if not kill_criteria:
        kill_criteria = []
        if su.get("gap", 0.0) > 0:
            kill_criteria.append(f"Walk away or restructure if the funding gap remains at about ${su['gap']:,.0f}.")
        if labor_pct > 0:
            kill_criteria.append(f"Walk away if labor drifts materially above {(labor_pct + 0.05) * 100:,.1f}% of sales.")
        if cogs_pct > 0:
            kill_criteria.append(f"Walk away if COGS drifts materially above {(cogs_pct + 0.03) * 100:,.1f}% of sales.")
        if downside_break_even is None or (isinstance(downside_break_even, (int, float)) and downside_break_even > 18):
            kill_criteria.append("Walk away if downside break-even is too delayed or not visible at all.")
        kill_criteria.append("Walk away if major diligence questions remain unanswered when you are expected to commit.")

    biggest_unknowns = []
    quotes_df = ss.get("quotes", pd.DataFrame())
    leases_df = ss.get("leases", pd.DataFrame())
    debt_df = ss.get("funding_debt", pd.DataFrame())

    if isinstance(quotes_df, pd.DataFrame) and not quotes_df.empty:
        pending_quotes = 0
        if "Status" in quotes_df.columns:
            pending_quotes = int((quotes_df["Status"].fillna("").astype(str).str.strip().str.lower() != "final").sum())
        if pending_quotes > 0:
            biggest_unknowns.append(f"{pending_quotes} quote items are still not final.")
    else:
        biggest_unknowns.append("Buildout quotes are still incomplete.")

    if isinstance(leases_df, pd.DataFrame) and not leases_df.empty:
        if "Status" in leases_df.columns:
            unresolved_leases = int((leases_df["Status"].fillna("").astype(str).str.strip() == "").sum())
            if unresolved_leases > 0:
                biggest_unknowns.append("Lease terms still need to be finalized and pressure tested.")
    else:
        biggest_unknowns.append("Lease economics still need to be confirmed.")

    if isinstance(debt_df, pd.DataFrame) and not debt_df.empty:
        if "Status" in debt_df.columns:
            active = debt_df["Status"].fillna("").astype(str).str.lower()
            if not active.str.contains("approved|term sheet|selected", regex=True).any():
                biggest_unknowns.append("Debt structure is still not clearly committed.")
    else:
        biggest_unknowns.append("Debt assumptions still need lender confirmation.")

    if financial_verdict == "Not yet modeled":
        biggest_unknowns.append("The deal model has not been built yet, so the workspace is missing its financial pressure test.")
    if not biggest_unknowns:
        biggest_unknowns.append("Major unknowns look more contained, but diligence discipline still matters.")

    next_actions = []
    if su.get("gap", 0.0) > 0:
        next_actions.append("Close the funding gap or reduce uses before treating the deal as executable.")
    if financial_verdict == "Not yet modeled":
        next_actions.append("Run the Deal Model so the workspace is anchored to actual economics, not just notes.")
    else:
        next_actions.append("Review the downside case and confirm whether the risk still matches your tolerance.")
    next_actions.append("Validate real local costs and support expectations before relying on system averages.")
    next_actions.append("Turn the biggest unknowns into specific diligence questions with owners and counterparties.")

    return {
        "sources_uses": su,
        "financial_verdict": financial_verdict,
        "what_must_be_true": what_must_be_true[:5],
        "kill_criteria": kill_criteria[:5],
        "biggest_unknowns": biggest_unknowns[:5],
        "next_actions": next_actions[:5],
    }
