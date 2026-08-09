"""
Unit tests for HTML report exporter.
"""

from aegis_ledger.exporter import generate_html_report
from aegis_ledger.models import (
    CandidateProfile,
    PracticalMetrics,
    ProvenanceMetadata,
    VacancyRecord,
)


def test_generate_html_report():
    profile = CandidateProfile()
    vac = VacancyRecord(
        id="VAC-EXPORT-1",
        title="ICT Security Officer",
        organization="eu-LISA",
        practical=PracticalMetrics(location="Tallinn, Estonia"),
        provenance=ProvenanceMetadata(source_url="https://example.com"),
    )

    html = generate_html_report(vac, profile)
    assert "<!DOCTYPE html>" in html
    assert "ICT Security Officer" in html
    assert "eu-LISA" in html
    assert "Executive Summary" in html
