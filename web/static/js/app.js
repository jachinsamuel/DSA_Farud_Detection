let visualizer = null;
let allAccounts = [];
let currentAccount = null;

document.addEventListener('DOMContentLoaded', () => {
  visualizer = new GraphVisualizer('graphCanvas');
  window.visualizer = visualizer;

  bindCategoryTabs();
  bindTabs();
  bindResizer();
  bindSizeButtons();
  bindControls();
  loadData();

  window.onNodeSelected = (node) => {
    selectAccount(node.id);
  };
});

function bindCategoryTabs() {
  const catBtns = document.querySelectorAll('.cat-tab-btn');
  catBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const cat = btn.getAttribute('data-cat');
      switchCategory(cat);
    });
  });
}

function switchCategory(catKey) {
  document.querySelectorAll('.cat-tab-btn').forEach(b => {
    b.classList.toggle('active', b.getAttribute('data-cat') === catKey);
  });
  if (visualizer) {
    visualizer.setCategory(catKey);
  }
}

function bindTabs() {
  const tabBtns = document.querySelectorAll('.tab-btn');
  tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const targetId = btn.getAttribute('data-tab');
      switchTab(targetId);
    });
  });
}

function switchTab(tabId) {
  document.querySelectorAll('.tab-btn').forEach(b => {
    b.classList.toggle('active', b.getAttribute('data-tab') === tabId);
  });
  document.querySelectorAll('.tab-content').forEach(p => {
    p.classList.toggle('active', p.id === tabId);
  });
}

function bindResizer() {
  const resizer = document.getElementById('panelResizer');
  const panel = document.getElementById('controlPanel');
  if (!resizer || !panel) return;

  let isDragging = false;

  resizer.addEventListener('mousedown', (e) => {
    isDragging = true;
    resizer.classList.add('dragging');
    panel.classList.add('no-transition');
    document.body.style.cursor = 'col-resize';
    document.body.style.userSelect = 'none';
  });

  window.addEventListener('mousemove', (e) => {
    if (!isDragging) return;
    const newWidth = window.innerWidth - e.clientX;
    if (newWidth >= 280 && newWidth <= 750) {
      panel.style.width = `${newWidth}px`;
      if (visualizer) visualizer.resizeCanvas();
    }
  });

  window.addEventListener('mouseup', () => {
    if (!isDragging) return;
    isDragging = false;
    resizer.classList.remove('dragging');
    panel.classList.remove('no-transition');
    document.body.style.cursor = '';
    document.body.style.userSelect = '';
    if (visualizer) {
      visualizer.resizeCanvas();
      visualizer.resetView();
    }
  });

  resizer.addEventListener('dblclick', () => {
    const curWidth = parseInt(window.getComputedStyle(panel).width);
    if (curWidth > 450) {
      setPanelSize('normal');
    } else {
      setPanelSize('wide');
    }
  });
}

function bindSizeButtons() {
  const sizeBtns = document.querySelectorAll('.btn-size');
  sizeBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const size = btn.getAttribute('data-size');
      setPanelSize(size);
    });
  });
}

function setPanelSize(sizeName) {
  const panel = document.getElementById('controlPanel');
  if (!panel) return;

  document.querySelectorAll('.btn-size').forEach(b => {
    b.classList.toggle('active', b.getAttribute('data-size') === sizeName);
  });

  if (sizeName === 'compact') {
    panel.style.width = '300px';
  } else if (sizeName === 'wide') {
    panel.style.width = '600px';
  } else {
    panel.style.width = '420px';
  }

  setTimeout(() => {
    if (visualizer) {
      visualizer.resizeCanvas();
      visualizer.resetView();
    }
  }, 120);
}

