"""
Unit tests for Recruiter Advisor Engine.
"""

from aegis_ledger.models import (
    CandidateProfile,
    ProvenanceMetadata,
    SubstantiveRequirements,
    VacancyRecord,
)
from aegis_ledger.recruiter_advisor import generate_recruiter_advice


def test_generate_recruiter_advice_grc():
    vac = VacancyRecord(
        id="VAC-REC-1",
        title="GRC Specialist",
        organization="ENISA",
        requirements=SubstantiveRequirements(domains=["GRC", "NIST CSF"], frameworks=["ISO 27001"]),
        provenance=ProvenanceMetadata(source_url="https://example.com"),
    )
    profile = CandidateProfile(certifications_held=["CISSP"])

    advice = generate_recruiter_advice(vac, profile)
    assert advice.certification_roadmap.domain_category == "Risk Management & Governance"
    assert len(advice.certification_roadmap.target_certifications) > 0
    assert any(
        c.code == "CISSP" and c.held for c in advice.certification_roadmap.target_certifications
    )
    assert len(advice.quantifiable_impact_templates) > 0
    assert len(advice.score_booster_steps) == 3
    assert advice.potential_max_score <= 100


def test_generate_recruiter_advice_cti():
    vac = VacancyRecord(
        id="VAC-REC-2",
        title="Threat Analyst",
        organization="CERT-EU",
        requirements=SubstantiveRequirements(domains=["CTI", "SOC"], frameworks=["MITRE ATT&CK"]),
        provenance=ProvenanceMetadata(source_url="https://example.com"),
    )
    profile = CandidateProfile(certifications_held=[])

    advice = generate_recruiter_advice(vac, profile)
    assert (
        advice.certification_roadmap.domain_category == "Security Operations & Incident Management"
    )
    assert any(c.code == "GCTI" for c in advice.certification_roadmap.target_certifications)
