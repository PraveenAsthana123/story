// ===== RGAIG+ Portal - Render Functions =====

function renderLayers() {
  const el = document.getElementById('layerStack');
  if (!el) return;
  el.innerHTML = layers.map(l => `<div class="layer-card" style="background:${l.color};color:${l.textColor}" onclick="this.classList.toggle('expanded')">
    <div class="layer-num">L${l.n}</div>
    <div class="layer-info"><h5>${l.name}</h5><p>${l.desc}</p>
    <div style="font-size:.7rem;opacity:.6"><i class="fas fa-certificate me-1"></i>${l.standards}</div>
    <div class="layer-detail">${l.controls}</div></div></div>`).join('');
}

function renderPillars() {
  const el = document.getElementById('pillarGrid');
  if (!el) return;
  el.innerHTML = pillars.map(p => `<div class="col-6 col-md-4 col-lg-3 col-xl-2"><div class="pillar-card">
    <div class="pillar-icon" style="background:${p.color}"><i class="fas ${p.icon}"></i></div>
    <h5 style="font-size:.9rem">${p.name}</h5><p style="font-size:.75rem">${p.desc}</p>
    <div style="font-size:1.4rem;font-weight:800;color:var(--success)">${p.rate}</div>
    <div style="font-size:.6rem;text-transform:uppercase;letter-spacing:1px;color:var(--gray-600)">Pass Rate</div>
    </div></div>`).join('');
}

function renderPillarDeep() {
  const el = document.getElementById('pillarDeep');
  if (!el) return;
  el.innerHTML = pillars.map(p => `<div class="col-12 mb-4">
    <div class="card-white" style="border-left:5px solid ${p.color}">
    <div style="display:flex;align-items:center;gap:.8rem;margin-bottom:1rem;cursor:pointer" onclick="this.parentElement.querySelector('.pillar-expand').classList.toggle('d-none')">
    <div style="width:50px;height:50px;border-radius:50%;background:${p.color};color:#fff;display:flex;align-items:center;justify-content:center;font-size:1.3rem;flex-shrink:0"><i class="fas ${p.icon}"></i></div>
    <div style="flex:1"><h5 style="margin:0;color:var(--green-dark);font-size:1.1rem">${p.name} <span class="badge" style="background:${p.color};font-size:.7rem">${p.rate}</span></h5>
    <p style="margin:0;font-size:.82rem;color:var(--gray-600)">${p.details}</p></div>
    <i class="fas fa-chevron-down" style="color:var(--gray-600)"></i></div>
    <div class="pillar-expand d-none">
    <div class="row g-3">
    <div class="col-md-4"><div class="p-2 rounded bg-green-soft"><h6 style="font-size:.82rem;color:var(--green-dark)"><i class="fas fa-clipboard-question me-1"></i>Assessment Questions</h6>
    ${p.questions?p.questions.map(q=>`<div style="font-size:.75rem;padding:.2rem 0;border-bottom:1px solid rgba(0,0,0,.05)">${q}</div>`).join(''):''}</div></div>
    <div class="col-md-4"><div class="p-2 rounded bg-maroon-soft"><h6 style="font-size:.82rem;color:var(--maroon)"><i class="fas fa-wrench me-1"></i>Tools & Solutions</h6>
    <div style="font-size:.72rem;font-weight:600;color:var(--navy);margin-bottom:.2rem">Tools:</div>
    ${p.tools?p.tools.map(t=>`<div style="font-size:.72rem">&bull; ${t}</div>`).join(''):''}
    <div style="font-size:.72rem;font-weight:600;color:var(--navy);margin:.3rem 0 .2rem">Solutions:</div>
    ${p.solutions?p.solutions.map(s=>`<div style="font-size:.72rem">&bull; ${s}</div>`).join(''):''}</div></div>
    <div class="col-md-4"><div class="p-2 rounded" style="background:rgba(0,48,87,.05)"><h6 style="font-size:.82rem;color:var(--navy)"><i class="fas fa-triangle-exclamation me-1"></i>Challenges & Edge Cases</h6>
    <div style="font-size:.72rem;font-weight:600;color:var(--maroon);margin-bottom:.2rem">Challenges:</div>
    ${p.challenges?p.challenges.map(c=>`<div style="font-size:.72rem">&bull; ${c}</div>`).join(''):''}
    <div style="font-size:.72rem;font-weight:600;color:var(--maroon);margin:.3rem 0 .2rem">Edge Cases:</div>
    ${p.edgeCases?p.edgeCases.map(e=>`<div style="font-size:.72rem">&bull; ${e}</div>`).join(''):''}</div></div>
    </div>
    <div class="mt-3"><h6 style="font-size:.82rem;color:var(--green-dark)"><i class="fas fa-road me-1"></i>Implementation Planning</h6>
    <div class="flow-container" style="padding:.3rem">${p.planning?p.planning.map((ph,i)=>`${i>0?'<div class="flow-arrow"><i class="fas fa-arrow-right"></i></div>':''}<div class="flow-box" style="background:${p.color};min-width:160px;font-size:.7rem">${ph}</div>`).join(''):''}</div></div>
    </div></div></div>`).join('');
}

function renderChannels() {
  const el = document.getElementById('channelGrid');
  if (!el) return;
  el.innerHTML = channelConfigs.map(c => `<div class="col-md-4 col-lg-2">
    <div class="channel-card">
    <div class="channel-count">${c.ch}</div>
    <div style="font-size:.7rem;color:var(--gold);text-transform:uppercase;letter-spacing:1px">Channels</div>
    <h6 style="color:#fff;font-size:.85rem;margin:.5rem 0">${c.name}</h6>
    <div style="font-size:.65rem;color:rgba(255,255,255,.5);text-transform:uppercase">${c.grade} Grade</div>
    <div style="margin-top:.8rem;font-size:.72rem;color:rgba(255,255,255,.7)">
    <div><strong>Positions:</strong> ${c.positions}</div>
    <div><strong>Resolution:</strong> ${c.resolution}</div>
    <div><strong>Use:</strong> ${c.useCase}</div>
    <div><strong>Accuracy:</strong> ${c.accuracy}</div>
    <div><strong>Cost:</strong> ${c.cost}</div>
    <div><strong>Diseases:</strong> ${c.diseases.join(', ')}</div>
    </div></div></div>`).join('');
}

function renderDiseases() {
  const el = document.getElementById('diseaseGrid');
  if (!el) return;
  el.innerHTML = diseases.map(d => `<div class="col-md-4 col-lg"><div class="disease-card">
    <div class="disease-header" style="background:${d.color}"><i class="fas fa-brain fa-2x mb-2"></i><h5 style="margin:0">${d.name}</h5></div>
    <div class="disease-body">
    <div class="metric"><span>Accuracy</span><span>${d.acc}</span></div>
    <div class="metric"><span>F1 Score</span><span>${d.f1}</span></div>
    <div class="metric"><span>AUC</span><span>${d.auc}</span></div>
    <div class="metric"><span>Subjects</span><span>${d.subjects}</span></div>
    <div class="metric"><span>Channels</span><span>${d.channels}</span></div>
    <div class="metric"><span>Impact</span><span style="font-size:.72rem">${d.impact}</span></div>
    <div style="margin-top:.5rem;padding-top:.5rem;border-top:1px solid var(--gray-100)">
    <div style="font-size:.72rem;font-weight:700;color:var(--navy);margin-bottom:.3rem">EEG Pattern</div>
    <div style="font-size:.7rem;color:var(--gray-600)">${d.eegPattern}</div></div>
    <div style="margin-top:.5rem;padding-top:.5rem;border-top:1px solid var(--gray-100)">
    <div style="font-size:.72rem;font-weight:700;color:var(--navy);margin-bottom:.3rem">Key Papers</div>
    ${d.papers.map(p => `<div style="font-size:.68rem;color:var(--gray-600)">&bull; ${p}</div>`).join('')}
    </div></div></div></div>`).join('');
}

