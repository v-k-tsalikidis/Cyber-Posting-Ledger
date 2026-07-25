"""
Data models and schemas for Cyber Vacancy Intelligence Tracker.
"""

from enum import Enum
from typing import List, Optional, Dict, Any
from datetime import date, datetime
from pydantic import BaseModel, Field


class OrgTier(int, Enum):
    TIER_1 = 1  # Core NATO/EU Cyber/INFOSEC agencies (NCIA, ENISA, CERT-EU, eu-LISA, Europol, ECCC)
    TIER_2 = 2  # EU Agencies & International Bodies with ICT/Security roles (EMA, EASA, EIB, etc.)
    TIER_3 = 3  # General monitoring orgs (UN agencies, tribunals, research institutes)


class MilestoneStatus(str, Enum):
    IDENTIFIED = "Identified"
    VERIFIED = "Verified"
    TAILORED = "Tailored"
    SUBMITTED = "Submitted"
    SCREENING = "Screening"
    INTERVIEW = "Interview"
    OFFER = "Offer"
    ARCHIVED = "Archived"


class EligibilityCriteria(BaseModel):
    allowed_nationalities: List[str] = Field(default_factory=lambda: ["EU", "NATO"])
    min_degree_level: str = Field(default="Master", description="Bachelor, Master, PhD")
    min_experience_years: int = Field(default=3, ge=0)
    security_clearance_required: str = Field(default="None", description="None, NATO SECRET, SECRET UE, COSMIC TOP SECRET")
    required_languages: List[str] = Field(default_factory=lambda: ["English"])


class SubstantiveRequirements(BaseModel):
    domains: List[str] = Field(default_factory=list, description="e.g. CIS, INFOSEC, COMSEC, CTI, SOC, GRC, DevSecOps")
    frameworks: List[str] = Field(default_factory=list, description="e.g. NIST CSF, OWASP, ISO 27001, MITRE ATT&CK, PM2")
    technologies: List[str] = Field(default_factory=list, description="e.g. Python, Neo4j, Linux, SIEM, Kubernetes")
    nato_eu_context: bool = Field(default=False, description="Requires NATO/EU or multinational operational context")


class CyBOKCategory(str, Enum):
    GOVERNANCE_RISK = "Risk Management & Governance"
    SECURITY_OPERATIONS = "Security Operations & Incident Management"
    SOFTWARE_SECURITY = "Software & Platform Security"
    NETWORK_INFRASTRUCTURE = "Network & Infrastructure Security"
    HUMAN_ORGANIZATIONAL = "Human, Organizational & Regulatory Aspects"


class CyBOKMapping(BaseModel):
    primary_category: CyBOKCategory
    matched_knowledge_areas: List[str] = Field(default_factory=list)
    nice_framework_role: str = Field(default="Cyber Defense / INFOSEC Specialist")


class CertificationItem(BaseModel):
    name: str
    code: str
    held: bool = False
    priority: str = Field(default="Recommended", description="Must-Have, Recommended, Optional")


class CertificationRoadmap(BaseModel):
    domain_category: str
    target_certifications: List[CertificationItem] = Field(default_factory=list)


class RecruiterImpactMetric(BaseModel):
    category: str  # Scale, Risk Reduction, Compliance Audit, Scripting
    template_bullet: str
    guidance: str


class ScoreBoosterStep(BaseModel):
    step_number: int
    title: str
    score_delta: int
    action_item: str


class RecruiterAdvice(BaseModel):
    certification_roadmap: CertificationRoadmap
    quantifiable_impact_templates: List[RecruiterImpactMetric] = Field(default_factory=list)
    score_booster_steps: List[ScoreBoosterStep] = Field(default_factory=list)
    potential_max_score: int = Field(..., ge=0, le=100)


class PurchasingPowerMetrics(BaseModel):
    raw_salary_net_eur: Optional[float] = Field(default=None)
    location: str = Field(default="Brussels, Belgium")
    ppp_multiplier: float = Field(default=1.0, description="Purchasing Power Parity index relative to Brussels base 1.0")
    ppp_adjusted_net_eur: Optional[float] = Field(default=None, description="Purchasing power equivalent salary")


class StrategicMetrics(BaseModel):
    org_tier: OrgTier = Field(default=OrgTier.TIER_2)
    brand_value_score: int = Field(default=70, ge=0, le=100, description="Reputation & brand weight")
    stepping_stone_score: int = Field(default=70, ge=0, le=100, description="Long-term career trajectory value")
    ecosystem_alignment: bool = Field(default=True, description="Direct alignment with EU/NATO cybersecurity mission")


