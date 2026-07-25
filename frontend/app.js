/**
 * AEGIS-LEDGER Dashboard, Radar Chart, Brief Generator, CV Analyzer & Recruiter Advisor Logic
 */

let allVacancies = [];
let currentProfile = {};
let activeBriefMarkdown = '';
let activeBriefId = '';
let activeCvVacancyId = '';

const PRESET_SCENARIOS = {
  current: {
    candidate_name: 'Vasileios Tsalikidis (Current)',
    nationalities: ['Greek', 'EU', 'NATO'],
    degree_level: 'Master',
    total_experience_years: 8,
    cyber_experience_years: 5,
    clearance_held: 'National Secret / NATO Secret eligible',
    languages_proficient: ['English', 'Greek'],
    skills_and_domains: ['CIS', 'INFOSEC', 'COMSEC', 'CTI', 'SOC', 'GRC', 'NIST CSF', 'OWASP', 'MITRE ATT&CK', 'Python', 'NATO', 'EU'],
    certifications_held: ['PM2 Advanced', 'Security+ Eligible', 'CISSP Candidate']
  },
  post_thesis: {
    candidate_name: 'Vasileios Tsalikidis (Post-Thesis Target)',
    nationalities: ['Greek', 'EU', 'NATO'],
    degree_level: 'Master',
    total_experience_years: 9,
    cyber_experience_years: 6,
    clearance_held: 'NATO SECRET / SECRET UE',
    languages_proficient: ['English', 'Greek', 'French'],
    skills_and_domains: ['CIS', 'INFOSEC', 'COMSEC', 'CTI', 'SOC', 'GRC', 'NIST CSF', 'OWASP', 'MITRE ATT&CK', 'Python', 'Neo4j', 'Knowledge Graphs', 'NATO', 'EU'],
    certifications_held: ['CISSP', 'ISO 27001 LA', 'PM2 Advanced']
  },
  nato_specialist: {
    candidate_name: 'Vasileios Tsalikidis (NATO CIS/COMSEC Focus)',
    nationalities: ['Greek', 'EU', 'NATO'],
    degree_level: 'Master',
    total_experience_years: 10,
    cyber_experience_years: 7,
    clearance_held: 'COSMIC TOP SECRET',
    languages_proficient: ['English', 'Greek'],
    skills_and_domains: ['CIS', 'COMSEC', 'INFOSEC', 'NATO CIS', 'Crypto', 'Networks', 'NATO', 'EU', 'Service Management', 'PM2'],
    certifications_held: ['CISSP', 'Security+', 'CCNP Security', 'NATO IA']
  }
};

document.addEventListener('DOMContentLoaded', () => {
  initApp();
  setupListeners();
});

async function initApp() {
  await fetchProfile();
  await fetchVacancies();
}

async function fetchProfile() {
  try {
    const res = await fetch('/api/profile');
    if (!res.ok) throw new Error('Failed to fetch profile');
    currentProfile = await res.json();
    populateProfileForm(currentProfile);
    document.getElementById('stat-candidate-name').textContent = currentProfile.candidate_name || 'Vasileios Tsalikidis';
  } catch (err) {
    console.error('Profile fetch error, using default candidate profile', err);
    currentProfile = PRESET_SCENARIOS.current;
    populateProfileForm(currentProfile);
  }
}

async function fetchVacancies() {
  try {
    const res = await fetch('/api/vacancies');
    if (!res.ok) throw new Error('API fetch error');
    allVacancies = await res.json();
    render();
  } catch (err) {
    console.error('Failed to fetch vacancies from API, using fallback data', err);
    renderFallback();
  }
}