function renderIndustries() {
  const el = document.getElementById('industryGrid');
  if (!el) return;
  el.innerHTML = industries.map(ind => `<div class="col-md-6 col-lg-3"><div class="industry-card">
    <div class="industry-header" style="background:${ind.bg}"><i class="fas ${ind.icon} fa-2x mb-1"></i><h5>${ind.name}</h5>
    <span class="badge" style="background:var(--gold);color:var(--navy)">${ind.maturity}</span></div>
    <div class="industry-body"><ul>${ind.items.map(i => `<li>${i}</li>`).join('')}</ul></div></div></div>`).join('');
}

function renderComparison() {
  const el = document.getElementById('comparisonTable');
  if (!el) return;
  let html = `<thead><tr>${compHeaders.map(h => `<th>${h}</th>`).join('')}</tr></thead><tbody>`;
  compCaps.forEach(row => {
    html += `<tr>${row.map((c, i) => {
      if (i === 0) return `<td>${c}</td>`;
      if (c === 'check') return `<td class="check"><i class="fas fa-check-circle"></i></td>`;
      if (c === 'partial') return `<td class="partial">Partial</td>`;
      return `<td class="dash">&mdash;</td>`;
    }).join('')}</tr>`;
  });
  html += `<tr style="background:var(--gray-50);font-weight:700"><td>Total (of 15)</td><td class="text-center">3</td><td class="text-center">3</td><td class="text-center">3</td><td class="text-center">3</td><td class="text-center" style="color:var(--success)">15</td></tr></tbody>`;
  el.innerHTML = html;
}

function renderIsoNist() {
  const el = document.getElementById('isoNistTable');
  if (!el) return;
  let html = '<thead><tr><th>Dimension</th><th>ISO 42001</th><th>NIST AI RMF</th><th>RGAIG+</th></tr></thead><tbody>';
  isoNistComparison.forEach(r => {
    html += `<tr><td style="font-weight:600">${r.dim}</td><td>${r.iso}</td><td>${r.nist}</td><td style="color:var(--success);font-weight:600">${r.rgaig}</td></tr>`;
  });
  html += '</tbody>';
  el.innerHTML = html;
}

function renderPhases() {
  const el = document.getElementById('phaseGrid');
  if (!el) return;
  el.innerHTML = phases.map(p => `<div class="col-6 col-md-4 col-lg-3"><div class="p-2 rounded" style="background:rgba(255,255,255,.08)">
    <div style="display:flex;align-items:center;gap:.5rem">
    <div style="background:var(--gold);color:var(--navy);width:30px;height:30px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:.75rem;flex-shrink:0">P${p.n}</div>
    <div><div style="font-size:.78rem;font-weight:700;color:#fff">${p.name}</div>
    <div style="font-size:.62rem;color:rgba(255,255,255,.5)">${p.ch} | ${p.output}</div></div></div></div></div>`).join('');
}

function renderLifecycle() {
  const el = document.getElementById('lifecycleFlow');
  if (!el) return;
  el.innerHTML = lifecycleData.map(s => `<div class="lifecycle-stage">
    <div class="lifecycle-icon"><i class="fas ${s.icon}"></i></div><h6>${s.title}</h6><p>${s.desc}</p></div>`).join('');
}

function renderMLOps() {
  const el = document.getElementById('mlopsGrid');
  if (!el) return;
  el.innerHTML = mlopsStages.map((s, i) => `<div class="col-md-3 mb-3">
    <div class="card-white h-100" style="border-top:4px solid ${s.color}">
    <div style="display:flex;align-items:center;gap:.5rem;margin-bottom:.5rem">
    <div style="width:35px;height:35px;border-radius:50%;background:${s.color};color:#fff;display:flex;align-items:center;justify-content:center"><i class="fas ${s.icon}"></i></div>
    <h6 style="margin:0;font-size:.88rem;font-weight:700;color:var(--navy)">${s.name}</h6></div>
    <p style="font-size:.78rem;color:var(--gray-600);margin:0">${s.desc}</p></div></div>`).join('');
}

function renderLLMOps() {
  const el = document.getElementById('llmopsGrid');
  if (!el) return;
  el.innerHTML = llmopsStages.map(s => `<div class="col-md-3 mb-3">
    <div class="card-white h-100" style="border-top:4px solid ${s.color}">
    <div style="display:flex;align-items:center;gap:.5rem;margin-bottom:.5rem">
    <div style="width:35px;height:35px;border-radius:50%;background:${s.color};color:#fff;display:flex;align-items:center;justify-content:center"><i class="fas ${s.icon}"></i></div>
    <h6 style="margin:0;font-size:.88rem;font-weight:700;color:var(--navy)">${s.name}</h6></div>
    <p style="font-size:.78rem;color:var(--gray-600);margin:0">${s.desc}</p></div></div>`).join('');
}

function renderAssessment() {
  const el = document.getElementById('assessmentContent');
  if (!el) return;
  const aiQs = ['AI strategy documented?','Dedicated AI/ML team?','AI governance board?','Model monitoring in production?','AI ethics guidelines?','Data quality management?','AI risk framework?','AI bias testing?','Explainability required?','AI incident response plans?'];
  const dataQs = ['Data governance policy?','Data quality standards?','Data lineage tracking?','Privacy compliance (GDPR/HIPAA)?','Data security controls?','Data integration platform?','Data catalog maintained?','Data literacy training?'];
  const techQs = ['ML infrastructure (GPU/cloud)?','MLOps pipeline?','Automated deployment?','Scalability architecture?','Security hardening?','Monitoring dashboards?','CI/CD for ML models?','Cloud-native architecture?'];
  function makeTab(id, qs, active) {
    return `<div class="tab-pane fade ${active ? 'show active' : ''}" id="${id}"><form id="${id}Form">
    ${qs.map((q, i) => `<div class="assessment-question"><label>Q${i + 1}: ${q}</label>
    <div class="radio-group"><label><input type="radio" name="${id}_q${i}" value="3"> Yes</label><label><input type="radio" name="${id}_q${i}" value="1"> Partial</label><label><input type="radio" name="${id}_q${i}" value="0" checked> No</label></div></div>`).join('')}
    <button type="button" class="btn btn-gold mt-3" onclick="calcAssessment('${id}',${qs.length})"><i class="fas fa-chart-pie me-2"></i>Calculate</button>
    <div id="${id}Result" class="maturity-gauge" style="display:none"></div></form></div>`;
  }
  el.innerHTML = makeTab('aiReadiness', aiQs, true) + makeTab('dataReadiness', dataQs, false) + makeTab('techAssessment', techQs, false);
}

