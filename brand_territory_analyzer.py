
from __future__ import annotations

import os
import re
from dataclasses import dataclass, asdict
from typing import Any
from urllib.parse import urlparse

try:
    import requests
    from bs4 import BeautifulSoup
except Exception:  # pragma: no cover - app still works without optional scrape packages
    requests = None
    BeautifulSoup = None

try:
    from openai import OpenAI
except Exception:  # pragma: no cover - app still works without OpenAI installed
    OpenAI = None


CATEGORY_KEYWORDS: dict[str, list[str]] = {
    "Coffee / Beverage": ["coffee", "espresso", "latte", "drive-thru", "drive thru", "beverage", "smoothie", "tea", "cafe", "cold brew"],
    "Restaurant / QSR": ["restaurant", "burger", "pizza", "chicken", "taco", "sandwich", "food", "qsr", "fast casual", "dining"],
    "Fitness / Wellness": ["fitness", "gym", "workout", "pilates", "yoga", "studio", "wellness", "membership", "trainer"],
    "Home Services": ["home service", "plumbing", "hvac", "cleaning", "restoration", "roofing", "pest", "lawn", "technician"],
    "Education / Child Services": ["child", "kids", "education", "tutoring", "school", "learning", "daycare", "preschool"],
    "Health / Beauty": ["salon", "spa", "beauty", "med spa", "hair", "lashes", "wax", "skincare", "massage"],
    "B2B / Professional Services": ["business services", "b2b", "staffing", "printing", "marketing", "consulting", "accounting", "payroll"],
}

CATEGORY_RISKS: dict[str, list[str]] = {
    "Coffee / Beverage": [
        "Daypart and staffing discipline matter more than the brand story.",
        "Drive-thru throughput, local awareness, and repeat frequency can determine whether the model works.",
        "COGS and approved-supplier economics should be pressure-tested against the local market.",
    ],
    "Restaurant / QSR": [
        "Labor scheduling, food cost controls, and speed of service are likely core operating risks.",
        "Buildout, occupancy, and ramp-time sensitivity can create early cash pressure.",
        "Third-party delivery economics and discounting should not be assumed to improve unit economics.",
    ],
    "Fitness / Wellness": [
        "Pre-sale execution and membership churn often drive early cash-flow stability.",
        "Coach/staff quality and local community building may matter as much as brand recognition.",
        "Seasonality and cancellation behavior should be modeled conservatively.",
    ],
    "Home Services": [
        "Technician recruiting, dispatch discipline, and territory quality are likely major success drivers.",
        "Lead generation costs and response times should be validated locally.",
        "Owner involvement may remain high until hiring and route density stabilize.",
    ],
    "Education / Child Services": [
        "Regulatory requirements, staffing ratios, and local trust-building can materially affect launch speed.",
        "Real estate, safety requirements, and parent acquisition timelines should be validated early.",
        "Local household income, commute patterns, and school density matter for fit.",
    ],
    "Health / Beauty": [
        "Provider hiring, repeat bookings, and local reputation are likely more important than initial buzz.",
        "Premium pricing must match local income levels and competitive alternatives.",
        "Service quality variability can create retention risk.",
    ],
    "B2B / Professional Services": [
        "Sales cycle discipline, local network quality, and owner-led selling may be central to success.",
        "Revenue ramp can be slower than consumer concepts if lead generation is not proven locally.",
        "Territory strength depends heavily on business density and decision-maker access.",
    ],
    "General Franchise": [
        "Validate whether the franchisor has proven support in markets like yours, not just in mature core markets.",
        "Pressure-test ramp time, owner dependency, staffing, local marketing, and fixed-cost leverage.",
        "Ask operators what surprised them after opening, not just whether they would do it again.",
    ],
}

