"""
Unit tests for CV text coverage analyzer.
"""

from aegis_ledger.analyzer import analyze_cv_coverage
from aegis_ledger.models import (
    EligibilityCriteria,
    ProvenanceMetadata,
    SubstantiveRequirements,
    VacancyRecord,
)


def test_analyze_cv_coverage_full_match():
    vac = VacancyRecord(
        id="VAC-ANALYZER-1",
        title="CTI Analyst",
        organization="CERT-EU",
        eligibility=EligibilityCriteria(
            min_degree_level="Master", security_clearance_required="SECRET UE"
        ),
        requirements=SubstantiveRequirements(
            domains=["CTI", "SOC"], frameworks=["MITRE ATT&CK"], technologies=["Python"]
        ),
        provenance=ProvenanceMetadata(source_url="https://example.com"),
    )

    cv_text = """
    Vasileios Tsalikidis - Cyber Security & CTI Analyst
    Holds a Master degree in Cyber Security. Experienced in CTI, SOC incident response, and MITRE ATT&CK mapping.
    Proficient in Python and holds SECRET UE clearance.
    """

    res = analyze_cv_coverage(cv_text, vac)
    assert res.coverage_percentage == 100
    assert len(res.missing_keywords) == 0


def test_analyze_cv_coverage_partial_match():
    vac = VacancyRecord(
        id="VAC-ANALYZER-2",
        title="Security Engineer",
        organization="ENISA",
        requirements=SubstantiveRequirements(
            domains=["INFOSEC", "COMSEC"], technologies=["Kubernetes", "Python"]
        ),
        provenance=ProvenanceMetadata(source_url="https://example.com"),
    )

    cv_text = "Experienced INFOSEC specialist with Python skills."

    res = analyze_cv_coverage(cv_text, vac)
    assert res.coverage_percentage < 100
    assert "COMSEC" in res.missing_keywords or "Kubernetes" in res.missing_keywords
