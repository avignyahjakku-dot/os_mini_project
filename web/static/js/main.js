/* main.js - Client Application Logic for Banker's Algorithm Dashboard */

let currentState = null;

document.addEventListener('DOMContentLoaded', () => {
    initTheme();
    loadState();
    setupEventListeners();
});

// Theme Toggle
function initTheme() {
    const savedTheme = localStorage.getItem('banker-theme') || 'dark';
    if (savedTheme === 'light') {
        document.body.classList.add('light-theme');
    }

    document.getElementById('btn-theme-toggle').addEventListener('click', () => {
        document.body.classList.toggle('light-theme');
        const theme = document.body.classList.contains('light-theme') ? 'light' : 'dark';
        localStorage.setItem('banker-theme', theme);
    });
}

// Fetch and render state from server
async function loadState() {
    try {
        const res = await fetch('/api/state');
        const data = await res.json();
        if (data.success) {
            currentState = data.state;
            renderState(currentState);
        }
    } catch (err) {
        console.error('Failed to load state:', err);
    }
}

// Render matrix, headers, utilization and forms
function renderState(state) {
    const n = state.num_processes;
    const m = state.num_resources;

    // Meta tag
    document.getElementById('matrix-meta').textContent = `${n} Processes • ${m} Resource Types`;

    // Table Subheaders
    const subheaderRow = document.getElementById('resource-subheaders');
    subheaderRow.innerHTML = '';
    
    // Set colspans
    document.getElementById('th-alloc').colSpan = m;
    document.getElementById('th-max').colSpan = m;
    document.getElementById('th-need').colSpan = m;
    document.getElementById('th-avail').colSpan = m;

    // 4 sections: Alloc, Max, Need, Available
    for (let sec = 0; sec < 4; sec++) {
        for (let j = 0; j < m; j++) {
            const th = document.createElement('th');
            th.textContent = state.resource_names[j];
            subheaderRow.appendChild(th);
        }
    }

    // Matrix Body
    const tbody = document.getElementById('matrix-tbody');
    tbody.innerHTML = '';

    for (let i = 0; i < n; i++) {
        const tr = document.createElement('tr');
        
        // Process name
        const tdName = document.createElement('td');
        tdName.className = 'proc-label';
        tdName.textContent = state.process_names[i];
        tr.appendChild(tdName);

        // Allocation
        for (let j = 0; j < m; j++) {
            const td = document.createElement('td');
            td.className = 'matrix-cell';
            td.textContent = state.allocation_matrix[i][j];
            tr.appendChild(td);
        }

        // Max
        for (let j = 0; j < m; j++) {
            const td = document.createElement('td');
            td.className = 'matrix-cell';
            td.textContent = state.max_matrix[i][j];
            tr.appendChild(td);
        }

        // Need
        for (let j = 0; j < m; j++) {
            const td = document.createElement('td');
            td.className = 'matrix-cell';
            td.textContent = state.need_matrix[i][j];
            tr.appendChild(td);
        }

        // Available (rowspan for first row)
        if (i === 0) {
            for (let j = 0; j < m; j++) {
                const td = document.createElement('td');
                td.className = 'matrix-cell avail-col';
                td.rowSpan = n;
                td.textContent = state.available[j];
                tr.appendChild(td);
            }
        }

        tbody.appendChild(tr);
    }

    // Utilization Bars
    const utilGrid = document.getElementById('utilization-bars');
    utilGrid.innerHTML = '';
    for (let j = 0; j < m; j++) {
        const rName = state.resource_names[j];
        const pct = state.utilization[rName] || 0;
        const total = state.total_resources[j];
        const allocated = total - state.available[j];

        const card = document.createElement('div');
        card.className = 'util-card';
        card.innerHTML = `
            <div class="util-card-header">
                <strong>Resource ${rName}</strong>
                <span>${allocated}/${total} (${pct}%)</span>
            </div>
            <div class="util-bar-track">
                <div class="util-bar-fill" style="width: ${pct}%"></div>
            </div>
        `;
        utilGrid.appendChild(card);
    }

    // Populate Request and Release Forms
    populateProcessDropdown('req-process-select', state);
    populateProcessDropdown('rel-process-select', state);
    populateVectorInputs('req-vector-inputs', state.resource_names, 'req-res-');
    populateVectorInputs('rel-vector-inputs', state.resource_names, 'rel-res-');
}

