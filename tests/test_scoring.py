"""
Unit tests for aegis_ledger scoring engine.
"""

from aegis_ledger.models import (
    CandidateProfile,
    EligibilityCriteria,
    OrgTier,
    PracticalMetrics,
    ProvenanceMetadata,
    StrategicMetrics,
    SubstantiveRequirements,
    VacancyRecord,
)
from aegis_ledger.scoring import (
    evaluate_formal_eligibility,
    evaluate_practical_value,
    evaluate_strategic_value,
    evaluate_substantive_fit,
    evaluate_vacancy,
)


def test_evaluate_formal_eligibility_success():
    profile = CandidateProfile(
        nationalities=["Greek", "EU", "NATO"],
        degree_level="Master",
        total_experience_years=8,
        languages_proficient=["English"],
    )

    vacancy = VacancyRecord(
        id="VAC-TEST-1",
        title="Cyber Security Specialist",
        organization="ENISA",
        eligibility=EligibilityCriteria(
            allowed_nationalities=["EU"],
            min_degree_level="Master",
            min_experience_years=5,
            required_languages=["English"],
        ),
        provenance=ProvenanceMetadata(source_url="https://example.com"),
    )

    score, disqualifications, _observations = evaluate_formal_eligibility(profile, vacancy)
    assert score == 100
    assert len(disqualifications) == 0


def test_evaluate_formal_eligibility_nationality_mismatch():
    profile = CandidateProfile(
        nationalities=["Japanese"],
        degree_level="Master",
        total_experience_years=8,
        languages_proficient=["English"],
    )

    vacancy = VacancyRecord(
        id="VAC-TEST-2",
        title="NATO CIS Officer",
        organization="NCIA",
        eligibility=EligibilityCriteria(
            allowed_nationalities=["NATO"],
            min_degree_level="Master",
            min_experience_years=5,
        ),
        provenance=ProvenanceMetadata(source_url="https://example.com"),
    )

    score, disqualifications, _observations = evaluate_formal_eligibility(profile, vacancy)
    assert score < 50
    assert any("Nationality mismatch" in d for d in disqualifications)


def test_evaluate_substantive_fit():
    profile = CandidateProfile(skills_and_domains=["CIS", "INFOSEC", "COMSEC", "NATO", "Python"])

    vacancy = VacancyRecord(
        id="VAC-TEST-3",
        title="COMSEC Auditor",
        organization="NSPA",
        requirements=SubstantiveRequirements(
            domains=["CIS", "COMSEC"],
            frameworks=["NIST CSF"],
            nato_eu_context=True,
        ),
        provenance=ProvenanceMetadata(source_url="https://example.com"),
    )

    score, _observations = evaluate_substantive_fit(profile, vacancy)
    assert score >= 80


def test_evaluate_strategic_value_tier1():
    vacancy = VacancyRecord(
        id="VAC-TEST-4",
        title="CERT-EU Threat Analyst",
        organization="CERT-EU",
        strategic=StrategicMetrics(
            org_tier=OrgTier.TIER_1,
            brand_value_score=90,
            stepping_stone_score=85,
            ecosystem_alignment=True,
        ),
        provenance=ProvenanceMetadata(source_url="https://example.com"),
    )

    score, _observations = evaluate_strategic_value(vacancy)
    assert score >= 85


def test_evaluate_practical_value_high_salary():
    vacancy = VacancyRecord(
        id="VAC-TEST-5",
        title="Senior Security Specialist",
        organization="EIB",
        practical=PracticalMetrics(
            estimated_monthly_net_eur=6500.0,
            location="Luxembourg",
        ),
        provenance=ProvenanceMetadata(source_url="https://example.com"),
    )

    score, _observations = evaluate_practical_value(vacancy)
    assert score >= 80


def test_evaluate_vacancy_full():
    vacancy = VacancyRecord(
        id="VAC-TEST-6",
        title="ICT Security Officer",
        organization="eu-LISA",
        provenance=ProvenanceMetadata(source_url="https://example.com"),
    )

    res = evaluate_vacancy(vacancy)
    assert res.overall_status in ["Eligible", "Conditional", "Disqualified"]
    assert 0 <= res.formal_eligibility_score <= 100
    assert 0 <= res.substantive_fit_score <= 100
    assert 0 <= res.strategic_value_score <= 100
    assert 0 <= res.practical_value_score <= 100