function bindControls() {
  document.getElementById('btnResetView').addEventListener('click', () => {
    visualizer.resetView();
    visualizer.clearHighlights();
    showToast('Network view centered.');
  });

  const fitBtn = document.getElementById('btnFitMap');
  if (fitBtn) fitBtn.addEventListener('click', () => visualizer.resetView());
  const zoomIn = document.getElementById('btnZoomIn');
  if (zoomIn) zoomIn.addEventListener('click', () => visualizer.zoomIn());
  const zoomOut = document.getElementById('btnZoomOut');
  if (zoomOut) zoomOut.addEventListener('click', () => visualizer.zoomOut());

  const themeBtn = document.getElementById('btnThemeToggle');
  themeBtn.addEventListener('click', () => {
    const isDark = document.body.getAttribute('data-theme') === 'dark';
    if (isDark) {
      document.body.removeAttribute('data-theme');
      themeBtn.innerText = 'Dark Mode';
    } else {
      document.body.setAttribute('data-theme', 'dark');
      themeBtn.innerText = 'Light Mode';
    }
  });

  document.getElementById('btnInspectCycle').addEventListener('click', inspectLaunderingRing);
  document.getElementById('btnInspectPath').addEventListener('click', inspectMuleRoute);
  document.getElementById('btnInspectSmurfing').addEventListener('click', inspectSmurfingSyndicate);
  document.getElementById('btnInspectOffshore').addEventListener('click', inspectOffshoreFunnel);
  document.getElementById('btnInspectSanctioned').addEventListener('click', inspectSanctionedAccount);
  document.getElementById('btnInspectTerminal').addEventListener('click', inspectTerminalAccount);
  document.getElementById('btnRefreshIncidents').addEventListener('click', loadData);

  document.getElementById('selectDossierAccount').addEventListener('change', (e) => {
    if (e.target.value) selectAccount(e.target.value);
  });

  document.getElementById('btnFreezeAccount').addEventListener('click', toggleFreezeAccount);
  document.getElementById('btnCheckLoopsForAccount').addEventListener('click', checkLoopsForSelectedAccount);
  document.getElementById('btnTraceFromAccount').addEventListener('click', traceFromSelectedAccount);

  document.getElementById('inputSendAmount').addEventListener('input', updateTransferRiskPreview);
  document.getElementById('selectSendFrom').addEventListener('change', updateTransferRiskPreview);
  document.getElementById('selectSendTo').addEventListener('change', updateTransferRiskPreview);
  document.getElementById('formSendMoney').addEventListener('submit', handleSendMoney);
}

async function loadData() {
  try {
    const res = await fetch('/api/graph');
    const data = await res.json();
    visualizer.setData(data);

    const accRes = await fetch('/api/accounts');
    allAccounts = await accRes.json();
    populateDropdowns(allAccounts);

    const countElem = document.getElementById('kpiAccounts');
    if (countElem) countElem.innerText = allAccounts.length;

    updateIncidentCounts();
  } catch (err) {
    console.error('Failed to load banking data:', err);
  }
}

function populateDropdowns(accounts) {
  const dossierSel = document.getElementById('selectDossierAccount');
  const traceSel = document.getElementById('selectTraceTarget');
  const sendFrom = document.getElementById('selectSendFrom');
  const sendTo = document.getElementById('selectSendTo');

  const populate = (sel, placeholder = false) => {
    if (!sel) return;
    sel.innerHTML = '';
    if (placeholder) {
      const opt = document.createElement('option');
      opt.value = '';
      opt.text = '-- Select Customer Account --';
      sel.appendChild(opt);
    }
    accounts.forEach(acc => {
      const opt = document.createElement('option');
      opt.value = acc.account_id;
      opt.text = `${acc.name} (${acc.account_id})`;
      sel.appendChild(opt);
    });
  };

  populate(dossierSel, true);
  populate(traceSel, false);
  populate(sendFrom, false);
  populate(sendTo, false);

  if (sendFrom.options.length > 0) sendFrom.value = 'ACC-101';
  if (sendTo.options.length > 1) sendTo.value = 'ACC-102';
  if (traceSel.options.length > 0) traceSel.value = 'ACC-999';
}

function updateIncidentCounts() {
  const cards = document.querySelectorAll('.incident-card');
  const total = cards.length;
  const badge = document.getElementById('tabAlertsCount');
  if (badge) badge.innerText = total;
  const kpiAlerts = document.getElementById('kpiAlerts');
  if (kpiAlerts) kpiAlerts.innerText = total;
}

async function inspectLaunderingRing() {
  try {
    switchCategory('rings');
    const res = await fetch('/api/detect/cycles');
    const data = await res.json();
    if (data.cycles && data.cycles.length > 0) {
      const primary = data.cycles[0];
      visualizer.highlightCycle(primary.path);
      showToast(`Showing circular laundering ring: ${primary.path.join(' ➔ ')}`);
      selectAccount(primary.path[0], false);
    }
  } catch (err) {
    showToast('Failed to scan for laundering rings.');
  }
}

async function inspectMuleRoute() {
  try {
    switchCategory('mules');
    const res = await fetch('/api/detect/shortest-path', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ source: 'ACC-901', target: 'ACC-999' })
    });
    const data = await res.json();
    if (data.result && data.result.found) {
      visualizer.highlightShortestPath(data.result.path);
      showToast(`Traced 3-hop mule route to Cash-Out terminal.`);
      selectAccount('ACC-901', false);
    }
  } catch (err) {
    showToast('Failed to trace route.');
  }
}