function calcAssessment(id, count) {
  const form = document.getElementById(id + 'Form');
  let score = 0;
  for (let i = 0; i < count; i++) { const v = form.querySelector(`input[name="${id}_q${i}"]:checked`); if (v) score += parseInt(v.value); }
  const max = count * 3, pct = Math.round(score / max * 100);
  let level, label;
  if (pct <= 20) { level = 1; label = 'Initial / Ad Hoc'; }
  else if (pct <= 40) { level = 2; label = 'Developing'; }
  else if (pct <= 60) { level = 3; label = 'Defined'; }
  else if (pct <= 80) { level = 4; label = 'Managed'; }
  else { level = 5; label = 'Optimizing'; }
  const res = document.getElementById(id + 'Result');
  res.style.display = 'block';
  res.innerHTML = `<div class="maturity-level">Level ${level}</div><div class="maturity-label">${label}</div><div style="font-size:1rem;color:var(--gray-600);margin-top:.5rem">Score: ${score}/${max} (${pct}%)</div>
  <div class="progress-bar-custom mt-2"><div class="progress-fill" style="width:${pct}%;background:linear-gradient(90deg,var(--navy),var(--gold))">${pct}%</div></div>`;
}

function renderSurveys() {
  const el = document.getElementById('surveyContent');
  if (!el) return;
  const likertLabels = ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree'];
  function makeTab(id, items, active, name) {
    return `<div class="tab-pane fade ${active ? 'show active' : ''}" id="${id}">
    <h5 style="color:var(--gold)">${name}</h5>
    <form id="${id}Form">${items.map((item, i) => `<div class="survey-item">
    <div class="item-text">${item.id}: ${item.text}</div>
    <div class="likert-scale">${likertLabels.map((l, j) => `<label><input type="radio" name="${id}_${i}" value="${j + 1}">${l}</label>`).join('')}</div>
    </div>`).join('')}
    <button type="button" class="btn btn-gold mt-3" onclick="calcSurvey('${id}',${items.length})"><i class="fas fa-paper-plane me-2"></i>Submit</button>
    <div id="${id}Result" class="mt-3" style="display:none"></div></form></div>`;
  }
  el.innerHTML = makeTab('surveyExpert', expertItems, true, 'Expert Panel (15 items)')
    + makeTab('surveyTAM', tamItems, false, 'TAM-TOE-RBV (22 items)')
    + makeTab('surveyTrust', trustItems, false, 'Clinical Trust (12 items)');
}

function calcSurvey(id, count) {
  const form = document.getElementById(id + 'Form');
  let total = 0, answered = 0;
  for (let i = 0; i < count; i++) { const v = form.querySelector(`input[name="${id}_${i}"]:checked`); if (v) { total += parseInt(v.value); answered++; } }
  if (answered === 0) { alert('Please answer at least one question.'); return; }
  const avg = (total / answered).toFixed(2);
  const res = document.getElementById(id + 'Result');
  res.style.display = 'block';
  res.innerHTML = `<div class="p-3 rounded" style="background:rgba(255,255,255,.1)">
  <p style="color:var(--gold);font-size:1.4rem;font-weight:800;margin:0">Average: ${avg} / 5.0</p>
  <p style="color:rgba(255,255,255,.7);margin:0">${answered}/${count} items | ${total} points</p></div>`;
}

function calculateROI() {
  const patients = parseInt(document.getElementById('roiPatients').value) || 50;
  const errorRate = parseInt(document.getElementById('roiError').value) || 15;
  const cost = parseInt(document.getElementById('roiCost').value) || 5000;
  const currentCost = patients * 365 * (errorRate / 100) * cost;
  const newError = Math.max(errorRate - (errorRate * 0.908), 1);
  const newCost = patients * 365 * (newError / 100) * cost;
  const savings = currentCost - newCost;
  const implCost = 250000;
  const roi = ((savings - implCost) / implCost * 100).toFixed(0);
  document.getElementById('roiOutput').innerHTML = `<div class="roi-result">${roi}% ROI</div>
  <p style="font-size:.85rem;color:var(--gray-600)">Annual savings: $${savings.toLocaleString()} | Implementation: $${implCost.toLocaleString()}</p>`;
}

function animateCounters() {
  document.querySelectorAll('.stat-number[data-target]').forEach(el => {
    const target = parseInt(el.dataset.target);
    let current = 0;
    const step = target / 60;
    const timer = setInterval(() => {
      current += step;
      if (current >= target) { current = target; clearInterval(timer); }
      el.textContent = Math.floor(current);
    }, 25);
  });
}