function populateProcessDropdown(elementId, state) {
    const select = document.getElementById(elementId);
    select.innerHTML = '';
    for (let i = 0; i < state.num_processes; i++) {
        const opt = document.createElement('option');
        opt.value = i;
        opt.textContent = `${state.process_names[i]}`;
        select.appendChild(opt);
    }
}

function populateVectorInputs(containerId, resourceNames, prefix) {
    const container = document.getElementById(containerId);
    container.innerHTML = '';
    resourceNames.forEach((name, idx) => {
        const wrapper = document.createElement('div');
        wrapper.innerHTML = `
            <label style="font-size:0.75rem;display:block;text-align:center;">${name}</label>
            <input type="number" min="0" value="0" class="form-control" id="${prefix}${idx}">
        `;
        container.appendChild(wrapper);
    });
}

// Setup Event Listeners
function setupEventListeners() {
    // Preset buttons
    document.querySelectorAll('.btn-preset').forEach(btn => {
        btn.addEventListener('click', async () => {
            document.querySelectorAll('.btn-preset').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            const preset = btn.getAttribute('data-preset');
            await loadPreset(preset);
        });
    });

    // Run Safety Algorithm
    document.getElementById('btn-run-safety').addEventListener('click', runSafetyAlgorithm);

    // Request Form
    document.getElementById('request-form').addEventListener('submit', handleResourceRequest);

    // Release Form
    document.getElementById('release-form').addEventListener('submit', handleResourceRelease);

    // Benchmark Button
    document.getElementById('btn-run-benchmark').addEventListener('click', runBenchmarkTask);
}

// Load Preset
async function loadPreset(presetName) {
    try {
        const res = await fetch('/api/load-preset', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ preset: presetName })
        });
        const data = await res.json();
        if (data.success) {
            currentState = data.state;
            renderState(currentState);
            resetTrace();
            resetRequestAlert();
            updateStatusBadge('Ready', 'badge-neutral');
        }
    } catch (err) {
        console.error('Failed to load preset:', err);
    }
}

// Safety Algorithm Execution
async function runSafetyAlgorithm() {
    try {
        const res = await fetch('/api/check-safety', { method: 'POST' });
        const data = await res.json();
        if (data.success) {
            renderSafetyTrace(data.result);
        }
    } catch (err) {
        console.error('Safety check failed:', err);
    }
}

