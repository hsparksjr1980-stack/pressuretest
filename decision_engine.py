from __future__ import annotations

import streamlit as st


DECISION_BUCKETS = {
<<<<<<< HEAD
    "proceed": "Proceed — evidence supports moving forward",
    "proceed_conditions": "Proceed only with conditions",
    "do_not_proceed": "Do not proceed — pressure test failed",
=======
    "proceed": "Proceed",
    "proceed_conditions": "Proceed with Conditions",
    "do_not_proceed": "Do Not Proceed",
>>>>>>> fec65288cb896b4679e84e61241f185fa625e150
}


DEFAULT_WEIGHTS = {
    "readiness": 0.20,
    "concept": 0.20,
    "financial": 0.25,
    "post_discovery": 0.25,
    "pressure_test": 0.10,
}


_PHASE_SCORE_KEYS = {
    "readiness": ["readiness_score", "phase_0_score"],
    "concept": ["concept_score", "concept_validation_score", "phase_1_score"],
    "financial": ["financial_score"],
    "post_discovery": ["post_discovery_score", "phase_2_score"],
    "pressure_test": ["pressure_test_score"],
}


def clamp_score(value: float, min_value: float = 0.0, max_value: float = 100.0) -> float:
    return max(min_value, min(max_value, value))


def normalize_yes_no(value) -> bool | None:
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        value = value.strip().lower()
        if value in {"yes", "y", "true"}:
            return True
        if value in {"no", "n", "false"}:
            return False
    return None


def _first_state_value(*keys: str):
    for key in keys:
        value = st.session_state.get(key)
        if value is not None:
            return value
    return None


def get_phase_scores() -> dict:
    return {phase: _first_state_value(*keys) for phase, keys in _PHASE_SCORE_KEYS.items()}


def calculate_weighted_score(phase_scores: dict, weights: dict | None = None) -> float:
    weights = weights or DEFAULT_WEIGHTS
    weighted_total = 0.0
    used_weight = 0.0

    for key, weight in weights.items():
        score = phase_scores.get(key)
        if score is None:
            continue
        weighted_total += float(score) * weight
        used_weight += weight

    if used_weight == 0:
        return 0.0

    return round(clamp_score(weighted_total / used_weight), 1)


def evaluate_guardrails() -> dict:
    guardrails = st.session_state.get("required_guardrails", {}) or {}
    results = {}
    passed = failed = unknown = 0

    for name, payload in guardrails.items():
        target = payload.get("target")
        actual = payload.get("actual")
        operator = payload.get("operator", "<=")

        status = "unknown"
        if target is not None and actual is not None:
            if operator == "<=":
                status = "pass" if actual <= target else "fail"
            elif operator == ">=":
                status = "pass" if actual >= target else "fail"
            elif operator == "==":
                status = "pass" if actual == target else "fail"

        if status == "pass":
            passed += 1
        elif status == "fail":
            failed += 1
        else:
            unknown += 1

        results[name] = {
            "target": target,
            "actual": actual,
            "operator": operator,
            "status": status,
        }

    return {
        "details": results,
        "passed": passed,
        "failed": failed,
        "unknown": unknown,
        "total": len(results),
    }


def get_hard_stop_flags() -> dict:
    flags = {
        "insufficient_liquidity": normalize_yes_no(st.session_state.get("flag_insufficient_liquidity")),
        "unsupported_personal_guarantee_risk": normalize_yes_no(st.session_state.get("flag_personal_guarantee_risk")),
        "buildout_too_high": normalize_yes_no(st.session_state.get("flag_buildout_too_high")),
        "rent_too_high": normalize_yes_no(st.session_state.get("flag_rent_too_high")),
        "no_margin_for_error": normalize_yes_no(st.session_state.get("flag_no_margin_for_error")),
        "unverified_item_19_or_unit_economics": normalize_yes_no(st.session_state.get("flag_unverified_unit_economics")),
        "major_unknowns_remaining": normalize_yes_no(st.session_state.get("flag_major_unknowns_remaining")),
    }
    active_flags = [key for key, value in flags.items() if value is True]
    return {"all_flags": flags, "active_flags": active_flags, "active_count": len(active_flags)}