// ===== CHARTS =====
function initCharts() {
  // Accuracy Bar
  const accCtx = document.getElementById('accuracyChart');
  if (accCtx) new Chart(accCtx, { type: 'bar', data: { labels: diseases.map(d => d.name), datasets: [{ label: 'Accuracy (%)', data: [97.67, 100, 99.02, 94.17, 91.07], backgroundColor: diseases.map(d => d.color), borderRadius: 5 }] }, options: { responsive: true, plugins: { legend: { display: false } }, scales: { y: { beginAtZero: false, min: 85, max: 102, ticks: { callback: v => v + '%' } } } } });

  // Metrics Radar
  const mrCtx = document.getElementById('metricsRadar');
  if (mrCtx) new Chart(mrCtx, { type: 'radar', data: { labels: ['Accuracy', 'F1', 'AUC', 'Sensitivity', 'Specificity'], datasets: [
    { label: 'ASD', data: [97.67, 97.6, 98.3, 97.0, 98.3], borderColor: '#1f77b4', fill: false },
    { label: 'PD', data: [100, 100, 100, 100, 100], borderColor: '#ff7f0e', fill: false },
    { label: 'Epilepsy', data: [99.02, 99.0, 99.2, 98.8, 99.2], borderColor: '#2ca02c', fill: false },
    { label: 'Depression', data: [91.07, 90.8, 92.6, 89.5, 92.6], borderColor: '#9467bd', fill: false },
    { label: 'Stress', data: [94.17, 94.0, 95.3, 93.5, 94.8], borderColor: '#d62728', fill: false }
  ] }, options: { responsive: true, scales: { r: { min: 85, max: 102 } }, plugins: { legend: { position: 'bottom', labels: { font: { size: 10 } } } } } });

  // Pillar Radar
  const prCtx = document.getElementById('pillarRadar');
  if (prCtx) new Chart(prCtx, { type: 'radar', data: { labels: pillars.map(p => p.name), datasets: [
    { label: 'RGAIG+', data: [98.4, 98.7, 97.8, 98.1, 97.4, 98.2, 97.9, 98, 100, 98.5], backgroundColor: 'rgba(0,48,87,.15)', borderColor: '#003057' },
    { label: 'Industry Avg', data: [72, 68, 65, 70, 75, 55, 50, 45, 40, 60], backgroundColor: 'rgba(128,0,32,.15)', borderColor: '#800020' }
  ] }, options: { responsive: true, scales: { r: { min: 0, max: 100 } }, plugins: { legend: { position: 'bottom' } } } });

  // Taxonomy Donut
  const tdCtx = document.getElementById('taxonomyDonut');
  if (tdCtx) new Chart(tdCtx, { type: 'doughnut', data: { labels: ['Tier 1: ML/DL (111)', 'Tier 2: GenAI (220)', 'Tier 3: Pillars (194)'], datasets: [{ data: [111, 220, 194], backgroundColor: ['var(--green)', 'var(--maroon)', 'var(--navy)'] }] }, options: { responsive: true, plugins: { legend: { position: 'bottom', labels: { font: { size: 10 } } } } } });

  // Comparison Bar
  const cbCtx = document.getElementById('comparisonChart');
  if (cbCtx) new Chart(cbCtx, { type: 'bar', data: { labels: ['NIST AI RMF', 'ISO 42001', 'EU AI Act', 'RAISEF', 'RGAIG+'], datasets: [{ label: 'Capabilities (of 15)', data: [3, 3, 3, 3, 15], backgroundColor: ['var(--navy)', 'var(--teal)', 'var(--maroon)', 'var(--gray-600)', 'var(--gold)'], borderRadius: 5 }] }, options: { responsive: true, plugins: { legend: { display: false } }, scales: { y: { beginAtZero: true, max: 16 } } } });

  // Channel comparison — BLUE theme
  const chCtx = document.getElementById('channelChart');
  if (chCtx) new Chart(chCtx, { type: 'bar', data: { labels: channelConfigs.map(c => c.ch + '-ch'), datasets: [
    { label: 'Min Accuracy (%)', data: [85, 88, 92, 94, 96, 97], backgroundColor: 'rgba(0,48,87,.5)', borderRadius: 3 },
    { label: 'Max Accuracy (%)', data: [90, 93, 97, 98, 99, 100], backgroundColor: 'rgba(0,48,87,.85)', borderRadius: 3 }
  ] }, options: { responsive: true, scales: { y: { beginAtZero: false, min: 80, max: 102 } }, plugins: { legend: { position: 'bottom' } } } });

  // Emotiv Device Circle Graph
  const emCtx = document.getElementById('emotivDonut');
  if (emCtx && typeof emotivDevices !== 'undefined') new Chart(emCtx, { type: 'doughnut', data: {
    labels: emotivDevices.map(d => d.name + ' (' + d.channels + 'ch)'),
    datasets: [{ data: emotivDevices.map(d => d.channels), backgroundColor: emotivDevices.map(d => d.color), borderWidth: 2, borderColor: '#fff' }]
  }, options: { responsive: true, plugins: { legend: { position: 'bottom', labels: { font: { size: 11 }, padding: 12 } },
    tooltip: { callbacks: { label: function(ctx) { const d = emotivDevices[ctx.dataIndex]; return d.name + ': ' + d.channels + ' ch | ' + d.price + ' | ' + d.accuracy; } } } } } });
}

// ===== EMOTIV DEVICES RENDER =====
function renderEmotivDevices() {
  const el = document.getElementById('emotivGrid');
  if (!el || typeof emotivDevices === 'undefined') return;
  el.innerHTML = emotivDevices.map(d => `<div class="col-md-3"><div class="card-white h-100 text-center" style="border-top:4px solid ${d.color}">
    <div style="font-size:2.5rem;font-weight:800;color:${d.color}">${d.channels}</div>
    <div style="font-size:.65rem;color:var(--gold);text-transform:uppercase;letter-spacing:1px">Channels</div>
    <h6 style="font-weight:700;margin:.5rem 0">${d.name}</h6>
    <div style="font-size:.82rem;font-weight:700;color:var(--navy)">${d.price}</div>
    <div style="font-size:.72rem;color:var(--gray-600);margin:.3rem 0">${d.sampling} | ${d.battery}</div>
    <div style="font-size:.72rem;color:var(--gray-600)">${d.electrodes}</div>
    <div style="margin-top:.5rem;padding-top:.5rem;border-top:1px solid var(--gray-100)">
    <div style="font-size:.68rem;font-weight:600;color:var(--green)">Accuracy: ${d.accuracy}</div>
    <div style="font-size:.65rem;color:var(--gray-600);margin-top:.3rem">${d.useCases.join(' • ')}</div>
    </div></div></div>`).join('');
}

// ===== ANALYSIS LIST RENDER =====
function renderAnalysisList() {
  const el = document.getElementById('analysisDetailGrid');
  if (!el || typeof analysisList === 'undefined') return;
  const statHtml = analysisList.statistical.map(s => `<tr><td style="font-weight:600">${s.name}</td><td>${s.purpose}</td><td style="color:var(--green);font-weight:600">${s.result}</td><td><span class="badge" style="background:var(--navy);font-size:.65rem">${s.category}</span></td></tr>`).join('');
  const sensHtml = analysisList.sensitivity.map(s => `<tr><td style="font-weight:600">${s.name}</td><td>${s.method}</td><td style="color:var(--maroon);font-weight:600">${s.finding}</td><td><span class="badge" style="background:var(--green);font-size:.65rem">${s.category}</span></td></tr>`).join('');
  const valHtml = analysisList.validation.map(v => `<tr><td style="font-weight:600">${v.name}</td><td colspan="3">${v.purpose}</td></tr>`).join('');
  el.innerHTML = `<div class="col-12 mb-4"><div class="card-white"><h5 style="color:var(--green);font-weight:700"><i class="fas fa-chart-bar me-2"></i>Statistical Tests (${analysisList.statistical.length})</h5>
    <div class="table-responsive"><table class="table table-sm" style="font-size:.78rem"><thead style="background:var(--green);color:#fff"><tr><th>Test</th><th>Purpose</th><th>Result</th><th>Category</th></tr></thead><tbody>${statHtml}</tbody></table></div></div></div>
    <div class="col-12 mb-4"><div class="card-white"><h5 style="color:var(--maroon);font-weight:700"><i class="fas fa-sliders me-2"></i>Sensitivity Analyses (${analysisList.sensitivity.length})</h5>
    <div class="table-responsive"><table class="table table-sm" style="font-size:.78rem"><thead style="background:var(--maroon);color:#fff"><tr><th>Analysis</th><th>Method</th><th>Finding</th><th>Category</th></tr></thead><tbody>${sensHtml}</tbody></table></div></div></div>
    <div class="col-12"><div class="card-white"><h5 style="color:var(--navy);font-weight:700"><i class="fas fa-vial me-2"></i>Validation Methods (${analysisList.validation.length})</h5>
    <div class="table-responsive"><table class="table table-sm" style="font-size:.78rem"><thead style="background:var(--navy);color:#fff"><tr><th>Method</th><th colspan="3">Purpose</th></tr></thead><tbody>${valHtml}</tbody></table></div></div></div>`;
}

// ===== SCROLL ACTIVE STATE =====
function updateSidebarActive() {
  const sections = document.querySelectorAll('section[id]');
  const scrollPos = window.scrollY + 100;
  sections.forEach(section => {
    const top = section.offsetTop;
    const height = section.offsetHeight;
    const id = section.getAttribute('id');
    const link = document.querySelector(`.sidebar-nav a[href="#${id}"]`);
    if (link) {
      if (scrollPos >= top && scrollPos < top + height) link.classList.add('active');
      else link.classList.remove('active');
    }
  });
}