function setupListeners() {
  // Scenario Selector
  document.getElementById('scenario-selector').addEventListener('change', async (e) => {
    const val = e.target.value;
    if (PRESET_SCENARIOS[val]) {
      currentProfile = PRESET_SCENARIOS[val];
      populateProfileForm(currentProfile);
      document.getElementById('stat-candidate-name').textContent = currentProfile.candidate_name;

      try {
        await fetch('/api/profile', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(currentProfile)
        });
        await fetchVacancies();
      } catch (err) {
        console.error('Scenario switch save error', err);
      }
    }
  });

  // Filters
  document.getElementById('filter-status').addEventListener('change', render);
  document.getElementById('filter-tier').addEventListener('change', render);
  document.getElementById('filter-search').addEventListener('input', render);

  // Profile Modal
  const modalProfile = document.getElementById('modal-profile');
  document.getElementById('btn-open-profile').addEventListener('click', () => modalProfile.classList.add('active'));
  document.getElementById('close-profile').addEventListener('click', () => modalProfile.classList.remove('active'));
  document.getElementById('cancel-profile').addEventListener('click', () => modalProfile.classList.remove('active'));

  // Profile Form Submit
  document.getElementById('form-profile').addEventListener('submit', async (e) => {
    e.preventDefault();
    const updatedProfile = {
      candidate_name: document.getElementById('prof-name').value.trim(),
      nationalities: document.getElementById('prof-nats').value.split(',').map(s => s.trim()).filter(Boolean),
      degree_level: document.getElementById('prof-degree').value,
      total_experience_years: parseInt(document.getElementById('prof-exp-total').value) || 0,
      cyber_experience_years: parseInt(document.getElementById('prof-exp-cyber').value) || 0,
      clearance_held: document.getElementById('prof-clearance').value.trim(),
      languages_proficient: document.getElementById('prof-languages').value.split(',').map(s => s.trim()).filter(Boolean),
      skills_and_domains: document.getElementById('prof-skills').value.split(',').map(s => s.trim()).filter(Boolean),
      certifications_held: (currentProfile.certifications_held || ['CISSP Candidate'])
    };

    try {
      const res = await fetch('/api/profile', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(updatedProfile)
      });
      if (res.ok) {
        modalProfile.classList.remove('active');
        await initApp();
      }
    } catch (err) {
      alert('Error saving profile: ' + err.message);
    }
  });

  // Add Vacancy Modal
  const modalAdd = document.getElementById('modal-add-vacancy');
  document.getElementById('btn-open-add-vacancy').addEventListener('click', () => {
    document.getElementById('vac-id').value = 'VAC-' + String(allVacancies.length + 1).padStart(3, '0');
    modalAdd.classList.add('active');
  });
  document.getElementById('close-add-vacancy').addEventListener('click', () => modalAdd.classList.remove('active'));
  document.getElementById('cancel-add-vacancy').addEventListener('click', () => modalAdd.classList.remove('active'));

  // Add Vacancy Submit
  document.getElementById('form-add-vacancy').addEventListener('submit', async (e) => {
    e.preventDefault();
    const newVacancy = {
      id: document.getElementById('vac-id').value.trim(),
      title: document.getElementById('vac-title').value.trim(),
      organization: document.getElementById('vac-org').value.trim(),
      grade_or_level: document.getElementById('vac-grade').value.trim() || 'N/A',
      eligibility: {
        allowed_nationalities: ['EU', 'NATO'],
        min_degree_level: document.getElementById('vac-min-degree').value,
        min_experience_years: parseInt(document.getElementById('vac-min-exp').value) || 0,
        security_clearance_required: document.getElementById('vac-clearance').value.trim() || 'None',
        required_languages: ['English']
      },
      requirements: {
        domains: document.getElementById('vac-domains').value.split(',').map(s => s.trim()).filter(Boolean),
        frameworks: ['NIST CSF'],
        technologies: ['Python'],
        nato_eu_context: true
      },
      strategic: {
        org_tier: parseInt(document.getElementById('vac-tier').value) || 2,
        brand_value_score: 80,
        stepping_stone_score: 80,
        ecosystem_alignment: true
      },
      practical: {
        estimated_monthly_net_eur: parseFloat(document.getElementById('vac-salary').value) || null,
        location: document.getElementById('vac-location').value.trim() || 'Brussels, Belgium',
        country: 'EU',
        contract_type: 'Temporary Agent',
        remote_policy: 'Hybrid'
      },
      provenance: {
        source_url: document.getElementById('vac-url').value.trim(),
        is_official_source: true,
        verified_at: new Date().toISOString().split('T')[0]
      },
      milestones: [{ status: 'Identified', notes: 'Added via Dashboard UI' }]
    };

    try {
      const res = await fetch('/api/vacancies', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newVacancy)
      });
      if (res.ok) {
        modalAdd.classList.remove('active');
        document.getElementById('form-add-vacancy').reset();
        await fetchVacancies();
      }
    } catch (err) {
      alert('Error adding vacancy: ' + err.message);
    }
  });

  // Brief Modal Listeners
  const modalBrief = document.getElementById('modal-brief');
  document.getElementById('close-brief').addEventListener('click', () => modalBrief.classList.remove('active'));
  document.getElementById('close-brief-btn').addEventListener('click', () => modalBrief.classList.remove('active'));
  document.getElementById('print-html-btn').addEventListener('click', () => {
    if (activeBriefId) {
      window.open(`/api/vacancies/${activeBriefId}/export-html`, '_blank');
    }
  });
  document.getElementById('download-brief-btn').addEventListener('click', () => {
    if (!activeBriefMarkdown) return;
    const blob = new Blob([activeBriefMarkdown], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `Application_Brief_${activeBriefId}.md`;
    a.click();
    URL.revokeObjectURL(url);
  });

  // CV Analyzer Modal Listeners
  const modalCv = document.getElementById('modal-cv-analyzer');
  document.getElementById('close-cv-analyzer').addEventListener('click', () => modalCv.classList.remove('active'));
  document.getElementById('close-cv-btn').addEventListener('click', () => modalCv.classList.remove('active'));
  document.getElementById('run-cv-analysis-btn').addEventListener('click', async () => {
    const text = document.getElementById('cv-text-input').value.trim();
    if (!text) {
      alert('Please paste CV text before running analysis.');
      return;
    }

    try {
      const res = await fetch(`/api/vacancies/${activeCvVacancyId}/analyze-cv`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ cv_text: text })
      });
      if (!res.ok) throw new Error('CV analysis API error');
      const data = await res.json();
      renderCvResults(data.coverage);
    } catch (err) {
      alert('CV Analysis error: ' + err.message);
    }
  });
}

