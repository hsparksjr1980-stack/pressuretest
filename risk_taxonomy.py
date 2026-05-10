# risk_taxonomy.py

from __future__ import annotations

from typing import Final


RISK_TAXONOMY: Final[dict[str, dict[str, str]]] = {
    "liquidity_risk": {
        "label": "Liquidity risk",
        "description": "Risk that available cash is insufficient to absorb ramp timing, shortfalls, or operating pressure.",
    },
    "debt_pressure": {
        "label": "Debt pressure",
        "description": "Risk created by fixed repayment obligations or financing structures that reduce operating flexibility.",
    },
    "lease_rent_pressure": {
        "label": "Lease/rent pressure",
        "description": "Risk created by rent, lease terms, location obligations, or facility commitments.",
    },
    "labor_dependency": {
        "label": "Labor dependency",
        "description": "Risk created by staffing availability, hiring needs, training burden, or founder/operator capacity.",
    },
    "vendor_dependency": {
        "label": "Vendor dependency",
        "description": "Risk created by reliance on suppliers, platforms, partners, or outside providers.",
    },
    "revenue_validation_risk": {
        "label": "Revenue validation risk",
        "description": "Risk that pricing, conversion, demand, or repeat revenue assumptions have not been validated.",
    },
    "market_risk": {
        "label": "Market risk",
        "description": "Risk that the market, customer segment, competitive context, or demand signal is weaker than expected.",
    },
    "execution_risk": {
        "label": "Execution risk",
        "description": "Risk that launch, operating cadence, decision quality, or implementation difficulty exceeds current readiness.",
    },
    "operational_complexity": {
        "label": "Operational complexity",
        "description": "Risk created by moving parts, process burden, compliance needs, logistics, or coordination demands.",
    },
    "legal_document_risk": {
        "label": "Legal/document risk",
        "description": "Risk created by agreements, filings, disclosures, obligations, or unresolved professional review needs.",
    },
}


def get_risk_label(risk_key: str) -> str:
    return RISK_TAXONOMY.get(risk_key, {}).get("label", risk_key.replace("_", " ").title())
