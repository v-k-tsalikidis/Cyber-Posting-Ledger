"""
Multi-dimensional evaluation engine, CyBOK taxonomy classifier, and PPP calculator for Cyber Vacancy Intelligence Tracker.
"""

from aegis_ledger.models import (
    CandidateProfile,
    CyBOKCategory,
    CyBOKMapping,
    FitScoreResult,
    OrgTier,
    PurchasingPowerMetrics,
    VacancyRecord,
)
from aegis_ledger.recruiter_advisor import generate_recruiter_advice

# Cost of Living Purchasing Power Index relative to Brussels (Base 1.0)
CITY_PPP_INDEX = {
    "athens": 1.25,  # Lower cost of living -> Higher purchasing power multiplier
    "greece": 1.25,
    "brussels": 1.00,  # Base
    "belgium": 1.00,
    "the hague": 0.90,  # Netherlands
    "netherlands": 0.90,
    "luxembourg": 0.85,  # Higher cost of living
    "munich": 0.88,  # Germany
    "germany": 0.92,
}


def calculate_purchasing_power(location: str, raw_salary: float | None) -> PurchasingPowerMetrics:
    """Calculates Purchasing Power Parity (PPP) equivalent net salary."""
    loc_lower = location.lower()
    mult = 1.0
    for key, val in CITY_PPP_INDEX.items():
        if key in loc_lower:
            mult = val
            break

    ppp_adjusted = (raw_salary * mult) if raw_salary is not None else None
    return PurchasingPowerMetrics(
        raw_salary_net_eur=raw_salary,
        location=location,
        ppp_multiplier=mult,
        ppp_adjusted_net_eur=ppp_adjusted,
    )


def classify_cybok_taxonomy(vacancy: VacancyRecord) -> CyBOKMapping:
    """
    Classifies vacancy requirements into CyBOK v1.1 Knowledge Areas and NICE Framework roles.
    """
    domains = [d.upper() for d in vacancy.requirements.domains]
    frameworks = [f.upper() for f in vacancy.requirements.frameworks]
    tech = [t.upper() for t in vacancy.requirements.technologies]

    all_tokens = domains + frameworks + tech

    if any(k in all_tokens for k in ["GRC", "NIST CSF", "ISO 27001", "GOVERNANCE", "RISK"]):
        primary = CyBOKCategory.GOVERNANCE_RISK
        nice_role = "Security Control Assessor / GRC Specialist"
        ka = ["Risk Management & Governance", "Security Culture & Hygiene"]
    elif any(
        k in all_tokens for k in ["CTI", "SOC", "INCIDENT RESPONSE", "THREAT HUNTING", "MISP"]
    ):
        primary = CyBOKCategory.SECURITY_OPERATIONS
        nice_role = "Cyber Defense Analyst / CTI Specialist"
        ka = [
            "Security Operations & Incident Management",
            "Malware & Attack Technologies",
        ]
    elif any(k in all_tokens for k in ["CIS", "COMSEC", "NETWORKS", "CRYPTO", "NATO CIS"]):
        primary = CyBOKCategory.NETWORK_INFRASTRUCTURE
        nice_role = "Information Systems Security Officer (ISSO) / Network Security Engineer"
        ka = ["Network Security", "Cryptography & Key Management"]
    elif any(k in all_tokens for k in ["DEVSECOPS", "SOFTWARE", "PYTHON", "KUBERNETES", "CODE"]):
        primary = CyBOKCategory.SOFTWARE_SECURITY
        nice_role = "Secure Software / Application Security Engineer"
        ka = ["Software Security", "Web & Mobile Security"]
    else:
        primary = CyBOKCategory.HUMAN_ORGANIZATIONAL
        nice_role = "Information Security Specialist"
        ka = ["Human, Organizational & Regulatory Aspects"]

    return CyBOKMapping(
        primary_category=primary,
        matched_knowledge_areas=ka,
        nice_framework_role=nice_role,
    )


