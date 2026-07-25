"""
Unit tests for cyber_vacancy_tracker data models.
"""

from datetime import date
from cyber_vacancy_tracker.models import (
    VacancyRecord,
    EligibilityCriteria,
    SubstantiveRequirements,
    StrategicMetrics,
    PracticalMetrics,
    ProvenanceMetadata,
    CandidateProfile,
    OrgTier,
)


def test_vacancy_record_instantiation():
    record = VacancyRecord(
        id="VAC-100",
        title="INFOSEC Lead",
        organization="Europol",
        grade_or_level="AD 8",
        provenance=ProvenanceMetadata(
            source_url="https://europol.europa.eu/jobs/infosec-lead",
            is_official_source=True,
            deadline=date(2026, 12, 31),
        ),
    )
    assert record.id == "VAC-100"
    assert record.title == "INFOSEC Lead"
    assert record.organization == "Europol"
    assert record.provenance.is_official_source is True


def test_candidate_profile_default():
    profile = CandidateProfile()
    assert profile.candidate_name == "Vasileios Tsalikidis"
    assert "Greek" in profile.nationalities
    assert "INFOSEC" in profile.skills_and_domains