def classify_decision(weighted_score: float, guardrail_eval: dict, hard_stop_eval: dict) -> str:
    failed_guardrails = guardrail_eval["failed"]
    active_hard_stops = hard_stop_eval["active_count"]

    if active_hard_stops >= 3:
        return DECISION_BUCKETS["do_not_proceed"]
    if failed_guardrails >= 2 and weighted_score < 65:
        return DECISION_BUCKETS["do_not_proceed"]
    if weighted_score >= 80 and failed_guardrails == 0 and active_hard_stops <= 1:
        return DECISION_BUCKETS["proceed"]
    if weighted_score < 55:
        return DECISION_BUCKETS["do_not_proceed"]
    return DECISION_BUCKETS["proceed_conditions"]


def _pretty(text: str) -> str:
    return text.replace("_", " ").title()


def summarize_key_risks(guardrail_eval: dict, hard_stop_eval: dict, phase_scores: dict) -> list[str]:
    risks: list[str] = []
    for flag in hard_stop_eval["active_flags"]:
        risks.append(_pretty(flag))
    for name, payload in guardrail_eval["details"].items():
        if payload["status"] == "fail":
            risks.append(f"Failed guardrail: {_pretty(name)}")
    for phase, score in phase_scores.items():
        if score is not None and score < 60:
            risks.append(f"Weak score in {_pretty(phase)}")
    return list(dict.fromkeys(risks))[:10]


def build_conditions_list(guardrail_eval: dict, hard_stop_eval: dict, phase_scores: dict) -> list[str]:
    items: list[str] = []
    for name, payload in guardrail_eval["details"].items():
        if payload["status"] == "fail":
            items.append(f"Resolve failed guardrail: {_pretty(name)}")
    for flag in hard_stop_eval["active_flags"]:
        items.append(f"Address major risk: {_pretty(flag)}")
    for phase, score in phase_scores.items():
        if score is not None and score < 70:
            items.append(f"Strengthen weak area: {_pretty(phase)}")
    return list(dict.fromkeys(items))[:10]


def build_strengths_list(phase_scores: dict, recommendation: str, guardrail_eval: dict, hard_stop_eval: dict) -> list[str]:
    strengths: list[str] = []
    if recommendation == DECISION_BUCKETS["proceed"]:
        strengths.append("The overall profile is supporting a cleaner path forward.")
    elif recommendation == DECISION_BUCKETS["proceed_conditions"]:
        strengths.append("The deal still appears alive, but only with explicit conditions.")

    for phase, score in phase_scores.items():
        if score is not None and score >= 75:
            strengths.append(f"{_pretty(phase)} is showing comparatively stronger results.")

    if guardrail_eval["total"] and guardrail_eval["failed"] == 0:
        strengths.append("No entered guardrails are currently failing.")
    if hard_stop_eval["active_count"] == 0:
        strengths.append("No hard-stop flags are currently active.")

    return list(dict.fromkeys(strengths))[:8]


def build_unresolved_risks(phase_scores: dict, guardrail_eval: dict, hard_stop_eval: dict) -> list[str]:
    unresolved = summarize_key_risks(guardrail_eval, hard_stop_eval, phase_scores)
    if not unresolved:
        low_count = len([score for score in phase_scores.values() if score is not None and score < 70])
        if low_count:
            unresolved.append("Some phase scores are still too soft for a fully confident commitment.")
        else:
            unresolved.append("No major unresolved risks are currently flagged from the stored data.")
    return unresolved[:6]


<<<<<<< HEAD

def get_brand_intelligence_adjustment() -> dict:
    analysis = st.session_state.get("brand_territory_analysis", {}) or {}
    intel = analysis.get("brand_intelligence", {}) or {}
    adjustment = float(intel.get("risk_adjustment", st.session_state.get("brand_intelligence_adjustment", 0)) or 0)
    level = intel.get("brand_risk_level", st.session_state.get("brand_intelligence_level", "Low / Unknown"))
    signals = intel.get("signals", st.session_state.get("brand_intelligence_signals", [])) or []
    note = intel.get("scoring_note", "Brand/territory intelligence has not been generated yet.")
    return {
        "adjustment": adjustment,
        "level": level,
        "signals": signals,
        "note": note,
    }


