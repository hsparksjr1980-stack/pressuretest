from __future__ import annotations

import streamlit as st

from premium_components import esc, hero, info_card

LANDING_PAGES = [
    {
        "title": "Franchise Working Capital Calculator",
        "slug": "franchise-working-capital-calculator",
        "intent": "Estimate early cash runway and working-capital pressure before signing or financing.",
        "primary_cta": "Open calculator",
        "calculator": "Working capital",
    },
    {
        "title": "Franchise Ramp Timeline Calculator",
        "slug": "franchise-ramp-timeline-calculator",
        "intent": "Test how long it may take to reach a target monthly revenue level and how much cash the ramp may consume.",
        "primary_cta": "Open calculator",
        "calculator": "Ramp timeline",
    },
    {
        "title": "Staffing Cost Pressure Calculator",
        "slug": "staffing-cost-pressure-calculator",
        "intent": "Estimate whether wage, coverage, and management assumptions are likely to strain margins.",
        "primary_cta": "Open calculator",
        "calculator": "Staffing pressure",
    },
]

EDUCATIONAL_PAGES = [
    "How much working capital should a franchise buyer pressure test?",
    "What to validate before relying on franchisor ramp assumptions",
    "Why staffing assumptions often break early franchise models",
    "How to use a break-even estimate without treating it as a guarantee",
    "Questions to ask operators before signing a franchise agreement",
]


def _seo_brief(page: dict[str, str]) -> str:
    return f"""# {page['title']}

## Search intent
{page['intent']}

## Recommended URL
/resources/{page['slug']}

## Page structure
- Plain-English explanation of the pressure point
- Calculator module
- Inputs users should validate independently
- Common diligence questions
- Downloadable summary
- Lead capture prompt: save this calculator output

## Compliance framing
PressureTest is an educational diligence-support platform. This page should not recommend investments, predict success, guarantee outcomes, or provide legal, tax, accounting, financial, or investment advice.
"""


def render_seo_resources() -> None:
    hero(
        "SEO Resource & Calculator Landing Pages",
        "This page defines the first organic acquisition cluster: practical calculators, diligence education, downloadable outputs, and non-advisory framing.",
        "Acquisition infrastructure",
    )

    st.markdown("### First calculator landing pages")
    cols = st.columns(3)
    for index, page in enumerate(LANDING_PAGES):
        with cols[index % 3]:
            info_card(page["title"], page["intent"], page["calculator"])

    st.markdown("### Educational support pages")
    for title in EDUCATIONAL_PAGES:
        st.markdown(f"- {esc(title)}")

    st.markdown("### Export SEO briefs")
    selected = st.selectbox("Select page brief", [p["title"] for p in LANDING_PAGES])
    page = next(p for p in LANDING_PAGES if p["title"] == selected)
    brief = _seo_brief(page)
    st.code(brief, language="markdown")
    st.download_button(
        "Download SEO brief",
        data=brief.encode("utf-8"),
        file_name=f"{page['slug']}-brief.md",
        mime="text/markdown",
        use_container_width=True,
    )

    st.markdown(
        """
        <div class="pt-note">
        Build recommendation: these pages can start inside the Streamlit app for prototype validation, but should eventually move into a static or server-rendered marketing site for stronger indexing, faster page speed, and cleaner analytics.
        </div>
        """,
        unsafe_allow_html=True,
    )
