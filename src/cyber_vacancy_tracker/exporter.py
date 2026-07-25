"""
Publication-Quality HTML Report Exporter for AEGIS-LEDGER.
Generates standalone, styled HTML assessment briefs with recruiter intelligence (Zero Emojis).
"""

from datetime import datetime
from cyber_vacancy_tracker.models import VacancyRecord, CandidateProfile
from cyber_vacancy_tracker.scoring import evaluate_vacancy
from cyber_vacancy_tracker.generator import generate_application_brief


def generate_html_report(vacancy: VacancyRecord, profile: CandidateProfile) -> str:
    """Generates a standalone, beautifully styled HTML document for a vacancy brief."""
    fit_res = evaluate_vacancy(vacancy, profile)
    brief = generate_application_brief(vacancy, profile)
    cybok = fit_res.cybok_mapping
    rec = fit_res.recruiter_advice

    status_color = "#0F5257" if fit_res.overall_status == "Eligible" else "#8C531B" if fit_res.overall_status == "Conditional" else "#992B2B"
    status_bg = "#E6F4F1" if fit_res.overall_status == "Eligible" else "#FDF4E7" if fit_res.overall_status == "Conditional" else "#FDF0F0"

    certs_html = ""
    if rec:
        certs_html = "".join([
            f"<li style='margin-bottom:6px;'>{'<span style=\"color:#0F5257;font-weight:700;\">[HELD]</span>' if c.held else '<span style=\"color:#8C531B;font-weight:700;\">[TARGET]</span>'} <strong>{c.name} ({c.code})</strong> &bull; <em>{c.priority}</em></li>"
            for c in rec.certification_roadmap.target_certifications
        ])

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Application Alignment Report - {vacancy.title}</title>
  <style>
    body {{
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background: #FAF9F6;
      color: #1E293B;
      line-height: 1.6;
      margin: 0;
      padding: 40px;
    }}
    .report-card {{
      max-width: 800px;
      margin: 0 auto;
      background: #FFFFFF;
      border: 1px solid #E2E8F0;
      border-radius: 8px;
      padding: 40px;
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
    }}
    .header {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      border-bottom: 1px solid #E2E8F0;
      padding-bottom: 20px;
      margin-bottom: 24px;
    }}
    .title {{
      font-size: 1.35rem;
      font-weight: 700;
      color: #0F5257;
      margin: 0 0 6px 0;
      letter-spacing: -0.01em;
    }}
    .subtitle {{
      font-size: 0.85rem;
      color: #64748B;
      margin: 0;
    }}
    .status-badge {{
      display: inline-block;
      font-size: 0.75rem;
      font-weight: 700;
      padding: 4px 14px;
      border-radius: 12px;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      background: {status_bg};
      color: {status_color};
    }}
    .grid-scores {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 16px;
      background: #FAF9F6;
      padding: 16px;
      border-radius: 6px;
      border: 1px solid #E2E8F0;
      margin-bottom: 28px;
    }}
    .score-box {{
      text-align: center;
    }}
    .score-label {{
      font-size: 0.7rem;
      text-transform: uppercase;
      color: #64748B;
      font-weight: 600;
    }}
    .score-val {{
      font-size: 1.25rem;
      font-weight: 700;
      font-family: 'JetBrains Mono', monospace;
      color: #1E293B;
    }}
    .section {{
      margin-bottom: 24px;
    }}
    .section-title {{
      font-size: 1rem;
      font-weight: 600;
      color: #0F5257;
      border-bottom: 1px solid #E2E8F0;
      padding-bottom: 4px;
      margin-bottom: 12px;
    }}
    ul {{
      padding-left: 20px;
      margin: 0;
    }}
    li {{
      margin-bottom: 8px;
    }}
    .footer {{
      margin-top: 40px;
      padding-top: 16px;
      border-top: 1px solid #E2E8F0;
      font-size: 0.75rem;
      color: #94A3B8;
      text-align: center;
    }}
  </style>
</head>
<body>
  <div class="report-card">
    <div class="header">
      <div>
        <h1 class="title">{vacancy.title}</h1>
        <p class="subtitle"><strong>{vacancy.organization}</strong> &bull; {vacancy.grade_or_level} &bull; {vacancy.practical.location}</p>
        <p class="subtitle" style="margin-top: 4px;">Candidate: <strong>{profile.candidate_name}</strong></p>
      </div>
      <div>
        <span class="status-badge">{fit_res.overall_status}</span>
      </div>
    </div>

    <div class="grid-scores">
      <div class="score-box">
        <div class="score-label">Formal Eligibility</div>
        <div class="score-val">{fit_res.formal_eligibility_score}</div>
      </div>
      <div class="score-box">
        <div class="score-label">Substantive Fit</div>
        <div class="score-val">{fit_res.substantive_fit_score}</div>
      </div>
      <div class="score-box">
        <div class="score-label">Strategic Value</div>
        <div class="score-val">{fit_res.strategic_value_score}</div>
      </div>
      <div class="score-box">
        <div class="score-label">Practical Value</div>
        <div class="score-val">{fit_res.practical_value_score}</div>
      </div>
    </div>

    <div class="section">
      <h2 class="section-title">CyBOK &amp; NICE Framework Taxonomy</h2>
      <p><strong>Primary Category:</strong> {cybok.primary_category.value if cybok else 'N/A'}</p>
      <p><strong>NICE Role Alignment:</strong> {cybok.nice_framework_role if cybok else 'N/A'}</p>
    </div>

    {f'''
    <div class="section">
      <h2 class="section-title">Recruiter Intelligence &amp; Certification Roadmap</h2>
      <p><strong>Domain Target:</strong> {rec.certification_roadmap.domain_category} | <strong>Potential Max Score:</strong> {rec.potential_max_score}/100</p>
      <ul style="list-style:none; padding-left:0; margin-top:8px;">
        {certs_html}
      </ul>
    </div>
    ''' if rec else ''}

    <div class="section">
      <h2 class="section-title">Executive Summary</h2>
      <p>{brief.executive_summary}</p>
    </div>

    <div class="section">
      <h2 class="section-title">Key Selling Points for Motivation &amp; Cover Letter</h2>
      <ul>
        {''.join([f"<li><strong>{pt}</strong></li>" for pt in brief.key_selling_points])}
      </ul>
    </div>

    <div class="section">
      <h2 class="section-title">Tailored Experience Bullets for CV</h2>
      <ul>
        {''.join([f"<li>{bullet}</li>" for bullet in brief.tailored_experience_bullets])}
      </ul>
    </div>

    <div class="section">
      <h2 class="section-title">Gap Mitigation &amp; Advice</h2>
      <ul>
        {''.join([f"<li>{adv}</li>" for adv in brief.gap_mitigation_advice])}
      </ul>
    </div>

    <div class="footer">
      Generated by AEGIS-LEDGER &bull; {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} &bull; Personal Confidential Career Evidence
    </div>
  </div>
</body>
</html>
"""
    return html