CATEGORY_WEIGHTS: dict[str, dict[str, str]] = {
    "Coffee / Beverage": {"labor": "High", "buildout": "High", "competition": "High", "owner_dependency": "Moderate–High", "ramp": "High"},
    "Restaurant / QSR": {"labor": "High", "buildout": "High", "competition": "High", "owner_dependency": "High", "ramp": "High"},
    "Fitness / Wellness": {"labor": "Moderate", "buildout": "Moderate–High", "competition": "Moderate–High", "owner_dependency": "Moderate", "ramp": "High"},
    "Home Services": {"labor": "Moderate–High", "buildout": "Low–Moderate", "competition": "Moderate", "owner_dependency": "High", "ramp": "Moderate–High"},
    "Education / Child Services": {"labor": "High", "buildout": "Moderate–High", "competition": "Moderate", "owner_dependency": "Moderate–High", "ramp": "Moderate"},
    "Health / Beauty": {"labor": "Moderate–High", "buildout": "Moderate", "competition": "Moderate–High", "owner_dependency": "Moderate", "ramp": "Moderate–High"},
    "B2B / Professional Services": {"labor": "Low–Moderate", "buildout": "Low", "competition": "Moderate", "owner_dependency": "High", "ramp": "High"},
    "General Franchise": {"labor": "Unknown", "buildout": "Unknown", "competition": "Unknown", "owner_dependency": "Unknown", "ramp": "Unknown"},
}

CLOSURE_QUESTIONS: list[str] = [
    "How many units opened and closed in the past 36 months?",
    "Were closures concentrated in newer expansion markets or markets far from the brand's core region?",
    "Were closed units franchisee-owned, company-owned, or a mix?",
    "How do average unit volumes differ between core markets and newer outer markets?",
    "What operational changes were made after closures or market exits?",
    "Are Item 19 results primarily based on mature/core-market stores?",
    "What local supply chain, freight, labor, or marketing assumptions differ from the home market?",
]

@dataclass
class WebsiteSnapshot:
    url: str
    final_url: str
    title: str
    description: str
    extracted_text: str
    scrape_status: str


def normalize_url(url: str) -> str:
    value = (url or "").strip()
    if not value:
        return ""
    if not value.startswith(("http://", "https://")):
        value = "https://" + value
    return value


def scrape_website(url: str, timeout: int = 10) -> WebsiteSnapshot:
    normalized = normalize_url(url)
    if not normalized:
        return WebsiteSnapshot(url="", final_url="", title="", description="", extracted_text="", scrape_status="No website provided.")

    if requests is None or BeautifulSoup is None:
        return WebsiteSnapshot(
            url=normalized,
            final_url=normalized,
            title="",
            description="",
            extracted_text="",
            scrape_status="Website scraping packages are not installed. Add requests and beautifulsoup4 to requirements.txt.",
        )

    try:
        response = requests.get(
            normalized,
            timeout=timeout,
            headers={"User-Agent": "Mozilla/5.0 PressureTest brand review prototype"},
        )
        response.raise_for_status()
    except Exception as exc:
        return WebsiteSnapshot(
            url=normalized,
            final_url=normalized,
            title="",
            description="",
            extracted_text="",
            scrape_status=f"Could not fetch website automatically: {exc}",
        )

    soup = BeautifulSoup(response.text, "html.parser")
    for tag in soup(["script", "style", "noscript", "svg"]):
        tag.decompose()

    title = soup.title.get_text(" ", strip=True) if soup.title else ""
    desc_tag = soup.find("meta", attrs={"name": "description"}) or soup.find("meta", attrs={"property": "og:description"})
    description = desc_tag.get("content", "").strip() if desc_tag else ""
    text = soup.get_text(" ", strip=True)
    text = re.sub(r"\s+", " ", text)
    return WebsiteSnapshot(
        url=normalized,
        final_url=response.url,
        title=title[:250],
        description=description[:500],
        extracted_text=text[:9000],
        scrape_status="Website text imported successfully.",
    )


def classify_category(text: str, user_category: str = "Auto-detect") -> str:
    if user_category and user_category != "Auto-detect":
        return user_category
    lower = (text or "").lower()
    scores: dict[str, int] = {}
    for category, keywords in CATEGORY_KEYWORDS.items():
        scores[category] = sum(lower.count(keyword) for keyword in keywords)
    best = max(scores, key=scores.get) if scores else "General Franchise"
    return best if scores.get(best, 0) > 0 else "General Franchise"