// ===== PILLAR ASSESSMENT =====
function renderPillarAssess() {
  const el = document.getElementById('pillarAssessGrid');
  if (!el) return;
  const levels = ['0 - None','1 - Ad Hoc','2 - Developing','3 - Defined','4 - Managed','5 - Optimizing'];
  el.innerHTML = pillars.map((p, i) => `<div class="col-md-6">
    <div class="p-3 rounded" style="background:rgba(255,255,255,.06)">
    <label style="color:#fff;font-weight:600;font-size:.88rem"><i class="fas ${p.icon} me-2" style="color:var(--gold)"></i>${p.name}</label>
    <p style="color:rgba(255,255,255,.5);font-size:.72rem;margin:.3rem 0 .5rem">${p.details ? p.details.substring(0, 120) + '...' : p.desc}</p>
    <select class="form-select form-select-sm" id="pillarQ${i}" style="font-size:.8rem">
    ${levels.map((l, j) => `<option value="${j}">${l}</option>`).join('')}
    </select></div></div>`).join('');
}

function calcPillarAssess() {
  let scores = [];
  pillars.forEach((p, i) => {
    const sel = document.getElementById('pillarQ' + i);
    scores.push(sel ? parseInt(sel.value) : 0);
  });
  const total = scores.reduce((a, b) => a + b, 0);
  const max = pillars.length * 5;
  const pct = Math.round(total / max * 100);
  let level, label, color;
  if (pct <= 20) { level = 1; label = 'Initial'; color = 'var(--danger)'; }
  else if (pct <= 40) { level = 2; label = 'Developing'; color = 'var(--warning)'; }
  else if (pct <= 60) { level = 3; label = 'Defined'; color = 'var(--info)'; }
  else if (pct <= 80) { level = 4; label = 'Managed'; color = 'var(--green)'; }
  else { level = 5; label = 'Optimizing'; color = 'var(--success)'; }

  const res = document.getElementById('pillarAssessResult');
  res.style.display = 'block';
  res.innerHTML = `<div class="row g-4">
  <div class="col-md-4 text-center">
  <div style="font-size:4rem;font-weight:800;color:${color}">${pct}%</div>
  <div style="font-size:1.2rem;font-weight:700;color:var(--gold)">Level ${level}: ${label}</div>
  <div style="font-size:.85rem;color:rgba(255,255,255,.6)">Score: ${total}/${max}</div>
  </div>
  <div class="col-md-8">
  <h6 style="color:var(--gold)">Per-Pillar Breakdown</h6>
  ${pillars.map((p, i) => `<div style="display:flex;align-items:center;gap:.5rem;margin-bottom:.4rem">
  <div style="width:120px;font-size:.75rem;color:#fff">${p.name}</div>
  <div style="flex:1;height:20px;background:rgba(255,255,255,.1);border-radius:10px;overflow:hidden">
  <div style="width:${scores[i]/5*100}%;height:100%;background:${p.color};border-radius:10px;display:flex;align-items:center;justify-content:center;color:#fff;font-size:.65rem;font-weight:700">${scores[i]}/5</div>
  </div></div>`).join('')}
  </div></div>`;
}


// ===== AI TECHNIQUES =====
function renderAITechniques() {
  const el = document.getElementById('aiTechGrid');
  if (!el) return;
  el.innerHTML = aiTechniques.map(t => `<div class="col-12 mb-4">
    <div class="card-white" style="border-left:5px solid ${t.color}">
    <div style="display:flex;align-items:center;gap:1rem;cursor:pointer" onclick="this.parentElement.querySelector('.tech-expand').classList.toggle('d-none')">
    <div style="width:55px;height:55px;border-radius:50%;background:${t.color};color:#fff;display:flex;align-items:center;justify-content:center;font-size:1.4rem;flex-shrink:0"><i class="fas ${t.icon}"></i></div>
    <div style="flex:1"><h5 style="margin:0;font-weight:700">${t.name} <span class="badge" style="background:${t.color};font-size:.7rem">${t.abbr}</span></h5>
    <p style="margin:0;font-size:.82rem;color:var(--gray-600)">${t.desc}</p></div>
    <i class="fas fa-chevron-down" style="color:var(--gray-600)"></i></div>
    <div class="tech-expand d-none">
    <div class="flow-container justify-content-center my-3">${t.flow.map((f,i) => `${i>0?'<div class="flow-arrow"><i class="fas fa-arrow-right"></i></div>':''}<div class="flow-box" style="background:${t.color};min-width:120px;font-size:.68rem">${f}</div>`).join('')}</div>
    <div class="row g-3">
    <div class="col-md-3"><div class="p-2 rounded bg-green-soft"><h6 style="font-size:.78rem;color:var(--green-dark)">Tools</h6>${t.tools.map(tool=>`<div style="font-size:.72rem">&bull; ${tool}</div>`).join('')}</div></div>
    <div class="col-md-3"><div class="p-2 rounded bg-maroon-soft"><h6 style="font-size:.78rem;color:var(--maroon)">Performance</h6><div style="font-size:.72rem">${t.metrics}</div></div></div>
    <div class="col-md-3"><div class="p-2 rounded" style="background:rgba(0,48,87,.05)"><h6 style="font-size:.78rem;color:var(--navy)">Strengths</h6>${t.strengths.map(s=>`<div style="font-size:.72rem">&bull; ${s}</div>`).join('')}</div></div>
    <div class="col-md-3"><div class="p-2 rounded" style="background:rgba(196,163,90,.08)"><h6 style="font-size:.78rem;color:var(--gold-dark)">Limitations</h6>${t.limitations.map(l=>`<div style="font-size:.72rem">&bull; ${l}</div>`).join('')}</div></div>
    </div></div></div></div>`).join('');
}

// ===== B2C / B2B =====
function renderB2CB2B() {
  const el = document.getElementById('b2cB2bGrid');
  if (!el) return;
  const renderSide = (data) => `<div class="col-md-6"><div class="card-white h-100" style="border-top:4px solid ${data.color}">
    <h5 style="color:${data.color};font-weight:700"><i class="fas ${data.icon} me-2"></i>${data.title}</h5>
    ${data.items.map(item => `<div class="p-2 rounded mb-2" style="background:rgba(0,0,0,.02);border-left:3px solid ${data.color}">
    <div style="font-size:.85rem;font-weight:600">${item.label}</div>
    <div style="font-size:.75rem;color:var(--gray-600)">${item.desc}</div></div>`).join('')}</div></div>`;
  el.innerHTML = renderSide(b2cB2b.b2c) + renderSide(b2cB2b.b2b);
}

// ===== AI LEVERS =====
function renderAILevers() {
  const el = document.getElementById('leverGrid');
  if (!el) return;
  el.innerHTML = aiLevers.map(l => `<div class="col-md-3 mb-3"><div class="card-white h-100 text-center" style="border-top:4px solid ${l.color}">
    <div style="font-size:1.8rem;color:${l.color}"><i class="fas ${l.icon}"></i></div>
    <h6 style="font-weight:700;margin:.5rem 0 .2rem">${l.name}</h6>
    <div style="font-size:1.4rem;font-weight:800;color:${l.color}">${l.value}</div>
    <p style="font-size:.75rem;color:var(--gray-600);margin:.3rem 0 0">${l.desc}</p></div></div>`).join('');
}

