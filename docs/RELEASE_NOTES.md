# Release Notes & Version History - Cyber Posting Ledger

This document maintains the version history, feature additions, and release documentation for **Cyber Posting Ledger** (*Cyber Posting Ledger Vacancy Intelligence Ledger*).

---

## [v0.4.0] - 2026-07-25 (Cyber Posting Ledger Rebrand & Premium Minimalist Overhaul)

### Added & Refactored
- **Official Rebrand to Cyber Posting Ledger:**
  - Renamed platform identity to **Cyber Posting Ledger** (*Academic & Recruiter-Grounded Cybersecurity Career Intelligence*).
- **Brand Style Guide & Vector Logo:**
  - Added [`docs/BRAND_STYLE_GUIDE.md`](file:///Users/basilt/Projects/NewJob_Cyber/cyber-posting-ledger/docs/BRAND_STYLE_GUIDE.md) detailing color tokens, typography rules, SVG logo specs, and zero-emoji guidelines.
  - Created vector SVG logo mark `src/cyber_posting_ledger/frontend/assets/cyber-posting-ledger_logo.svg`.
- **100% Zero-Emoji UI Cleanup:**
  - Completely stripped decorative emojis from Web UI, CLI output, Markdown Briefs, and HTML reports.
  - Applied Warm Off-White paper canvas (`#FAF9F6`), Deep Teal (`#0F5257`), and monospaced numeric scores (`JetBrains Mono`).

---

## [v0.3.0] - 2026-07-25 (Recruiter Intelligence & Career Advisor Release)

### Added
- **Recruiter Intelligence Advisory Engine (`recruiter_advisor.py`):**
  - Mapped CyBOK categories to industry-recognized certification roadmaps (*CISSP, CISA, CISM, GCTI, Security+, ISO 27001 LA, CSSLP*).
  - Added status tracking for certifications held vs recommended targets (`[HELD]` vs `[TARGET]`).
  - Added **Quantifiable Impact Templates** tailored for recruiter screening (log scale, MTTR %, compliance audit coverage).
  - Added **Score Booster Roadmap** calculating potential max score and step-by-step career path recommendations.
- **Documentation & Evidence:**
  - Added [`docs/RECRUITER_INTELLIGENCE.md`](file:///Users/basilt/Projects/NewJob_Cyber/cyber-posting-ledger/docs/RECRUITER_INTELLIGENCE.md) explaining recruiter filtering logic, metrics, and certification roadmaps.

---

## [v0.2.0] - 2026-07-25 (Phase 2 Feature Expansion Release)

### Added
- **CV & Cover Letter Coverage Analyzer (`analyzer.py`):**
  - Text matching engine scanning raw CV text against vacancy required domains, frameworks, technologies, degree level, and clearance.
- **Publication-Quality HTML Report Exporter (`exporter.py`):**
  - Generates standalone, styled HTML assessment briefs using the Premium Minimalist design system.
- **Multi-Profile Scenario Engine:**
  - 1-click UI dropdown to evaluate vacancies under different profile scenarios (*Current*, *Post-Thesis Target*, *NATO Specialist*).

---

## [v0.1.0] - 2026-07-23 (Initial Base Release)

### Added
- Multi-dimensional fit scoring engine (`scoring.py`) evaluating *Formal Eligibility*, *Substantive Fit*, *Strategic Value*, and *Practical Value*.
- CyBOK v1.1 Knowledge Area taxonomy classifier and NIST NICE role alignment.
- Purchasing Power Parity (PPP) salary adjustment engine for EU locations (Athens, Brussels, The Hague, Luxembourg, Munich).
- Local storage persistence (`storage.py`) and JSON storage.
- CLI interface (`cli.py`) and Web Dashboard UI (`http://localhost:8000`).