def _text_contains_any(text: str, terms: list[str]) -> bool:
    lower = (text or "").lower()
    return any(term in lower for term in terms)


def detect_brand_intelligence_signals(
    analysis_context: str,
    category: str,
    competitor_count: int | None = None,
    market_notes: str = "",
) -> dict[str, Any]:
    """Rules-based fallback used for BOTH OpenAI output and manual paste mode."""
    context = "\n".join([analysis_context or "", market_notes or ""]).lower()
    signals: list[str] = []
    risk_points = 0

    if _text_contains_any(context, ["closed", "closure", "closures", "shut down", "shuttered", "ceased operations", "market exit", "withdrawal"]):
        risk_points += 8
        signals.append("Closure / market withdrawal language detected. Validate whether closures are isolated or pattern-based.")

    if _text_contains_any(context, ["non-core", "outer market", "outside core", "new market", "far from", "expansion market", "regional expansion"]):
        risk_points += 6
        signals.append("Outer-market expansion signal detected. Validate whether the concept travels well outside its core region.")

    if _text_contains_any(context, ["supply chain", "approved vendor", "freight", "distribution", "minimum order", "local supplier", "proprietary product"]):
        risk_points += 5
        signals.append("Supply-chain or vendor dependency signal detected. Validate local landed costs and fulfillment reliability.")

    if _text_contains_any(context, ["ramp", "brand awareness", "awareness", "local marketing", "slow start", "sales ramp"]):
        risk_points += 4
        signals.append("Ramp-time / local-awareness signal detected. Model a longer runway before assuming mature-store performance.")

    if _text_contains_any(context, ["item 19", "mature market", "top quartile", "average unit volume", "auv", "system average"]):
        risk_points += 3
        signals.append("Item 19 / benchmark signal detected. Compare core-market and mature-store averages to newer-market results.")

    if competitor_count is not None:
        if competitor_count >= 16:
            risk_points += 6
            signals.append("Direct competitor count is high. Differentiation, site quality, and local awareness need stronger validation.")
        elif competitor_count >= 9:
            risk_points += 4
            signals.append("Direct competitor count appears elevated. Validate demand and share capture assumptions.")

    if category in {"Coffee / Beverage", "Restaurant / QSR"}:
        risk_points += 2
        signals.append("Food/beverage concepts commonly carry labor, throughput, COGS, and occupancy leverage risk.")

    capped = min(risk_points, 25)
    if capped >= 18:
        level = "High"
    elif capped >= 10:
        level = "Elevated"
    elif capped >= 5:
        level = "Moderate"
    else:
        level = "Low / Unknown"

    return {
        "brand_risk_level": level,
        "risk_adjustment": -capped,
        "risk_points": capped,
        "signals": list(dict.fromkeys(signals))[:8],
        "scoring_note": (
            f"Brand/territory intelligence adjustment: -{capped} points. "
            "This is a directional risk adjustment, not investment advice. It should be validated with FDD data, operator calls, and territory research."
        ),
        "closure_questions": CLOSURE_QUESTIONS,
    }


def infer_signals(text: str, category: str, territory: str, competitor_count: int | None, market_notes: str) -> dict[str, Any]:
    lower = (text or "").lower()
    signals = CATEGORY_WEIGHTS.get(category, CATEGORY_WEIGHTS["General Franchise"]).copy()

    claim_terms = ["proven", "turnkey", "low cost", "semi-absentee", "passive", "fast growing", "award", "recession", "guarantee"]
    found_claims = sorted({term for term in claim_terms if term in lower})

    operations_terms = ["drive-thru", "membership", "technician", "delivery", "catering", "training", "real estate", "site selection", "approved vendor", "call center"]
    found_operations = sorted({term for term in operations_terms if term in lower})

    competition_level = "Unknown"
    if competitor_count is not None:
        if competitor_count <= 3:
            competition_level = "Low–Moderate"
        elif competitor_count <= 8:
            competition_level = "Moderate"
        elif competitor_count <= 15:
            competition_level = "Elevated"
        else:
            competition_level = "High"
        signals["competition"] = competition_level

    territory_clean = territory.strip() or "the target territory"
    summary = (
        f"This appears to be a {category.lower()} concept being evaluated for {territory_clean}. "
        "The first-pass read should focus on local demand, competitor density, ramp assumptions, store closures, and whether the franchisor has proven support in markets similar to the target territory."
    )

    if found_claims:
        summary += " The website language includes franchise-sales signals that should be verified through operator validation rather than accepted at face value."

    return {
        "category": category,
        "signals": signals,
        "found_claims": found_claims,
        "found_operations": found_operations,
        "competition_level": competition_level,
        "summary": summary,
        "market_notes": market_notes.strip(),
    }


