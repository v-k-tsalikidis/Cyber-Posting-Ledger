"""
Recruiter Intelligence & Career Path Upgrade Advisory Engine.
Provides recruiter-aligned certification roadmaps, quantifiable achievement templates, and score booster steps.
"""

from cyber_posting_ledger.models import (
    CandidateProfile,
    CertificationItem,
    CertificationRoadmap,
    CyBOKCategory,
    RecruiterAdvice,
    RecruiterImpactMetric,
    ScoreBoosterStep,
    VacancyRecord,
)

CERT_DATABASE = {
    CyBOKCategory.GOVERNANCE_RISK: [
        CertificationItem(
            name="Certified Information Systems Security Professional",
            code="CISSP",
            priority="Must-Have",
        ),
        CertificationItem(
            name="Certified Information Systems Auditor",
            code="CISA",
            priority="Recommended",
        ),
        CertificationItem(
            name="Certified Information Security Manager",
            code="CISM",
            priority="Recommended",
        ),
        CertificationItem(
            name="ISO/IEC 27001 Lead Auditor", code="ISO 27001 LA", priority="Must-Have"
        ),
    ],
    CyBOKCategory.SECURITY_OPERATIONS: [
        CertificationItem(name="GIAC Cyber Threat Intelligence", code="GCTI", priority="Must-Have"),
        CertificationItem(
            name="GIAC Certified Incident Handler", code="GCIH", priority="Recommended"
        ),
        CertificationItem(
            name="CompTIA Cybersecurity Analyst", code="CySA+", priority="Recommended"
        ),
        CertificationItem(
            name="Offensive Security Certified Professional",
            code="OSCP",
            priority="Optional",
        ),
    ],
    CyBOKCategory.NETWORK_INFRASTRUCTURE: [
        CertificationItem(
            name="Certified Information Systems Security Professional",
            code="CISSP",
            priority="Must-Have",
        ),
        CertificationItem(name="CompTIA Security+", code="Security+", priority="Must-Have"),
        CertificationItem(
            name="CCNP Security / Cisco CyberOps",
            code="CCNP Security",
            priority="Recommended",
        ),
        CertificationItem(
            name="NATO Information Assurance Specialist",
            code="NATO IA",
            priority="Recommended",
        ),
    ],
    CyBOKCategory.SOFTWARE_SECURITY: [
        CertificationItem(
            name="Certified Secure Software Lifecycle Professional",
            code="CSSLP",
            priority="Must-Have",
        ),
        CertificationItem(
            name="Certified DevSecOps Professional", code="CDP", priority="Recommended"
        ),
        CertificationItem(
            name="GIAC Web Application Penetration Tester",
            code="GWAPT",
            priority="Recommended",
        ),
    ],
    CyBOKCategory.HUMAN_ORGANIZATIONAL: [
        CertificationItem(
            name="Certified Information Privacy Professional/Europe",
            code="CIPP/E",
            priority="Must-Have",
        ),
        CertificationItem(
            name="Certified Information Security Manager",
            code="CISM",
            priority="Recommended",
        ),
    ],
}


def generate_recruiter_advice(vacancy: VacancyRecord, profile: CandidateProfile) -> RecruiterAdvice:
    """Generates recruiter-aligned certification roadmap, impact metrics, and score booster steps."""
    from cyber_posting_ledger.scoring import classify_cybok_taxonomy

    cybok = classify_cybok_taxonomy(vacancy)
    cat = cybok.primary_category

    # Get target certs
    raw_certs = CERT_DATABASE.get(cat, CERT_DATABASE[CyBOKCategory.GOVERNANCE_RISK])
    target_certs = []

    held_lower = [c.lower() for c in (profile.certifications_held or [])]
    for c in raw_certs:
        is_held = any(c.code.lower() in h or c.name.lower() in h for h in held_lower)
        target_certs.append(
            CertificationItem(
                name=c.name,
                code=c.code,
                held=is_held,
                priority=c.priority,
            )
        )

    cert_roadmap = CertificationRoadmap(
        domain_category=cat.value,
        target_certifications=target_certs,
    )

    # Quantifiable Impact Metrics for Recruiters
    impact_metrics = [
        RecruiterImpactMetric(
            category="Scale & Environment Scope",
            template_bullet="Managed security controls and risk assessments across an operational footprint of 500+ endpoints and 50GB/day log ingestion in a multi-agency EU/NATO context.",
            guidance="Cyber recruiters filter for scale (e.g. log volume, endpoint count, user base). Quantify your exact environment scope.",
        ),
        RecruiterImpactMetric(
            category="MTTR & Risk Reduction",
            template_bullet="Reduced Mean-Time-To-Respond (MTTR) by 35% through standardized incident response playbooks and automated threat intelligence triage.",
            guidance="Highlight percentage reductions in response times or vulnerability remediation SLAs.",
        ),
        RecruiterImpactMetric(
            category="Compliance & Audit Success",
            template_bullet="Successfully conducted internal compliance audits against NIST CSF 2.0 and ISO 27001, closing 100% of high-risk audit findings within 30 days.",
            guidance="Show proof of closed audit findings and compliance framework adherence.",
        ),
    ]

    # Score Booster Roadmap
    current_substantive = 80  # Default baseline
    steps = [
        ScoreBoosterStep(
            step_number=1,
            title="Recruiter Keyword & Metric Quantify",
            score_delta=10,
            action_item="Format CV experience bullets with explicit scale metrics (log volume, MTTR %, endpoint count) and tool names (Splunk, Wireshark, Python).",
        ),
        ScoreBoosterStep(
            step_number=2,
            title=f"Certification Gain ({target_certs[0].code})",
            score_delta=10,
            action_item=f"Obtain target certification '{target_certs[0].name} ({target_certs[0].code})' to satisfy hard recruiter filters.",
        ),
        ScoreBoosterStep(
            step_number=3,
            title="Lab & Portfolio Evidence",
            score_delta=10,
            action_item="Link public GitHub portfolio or CTF write-ups demonstrating hands-on tool proficiencies (Python automation, CyBOK mapping).",
        ),
    ]

    potential_max = min(100, current_substantive + 20)

    return RecruiterAdvice(
        certification_roadmap=cert_roadmap,
        quantifiable_impact_templates=impact_metrics,
        score_booster_steps=steps,
        potential_max_score=potential_max,
    )