def evaluate_formal_eligibility(
    profile: CandidateProfile, vacancy: VacancyRecord
) -> tuple[int, list[str], list[str]]:
    """
    Evaluates hard formal eligibility gates: nationality, degree, experience, clearance, languages.
    Returns (score, disqualification_reasons, observations).
    """
    score = 100
    disqualifications = []
    observations = []

    # 1. Nationality Gate
    allowed_nats = [n.upper() for n in vacancy.eligibility.allowed_nationalities]
    candidate_nats = [n.upper() for n in profile.nationalities]

    nat_match = any(
        c_nat in allowed_nats
        or ("EU" in allowed_nats and "GREEK" in candidate_nats)
        or ("NATO" in allowed_nats and "GREEK" in candidate_nats)
        for c_nat in candidate_nats
    )
    if not nat_match:
        disqualifications.append(
            f"Nationality mismatch: Allowed {vacancy.eligibility.allowed_nationalities}, Candidate holds {profile.nationalities}"
        )
        score -= 60

    # 2. Degree Level Gate
    degree_hierarchy = {"BSc": 1, "Bachelor": 1, "MSc": 2, "Master": 2, "PhD": 3}
    req_degree_val = degree_hierarchy.get(vacancy.eligibility.min_degree_level, 2)
    cand_degree_val = degree_hierarchy.get(profile.degree_level, 2)

    if cand_degree_val < req_degree_val:
        disqualifications.append(
            f"Degree level shortfall: Required {vacancy.eligibility.min_degree_level}, Candidate has {profile.degree_level}"
        )
        score -= 40
    else:
        observations.append(
            f"Degree requirement met ({profile.degree_level} >= {vacancy.eligibility.min_degree_level})"
        )

    # 3. Years of Experience
    diff_years = profile.total_experience_years - vacancy.eligibility.min_experience_years
    if diff_years < 0:
        penalty = abs(diff_years) * 20
        score -= penalty
        disqualifications.append(
            f"Experience shortfall: Required {vacancy.eligibility.min_experience_years} years, Candidate has {profile.total_experience_years}"
        )
    else:
        observations.append(
            f"Sufficient experience ({profile.total_experience_years} yrs vs {vacancy.eligibility.min_experience_years} yrs required)"
        )

    # 4. Required Languages
    for req_lang in vacancy.eligibility.required_languages:
        if not any(req_lang.lower() in p_lang.lower() for p_lang in profile.languages_proficient):
            score -= 20
            observations.append(f"Missing required language: {req_lang}")

    final_score = max(0, min(100, score))
    return final_score, disqualifications, observations


def evaluate_substantive_fit(
    profile: CandidateProfile, vacancy: VacancyRecord
) -> tuple[int, list[str]]:
    """
    Evaluates technical and domain alignment (CIS, INFOSEC, COMSEC, CTI/SOC, GRC, NATO/EU context).
    Returns (score, observations).
    """
    score = 50  # Baseline
    observations = []

    req_domains = vacancy.requirements.domains
    cand_skills = [s.upper() for s in profile.skills_and_domains]

    if req_domains:
        matched = [d for d in req_domains if any(d.upper() in s for s in cand_skills)]
        match_ratio = len(matched) / len(req_domains)
        domain_pts = int(match_ratio * 30)
        score += domain_pts
        observations.append(
            f"Matched {len(matched)}/{len(req_domains)} required domains: {matched}"
        )
    else:
        score += 20

    # Framework & Tech alignment
    matched_frameworks = [
        f for f in vacancy.requirements.frameworks if any(f.upper() in s for s in cand_skills)
    ]
    if matched_frameworks:
        score += min(15, len(matched_frameworks) * 5)
        observations.append(f"Framework overlap: {matched_frameworks}")

    # NATO/EU context bonus
    if vacancy.requirements.nato_eu_context:
        if any(term in cand_skills for term in ["NATO", "EU"]):
            score += 15
            observations.append(
                "NATO/EU operational context requirement matched candidate background (+15 pts)"
            )
        else:
            observations.append(
                "NATO/EU operational context requested but missing in candidate profile"
            )

    final_score = max(0, min(100, score))
    return final_score, observations


