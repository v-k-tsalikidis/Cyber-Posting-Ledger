# Release Notes & Version History - Cyber Vacancy Intelligence Tracker

This document maintains the version history, feature additions, and release documentation for **Cyber Vacancy Intelligence Tracker** (**Vacancy Intelligence Ledger**).

---

## [v0.3.0] - 2026-07-25 (Recruiter Intelligence & Career Advisor Release)

### Added
- **Recruiter Intelligence Advisory Engine (`recruiter_advisor.py`):**
  - Mapped CyBOK categories to industry-recognized certification roadmaps (*CISSP, CISA, CISM, GCTI, Security+, ISO 27001 LA, CSSLP*).
  - Added status tracking for certifications held vs recommended targets (`Held ✓` vs `Target 🎯`).
  - Added **Quantifiable Impact Templates** tailored for recruiter screening (log scale, MTTR %, compliance audit coverage).
  - Added **Score Booster Roadmap** calculating potential max score and step-by-step career path recommendations.
- **Documentation & Evidence:**
  - Added [`docs/RECRUITER_INTELLIGENCE.md`](file:///Users/basilt/Projects/NewJob_Cyber/cyber-vacancy-tracker/docs/RECRUITER_INTELLIGENCE.md) explaining recruiter filtering logic, metrics, and certification roadmaps.
- **Unit Tests:**
  - Added `tests/test_recruiter_advisor.py` (17 total pytest unit tests passing).

---

## [v0.2.0] - 2026-07-25 (Phase 2 Feature Expansion Release)

### Added
- **CV & Cover Letter Coverage Analyzer (`analyzer.py`):**
  - Text matching engine scanning raw CV text against vacancy required domains, frameworks, technologies, degree level, and clearance.
  - Generates coverage percentage, matched terms, and missing keywords list.
- **Publication-Quality HTML Report Exporter (`exporter.py`):**
  - Generates standalone, styled HTML assessment briefs using the Premium Minimalist design system.
- **Multi-Profile Scenario Engine:**
  - 1-click UI dropdown to evaluate vacancies under different profile scenarios (*Current*, *Post-Thesis Target*, *NATO Specialist*).
- **Interactive Web UI Enhancements:**
  - Added CV Coverage Analyzer Modal, 4-Axis Score Radar SVG generator, and HTML export viewer.

---

## [v0.1.0] - 2026-07-23 (Initial Base Release)

### Added
- Multi-dimensional fit scoring engine (`scoring.py`) evaluating *Formal Eligibility*, *Substantive Fit*, *Strategic Value*, and *Practical Value*.
- CyBOK v1.1 Knowledge Area taxonomy classifier and NIST NICE role alignment.
- Purchasing Power Parity (PPP) salary adjustment engine for EU locations (Athens, Brussels, The Hague, Luxembourg, Munich).
- Local storage persistence (`storage.py`) and JSON storage.
- CLI interface (`cli.py`) and Web Dashboard UI (`http://localhost:8000`).