// ===== DRIVERS =====
function renderDrivers() {
  const el = document.getElementById('driverGrid');
  if (!el) return;
  el.innerHTML = drivers.map(d => `<div class="col-md-3"><div class="card-white h-100" style="border-top:4px solid ${d.color}">
    <h6 style="color:${d.color};font-weight:700"><i class="fas ${d.icon} me-2"></i>${d.category} Drivers</h6>
    <ul style="font-size:.78rem;padding-left:1rem">${d.items.map(i => `<li style="margin-bottom:.3rem">${i}</li>`).join('')}</ul></div></div>`).join('');
}

// ===== PPPT =====
function renderPPPT() {
  const el = document.getElementById('ppptGrid');
  if (!el) return;
  el.innerHTML = ppptFramework.map(p => `<div class="col-md-3"><div class="card-white h-100" style="border-top:4px solid ${p.color}">
    <div class="text-center mb-2"><div style="width:60px;height:60px;border-radius:50%;background:${p.color};color:#fff;display:inline-flex;align-items:center;justify-content:center;font-size:1.5rem"><i class="fas ${p.icon}"></i></div></div>
    <h5 class="text-center" style="color:${p.color};font-weight:700">${p.pillar}</h5>
    <div style="font-size:.78rem"><strong style="color:var(--navy)">Components:</strong>
    <ul style="padding-left:1rem">${p.items.map(i => `<li style="margin-bottom:.2rem">${i}</li>`).join('')}</ul></div>
    <div style="font-size:.78rem;margin-top:.5rem;padding-top:.5rem;border-top:1px solid var(--gray-100)"><strong style="color:var(--maroon)">KPIs:</strong>
    <ul style="padding-left:1rem">${p.kpis.map(k => `<li style="margin-bottom:.2rem">${k}</li>`).join('')}</ul></div></div></div>`).join('');
}

// ===== OPEN SOURCE MODELS =====
function renderOpenSource() {
  const el = document.getElementById('openSourceGrid');
  if (!el) return;
  el.innerHTML = openSourceModels.map(m => `<div class="col-md-4 col-lg-2"><div class="card-white h-100 text-center" style="border-top:4px solid ${m.color}">
    <h6 style="font-weight:700;color:${m.color}">${m.name}</h6>
    <div style="font-size:.7rem;color:var(--gray-600)">${m.org}</div>
    <div style="font-size:.82rem;font-weight:700;color:var(--navy);margin:.3rem 0">${m.params}</div>
    <div style="font-size:.68rem;background:var(--gray-50);border-radius:4px;padding:.2rem .4rem;margin:.3rem 0">${m.license}</div>
    <div style="font-size:.72rem;color:var(--gray-600);margin-top:.3rem">${m.useCase}</div></div></div>`).join('');
}

// ===== DATABASE TYPES =====
function renderDatabases() {
  const el = document.getElementById('dbGrid');
  if (!el) return;
  el.innerHTML = databaseTypes.map(db => `<div class="col-md-4"><div class="card-white h-100" style="border-left:5px solid ${db.color}">
    <h5 style="color:${db.color};font-weight:700"><i class="fas ${db.icon} me-2"></i>${db.name}</h5>
    <div style="font-size:.78rem;color:var(--gray-600);margin-bottom:.5rem"><strong>Tech:</strong> ${db.tech}</div>
    <div style="font-size:.78rem;margin-bottom:.5rem">${db.useCase}</div>
    <div class="p-2 rounded mb-2" style="background:var(--gray-50);font-size:.72rem"><strong>Schema:</strong> ${db.schema}</div>
    <div style="font-size:.72rem;margin-bottom:.3rem"><strong style="color:var(--navy)">Sample Queries:</strong></div>
    ${db.queries.map(q => `<div style="font-size:.68rem;font-family:monospace;background:var(--gray-50);padding:.3rem;border-radius:4px;margin-bottom:.2rem;word-break:break-all">${q}</div>`).join('')}
    <div style="font-size:.72rem;margin-top:.5rem"><strong style="color:var(--green)">Benefits:</strong></div>
    ${db.benefits.map(b => `<div style="font-size:.72rem">&bull; ${b}</div>`).join('')}</div></div>`).join('');
}

// ===== MCP PIPELINE =====
function renderMCPPipeline() {
  const el = document.getElementById('mcpPipelineFlow');
  if (!el) return;
  el.innerHTML = `<div class="flow-container justify-content-center mb-4">${mcpPipeline.map((s,i) => `${i>0?'<div class="flow-arrow"><i class="fas fa-arrow-right"></i></div>':''}<div class="flow-box" style="background:${s.color};min-width:110px;font-size:.7rem">${s.stage}</div>`).join('')}</div>
  <div class="row g-3">${mcpPipeline.map(s => `<div class="col-md-3 mb-3"><div class="p-3 rounded" style="background:rgba(255,255,255,.06)">
    <div style="display:flex;align-items:center;gap:.5rem;margin-bottom:.5rem">
    <div style="width:35px;height:35px;border-radius:50%;background:${s.color};color:#fff;display:flex;align-items:center;justify-content:center"><i class="fas ${s.icon}"></i></div>
    <h6 style="margin:0;color:#fff;font-size:.85rem">${s.stage}</h6></div>
    <div style="font-size:.75rem;color:var(--gold);margin-bottom:.3rem">${s.details}</div>
    <ul style="font-size:.7rem;color:rgba(255,255,255,.7);padding-left:1rem;margin:0">${s.specs.map(sp => `<li>${sp}</li>`).join('')}</ul></div></div>`).join('')}</div>`;
}

// ===== PATIENT JOURNEY =====
function renderPatientJourney() {
  const el = document.getElementById('journeyGrid');
  if (!el) return;
  el.innerHTML = patientJourney.map((p,i) => `<div class="col-12 mb-3">
    <div class="card-white" style="border-left:5px solid ${p.color}">
    <div style="display:flex;align-items:center;gap:1rem">
    <div style="width:50px;height:50px;border-radius:50%;background:${p.color};color:#fff;display:flex;align-items:center;justify-content:center;font-size:1.2rem;flex-shrink:0"><i class="fas ${p.icon}"></i></div>
    <div style="flex:1">
    <h6 style="margin:0;font-weight:700"><span class="badge" style="background:${p.color};font-size:.65rem">Phase ${i+1}</span> ${p.phase} <span style="font-size:.72rem;color:var(--gray-600);font-weight:400">(${p.duration})</span></h6></div></div>
    <div class="row g-2 mt-2">
    <div class="col-md-3"><div class="p-2 rounded bg-green-soft"><div style="font-size:.72rem;font-weight:600;color:var(--green-dark)">Touchpoints</div>${p.touchpoints.map(t=>`<div style="font-size:.7rem">&bull; ${t}</div>`).join('')}</div></div>
    <div class="col-md-3"><div class="p-2 rounded bg-maroon-soft"><div style="font-size:.72rem;font-weight:600;color:var(--maroon)">Pain Points</div>${p.painPoints.map(pp=>`<div style="font-size:.7rem">&bull; ${pp}</div>`).join('')}</div></div>
    <div class="col-md-6"><div class="p-2 rounded" style="background:rgba(0,48,87,.05)"><div style="font-size:.72rem;font-weight:600;color:var(--navy)">RGAIG+ Value</div><div style="font-size:.75rem">${p.rgaigValue}</div></div></div>
    </div></div></div>`).join('');
}