def build_pressure_points(category: str, signals: dict[str, str], competitor_count: int | None, market_notes: str, brand_intel: dict[str, Any] | None = None) -> list[str]:
    points = list(CATEGORY_RISKS.get(category, CATEGORY_RISKS["General Franchise"]))
    if competitor_count is not None and competitor_count >= 9:
        points.insert(0, "Competition density appears elevated; the unit may need stronger local awareness, site quality, and differentiation than the base sales story implies.")
    if brand_intel and brand_intel.get("brand_risk_level") in {"Elevated", "High"}:
        points.insert(0, "Brand/territory intelligence shows elevated risk signals that should affect the overall PressureTest score until validated.")
    if market_notes.strip():
        points.append("User territory notes indicate local conditions should be treated as part of the risk review, not background context.")
    return points[:7]


def build_diligence_questions(category: str, territory: str, competitor_count: int | None, brand_intel: dict[str, Any] | None = None) -> list[str]:
    territory_label = territory.strip() or "this territory"
    questions = [
        f"How many open units does the franchisor have in markets similar to {territory_label}, not just in its core market?",
        "How many units opened and closed in the past 36 months?",
        "Were closures concentrated in newer expansion markets or markets far from the brand's core region?",
        "What did first-year revenue, labor, COGS, and occupancy look like for newer units versus mature units?",
        "What local marketing support is provided before and after opening, and who pays for it?",
        "Which assumptions in the Item 19 or sales materials are based on mature markets, high-performing units, or different real estate profiles?",
        "What are the top three reasons recent franchisees have underperformed or closed?",
    ]
    if category in {"Coffee / Beverage", "Restaurant / QSR"}:
        questions.extend([
            "What are the actual approved-vendor costs in this region after freight, markups, and minimums?",
            "What transaction count and average ticket are needed to cover labor, rent, debt, royalties, and marketing?",
        ])
    if category == "Home Services":
        questions.extend([
            "What does technician recruiting look like in this territory and what is the realistic time to full route density?",
            "What is the expected local customer acquisition cost by channel?",
        ])
    if competitor_count is not None and competitor_count >= 9:
        questions.append("What specific evidence shows this territory can support another operator in a crowded category?")
    return questions[:10]


def build_chatgpt_prompt(brand_name: str, website: str, territory: str, category: str, website_text: str, market_notes: str) -> str:
    trimmed = (website_text or "")[:6000]
    return f"""Analyze this franchise opportunity for a structured diligence app called PressureTest.

Important: Do not give legal, tax, lending, accounting, or investment advice. Produce a blunt but cautious operator-focused pressure test. Use terms like appears, may, commonly, should be validated, and based on available signals. Do not tell the user to buy, invest, or sign.

Brand: {brand_name or 'Unknown'}
Website: {website or 'Unknown'}
Target territory: {territory or 'Unknown'}
Detected/selected category: {category}
User territory notes: {market_notes or 'None'}

Website text excerpt:
{trimmed}

Search/consider current public information where possible, especially:
- recent store closures
- market withdrawals
- locations opened and then closed in the past 36 months
- closures concentrated outside the brand's core geography
- signs that the concept may perform differently in outer or newer expansion markets
- local competition in the target territory

Return the analysis in this exact structure:
1. Brand model summary: 3 bullets
2. Likely operational pressure points: 5 bullets
3. Territory / competition concerns: 4 bullets
4. Expansion & closure signals: 5 bullets
5. Outer-market expansion risk: 4 bullets
6. Questions to ask franchisor: 8 bullets
7. Questions to ask existing operators: 6 bullets
8. What could break first: 4 bullets
9. Inputs the user should verify before signing: 6 bullets
""".strip()


