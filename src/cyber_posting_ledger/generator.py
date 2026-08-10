"""
Application Alignment Brief Generator for Cyber Posting Ledger.
Generates tailored cover letter & CV briefs based on multi-dimensional fit analysis and recruiter advisor insights.
"""

from datetime import datetime, timezone

from cyber_posting_ledger.models import (
    ApplicationBrief,
    CandidateProfile,
    VacancyRecord,
)
from cyber_posting_ledger.scoring import classify_cybok_taxonomy, evaluate_vacancy


def generate_application_brief(
    vacancy: VacancyRecord, profile: CandidateProfile
) -> ApplicationBrief:
    """
    Generates a structured Application Alignment Brief for a candidate and vacancy.
    """
    fit_res = evaluate_vacancy(vacancy, profile)
    cybok = classify_cybok_taxonomy(vacancy)

    # Executive Summary
    summary = (
        f"The candidate ({profile.candidate_name}) evaluated with an overall status of '{fit_res.overall_status}' "
        f"for the '{vacancy.title}' position at {vacancy.organization} ({vacancy.grade_or_level}). "
        f"Formal Eligibility: {fit_res.formal_eligibility_score}/100, Substantive Fit: {fit_res.substantive_fit_score}/100, "
        f"Strategic Value: {fit_res.strategic_value_score}/100, Practical Value: {fit_res.practical_value_score}/100."
    )

    # Key Selling Points
    selling_points = [
        f"Direct alignment with {cybok.primary_category.value} ({cybok.nice_framework_role}).",
        f"Satisfies degree requirement ({profile.degree_level}) and experience requirement ({profile.total_experience_years} years vs {vacancy.eligibility.min_experience_years} years required).",
    ]

    if vacancy.requirements.nato_eu_context:
        selling_points.append(
            "Proven operational background in NATO/EU environments and multinational CIS/INFOSEC coordination."
        )

    matched_domains = [
        d
        for d in vacancy.requirements.domains
        if any(d.upper() in s.upper() for s in profile.skills_and_domains)
    ]
    if matched_domains:
        selling_points.append(f"Demonstrated technical expertise in {', '.join(matched_domains)}.")

    # Tailored Experience Bullets
    tailored_bullets = [
        f"Highlight lead responsibility in managing {cybok.primary_category.value} frameworks (e.g. NIST CSF 2.0, OWASP, ISO 27001).",
        "Emphasize experience in multi-agency/multinational coordination across EU and NATO information systems.",
        f"Reference hands-on experience with core tooling ({', '.join(vacancy.requirements.technologies or ['Python', 'Linux'])}).",
    ]

    # Gap Mitigation Advice
    gap_advice = []
    if fit_res.disqualification_reasons:
        for disq in fit_res.disqualification_reasons:
            gap_advice.append(f"CRITICAL GATE: {disq}")

    if vacancy.eligibility.security_clearance_required != "None":
        gap_advice.append(
            f"Confirm security clearance status ({vacancy.eligibility.security_clearance_required}) and state willingness to undergo vetting if required."
        )

    if not gap_advice:
        gap_advice.append(
            "No critical eligibility gaps identified. Proceed with direct CV tailoring and application submission."
        )

    return ApplicationBrief(
        vacancy_id=vacancy.id,
        vacancy_title=vacancy.title,
        organization=vacancy.organization,
        fit_status=fit_res.overall_status,
        executive_summary=summary,
        key_selling_points=selling_points,
        tailored_experience_bullets=tailored_bullets,
        gap_mitigation_advice=gap_advice,
        cybok_category=cybok.primary_category.value,
        recruiter_advice=fit_res.recruiter_advice,
        generated_at=datetime.now(timezone.utc),
    )


def format_brief_markdown(brief: ApplicationBrief) -> str:
    """Formats an ApplicationBrief into a clean Markdown document (Zero Emojis)."""
    lines = [
        f"# Application Alignment Brief: {brief.vacancy_title}",
        f"**Organization:** {brief.organization}  |  **Vacancy ID:** `{brief.vacancy_id}`",
        f"**Overall Fit Status:** `{brief.fit_status}`  |  **CyBOK Category:** `{brief.cybok_category}`",
        f"*Generated on {brief.generated_at.strftime('%Y-%m-%d %H:%M:%S')}*",
        "",
        "---",
        "",
        "## Executive Summary",
        brief.executive_summary,
        "",
        "## Key Selling Points for Motivation / Cover Letter",
        "\n".join([f"- **Point {i + 1}:** {pt}" for i, pt in enumerate(brief.key_selling_points)]),
        "",
        "## Tailored Experience Bullets for CV",
        "\n".join([f"- {bullet}" for bullet in brief.tailored_experience_bullets]),
        "",
        "## Gap Mitigation & Actionable Advice",
        "\n".join([f"- {adv}" for adv in brief.gap_mitigation_advice]),
        "",
    ]

    if brief.recruiter_advice:
        rec = brief.recruiter_advice
        lines.extend(
            [
                "## Recruiter Intelligence & Career Path Roadmap",
                f"**Domain Focus:** {rec.certification_roadmap.domain_category}  |  **Potential Max Score:** `{rec.potential_max_score}/100`",
                "",
                "### Must-Have & Recommended Certifications",
                "\n".join(
                    [
                        f"- {'[HELD]' if c.held else '[TARGET]'} **{c.name} ({c.code})** - *{c.priority}*"
                        for c in rec.certification_roadmap.target_certifications
                    ]
                ),
                "",
                "### Recruiter Metric Quantify Templates",
                "\n".join(
                    [
                        f'- **{m.category}:** *"{m.template_bullet}"*  \n  *(Guidance: {m.guidance})*'
                        for m in rec.quantifiable_impact_templates
                    ]
                ),
                "",
                "### Score Booster Roadmap",
                "\n".join(
                    [
                        f"{step.step_number}. **{step.title} (+{step.score_delta} pts):** {step.action_item}"
                        for step in rec.score_booster_steps
                    ]
                ),
                "",
            ]
        )

    lines.extend(
        [
            "---",
            "*Cyber Posting Ledger &bull; Confidential Personal Career Intelligence*",
        ]
    )
    return "\n".join(lines)