async function inspectSmurfingSyndicate() {
  try {
    switchCategory('smurfing');
    const res = await fetch('/api/detect/smurfing');
    const data = await res.json();
    if (data.patterns && data.patterns.length > 0) {
      const muleIds = ['ACC-200', 'ACC-201', 'ACC-202', 'ACC-203', 'ACC-204', 'ACC-205'];
      visualizer.highlightShortestPath(muleIds);
      showToast('Highlighted split deposit smurfing syndicate.');
      selectAccount('ACC-200', false);
    }
  } catch (err) {
    showToast('Failed to inspect smurfing syndicate.');
  }
}

async function inspectOffshoreFunnel() {
  try {
    switchCategory('offshore');
    visualizer.highlightShortestPath(['ACC-201', 'ACC-202', 'ACC-203', 'ACC-204', 'ACC-300']);
    showToast('Showing offshore funnel consolidation to ACC-300.');
    selectAccount('ACC-300', false);
  } catch (err) {
    showToast('Failed to inspect offshore funnel.');
  }
}

async function inspectSanctionedAccount() {
  try {
    switchCategory('watchlist');
    visualizer.highlightShortestPath(['ACC-901', 'ACC-902']);
    showToast('Inspecting Blacklisted Sanctioned Entity ACC-901.');
    selectAccount('ACC-901', true);
  } catch (err) {
    showToast('Failed to inspect account.');
  }
}

async function inspectTerminalAccount() {
  try {
    switchCategory('watchlist');
    visualizer.highlightShortestPath(['ACC-903', 'ACC-999']);
    showToast('Inspecting Dark Cash-Out Terminal ACC-999.');
    selectAccount('ACC-999', true);
  } catch (err) {
    showToast('Failed to inspect account.');
  }
}

async function selectAccount(accountId, openTab = true) {
  if (!accountId) return;

  try {
    const res = await fetch(`/api/search/account?id=${encodeURIComponent(accountId)}`);
    const data = await res.json();
    if (!data.found) return;

    currentAccount = data.account;
    renderDossier(currentAccount);

    const sel = document.getElementById('selectDossierAccount');
    if (sel) sel.value = accountId;

    if (openTab) {
      switchTab('tabDossier');
    }
    showToast(`Loaded dossier: ${currentAccount.name}`);
  } catch (err) {
    console.error('Account lookup error:', err);
  }
}

function renderDossier(acc) {
  document.getElementById('dossierPlaceholder').classList.add('hidden');
  const card = document.getElementById('dossierCard');
  card.classList.remove('hidden');

  document.getElementById('dossierName').innerText = acc.name;
  document.getElementById('dossierId').innerText = acc.account_id;
  document.getElementById('dossierBalance').innerText = `$${acc.balance.toLocaleString()}`;
  document.getElementById('dossierRiskScore').innerText = `${acc.risk_score}%`;

  const bar = document.getElementById('dossierRiskBar');
  bar.style.width = `${Math.min(100, acc.risk_score)}%`;
  bar.className = 'risk-bar-fill';

  const pill = document.getElementById('dossierRiskPill');
  const flagText = document.getElementById('dossierFlag');
  const standingText = document.getElementById('dossierStanding');

  if (acc.risk_score >= 80 || acc.is_flagged) {
    pill.className = 'risk-pill high';
    pill.innerText = 'High Risk';
    bar.classList.add('high');
    flagText.innerText = 'FLAGGED FOR SURVEILLANCE';
    flagText.style.color = 'var(--red)';
    standingText.innerText = 'Under Formal AML Audit';
  } else if (acc.risk_score >= 50) {
    pill.className = 'risk-pill medium';
    pill.innerText = 'Watchlist';
    bar.classList.add('medium');
    flagText.innerText = 'ELEVATED ACTIVITY';
    flagText.style.color = 'var(--amber)';
    standingText.innerText = 'Standard Monitoring';
  } else {
    pill.className = 'risk-pill low';
    pill.innerText = 'Verified';
    flagText.innerText = 'CLEAR';
    flagText.style.color = 'var(--green)';
    standingText.innerText = 'Good Standing';
  }

  const avatar = document.getElementById('dossierAvatar');
  if (acc.name.includes('Corp') || acc.name.includes('Ltd') || acc.name.includes('Inc') || acc.name.includes('Holdings')) {
    avatar.innerText = '🏢';
  } else if (acc.name.includes('Cartel') || acc.name.includes('Terminal') || acc.name.includes('Sanctioned')) {
    avatar.innerText = '⚠️';
  } else {
    avatar.innerText = '👤';
  }

  const freezeBtn = document.getElementById('btnFreezeAccount');
  freezeBtn.innerText = acc.is_frozen ? 'Unfreeze Account' : 'Freeze Account';
  freezeBtn.className = acc.is_frozen ? 'btn btn-secondary btn-sm' : 'btn btn-secondary btn-sm danger';

  document.getElementById('accountTraceResult').classList.add('hidden');
}