def run_openai_deep_dive(
    *,
    brand_name: str,
    website: str,
    territory: str,
    category: str,
    website_text: str,
    market_notes: str,
) -> dict[str, str]:
    """Runs a one-shot OpenAI analysis with web search when OPENAI_API_KEY is available."""
    if OpenAI is None:
        return {"ok": "false", "error": "OpenAI package is not installed. Run: pip install openai", "analysis": ""}
    if not os.getenv("OPENAI_API_KEY"):
        return {"ok": "false", "error": "OPENAI_API_KEY is not set. Manual paste mode is still available.", "analysis": ""}

    prompt = build_chatgpt_prompt(brand_name, website, territory, category, website_text, market_notes)
    instructions = (
        "You are PressureTest's silent franchise diligence analyst. Do not chat. "
        "Return a structured analysis only. Be blunt, cautious, operator-focused, and avoid legal, tax, lending, accounting, or investment advice. "
        "Use web search to look for recent closures, market exits, and competition signals when available."
    )
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    client = OpenAI()

    # Newer docs use web_search. Older accounts/libraries may still require web_search_preview.
    for tool_type in ("web_search", "web_search_preview", None):
        try:
            kwargs: dict[str, Any] = {
                "model": model,
                "instructions": instructions,
                "input": prompt,
                "max_output_tokens": 1800,
            }
            if tool_type:
                kwargs["tools"] = [{"type": tool_type}]
            response = client.responses.create(**kwargs)
            return {"ok": "true", "error": "", "analysis": getattr(response, "output_text", str(response))}
        except Exception as exc:
            last_error = str(exc)
            continue

    return {"ok": "false", "error": f"OpenAI analysis failed: {last_error}", "analysis": ""}


def build_analysis(
    brand_name: str,
    website: str,
    territory: str,
    selected_category: str,
    pasted_text: str,
    competitor_count: int | None,
    market_notes: str,
    ai_analysis_notes: str = "",
) -> dict[str, Any]:
    scraped = scrape_website(website) if website else WebsiteSnapshot("", "", "", "", "", "No website provided.")
    combined_text = " ".join([brand_name or "", scraped.title, scraped.description, scraped.extracted_text, pasted_text or "", ai_analysis_notes or ""])
    category = classify_category(combined_text, selected_category)
    brand_intel = detect_brand_intelligence_signals(combined_text, category, competitor_count, market_notes)
    signals = infer_signals(combined_text, category, territory, competitor_count, market_notes)
    pressure_points = build_pressure_points(category, signals["signals"], competitor_count, market_notes, brand_intel)
    questions = build_diligence_questions(category, territory, competitor_count, brand_intel)
    prompt = build_chatgpt_prompt(brand_name, website, territory, category, combined_text, market_notes)
    return {
        "brand_name": brand_name.strip(),
        "website": website.strip(),
        "territory": territory.strip(),
        "selected_category": selected_category,
        "category": category,
        "website_snapshot": asdict(scraped),
        "signals": signals,
        "brand_intelligence": brand_intel,
        "pressure_points": pressure_points,
        "diligence_questions": questions,
        "closure_questions": CLOSURE_QUESTIONS,
        "chatgpt_prompt": prompt,
        "analysis_notes": ai_analysis_notes or "",
    }


def refresh_analysis_with_notes(result: dict[str, Any], notes: str) -> dict[str, Any]:
    """Re-run scoring when AI output or manually pasted research is added."""
    return build_analysis(
        brand_name=result.get("brand_name", ""),
        website=result.get("website", ""),
        territory=result.get("territory", ""),
        selected_category=result.get("selected_category", "Auto-detect"),
        pasted_text=" ".join([
            result.get("website_snapshot", {}).get("extracted_text", ""),
            notes or "",
        ]),
        competitor_count=None if result.get("territory_competitor_count") is None else result.get("territory_competitor_count"),
        market_notes=result.get("signals", {}).get("market_notes", ""),
        ai_analysis_notes=notes,
    )