function populateProfileForm(prof) {
  document.getElementById('prof-name').value = prof.candidate_name || '';
  document.getElementById('prof-nats').value = (prof.nationalities || []).join(', ');
  document.getElementById('prof-degree').value = prof.degree_level || 'Master';
  document.getElementById('prof-exp-total').value = prof.total_experience_years || 0;
  document.getElementById('prof-exp-cyber').value = prof.cyber_experience_years || 0;
  document.getElementById('prof-clearance').value = prof.clearance_held || '';
  document.getElementById('prof-languages').value = (prof.languages_proficient || []).join(', ');
  document.getElementById('prof-skills').value = (prof.skills_and_domains || []).join(', ');
}

function render() {
  const statusFilter = document.getElementById('filter-status').value;
  const tierFilter = document.getElementById('filter-tier').value;
  const searchQuery = document.getElementById('filter-search').value.toLowerCase().trim();

  const filtered = allVacancies.filter(item => {
    const res = item.fit_result || {};
    const status = res.overall_status || 'Eligible';
    const tier = item.strategic?.org_tier || 2;

    if (statusFilter !== 'ALL' && status !== statusFilter) return false;
    if (tierFilter !== 'ALL' && String(tier) !== tierFilter) return false;

    if (searchQuery) {
      const haystack = `${item.id} ${item.organization} ${item.title} ${item.grade_or_level}`.toLowerCase();
      if (!haystack.includes(searchQuery)) return false;
    }
    return true;
  });

  // Update Stats
  document.getElementById('stat-total').textContent = allVacancies.length;
  document.getElementById('stat-eligible').textContent = allVacancies.filter(v => (v.fit_result?.overall_status || '') === 'Eligible').length;
  document.getElementById('stat-tier1').textContent = allVacancies.filter(v => v.strategic?.org_tier === 1).length;
  document.getElementById('list-count').textContent = `${filtered.length} of ${allVacancies.length} items`;

  const container = document.getElementById('vacancy-list');
  if (filtered.length === 0) {
    container.innerHTML = '<div class="panel">No vacancies match the selected filter criteria.</div>';
    return;
  }

  container.innerHTML = filtered.map(item => {
    const res = item.fit_result || {};
    const status = res.overall_status || 'Eligible';
    const pillClass = status === 'Eligible' ? 'pill-eligible' : status === 'Conditional' ? 'pill-conditional' : 'pill-disqualified';
    const observations = res.observations || [];
    const cybok = res.cybok_mapping?.primary_category || 'CyBOK Mapped';

    const ppp = item.practical?.purchasing_power || {};
    const pppText = ppp.ppp_adjusted_net_eur ? `PPP Equiv: €${Math.round(ppp.ppp_adjusted_net_eur)}/mo (${ppp.ppp_multiplier}x)` : '';

    return `
      <div class="vacancy-card">
        <div class="card-top">
          <div>
            <span class="org-name">${escapeHtml(item.organization)} &bull; ${escapeHtml(item.grade_or_level)}</span>
            <h3 class="vacancy-title">${escapeHtml(item.title)}</h3>
            <span class="cybok-badge">CyBOK: ${escapeHtml(cybok)}</span>
            ${pppText ? `<span class="ppp-badge">${escapeHtml(pppText)}</span>` : ''}
          </div>
          <div style="display:flex; gap:8px; align-items:center; flex-wrap:wrap;">
            <span class="status-pill ${pillClass}">${status}</span>
            <button class="btn btn-outline" onclick="openCvAnalyzer('${item.id}', '${escapeHtml(item.title)}')">CV Match</button>
            <button class="btn btn-outline" onclick="openBriefModal('${item.id}')">Brief</button>
            <button class="btn btn-danger" onclick="deleteVacancy('${item.id}')">Delete</button>
          </div>
        </div>

        <div class="card-body-row">
          <div>
            <div class="scores-row">
              <div class="score-box">
                <span class="score-name">Formal Elig.</span>
                <span class="score-val">${res.formal_eligibility_score ?? '-'}</span>
              </div>
              <div class="score-box">
                <span class="score-name">Substantive</span>
                <span class="score-val">${res.substantive_fit_score ?? '-'}</span>
              </div>
              <div class="score-box">
                <span class="score-name">Strategic</span>
                <span class="score-val">${res.strategic_value_score ?? '-'}</span>
              </div>
              <div class="score-box">
                <span class="score-name">Practical</span>
                <span class="score-val">${res.practical_value_score ?? '-'}</span>
              </div>
            </div>

            ${observations.length > 0 ? `
              <ul class="obs-list">
                ${observations.slice(0, 3).map(o => `<li>&bull; ${escapeHtml(o)}</li>`).join('')}
              </ul>
            ` : ''}
          </div>

          <div class="radar-chart-container">
            ${renderRadarSVG(res)}
          </div>
        </div>

        <div class="card-footer">
          <span>Location: <strong>${escapeHtml(item.practical?.location || 'N/A')}</strong></span>
          <span>Source: <strong>${item.provenance?.is_official_source ? 'Official Portal' : 'Aggregator'}</strong></span>
          <a href="${escapeHtml(item.provenance?.source_url || '#')}" target="_blank" rel="noopener" class="source-link">View Portal Announcement &rarr;</a>
        </div>
      </div>
    `;
  }).join('');
}