function renderSafetyTrace(result) {
    const alertBox = document.getElementById('safe-seq-alert');
    const alertTitle = document.getElementById('alert-title');
    const alertMessage = document.getElementById('alert-message');
    const alertIcon = document.getElementById('alert-icon');
    const allSeqsContainer = document.getElementById('all-seqs-container');
    const allSeqsList = document.getElementById('all-seqs-list');

    alertBox.classList.remove('hidden', 'alert-safe', 'alert-unsafe');

    if (result.is_safe) {
        alertBox.classList.add('alert-safe');
        alertIcon.textContent = '✓';
        alertTitle.textContent = 'SYSTEM IS IN A SAFE STATE';
        alertMessage.innerHTML = `<strong>Safe Sequence:</strong> ${result.safe_sequence.join(' &rarr; ')}`;
        updateStatusBadge('SAFE STATE', 'badge-safe');

        if (result.all_safe_sequences && result.all_safe_sequences.length > 1) {
            allSeqsContainer.classList.remove('hidden');
            allSeqsList.innerHTML = '';
            result.all_safe_sequences.forEach((seq) => {
                const chip = document.createElement('span');
                chip.className = 'seq-chip';
                chip.textContent = seq.join(' → ');
                allSeqsList.appendChild(chip);
            });
        } else {
            allSeqsContainer.classList.add('hidden');
        }
    } else {
        alertBox.classList.add('alert-unsafe');
        alertIcon.textContent = '⚠';
        alertTitle.textContent = 'SYSTEM IS IN AN UNSAFE STATE!';
        alertMessage.textContent = 'Deadlock danger: No valid topological completion sequence satisfies remaining process needs.';
        allSeqsContainer.classList.add('hidden');
        updateStatusBadge('UNSAFE STATE', 'badge-unsafe');
    }

    // Populate Trace Table
    const tbody = document.getElementById('trace-tbody');
    tbody.innerHTML = '';

    if (result.steps.length === 0) {
        tbody.innerHTML = `<tr><td colspan="7" class="placeholder-text">No processes could complete with currently available resources.</td></tr>`;
        return;
    }

    result.steps.forEach(s => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>#${s.step_number}</td>
            <td class="proc-label">${s.process_name}</td>
            <td>[${s.work_before.join(', ')}]</td>
            <td>[${s.need.join(', ')}]</td>
            <td>+ [${s.allocation.join(', ')}]</td>
            <td><strong>[${s.work_after.join(', ')}]</strong></td>
            <td><span style="color:var(--success)">Finished</span></td>
        `;
        tbody.appendChild(tr);
    });
}

// Handle Resource Request
async function handleResourceRequest(e) {
    e.preventDefault();
    const pid = parseInt(document.getElementById('req-process-select').value, 10);
    const m = currentState.num_resources;
    const reqVector = [];

    for (let j = 0; j < m; j++) {
        const val = parseInt(document.getElementById(`req-res-${j}`).value, 10) || 0;
        reqVector.push(val);
    }

    try {
        const res = await fetch('/api/request', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ process_id: pid, request: reqVector })
        });
        const data = await res.json();
        
        if (data.success) {
            const outcome = data.outcome;
            displayRequestOutcome(outcome);
            if (data.state) {
                currentState = data.state;
                renderState(currentState);
            }
            if (outcome.safety_result) {
                renderSafetyTrace(outcome.safety_result);
            }
        } else {
            displayRequestOutcome({
                granted: false,
                status_code: 'ERROR',
                message: data.message
            });
        }
    } catch (err) {
        console.error('Request error:', err);
    }
}

function displayRequestOutcome(outcome) {
    const banner = document.getElementById('request-result-banner');
    const title = document.getElementById('request-result-title');
    const body = document.getElementById('request-result-body');

    banner.classList.remove('hidden', 'alert-safe', 'alert-unsafe', 'alert-warning');

    if (outcome.granted) {
        banner.classList.add('alert-safe');
        title.textContent = `[GRANTED] ${outcome.status_code}`;
        body.textContent = outcome.message;
    } else {
        banner.classList.add('alert-unsafe');
        title.textContent = `[DENIED] ${outcome.status_code}`;
        body.textContent = outcome.message;
    }
}

// Handle Resource Release
async function handleResourceRelease(e) {
    e.preventDefault();
    const pid = parseInt(document.getElementById('rel-process-select').value, 10);
    const m = currentState.num_resources;
    const relVector = [];

    for (let j = 0; j < m; j++) {
        const val = parseInt(document.getElementById(`rel-res-${j}`).value, 10) || 0;
        relVector.push(val);
    }

    try {
        const res = await fetch('/api/release', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ process_id: pid, release: relVector })
        });
        const data = await res.json();
        
        alert(data.message);
        if (data.success && data.state) {
            currentState = data.state;
            renderState(currentState);
            resetTrace();
        }
    } catch (err) {
        console.error('Release error:', err);
    }
}

// Benchmark
async function runBenchmarkTask() {
    const btn = document.getElementById('btn-run-benchmark');
    btn.textContent = 'Measuring...';
    btn.disabled = true;

    try {
        const res = await fetch('/api/benchmark');
        const data = await res.json();
        if (data.success) {
            const container = document.getElementById('benchmark-results');
            const tbody = document.getElementById('benchmark-tbody');
            tbody.innerHTML = '';
            container.classList.remove('hidden');

            data.benchmark.forEach(row => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>n = ${row.num_processes}</td>
                    <td>${row.avg_time_ms} ms</td>
                    <td>${row.operations_theoretical}</td>
                `;
                tbody.appendChild(tr);
            });
        }
    } catch (err) {
        console.error('Benchmark error:', err);
    } finally {
        btn.textContent = 'Run Benchmark';
        btn.disabled = false;
    }
}

function updateStatusBadge(text, className) {
    const badge = document.getElementById('system-status-badge');
    badge.className = `badge ${className}`;
    badge.textContent = `Status: ${text}`;
}

function resetTrace() {
    document.getElementById('safe-seq-alert').classList.add('hidden');
    document.getElementById('trace-tbody').innerHTML = `<tr><td colspan="7" class="placeholder-text">Click "Run Safety Algorithm" to view step-by-step trace execution.</td></tr>`;
}

function resetRequestAlert() {
    document.getElementById('request-result-banner').classList.add('hidden');
}