def build_decision_packet() -> dict:
    phase_scores = get_phase_scores()
    weighted_score = calculate_weighted_score(phase_scores)
    brand_intel_eval = get_brand_intelligence_adjustment()
    adjusted_score = round(clamp_score(weighted_score + brand_intel_eval["adjustment"]), 1)
    guardrail_eval = evaluate_guardrails()
    hard_stop_eval = get_hard_stop_flags()
    recommendation = classify_decision(adjusted_score, guardrail_eval, hard_stop_eval)
    conditions = build_conditions_list(guardrail_eval, hard_stop_eval, phase_scores)
    key_risks = summarize_key_risks(guardrail_eval, hard_stop_eval, phase_scores)
    if brand_intel_eval["adjustment"] < 0:
        key_risks.append(f"Brand/territory intelligence adjustment: {int(brand_intel_eval['adjustment'])} points ({brand_intel_eval['level']})")
        key_risks.extend(brand_intel_eval.get("signals", [])[:3])
=======
def build_decision_packet() -> dict:
    phase_scores = get_phase_scores()
    weighted_score = calculate_weighted_score(phase_scores)
    guardrail_eval = evaluate_guardrails()
    hard_stop_eval = get_hard_stop_flags()
    recommendation = classify_decision(weighted_score, guardrail_eval, hard_stop_eval)
    conditions = build_conditions_list(guardrail_eval, hard_stop_eval, phase_scores)
    key_risks = summarize_key_risks(guardrail_eval, hard_stop_eval, phase_scores)
>>>>>>> fec65288cb896b4679e84e61241f185fa625e150
    strengths = build_strengths_list(phase_scores, recommendation, guardrail_eval, hard_stop_eval)
    unresolved = build_unresolved_risks(phase_scores, guardrail_eval, hard_stop_eval)

    populated_scores = [v for v in phase_scores.values() if v is not None]
    confidence = "Low"
    if len(populated_scores) >= 3:
        confidence = "Medium"
    if len(populated_scores) == 5 and guardrail_eval["unknown"] == 0:
        confidence = "High"

    if recommendation == DECISION_BUCKETS["proceed"]:
<<<<<<< HEAD
        summary = "The current information clears the basic pressure test. Do not treat that as a green light to sign blindly; keep advisor review and deal conditions explicit."
    elif recommendation == DECISION_BUCKETS["do_not_proceed"]:
        summary = "The current information is flashing a stop signal. The cleaner answer is to walk away unless the weak points materially change."
    else:
        summary = "This is not a clean yes. The deal only stays alive if the biggest weak areas are fixed, verified, or renegotiated."

    if brand_intel_eval["adjustment"] < 0:
        summary += f" Brand/territory intelligence adjusted the score by {int(brand_intel_eval['adjustment'])} points due to {brand_intel_eval['level'].lower()} risk signals."

    packet = {
        "weighted_score": weighted_score,
        "base_score": weighted_score,
        "brand_intelligence_adjustment": brand_intel_eval["adjustment"],
        "brand_intelligence_level": brand_intel_eval["level"],
        "brand_intelligence_signals": brand_intel_eval.get("signals", []),
        "brand_intelligence_note": brand_intel_eval.get("note", ""),
        "final_score": adjusted_score,
=======
        summary = "The current information is supportive enough to move forward, but only if you keep conditions explicit."
    elif recommendation == DECISION_BUCKETS["do_not_proceed"]:
        summary = "The current information is pointing to a stop signal rather than a pause."
    else:
        summary = "The deal may still work, but only after the biggest weak areas are tightened."

    packet = {
        "weighted_score": weighted_score,
        "final_score": weighted_score,
>>>>>>> fec65288cb896b4679e84e61241f185fa625e150
        "recommendation": recommendation,
        "master_verdict": recommendation,
        "confidence": confidence,
        "phase_scores": phase_scores,
        "guardrails": guardrail_eval,
        "hard_stops": hard_stop_eval,
        "conditions": conditions,
        "key_risks": key_risks,
        "risks": unresolved,
        "strengths": strengths,
        "standouts": strengths,
        "summary": summary,
    }

    st.session_state["decision_packet"] = packet
    return packet