function renderRadarSVG(res) {
  const f = (res.formal_eligibility_score || 0) / 100;
  const s = (res.substantive_fit_score || 0) / 100;
  const st = (res.strategic_value_score || 0) / 100;
  const p = (res.practical_value_score || 0) / 100;

  const cx = 60, cy = 60, r = 45;
  const pTop = [cx, cy - r * f];
  const pRight = [cx + r * s, cy];
  const pBottom = [cx, cy + r * st];
  const pLeft = [cx - r * p, cy];

  const points = `${pTop[0]},${pTop[1]} ${pRight[0]},${pRight[1]} ${pBottom[0]},${pBottom[1]} ${pLeft[0]},${pLeft[1]}`;

  return `
    <svg width="120" height="120" viewBox="0 0 120 120">
      <circle cx="${cx}" cy="${cy}" r="${r}" fill="#FAF9F6" stroke="#E2E8F0" stroke-width="1"/>
      <circle cx="${cx}" cy="${cy}" r="${r * 0.5}" fill="none" stroke="#E2E8F0" stroke-dasharray="2,2"/>
      <line x1="${cx}" y1="${cy - r}" x2="${cx}" y2="${cy + r}" stroke="#CBD5E1"/>
      <line x1="${cx - r}" y1="${cy}" x2="${cx + r}" y2="${cy}" stroke="#CBD5E1"/>
      <polygon points="${points}" fill="rgba(15, 82, 87, 0.15)" stroke="#0F5257" stroke-width="1.5"/>
    </svg>
  `;
}

