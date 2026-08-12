"""
Local JSON storage repository, candidate profile persistence, and seed data provider for Cyber Posting Ledger.
"""

import json
from datetime import date, datetime, timezone
from pathlib import Path

from cyber_posting_ledger.models import (
    CandidateProfile,
    EligibilityCriteria,
    Milestone,
    MilestoneStatus,
    OrgTier,
    PracticalMetrics,
    ProvenanceMetadata,
    StrategicMetrics,
    SubstantiveRequirements,
    VacancyRecord,
)
from cyber_posting_ledger.scoring import evaluate_vacancy

DEFAULT_DATA_DIR = Path.home() / ".cyber_posting_ledger"
DEFAULT_VACANCIES_FILE = DEFAULT_DATA_DIR / "vacancies.json"
DEFAULT_PROFILE_FILE = DEFAULT_DATA_DIR / "candidate_profile.json"


def get_default_seed_records() -> list[VacancyRecord]:
    """Generates synthetic demo seed vacancies based on public organization specs."""
    now = datetime.now(timezone.utc)
    today = datetime.now(timezone.utc).date()

    vac1 = VacancyRecord(
        id="VAC-001",
        title="ICT Security Coordinator",
        organization="ENISA",
        grade_or_level="AD 7",
        eligibility=EligibilityCriteria(
            allowed_nationalities=["EU"],
            min_degree_level="Master",
            min_experience_years=6,
            security_clearance_required="SECRET UE / EU SECRET",
            required_languages=["English"],
        ),
        requirements=SubstantiveRequirements(
            domains=["INFOSEC", "CIS", "GRC", "Incident Response"],
            frameworks=["NIST CSF", "ISO 27001", "EU NIS2 Directive"],
            technologies=["Python", "Linux", "SIEM"],
            nato_eu_context=True,
        ),
        strategic=StrategicMetrics(
            org_tier=OrgTier.TIER_1,
            brand_value_score=95,
            stepping_stone_score=90,
            ecosystem_alignment=True,
        ),
        practical=PracticalMetrics(
            estimated_monthly_net_eur=5800.0,
            location="Athens, Greece",
            country="Greece",
            contract_type="Temporary Agent (TA 2f)",
            remote_policy="Hybrid",
        ),
        provenance=ProvenanceMetadata(
            source_url="https://www.enisa.europa.eu/recruitment/vacancies/ict-security-coordinator",
            is_official_source=True,
            verified_at=today,
            deadline=date(2026, 9, 15),
            created_at=now,
        ),
        milestones=[
            Milestone(
                status=MilestoneStatus.IDENTIFIED,
                timestamp=now,
                notes="Discovered via official ENISA recruitment page",
            ),
            Milestone(
                status=MilestoneStatus.VERIFIED,
                timestamp=now,
                notes="Verified official source URL & deadline",
            ),
        ],
    )

    vac2 = VacancyRecord(
        id="VAC-002",
        title="CIS Security & COMSEC Analyst",
        organization="NCIA (NATO Communications and Information Agency)",
        grade_or_level="A2 / Grade 15",
        eligibility=EligibilityCriteria(
            allowed_nationalities=["NATO"],
            min_degree_level="Bachelor",
            min_experience_years=5,
            security_clearance_required="NATO SECRET",
            required_languages=["English"],
        ),
        requirements=SubstantiveRequirements(
            domains=["CIS", "COMSEC", "INFOSEC", "NATO CIS"],
            frameworks=["NATO AC/322", "NIST SP 800-53"],
            technologies=["Crypto", "Networks", "Python"],
            nato_eu_context=True,
        ),
        strategic=StrategicMetrics(
            org_tier=OrgTier.TIER_1,
            brand_value_score=95,
            stepping_stone_score=95,
            ecosystem_alignment=True,
        ),
        practical=PracticalMetrics(
            estimated_monthly_net_eur=6200.0,
            location="The Hague, Netherlands",
            country="Netherlands",
            contract_type="NATO International Civilian",
            remote_policy="On-site",
        ),
        provenance=ProvenanceMetadata(
            source_url="https://eRecruitment.ncia.nato.int/vacancies/cis-security-analyst",
            is_official_source=True,
            verified_at=today,
            deadline=date(2026, 9, 30),
            created_at=now,
        ),
        milestones=[
            Milestone(
                status=MilestoneStatus.IDENTIFIED,
                timestamp=now,
                notes="Direct match for NATO CIS & COMSEC background",
            ),
        ],
    )

    vac3 = VacancyRecord(
        id="VAC-003",
        title="Cyber Threat Intelligence Specialist",
        organization="CERT-EU",
        grade_or_level="AD 6",
        eligibility=EligibilityCriteria(
            allowed_nationalities=["EU"],
            min_degree_level="Master",
            min_experience_years=3,
            security_clearance_required="SECRET UE",
            required_languages=["English"],
        ),
        requirements=SubstantiveRequirements(
            domains=["CTI", "SOC", "Incident Response", "Threat Hunting"],
            frameworks=["MITRE ATT&CK", "MISP", "STIX/TAXII"],
            technologies=["Python", "Neo4j", "Elasticsearch"],
            nato_eu_context=True,
        ),
        strategic=StrategicMetrics(
            org_tier=OrgTier.TIER_1,
            brand_value_score=90,
            stepping_stone_score=85,
            ecosystem_alignment=True,
        ),
        practical=PracticalMetrics(
            estimated_monthly_net_eur=5400.0,
            location="Brussels, Belgium",
            country="Belgium",
            contract_type="Contract Agent / TA",
            remote_policy="Hybrid",
        ),
        provenance=ProvenanceMetadata(
            source_url="https://cert.europa.eu/jobs/cti-specialist",
            is_official_source=True,
            verified_at=today,
            deadline=date(2026, 10, 10),
            created_at=now,
        ),
        milestones=[
            Milestone(
                status=MilestoneStatus.IDENTIFIED,
                timestamp=now,
                notes="Aligns with CTI & Threat Graph research",
            ),
        ],
    )

    # Three postings the candidate does not fit. A tracker whose demo shows
    # every role as a perfect match demonstrates nothing: the first question
    # a reader asks is when it says no, and there has to be an answer. The
    # gaps below are real ones in the profile — no cloud engineering, no
    # offensive security, and a nationality that cannot hold a US clearance.
    #
    # These employers are invented, and their URLs point at example.com, so
    # nothing here can be mistaken for a real advertisement.

    vac4 = VacancyRecord(
        id="VAC-004",
        title="Cloud Security Architect",
        organization="Northwind Cloud Services (fictional)",
        grade_or_level="Senior",
        eligibility=EligibilityCriteria(
            allowed_nationalities=["EU"],
            min_degree_level="Bachelor",
            min_experience_years=10,
            security_clearance_required="None",
            required_languages=["English"],
        ),
        requirements=SubstantiveRequirements(
            domains=["Cloud Security", "DevSecOps", "Application Security"],
            frameworks=["CIS Benchmarks", "CSA CCM"],
            technologies=["AWS", "Azure", "Kubernetes", "Terraform"],
            nato_eu_context=False,
        ),
        strategic=StrategicMetrics(
            org_tier=OrgTier.TIER_3,
            brand_value_score=45,
            stepping_stone_score=40,
            ecosystem_alignment=False,
        ),
        practical=PracticalMetrics(
            estimated_monthly_net_eur=6200.0,
            location="Amsterdam, Netherlands",
            country="Netherlands",
            contract_type="Permanent",
            remote_policy="On-site",
        ),
        provenance=ProvenanceMetadata(
            source_url="https://example.com/fictional/cloud-security-architect",
            is_official_source=False,
            verified_at=today,
            deadline=date(2026, 10, 1),
            created_at=now,
        ),
        milestones=[
            Milestone(
                status=MilestoneStatus.IDENTIFIED,
                timestamp=now,
                notes="Synthetic record. Kept as a demonstration of a poor substantive fit: "
                "no cloud engineering history and none of the platform certifications asked for.",
            ),
        ],
    )

    vac5 = VacancyRecord(
        id="VAC-005",
        title="Senior Red Team Operator",
        organization="Halberd Offensive Security (fictional)",
        grade_or_level="Senior",
        eligibility=EligibilityCriteria(
            allowed_nationalities=["EU"],
            min_degree_level="Bachelor",
            min_experience_years=6,
            security_clearance_required="None",
            required_languages=["English"],
        ),
        requirements=SubstantiveRequirements(
            domains=["Penetration Testing", "Red Teaming", "Exploit Development"],
            frameworks=["OSSTMM", "PTES"],
            technologies=["C", "Assembly", "Cobalt Strike", "Burp Suite"],
            nato_eu_context=False,
        ),
        strategic=StrategicMetrics(
            org_tier=OrgTier.TIER_3,
            brand_value_score=50,
            stepping_stone_score=35,
            ecosystem_alignment=False,
        ),
        practical=PracticalMetrics(
            estimated_monthly_net_eur=5400.0,
            location="Berlin, Germany",
            country="Germany",
            contract_type="Permanent",
            remote_policy="Hybrid",
        ),
        provenance=ProvenanceMetadata(
            source_url="https://example.com/fictional/senior-red-team-operator",
            is_official_source=False,
            verified_at=today,
            deadline=date(2026, 9, 30),
            created_at=now,
        ),
        milestones=[
            Milestone(
                status=MilestoneStatus.IDENTIFIED,
                timestamp=now,
                notes="Synthetic record. Defensive and governance experience does not transfer "
                "to an offensive role, and the tool should not pretend otherwise.",
            ),
        ],
    )

    vac6 = VacancyRecord(
        id="VAC-006",
        title="Cyber Operations Officer",
        organization="Ridgeline Defense Systems (fictional)",
        grade_or_level="GS-13 equivalent",
        eligibility=EligibilityCriteria(
            allowed_nationalities=["US"],
            min_degree_level="Bachelor",
            min_experience_years=5,
            security_clearance_required="US TOP SECRET / SCI",
            required_languages=["English"],
        ),
        requirements=SubstantiveRequirements(
            domains=["SOC", "Incident Response", "CTI"],
            frameworks=["NIST CSF", "MITRE ATT&CK"],
            technologies=["Splunk", "Python"],
            nato_eu_context=False,
        ),
        strategic=StrategicMetrics(
            org_tier=OrgTier.TIER_3,
            brand_value_score=55,
            stepping_stone_score=30,
            ecosystem_alignment=False,
        ),
        practical=PracticalMetrics(
            estimated_monthly_net_eur=7000.0,
            location="Virginia, United States",
            country="United States",
            contract_type="Permanent",
            remote_policy="On-site",
        ),
        provenance=ProvenanceMetadata(
            source_url="https://example.com/fictional/cyber-operations-officer",
            is_official_source=False,
            verified_at=today,
            deadline=date(2026, 11, 15),
            created_at=now,
        ),
        milestones=[
            Milestone(
                status=MilestoneStatus.IDENTIFIED,
                timestamp=now,
                notes="Synthetic record. The work itself is a close match; US citizenship and a "
                "US clearance are not obtainable, so the role is closed regardless of fit. "
                "Eligibility and fit are separate questions and this record keeps them apart.",
            ),
        ],
    )

    return [vac1, vac2, vac3, vac4, vac5, vac6]