class PracticalMetrics(BaseModel):
    estimated_monthly_net_eur: Optional[float] = Field(default=None, ge=0.0)
    location: str = Field(default="Brussels, Belgium")
    country: str = Field(default="Belgium")
    contract_type: str = Field(default="Temporary Agent / Contract Agent", description="Permanent, TA, CA, SNE, Consultant")
    remote_policy: str = Field(default="Hybrid", description="On-site, Hybrid, Remote")
    purchasing_power: Optional[PurchasingPowerMetrics] = None


class ProvenanceMetadata(BaseModel):
    source_url: str = Field(..., description="Primary vacancy announcement URL")
    is_official_source: bool = Field(default=True, description="True if employer official page, False if aggregator")
    verified_at: Optional[date] = Field(default_factory=date.today)
    deadline: Optional[date] = None
    created_at: datetime = Field(default_factory=datetime.now)


class Milestone(BaseModel):
    status: MilestoneStatus
    timestamp: datetime = Field(default_factory=datetime.now)
    notes: Optional[str] = None


class FitScoreResult(BaseModel):
    formal_eligibility_score: int = Field(..., ge=0, le=100)
    substantive_fit_score: int = Field(..., ge=0, le=100)
    strategic_value_score: int = Field(..., ge=0, le=100)
    practical_value_score: int = Field(..., ge=0, le=100)
    overall_status: str = Field(..., description="Eligible, Conditional, or Disqualified")
    disqualification_reasons: List[str] = Field(default_factory=list)
    observations: List[str] = Field(default_factory=list)
    cybok_mapping: Optional[CyBOKMapping] = None
    recruiter_advice: Optional[RecruiterAdvice] = None


class CandidateProfile(BaseModel):
    candidate_name: str = Field(default="Vasileios Tsalikidis")
    nationalities: List[str] = Field(default_factory=lambda: ["Greek", "EU", "NATO"])
    degree_level: str = Field(default="Master", description="BSc, MSc, PhD")
    total_experience_years: int = Field(default=8)
    cyber_experience_years: int = Field(default=5)
    clearance_held: str = Field(default="National Secret / NATO Secret eligible")
    languages_proficient: List[str] = Field(default_factory=lambda: ["English", "Greek"])
    skills_and_domains: List[str] = Field(
        default_factory=lambda: [
            "CIS", "INFOSEC", "COMSEC", "CTI", "SOC", "GRC",
            "NIST CSF", "OWASP", "MITRE ATT&CK", "Python",
            "NATO", "EU", "Incident Response", "Service Management", "PM2"
        ]
    )
    certifications_held: List[str] = Field(
        default_factory=lambda: ["PM2 Advanced", "Security+ Eligible", "CISSP Candidate"]
    )


class CVCoverageResult(BaseModel):
    coverage_percentage: int = Field(..., ge=0, le=100)
    total_required_keywords: int = Field(...)
    matched_keywords: List[str] = Field(default_factory=list)
    missing_keywords: List[str] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)


class VacancyRecord(BaseModel):
    id: str = Field(..., description="Unique ID, e.g., VAC-001")
    title: str = Field(..., description="Job Title")
    organization: str = Field(..., description="Organization Name")
    grade_or_level: str = Field(default="N/A", description="e.g. AD 7, A2, Grade 15")
    eligibility: EligibilityCriteria = Field(default_factory=EligibilityCriteria)
    requirements: SubstantiveRequirements = Field(default_factory=SubstantiveRequirements)
    strategic: StrategicMetrics = Field(default_factory=StrategicMetrics)
    practical: PracticalMetrics = Field(default_factory=PracticalMetrics)
    provenance: ProvenanceMetadata
    milestones: List[Milestone] = Field(default_factory=list)
    fit_result: Optional[FitScoreResult] = None


class ApplicationBrief(BaseModel):
    vacancy_id: str
    vacancy_title: str
    organization: str
    fit_status: str
    executive_summary: str
    key_selling_points: List[str]
    tailored_experience_bullets: List[str]
    gap_mitigation_advice: List[str]
    cybok_category: str
    recruiter_advice: Optional[RecruiterAdvice] = None
    generated_at: datetime = Field(default_factory=datetime.now)