def evaluate_strategic_value(vacancy: VacancyRecord) -> tuple[int, list[str]]:
    """
    Assesses organization tier, brand leverage, and long-term ecosystem value.
    Returns (score, observations).
    """
    observations = []
    tier_base = {OrgTier.TIER_1: 85, OrgTier.TIER_2: 70, OrgTier.TIER_3: 50}

    score = tier_base.get(vacancy.strategic.org_tier, 60)
    observations.append(f"Organization Tier {vacancy.strategic.org_tier.value} base score: {score}")

    # Brand and stepping stone weight
    bonus = int((vacancy.strategic.brand_value_score + vacancy.strategic.stepping_stone_score) / 20)
    score += bonus

    if vacancy.strategic.ecosystem_alignment:
        score += 10
        observations.append("Direct EU/NATO ecosystem alignment bonus (+10 pts)")

    final_score = max(0, min(100, score))
    return final_score, observations


def evaluate_practical_value(vacancy: VacancyRecord) -> tuple[int, list[str]]:
    """
    Evaluates salary adequacy, location preference, purchasing power, and contract stability.
    Returns (score, observations).
    """
    score = 60
    observations = []

    ppp_metrics = calculate_purchasing_power(
        vacancy.practical.location, vacancy.practical.estimated_monthly_net_eur
    )
    vacancy.practical.purchasing_power = ppp_metrics

    salary = vacancy.practical.estimated_monthly_net_eur
    if salary is not None:
        if salary >= 5000:
            score += 30
            observations.append(f"High net compensation tier: €{salary:.0f}/month (+30 pts)")
        elif salary >= 4000:
            score += 20
            observations.append(f"Competitive compensation tier: €{salary:.0f}/month (+20 pts)")
        elif salary >= 3000:
            score += 10
            observations.append(f"Standard compensation tier: €{salary:.0f}/month (+10 pts)")
        else:
            score -= 10
            observations.append(f"Lower compensation tier: €{salary:.0f}/month (-10 pts)")

    if ppp_metrics.ppp_adjusted_net_eur is not None:
        observations.append(
            f"Purchasing Power Adjusted Salary (vs Brussels 1.0): €{ppp_metrics.ppp_adjusted_net_eur:.0f}/month (Multiplier {ppp_metrics.ppp_multiplier}x)"
        )

    # Location preference
    pref_locations = ["athens", "brussels", "luxembourg", "the hague", "munich"]
    if any(p in vacancy.practical.location.lower() for p in pref_locations):
        score += 10
        observations.append(f"Preferred location match: {vacancy.practical.location}")

    final_score = max(0, min(100, score))
    return final_score, observations


def evaluate_vacancy(
    vacancy: VacancyRecord, profile: CandidateProfile | None = None
) -> FitScoreResult:
    """
    Runs full multi-dimensional evaluation of a vacancy against candidate profile.
    """
    if profile is None:
        profile = CandidateProfile()

    elig_score, disqualifications, elig_obs = evaluate_formal_eligibility(profile, vacancy)
    subst_score, subst_obs = evaluate_substantive_fit(profile, vacancy)
    strat_score, strat_obs = evaluate_strategic_value(vacancy)
    pract_score, pract_obs = evaluate_practical_value(vacancy)
    cybok_map = classify_cybok_taxonomy(vacancy)

    rec_advice = generate_recruiter_advice(vacancy, profile)

    all_obs = elig_obs + subst_obs + strat_obs + pract_obs

    if disqualifications or elig_score < 50:
        overall_status = "Disqualified"
    elif elig_score < 75:
        overall_status = "Conditional"
    else:
        overall_status = "Eligible"

    return FitScoreResult(
        formal_eligibility_score=elig_score,
        substantive_fit_score=subst_score,
        strategic_value_score=strat_score,
        practical_value_score=pract_score,
        overall_status=overall_status,
        disqualification_reasons=disqualifications,
        observations=all_obs,
        cybok_mapping=cybok_map,
        recruiter_advice=rec_advice,
    )