class VacancyStorage:
    def __init__(self, data_dir: Path | None = None):
        self.data_dir = data_dir or DEFAULT_DATA_DIR
        self.vacancies_path = self.data_dir / "vacancies.json"
        self.profile_path = self.data_dir / "candidate_profile.json"
        self.data_dir.mkdir(parents=True, exist_ok=True)

        if not self.vacancies_path.exists():
            self._save_all_vacancies(get_default_seed_records())

        if not self.profile_path.exists():
            self.save_profile(CandidateProfile())

    def load_profile(self) -> CandidateProfile:
        if not self.profile_path.exists():
            prof = CandidateProfile()
            self.save_profile(prof)
            return prof
        with open(self.profile_path, encoding="utf-8") as f:
            raw = json.load(f)
        return CandidateProfile.model_validate(raw)

    def save_profile(self, profile: CandidateProfile) -> None:
        with open(self.profile_path, "w", encoding="utf-8") as f:
            json.dump(json.loads(profile.model_dump_json()), f, indent=2)

    def _save_all_vacancies(self, records: list[VacancyRecord]) -> None:
        data = [json.loads(r.model_dump_json()) for r in records]
        with open(self.vacancies_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, default=str)

    def load_all(self) -> list[VacancyRecord]:
        if not self.vacancies_path.exists():
            records = get_default_seed_records()
            self._save_all_vacancies(records)

        with open(self.vacancies_path, encoding="utf-8") as f:
            raw_list = json.load(f)

        profile = self.load_profile()
        records = [VacancyRecord.model_validate(item) for item in raw_list]
        for r in records:
            r.fit_result = evaluate_vacancy(r, profile)
        return records

    def get_by_id(self, record_id: str) -> VacancyRecord | None:
        records = self.load_all()
        for r in records:
            if r.id.upper() == record_id.upper():
                return r
        return None

    def save(self, record: VacancyRecord) -> None:
        profile = self.load_profile()
        record.fit_result = evaluate_vacancy(record, profile)
        records = self.load_all()
        existing_index = next(
            (i for i, r in enumerate(records) if r.id.upper() == record.id.upper()),
            None,
        )
        if existing_index is not None:
            records[existing_index] = record
        else:
            records.append(record)
        self._save_all_vacancies(records)

    def delete(self, record_id: str) -> bool:
        records = self.load_all()
        initial_len = len(records)
        filtered = [r for r in records if r.id.upper() != record_id.upper()]
        if len(filtered) < initial_len:
            self._save_all_vacancies(filtered)
            return True
        return False

    def export_markdown(self) -> str:
        records = self.load_all()
        lines = [
            "# Cyber Posting Ledger - Summary Report",
            f"*Generated on {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}*",
            "",
            "| ID | Organization | Job Title | Grade | Status | Formal Score | Substantive | Strategic | Practical | Official Source |",
            "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
        ]
        for r in records:
            res = r.fit_result or evaluate_vacancy(r, self.load_profile())
            official = "Yes" if r.provenance.is_official_source else "No"
            lines.append(
                f"| `{r.id}` | **{r.organization}** | {r.title} | `{r.grade_or_level}` | `{res.overall_status}` | **{res.formal_eligibility_score}** | {res.substantive_fit_score} | {res.strategic_value_score} | {res.practical_value_score} | {official} |"
            )
        return "\n".join(lines)