async function openBriefModal(id) {
  try {
    const res = await fetch(`/api/vacancies/${id}/brief`);
    if (!res.ok) throw new Error('Brief fetch error');
    const data = await res.json();
    const brief = data.brief;
    activeBriefMarkdown = data.markdown;
    activeBriefId = id;

    const rec = brief.recruiter_advice;
    const certsHtml = rec ? rec.certification_roadmap.target_certifications.map(c => `
      <span class="kw-badge ${c.held ? 'kw-matched' : 'kw-missing'}">
        ${c.held ? '[HELD]' : '[TARGET]'}: ${escapeHtml(c.name)} (${escapeHtml(c.code)}) - ${c.priority}
      </span>
    `).join('') : '';

    const metricsHtml = rec ? rec.quantifiable_impact_templates.map(m => `
      <li style="margin-bottom: 8px;">
        <strong>${escapeHtml(m.category)}:</strong> <em>"${escapeHtml(m.template_bullet)}"</em><br>
        <span style="font-size: 0.75rem; color: var(--text-muted);">&bull; Recruiter Tip: ${escapeHtml(m.guidance)}</span>
      </li>
    `).join('') : '';

    const stepsHtml = rec ? rec.score_booster_steps.map(s => `
      <li><strong>Step ${s.step_number}: ${escapeHtml(s.title)} (+${s.score_delta} pts)</strong> - ${escapeHtml(s.action_item)}</li>
    `).join('') : '';

    const modalBody = document.getElementById('brief-modal-body');
    modalBody.innerHTML = `
      <div class="brief-section">
        <h3>Executive Summary</h3>
        <p>${escapeHtml(brief.executive_summary)}</p>
      </div>

      ${rec ? `
      <div class="brief-section" style="background: #E6F4F1; padding: 16px; border-radius: 6px; border: 1px solid #B8E2DA;">
        <h3 style="color: #0F5257;">Recruiter Intelligence &amp; Certification Roadmap</h3>
        <p style="font-size: 0.85rem; margin-bottom: 8px;">
          <strong>Target Domain:</strong> ${escapeHtml(rec.certification_roadmap.domain_category)} &bull; 
          <strong>Potential Max Score:</strong> <span style="font-weight:700; color:#0F5257;">${rec.potential_max_score}/100</span>
        </p>
        <div style="margin-bottom: 12px;">${certsHtml}</div>
        
        <h4 style="font-size: 0.85rem; font-weight: 600; margin-top: 12px; margin-bottom: 6px;">Quantifiable Impact Metrics for Recruiters</h4>
        <ul style="padding-left: 16px; font-size: 0.85rem;">${metricsHtml}</ul>

        <h4 style="font-size: 0.85rem; font-weight: 600; margin-top: 12px; margin-bottom: 6px;">Score Booster Roadmap</h4>
        <ol style="padding-left: 16px; font-size: 0.85rem;">${stepsHtml}</ol>
      </div>
      ` : ''}

      <div class="brief-section">
        <h3>Key Selling Points (Motivation &amp; Cover Letter)</h3>
        <ul>
          ${brief.key_selling_points.map(pt => `<li>${escapeHtml(pt)}</li>`).join('')}
        </ul>
      </div>

      <div class="brief-section">
        <h3>Tailored Experience Bullets (CV)</h3>
        <ul>
          ${brief.tailored_experience_bullets.map(b => `<li>${escapeHtml(b)}</li>`).join('')}
        </ul>
      </div>

      <div class="brief-section">
        <h3>Gap Mitigation &amp; Advice</h3>
        <ul>
          ${brief.gap_mitigation_advice.map(a => `<li>${escapeHtml(a)}</li>`).join('')}
        </ul>
      </div>
    `;

    document.getElementById('brief-modal-title').textContent = `Application Brief: ${brief.vacancy_title} (${brief.organization})`;
    document.getElementById('modal-brief').classList.add('active');
  } catch (err) {
    alert('Error loading brief: ' + err.message);
  }
}

