
from __future__ import annotations

import streamlit as st

from assessment_template import AssessmentGroup, AssessmentQuestion, render_assessment_template
from brand_territory_analyzer import (
    CATEGORY_KEYWORDS,
    build_analysis,
    refresh_analysis_with_notes,
    run_openai_deep_dive,
)
from premium_components import hero, info_card, metric_card

CATEGORY_OPTIONS = ["Auto-detect", *CATEGORY_KEYWORDS.keys(), "General Franchise"]


def _store_analysis(result: dict) -> None:
    st.session_state["brand_territory_analysis"] = result
    st.session_state["brand_analysis_done"] = True
    st.session_state["franchise_name"] = result.get("brand_name") or st.session_state.get("franchise_name", "")
    st.session_state["city_state"] = result.get("territory") or st.session_state.get("city_state", "")
    st.session_state["brand_intelligence_adjustment"] = result.get("brand_intelligence", {}).get("risk_adjustment", 0)
    st.session_state["brand_intelligence_level"] = result.get("brand_intelligence", {}).get("brand_risk_level", "Low / Unknown")
    st.session_state["brand_intelligence_signals"] = result.get("brand_intelligence", {}).get("signals", [])


def _render_snapshot(result: dict) -> None:
    signals = result.get("signals", {})
    signal_map = signals.get("signals", {})
    website_snapshot = result.get("website_snapshot", {})
    brand_intel = result.get("brand_intelligence", {})

    st.markdown("### PressureTest Snapshot")
    st.info(signals.get("summary", "Initial analysis will appear here after you run the snapshot."))

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        metric_card("Category", result.get("category", "Unknown"), "Auto-detected or selected")
    with c2:
        metric_card("Labor", signal_map.get("labor", "Unknown"), "Likely intensity")
    with c3:
        metric_card("Buildout", signal_map.get("buildout", "Unknown"), "Likely capital burden")
    with c4:
        metric_card("Competition", signal_map.get("competition", "Unknown"), "Territory signal")
    with c5:
        metric_card("Brand Risk", brand_intel.get("brand_risk_level", "Low / Unknown"), f"Score adj. {brand_intel.get('risk_adjustment', 0)}")

    st.markdown("### Brand intelligence scoring")
    st.warning(brand_intel.get("scoring_note", "Brand/territory intelligence will be factored into the overall score after analysis is generated."))
    if brand_intel.get("signals"):
        for item in brand_intel.get("signals", []):
            st.markdown(f"- {item}")

    left, right = st.columns([1, 1])
    with left:
        st.markdown("### Likely pressure points")
        for item in result.get("pressure_points", []):
            st.markdown(f"- {item}")
    with right:
        st.markdown("### Diligence questions to ask")
        for item in result.get("diligence_questions", []):
            st.markdown(f"- {item}")

    st.markdown("### Expansion & closure validation")
    st.caption("These questions are included because closure patterns and failed expansion markets can materially change the risk profile, especially for brands expanding away from their core geography.")
    for item in result.get("closure_questions", []):
        st.markdown(f"- {item}")

    with st.expander("Website import details", expanded=False):
        st.write(website_snapshot.get("scrape_status", ""))
        if website_snapshot.get("title"):
            st.write(f"**Title:** {website_snapshot.get('title')}")
        if website_snapshot.get("description"):
            st.write(f"**Description:** {website_snapshot.get('description')}")
        if website_snapshot.get("final_url"):
            st.write(f"**Final URL:** {website_snapshot.get('final_url')}")

    with st.expander("AI deep-dive / manual fallback", expanded=False):
        st.caption("Preferred path: use the OpenAI button to run a silent brand/territory search. Fallback path: copy the prompt into ChatGPT and paste the result back here. Either way, the notes feed the same scoring logic.")
        st.text_area("Fallback copy/paste prompt", value=result.get("chatgpt_prompt", ""), height=260)
        notes = st.text_area(
            "Paste AI/manual analysis notes here",
            value=result.get("analysis_notes", ""),
            height=260,
            placeholder="Paste ChatGPT output, FDD notes, store closure research, operator validation notes, or territory findings here. These notes will affect the brand intelligence adjustment.",
        )
        if st.button("Save notes and recalculate brand intelligence", use_container_width=True):
            updated = refresh_analysis_with_notes(result, notes)
            updated["territory_competitor_count"] = st.session_state.get("territory_competitor_count")
            _store_analysis(updated)
            st.success("Saved notes and recalculated the brand intelligence score.")
            st.rerun()

    if result.get("analysis_notes"):
        st.markdown("### Deep-dive notes used in scoring")
        st.markdown(result["analysis_notes"])