// ===== IMPACT =====
function renderImpact() {
  const el = document.getElementById('impactGrid');
  if (!el) return;
  el.innerHTML = impactMetrics.map(cat => `<div class="col-md-4"><div class="card-white h-100" style="border-top:4px solid ${cat.color}">
    <h5 style="color:${cat.color};font-weight:700"><i class="fas ${cat.icon} me-2"></i>${cat.category}</h5>
    <table class="table table-sm" style="font-size:.78rem;margin:0">
    <thead><tr><th>Metric</th><th>Value</th><th>vs Baseline</th></tr></thead>
    <tbody>${cat.metrics.map(m => `<tr><td>${m.label}</td><td style="font-weight:700;color:${cat.color}">${m.value}</td><td style="color:var(--success);font-size:.72rem">${m.improvement}</td></tr>`).join('')}</tbody></table></div></div>`).join('');
}

// ===== VALUE REALIZATION =====
function renderValueMatrix() {
  const el = document.getElementById('valueMatrixTable');
  if (!el) return;
  el.innerHTML = `<thead><tr><th>Stakeholder</th><th>Short-Term (0-6 mo)</th><th>Medium-Term (6-18 mo)</th><th>Long-Term (18+ mo)</th><th>Key Metrics</th></tr></thead>
  <tbody>${valueMatrix.map(v => `<tr><td style="font-weight:700">${v.stakeholder}</td><td style="font-size:.75rem">${v.shortTerm}</td><td style="font-size:.75rem">${v.mediumTerm}</td><td style="font-size:.75rem">${v.longTerm}</td><td style="font-size:.72rem;color:var(--navy)">${v.metrics}</td></tr>`).join('')}</tbody>`;
}

// ===== ROI MATRIX =====
function renderROIMatrix() {
  const el = document.getElementById('roiMatrixTable');
  if (!el) return;
  el.innerHTML = `<thead><tr><th>Investment Item</th><th>Cost</th><th>Year 1 Return</th><th>Year 2 Return</th><th>Year 3 Return</th><th>ROI</th></tr></thead>
  <tbody>${roiMatrix.map(r => `<tr style="${r.item==='TOTAL'?'background:var(--gray-50);font-weight:700':''}"><td>${r.item}</td><td>${r.cost}</td><td>${r.year1}</td><td>${r.year2}</td><td>${r.year3}</td><td style="color:var(--success);font-weight:700">${r.roi}</td></tr>`).join('')}</tbody>`;
}

// ===== KPI MATRIX =====
function renderKPIMatrix() {
  const el = document.getElementById('kpiGrid');
  if (!el) return;
  const statusIcon = s => s === 'pass' ? '<i class="fas fa-check-circle" style="color:var(--success)"></i>' : '<i class="fas fa-exclamation-triangle" style="color:var(--warning)"></i>';
  el.innerHTML = kpiMatrix.map(domain => `<div class="col-md-6 mb-3"><div class="card-white h-100">
    <h6 style="color:var(--navy);font-weight:700;border-bottom:2px solid var(--gold);padding-bottom:.3rem">${domain.domain} KPIs</h6>
    <table class="table table-sm" style="font-size:.75rem;margin:0">
    <thead><tr><th>KPI</th><th>Target</th><th>Actual</th><th></th></tr></thead>
    <tbody>${domain.kpis.map(k => `<tr><td>${k.name}</td><td>${k.target}</td><td style="font-weight:700">${k.actual}</td><td>${statusIcon(k.status)}</td></tr>`).join('')}</tbody></table></div></div>`).join('');
}

// ===== FEATURE MATRIX =====
function renderFeatureMatrix() {
  const el = document.getElementById('featureMatrixTable');
  if (!el) return;
  el.innerHTML = `<thead><tr><th>Feature</th><th style="color:var(--gold)">RGAIG+</th><th>Competitor A</th><th>Competitor B</th><th>Competitor C</th></tr></thead>
  <tbody>${featureMatrix.map(f => `<tr><td style="font-weight:600">${f.feature}</td><td style="color:var(--success);font-weight:600">${f.rgaig}</td><td style="font-size:.75rem">${f.competitor1}</td><td style="font-size:.75rem">${f.competitor2}</td><td style="font-size:.75rem">${f.competitor3}</td></tr>`).join('')}</tbody>`;
}

// ===== CASE STUDIES =====
function renderCaseStudies() {
  const el = document.getElementById('caseStudyGrid');
  if (!el) return;
  el.innerHTML = caseStudies.map(cs => `<div class="col-md-6 mb-3"><div class="card-white h-100" style="border-top:4px solid ${cs.color}">
    <h5 style="color:${cs.color};font-weight:700"><i class="fas ${cs.icon} me-2"></i>${cs.title}</h5>
    <span class="badge" style="background:${cs.color};font-size:.65rem">${cs.domain}</span>
    <div class="mt-2"><div style="font-size:.78rem"><strong style="color:var(--maroon)">Challenge:</strong> ${cs.challenge}</div>
    <div style="font-size:.78rem;margin-top:.4rem"><strong style="color:var(--green)">Solution:</strong> ${cs.solution}</div>
    <div style="margin-top:.4rem"><strong style="font-size:.78rem;color:var(--navy)">Results:</strong>
    <ul style="font-size:.75rem;padding-left:1rem;margin:.2rem 0">${cs.results.map(r => `<li>${r}</li>`).join('')}</ul></div>
    <div style="font-size:.78rem;margin-top:.4rem;padding:.5rem;background:rgba(196,163,90,.08);border-radius:6px"><strong style="color:var(--gold-dark)">Impact:</strong> ${cs.impact}</div></div></div></div>`).join('');
}

// ===== SCORECARD =====
const scorecardIndicators = {
  'Responsible AI': [{name:'Bias testing coverage',max:100},{name:'Fairness metric tracking',max:100},{name:'Accountability chain documented',max:100}],
  'Governance AI': [{name:'AI governance board active',max:100},{name:'Policy documentation completeness',max:100},{name:'Automated compliance rate',max:100}],
  'Risk AI': [{name:'Risk taxonomy coverage',max:100},{name:'Automated escalation rate',max:100},{name:'Sensitivity analysis frequency',max:100}],
  'Ethical AI': [{name:'IRB/consent compliance',max:100},{name:'Privacy protection score',max:100},{name:'Vulnerable population safeguards',max:100}],
  'Performance AI': [{name:'Cross-validation accuracy',max:100},{name:'Inference latency target met',max:100},{name:'Ablation study coverage',max:100}],
  'Explainable AI': [{name:'SHAP coverage per prediction',max:100},{name:'RAG faithfulness score',max:100},{name:'Consumer explanation quality',max:100}],
  'Interpretable AI': [{name:'Model card completeness',max:100},{name:'Decision path traceability',max:100},{name:'Confidence interval display',max:100}],
  'Portable AI': [{name:'Cross-domain generalization',max:100},{name:'Edge deployment readiness',max:100},{name:'Cross-platform coverage',max:100}],
  'Energy-Efficient AI': [{name:'Energy consumption tracked',max:100},{name:'Model compression applied',max:100},{name:'Carbon footprint monitored',max:100}],
  'Secure AI': [{name:'Encryption at rest/transit',max:100},{name:'Adversarial robustness tested',max:100},{name:'PII detection coverage',max:100}]
};
let scorecardScores = {};
Object.keys(scorecardIndicators).forEach(p => {
  scorecardScores[p] = scorecardIndicators[p].map(() => 0);
});

