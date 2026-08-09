"""
CV & Cover Letter Text Coverage Analyzer for Cyber Vacancy Intelligence Tracker.
Performs semantic keyword matching against candidate CV text to report skill coverage and missing terms.
"""

from aegis_ledger.models import CVCoverageResult, VacancyRecord


def analyze_cv_coverage(cv_text: str, vacancy: VacancyRecord) -> CVCoverageResult:
    """
    Analyzes raw CV or Cover Letter text against vacancy requirements.
    Returns CVCoverageResult with coverage %, matched skills, and missing keywords to add.
    """
    cv_lower = cv_text.lower()

    # Collect target keywords from vacancy
    target_keywords = []
    target_keywords.extend(vacancy.requirements.domains or [])
    target_keywords.extend(vacancy.requirements.frameworks or [])
    target_keywords.extend(vacancy.requirements.technologies or [])

    if vacancy.eligibility.min_degree_level:
        target_keywords.append(vacancy.eligibility.min_degree_level)

    if (
        vacancy.eligibility.security_clearance_required
        and vacancy.eligibility.security_clearance_required != "None"
    ):
        target_keywords.append(vacancy.eligibility.security_clearance_required)

    # Deduplicate preserving order
    dedup_keywords = []
    for kw in target_keywords:
        if kw and kw not in dedup_keywords:
            dedup_keywords.append(kw)

    if not dedup_keywords:
        return CVCoverageResult(
            coverage_percentage=100,
            total_required_keywords=0,
            matched_keywords=[],
            missing_keywords=[],
            recommendations=["Vacancy has no explicit technical keywords specified."],
        )

    matched = []
    missing = []

    for kw in dedup_keywords:
        kw_clean = kw.strip().lower()
        if kw_clean in cv_lower:
            matched.append(kw)
        else:
            missing.append(kw)

    coverage_pct = int((len(matched) / len(dedup_keywords)) * 100)

    recommendations = []
    if missing:
        recommendations.append(
            f"Add explicit mentions of missing target keywords: {', '.join(missing)} in your CV Experience section."
        )
    else:
        recommendations.append(
            "Excellent text alignment! All target vacancy keywords are present in your CV text."
        )

    return CVCoverageResult(
        coverage_percentage=coverage_pct,
        total_required_keywords=len(dedup_keywords),
        matched_keywords=matched,
        missing_keywords=missing,
        recommendations=recommendations,
    )