def render_brand_territory() -> None:
    hero(
        "Brand & Territory Snapshot",
        "Enter the brand website and target territory to generate a first-pass diligence read before the user starts filling out the full assessment.",
    )

    st.markdown(
        """
        <div class="pt-card">
          <div class="pt-eyebrow">Brand intelligence layer</div>
          <h3 style="margin:.1rem 0 .35rem 0;">Silent AI analysis when available. Manual fallback when not.</h3>
          <p>This version can use OpenAI to research brand, territory, competition, closures, and outer-market expansion signals. If the API key is not set, pasted notes still feed the same scoring engine. The output is a blunt diligence screen, not legal or investment advice.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.session_state.setdefault("brand_name_input", st.session_state.get("franchise_name", ""))
    st.session_state.setdefault("brand_website", st.session_state.get("brand_website", ""))
    st.session_state.setdefault("selected_category", "Auto-detect")
    st.session_state.setdefault("city_state", st.session_state.get("city_state", ""))
    st.session_state.setdefault("territory_competitor_count", int(st.session_state.get("territory_competitor_count", 0) or 0))
    st.session_state.setdefault("territory_notes", st.session_state.get("territory_notes", ""))

    input_groups = [
        AssessmentGroup(
            title="Brand context",
            description="Capture the basic brand details so the system can interpret the concept correctly.",
            questions=[
                AssessmentQuestion(
                    key="brand_name_input",
                    label="Brand name",
                    placeholder="Example: Sample Coffee Concept",
                ),
                AssessmentQuestion(
                    key="brand_website",
                    label="Brand website",
                    placeholder="https://www.examplefranchise.com",
                ),
                AssessmentQuestion(
                    key="selected_category",
                    label="Business category",
                    kind="select",
                    options=CATEGORY_OPTIONS,
                    help_text="Use Auto-detect first. Override it if the website is vague.",
                ),
            ],
        ),
        AssessmentGroup(
            title="Territory context",
            description="Add local market details to sharpen competition and expansion risk signals.",
            questions=[
                AssessmentQuestion(
                    key="city_state",
                    label="Target territory / city / zip",
                    placeholder="Example: St. Louis, MO or 63368",
                ),
                AssessmentQuestion(
                    key="territory_competitor_count",
                    label="Estimated direct competitors nearby",
                    kind="number",
                    min_value=0,
                    max_value=100,
                    help_text="No paid maps API yet. Enter a rough count from Google Maps/Yelp search in the target area.",
                ),
                AssessmentQuestion(
                    key="territory_notes",
                    label="Territory notes",
                    kind="textarea",
                    placeholder="Examples: new market for brand, heavy coffee competition, suburban drive-thru corridor, high rent area, college town, known closures in nearby markets, etc.",
                ),
            ],
        ),
    ]

    render_assessment_template(
        section_title="Brand inputs",
        context_description="Provide a quick diligence baseline before generating the snapshot.",
        groups=input_groups,
        why_this_matters="Clear brand and territory inputs make pressure points more realistic and reduce false confidence from generic assumptions.",
        next_step_guidance="Complete both groups, then run Generate Brand & Territory Snapshot. Use Deep Dive if you need stronger market evidence.",
    )

    brand_name = st.session_state.get("brand_name_input", "")
    website = st.session_state.get("brand_website", "")
    selected_category = st.session_state.get("selected_category", "Auto-detect")
    territory = st.session_state.get("city_state", "")
    competitor_count_raw = int(st.session_state.get("territory_competitor_count", 0) or 0)
    market_notes = st.session_state.get("territory_notes", "")

    with st.expander("Optional: paste website/franchise/FDD/operator text manually", expanded=False):
        pasted_text = st.text_area(
            "Paste franchise page text, Item 19 excerpts, closure research, franchise brochure notes, or validation notes",
            value=st.session_state.get("brand_pasted_text", ""),
            height=180,
        )

    cta1, cta2 = st.columns([1, 1])
    with cta1:
        run = st.button("Generate Brand & Territory Snapshot", type="primary", use_container_width=True)
    with cta2:
        run_ai = st.button("Run OpenAI Deep Dive", use_container_width=True, help="Requires OPENAI_API_KEY. Searches for closures, market exits, competition, and outer-market risk signals.")

    if run or run_ai:
        st.session_state["brand_website"] = website
        st.session_state["territory_competitor_count"] = int(competitor_count_raw)
        st.session_state["territory_notes"] = market_notes
        st.session_state["brand_pasted_text"] = pasted_text

        result = build_analysis(
            brand_name=brand_name,
            website=website,
            territory=territory,
            selected_category=selected_category,
            pasted_text=pasted_text,
            competitor_count=int(competitor_count_raw) if competitor_count_raw is not None else None,
            market_notes=market_notes,
        )
        result["territory_competitor_count"] = int(competitor_count_raw)

        if run_ai:
            with st.spinner("Running silent OpenAI brand/territory analysis..."):
                ai = run_openai_deep_dive(
                    brand_name=brand_name,
                    website=website,
                    territory=territory,
                    category=result.get("category", selected_category),
                    website_text=" ".join([
                        result.get("website_snapshot", {}).get("title", ""),
                        result.get("website_snapshot", {}).get("description", ""),
                        result.get("website_snapshot", {}).get("extracted_text", ""),
                        pasted_text or "",
                    ]),
                    market_notes=market_notes,
                )
            if ai.get("ok") == "true":
                result = build_analysis(
                    brand_name=brand_name,
                    website=website,
                    territory=territory,
                    selected_category=selected_category,
                    pasted_text=pasted_text,
                    competitor_count=int(competitor_count_raw) if competitor_count_raw is not None else None,
                    market_notes=market_notes,
                    ai_analysis_notes=ai.get("analysis", ""),
                )
                result["territory_competitor_count"] = int(competitor_count_raw)
                st.success("OpenAI deep dive completed and included in scoring. Review the blunt read and validate any legal, financial, or contract issues with qualified advisors.")
            else:
                st.warning(ai.get("error", "OpenAI deep dive was unavailable. Manual snapshot still generated."))
                st.info("You can still copy the fallback prompt into ChatGPT and paste the response back into the app. Pasted notes affect scoring too.")
        else:
            st.success("Snapshot generated. Use OpenAI deep dive or manual paste notes for a richer scoring adjustment.")

        _store_analysis(result)

    result = st.session_state.get("brand_territory_analysis")
    if result:
        _render_snapshot(result)
    else:
        st.markdown("### What this will produce")
        a, b, c = st.columns(3)
        with a:
            info_card("Business model read", "Detects the likely category and highlights operating-model risks before the questionnaire starts.", "brand context")
        with b:
            info_card("Territory pressure", "Uses the target market, competitor count, and local notes to flag saturation and ramp concerns.", "local context")
        with c:
            info_card("Brand stability signals", "Looks for closures, market exits, and outer-market expansion risk before it reaches the final score.", "risk adjustment")