function renderScorecard() {
  const el = document.getElementById('scorecardPillars');
  if (!el) return;
  el.innerHTML = Object.keys(scorecardIndicators).map((pName, pi) => {
    const pColor = pillars[pi] ? pillars[pi].color : 'var(--navy)';
    const pIcon = pillars[pi] ? pillars[pi].icon : 'fa-shield-halved';
    return `<div class="mb-2"><div class="p-2 rounded" style="background:rgba(255,255,255,.06);cursor:pointer" onclick="this.nextElementSibling.classList.toggle('d-none')">
    <div style="display:flex;align-items:center;gap:.5rem">
    <i class="fas ${pIcon}" style="color:var(--gold)"></i>
    <span style="color:#fff;font-weight:600;font-size:.85rem;flex:1">${pName}</span>
    <span id="pillarScore_${pi}" class="badge" style="background:${pColor};font-size:.72rem">0%</span>
    <i class="fas fa-chevron-down" style="color:rgba(255,255,255,.4);font-size:.7rem"></i></div></div>
    <div class="d-none" style="padding:.5rem .5rem .5rem 2rem">${scorecardIndicators[pName].map((ind, ii) => `<div class="mb-2 p-2 rounded" style="background:rgba(255,255,255,.04)">
    <div style="display:flex;align-items:center;gap:.5rem">
    <span style="color:rgba(255,255,255,.7);font-size:.78rem;flex:1">${ind.name}</span>
    <input type="range" min="0" max="100" value="0" id="sc_${pi}_${ii}" style="width:120px;accent-color:${pColor}" oninput="updateScorecardScore(${pi},${ii},this.value)">
    <span id="scVal_${pi}_${ii}" style="color:var(--gold);font-size:.78rem;font-weight:700;min-width:35px;text-align:right">0</span>
    </div></div>`).join('')}</div></div>`;
  }).join('');
}

function updateScorecardScore(pi, ii, val) {
  const pName = Object.keys(scorecardIndicators)[pi];
  scorecardScores[pName][ii] = parseInt(val);
  document.getElementById('scVal_'+pi+'_'+ii).textContent = val;
  recalcScorecard();
}

function recalcScorecard() {
  const pillarAvgs = [];
  Object.keys(scorecardScores).forEach((pName, pi) => {
    const scores = scorecardScores[pName];
    const avg = scores.length ? Math.round(scores.reduce((a,b)=>a+b,0) / scores.length) : 0;
    pillarAvgs.push(avg);
    const badge = document.getElementById('pillarScore_'+pi);
    if (badge) { badge.textContent = avg+'%'; badge.style.background = avg >= 70 ? 'var(--success)' : avg >= 40 ? 'var(--warning)' : 'var(--danger)'; }
  });
  const headline = pillarAvgs.length ? Math.round(pillarAvgs.reduce((a,b)=>a+b,0) / pillarAvgs.length) : 0;
  const hEl = document.getElementById('headlineScore');
  if (hEl) hEl.textContent = headline;
  const hLevel = document.getElementById('headlineLevel');
  if (hLevel) {
    if (headline >= 80) hLevel.textContent = 'Level 5: Optimizing';
    else if (headline >= 60) hLevel.textContent = 'Level 4: Managed';
    else if (headline >= 40) hLevel.textContent = 'Level 3: Defined';
    else if (headline >= 20) hLevel.textContent = 'Level 2: Developing';
    else hLevel.textContent = 'Level 1: Initial';
  }
  if (window.scorecardChart) {
    window.scorecardChart.data.datasets[0].data = pillarAvgs;
    window.scorecardChart.update();
  }
}

function expandAllScorecard() { document.querySelectorAll('#scorecardPillars .d-none').forEach(el => el.classList.remove('d-none')); }
function collapseAllScorecard() { document.querySelectorAll('#scorecardPillars > div > div:nth-child(2)').forEach(el => el.classList.add('d-none')); }
function resetScorecard() {
  Object.keys(scorecardScores).forEach(p => { scorecardScores[p] = scorecardScores[p].map(() => 0); });
  document.querySelectorAll('[id^="sc_"]').forEach(el => { if (el.tagName === 'INPUT') el.value = 0; });
  document.querySelectorAll('[id^="scVal_"]').forEach(el => el.textContent = '0');
  recalcScorecard();
}

function initScorecardRadar() {
  const ctx = document.getElementById('scorecardRadar');
  if (!ctx) return;
  window.scorecardChart = new Chart(ctx, {
    type: 'radar',
    data: { labels: Object.keys(scorecardIndicators), datasets: [{
      label: 'Your Score', data: new Array(10).fill(0),
      backgroundColor: 'rgba(196,163,90,.2)', borderColor: 'var(--gold)', borderWidth: 2, pointBackgroundColor: 'var(--gold)'
    }] },
    options: { responsive: true, scales: { r: { min: 0, max: 100, ticks: { stepSize: 20, color: 'rgba(255,255,255,.5)', backdropColor: 'transparent' }, grid: { color: 'rgba(255,255,255,.15)' }, pointLabels: { color: 'rgba(255,255,255,.7)', font: { size: 9 } } } }, plugins: { legend: { display: false } } }
  });
}

// ===== INIT =====
document.addEventListener('DOMContentLoaded', function () {
  renderLayers();
  renderPillars();
  renderPillarDeep();
  renderChannels();
  renderDiseases();
  renderIndustries();
  renderComparison();
  renderIsoNist();
  renderPhases();
  renderLifecycle();
  renderMLOps();
  renderLLMOps();
  renderAssessment();
  renderSurveys();
  renderPillarAssess();
  renderAITechniques();
  renderB2CB2B();
  renderAILevers();
  renderDrivers();
  renderPPPT();
  renderOpenSource();
  renderDatabases();
  renderMCPPipeline();
  renderPatientJourney();
  renderImpact();
  renderValueMatrix();
  renderROIMatrix();
  renderKPIMatrix();
  renderFeatureMatrix();
  renderCaseStudies();
  renderScorecard();
  renderEmotivDevices();
  renderAnalysisList();
  initCharts();
  initScorecardRadar();
  animateCounters();
  window.addEventListener('scroll', updateSidebarActive);

  // Fade-in animation
  const observer = new IntersectionObserver(entries => {
    entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('visible'); });
  }, { threshold: 0.1 });
  document.querySelectorAll('.fade-in').forEach(el => observer.observe(el));
});