function toggleFreezeAccount() {
  if (!currentAccount) return;
  currentAccount.is_frozen = !currentAccount.is_frozen;
  const freezeBtn = document.getElementById('btnFreezeAccount');
  if (currentAccount.is_frozen) {
    freezeBtn.innerText = 'Unfreeze Account';
    freezeBtn.className = 'btn btn-secondary btn-sm';
    showToast(`Account ${currentAccount.account_id} FROZEN by Manager Order.`);
  } else {
    freezeBtn.innerText = 'Freeze Account';
    freezeBtn.className = 'btn btn-secondary btn-sm danger';
    showToast(`Account ${currentAccount.account_id} un-frozen.`);
  }
}

async function checkLoopsForSelectedAccount() {
  if (!currentAccount) return;
  try {
    const res = await fetch('/api/detect/cycles');
    const data = await res.json();
    const cycle = (data.cycles || []).find(c => c.path.includes(currentAccount.account_id));
    if (cycle) {
      visualizer.highlightCycle(cycle.path);
      showToast(`Account is part of laundering loop: ${cycle.path.join(' ➔ ')}`);
    } else {
      showToast(`No circular loops involving ${currentAccount.account_id}.`);
    }
  } catch (err) {
    showToast('Check failed.');
  }
}

async function traceFromSelectedAccount() {
  if (!currentAccount) return;
  const dest = document.getElementById('selectTraceTarget').value;
  const resultBox = document.getElementById('accountTraceResult');

  if (currentAccount.account_id === dest) {
    showToast('Destination must be different from source.');
    return;
  }

  try {
    const res = await fetch('/api/detect/shortest-path', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ source: currentAccount.account_id, target: dest })
    });
    const data = await res.json();
    const resObj = data.result;

    resultBox.classList.remove('hidden');
    if (resObj && resObj.found) {
      resultBox.innerHTML = `Route identified (${resObj.hop_count} hops):<br><b>${resObj.path.join(' ➔ ')}</b>`;
      visualizer.highlightShortestPath(resObj.path);
      showToast(`Found ${resObj.hop_count}-hop transfer route.`);
    } else {
      resultBox.innerHTML = `No direct or intermediary transfer path connects these accounts.`;
    }
  } catch (err) {
    showToast('Routing lookup failed.');
  }
}

function updateTransferRiskPreview() {
  const amount = parseFloat(document.getElementById('inputSendAmount').value) || 0;
  const from = document.getElementById('selectSendFrom').value;
  const to = document.getElementById('selectSendTo').value;
  const badge = document.getElementById('transferRiskBadge');

  if (from === to) {
    badge.innerText = 'Invalid: Source and destination match';
    badge.style.color = 'var(--red)';
  } else if (amount >= 100000) {
    badge.innerText = 'Executive Approval Required (>$100k)';
    badge.style.color = 'var(--red)';
  } else if (amount >= 9000 && amount <= 9999) {
    badge.innerText = 'Flagged: Threshold Structuring Pattern';
    badge.style.color = 'var(--amber)';
  } else {
    badge.innerText = 'Standard Compliance Check Passed';
    badge.style.color = 'var(--green)';
  }
}

async function handleSendMoney(e) {
  e.preventDefault();
  const src = document.getElementById('selectSendFrom').value;
  const dest = document.getElementById('selectSendTo').value;
  const amount = parseFloat(document.getElementById('inputSendAmount').value);

  if (src === dest) {
    showToast('Sender and receiver must be different accounts.');
    return;
  }

  try {
    const res = await fetch('/api/transaction/create', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ src, dest, amount })
    });
    const data = await res.json();

    if (!data.success) {
      showToast(data.error || 'Transaction authorization denied.');
      return;
    }

    showToast(`Transfer of $${amount.toLocaleString()} approved & settled!`);
    loadData();
    switchTab('tabAlerts');
  } catch (err) {
    showToast('Transfer request failed.');
  }
}

function showToast(msg) {
  const toast = document.getElementById('toast');
  if (!toast) return;
  toast.innerText = msg;
  toast.classList.remove('hidden');
  setTimeout(() => {
    toast.classList.add('hidden');
  }, 3200);
}