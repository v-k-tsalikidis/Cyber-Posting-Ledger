"""
Unit tests for CyBOK mapping, PPP calculations, and Application Brief generation.
"""

from cyber_vacancy_tracker.models import (
    VacancyRecord,
    EligibilityCriteria,
    SubstantiveRequirements,
    StrategicMetrics,
    PracticalMetrics,
    ProvenanceMetadata,
    CandidateProfile,
    CyBOKCategory,
)
from cyber_vacancy_tracker.scoring import classify_cybok_taxonomy, calculate_purchasing_power
from cyber_vacancy_tracker.generator import generate_application_brief, format_brief_markdown


def test_classify_cybok_taxonomy_gov():
    vac = VacancyRecord(
        id="VAC-TEST-CYB1",
        title="GRC Audit Lead",
        organization="ENISA",
        requirements=SubstantiveRequirements(domains=["GRC"], frameworks=["NIST CSF"]),
        provenance=ProvenanceMetadata(source_url="https://example.com"),
    )
    cybok = classify_cybok_taxonomy(vac)
    assert cybok.primary_category == CyBOKCategory.GOVERNANCE_RISK


def test_classify_cybok_taxonomy_ops():
    vac = VacancyRecord(
        id="VAC-TEST-CYB2",
        title="CTI Threat Hunter",
        organization="CERT-EU",
        requirements=SubstantiveRequirements(domains=["CTI", "SOC"], frameworks=["MITRE ATT&CK"]),
        provenance=ProvenanceMetadata(source_url="https://example.com"),
    )
    cybok = classify_cybok_taxonomy(vac)
    assert cybok.primary_category == CyBOKCategory.SECURITY_OPERATIONS


def test_calculate_purchasing_power_athens():
    ppp = calculate_purchasing_power("Athens, Greece", 5000.0)
    assert ppp.ppp_multiplier == 1.25
    assert ppp.ppp_adjusted_net_eur == 6250.0


def test_generate_application_brief():
    profile = CandidateProfile()
    vac = VacancyRecord(
        id="VAC-TEST-BRIEF",
        title="ICT Security Coordinator",
        organization="ENISA",
        eligibility=EligibilityCriteria(min_experience_years=5),
        requirements=SubstantiveRequirements(domains=["INFOSEC", "CIS"]),
        practical=PracticalMetrics(location="Athens, Greece", estimated_monthly_net_eur=5800.0),
        provenance=ProvenanceMetadata(source_url="https://example.com"),
    )

    brief = generate_application_brief(vac, profile)
    assert brief.vacancy_id == "VAC-TEST-BRIEF"
    assert brief.fit_status == "Eligible"
    assert len(brief.key_selling_points) >= 2

    md = format_brief_markdown(brief)
    assert "# Application Alignment Brief" in md
    assert "ENISA" in md