function openCvAnalyzer(id, title) {
  activeCvVacancyId = id;
  document.getElementById('cv-modal-title').textContent = `CV Coverage Analyzer: ${title}`;
  document.getElementById('cv-analysis-results').style.display = 'none';
  document.getElementById('modal-cv-analyzer').classList.add('active');
}

function renderCvResults(cov) {
  const container = document.getElementById('cv-analysis-results');
  container.style.display = 'block';

  container.innerHTML = `
    <div style="background: #FAF9F6; padding: 16px; border-radius: 6px; border: 1px solid #E2E8F0; margin-bottom: 16px;">
      <h3 style="font-size: 1.05rem; color: #0F5257; margin-bottom: 6px;">
        Coverage Percentage: <strong>${cov.coverage_percentage}%</strong> (${cov.matched_keywords.length}/${cov.total_required_keywords} target terms)
      </h3>
    </div>

    <div class="brief-section">
      <h3>Matched Keywords in CV</h3>
      <div>
        ${cov.matched_keywords.length > 0 ? cov.matched_keywords.map(k => `<span class="kw-badge kw-matched">[MATCHED] ${escapeHtml(k)}</span>`).join('') : '<span class="text-muted">None</span>'}
      </div>
    </div>

    <div class="brief-section" style="margin-top: 12px;">
      <h3>Missing Keywords to Add</h3>
      <div>
        ${cov.missing_keywords.length > 0 ? cov.missing_keywords.map(k => `<span class="kw-badge kw-missing">[MISSING] ${escapeHtml(k)}</span>`).join('') : '<span class="text-muted">None</span>'}
      </div>
    </div>

    <div class="brief-section" style="margin-top: 12px;">
      <h3>Recommendations</h3>
      <ul>
        ${cov.recommendations.map(r => `<li>${escapeHtml(r)}</li>`).join('')}
      </ul>
    </div>
  `;
}

async function deleteVacancy(id) {
  if (!confirm(`Are you sure you want to delete vacancy ${id}?`)) return;
  try {
    const res = await fetch(`/api/vacancies/${id}`, { method: 'DELETE' });
    if (res.ok) {
      await fetchVacancies();
    }
  } catch (err) {
    alert('Delete error: ' + err.message);
  }
}

function renderFallback() {
  allVacancies = [
    {
      id: 'VAC-001',
      title: 'ICT Security Coordinator',
      organization: 'ENISA',
      grade_or_level: 'AD 7',
      fit_result: { formal_eligibility_score: 100, substantive_fit_score: 95, strategic_value_score: 90, practical_value_score: 85, overall_status: 'Eligible', observations: ['Degree requirement met', 'NATO/EU context matched'] },
      strategic: { org_tier: 1 },
      practical: { location: 'Athens, Greece' },
      provenance: { is_official_source: true, source_url: 'https://www.enisa.europa.eu' }
    }
  ];
  render();
}

function escapeHtml(str) {
  if (!str) return '';
  return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}
