# Cyber Vacancy Intelligence Tracker (Vacancy Intelligence Ledger)

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://python.org)
[![Version](https://img.shields.io/badge/version-0.3.0-teal.svg)](docs/RELEASE_NOTES.md)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-17%20passed-success.svg)](#testing)

A local-first, privacy-preserving **Cybersecurity Career Intelligence & Vacancy Assessment System** grounded in **CyBOK v1.1** (Cyber Security Body of Knowledge), **NIST NICE Framework**, and **Recruiter Intelligence**.

---

## 🌟 Key Features

### 1. Multi-Dimensional Un-Aggregated Fit Scoring
Evaluates vacancies across 4 distinct dimensions without collapsing data into generic match percentages:
- **Formal Eligibility (0–100):** Hard gates for nationality (`EU`/`NATO`), degree level (`BSc`/`Master`/`PhD`), experience years, security clearance (`NATO SECRET`, `SECRET UE`), and languages.
- **Substantive Role Fit (0–100):** Technical skill match ratio, framework overlap (NIST CSF 2.0, OWASP, ISO 27001), and NATO/EU operational context bonus.
- **Strategic Value (0–100):** Organization Tier classification (Tier 1 core NATO/EU agencies: NCIA, ENISA, CERT-EU, eu-LISA, Europol, ECCC vs Tier 2/3), brand weight, and ecosystem alignment.
- **Practical Value (0–100):** Net compensation tier and Purchasing Power Parity (PPP) location multipliers.

### 2. CyBOK v1.1 & NIST NICE Taxonomy Mapping
Classifies job requirements into 5 CyBOK Knowledge Areas and NIST NICE Framework roles:
- *Risk Management & Governance* (Security Control Assessor / GRC Specialist)
- *Security Operations & Incident Management* (Cyber Defense Analyst / CTI Specialist)
- *Network & Infrastructure Security* (ISSO / Network Security Engineer)
- *Software & Platform Security* (Secure Software / DevSecOps Engineer)
- *Human, Organizational & Regulatory Aspects* (Information Security Specialist)

### 3. Purchasing Power Parity (PPP) Calculator
Adjusts net salary estimates according to cost-of-living purchasing power indices relative to Brussels (Base 1.0), highlighting true purchasing power (e.g. Athens `1.25x` multiplier).

### 4. Recruiter Intelligence & Career Path Advisory Engine
- **Certification Roadmap:** Recommends domain-specific certifications (*CISSP, CISA, CISM, GCTI, Security+, ISO 27001 LA, CSSLP*) comparing credentials held vs target credentials.
- **Quantifiable Impact Templates:** Generates recruiter-aligned bullet templates focusing on scale (log volume, endpoint count), MTTR reduction %, and compliance audit proof.
- **Score Booster Roadmap:** Calculates potential max score and step-by-step career path recommendations.

### 5. CV & Cover Letter Coverage Analyzer
Scans raw candidate CV text against vacancy requirements, reporting percentage coverage, matched skills, and missing keywords to add before submitting.

### 6. Application Alignment Brief & HTML Exporter
Generates structured Markdown briefs and standalone, publication-quality HTML assessment reports for applications.

---

## 🛠️ Installation & Quick Start

```bash
# Clone repository
git clone https://github.com/basilt/cyber-vacancy-tracker.git
cd cyber-vacancy-tracker

# Install in editable mode
pip install -e .
```

### Run Web Dashboard UI
```bash
cyber-vacancy-tracker serve --port 8000
```
Open **[http://localhost:8000](http://localhost:8000)** in your browser.

### Run CLI Commands
```bash
# List tracked vacancies and fit scores
cyber-vacancy-tracker list

# Detailed multi-dimensional evaluation
cyber-vacancy-tracker score --id VAC-001

# Generate Application Alignment Brief
cyber-vacancy-tracker generate-brief --id VAC-001

# Analyze CV text coverage
cyber-vacancy-tracker analyze-cv --id VAC-001 --cv-file my_cv.md

# Export standalone HTML report
cyber-vacancy-tracker export-html --id VAC-001 --out report.html
```

---

## 🧪 Testing

Run the pytest test suite:
```bash
python3 -m pytest
```
*17 passed out of 17 tests (100% pass rate).*

---

## 📚 Documentation & Releases

- [`docs/RECRUITER_INTELLIGENCE.md`](file:///Users/basilt/Projects/NewJob_Cyber/cyber-vacancy-tracker/docs/RECRUITER_INTELLIGENCE.md) - Recruiter evaluation metrics & certification mapping
- [`docs/RELEASE_NOTES.md`](file:///Users/basilt/Projects/NewJob_Cyber/cyber-vacancy-tracker/docs/RELEASE_NOTES.md) - Version history & release notes (`v0.3.0`)

---
*Cyber Vacancy Intelligence Tracker &bull; Personal Confidential Career Evidence*
