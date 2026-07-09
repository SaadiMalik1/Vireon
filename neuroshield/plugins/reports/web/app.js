let currentMode = 'eeg';
let securityActive = false;
let nspActive = false;
let activeAttack = 'none';

let confidenceHistory = Array(100).fill(1.0);
let timeStep = 0;

// Oscilloscope and Chart Canvas references
const oscCanvas = document.getElementById('oscilloscope');
const oscCtx = oscCanvas.getContext('2d');
const chartCanvas = document.getElementById('confidence-chart');
const chartCtx = chartCanvas.getContext('2d');

// Resize canvases dynamically
function resizeCanvases() {
    oscCanvas.width = oscCanvas.parentElement.clientWidth;
    oscCanvas.height = oscCanvas.parentElement.clientHeight;
    chartCanvas.width = chartCanvas.parentElement.clientWidth;
    chartCanvas.height = chartCanvas.parentElement.clientHeight;
}
window.addEventListener('resize', resizeCanvases);
resizeCanvases();

// REST API calls
async function postControl(params) {
    try {
        const response = await fetch('/api/control', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(params)
        });
        const data = await response.json();
        updateControlButtons(data.context);
        syncSliders(null, data.context); // sync slider contexts immediately
    } catch (e) {
        console.error("Control API write error:", e);
    }
}

function setMode(mode) {
    currentMode = mode;
    postControl({ dbs_mode: mode === 'dbs' });
}

function setHardwareMode(hw_mode) {
    postControl({ hardware_mode: hw_mode });
}

function toggleSecurity() {
    securityActive = !securityActive;
    postControl({ secure_mode: securityActive });
}

function toggleNSP() {
    nspActive = !nspActive;
    postControl({ nsp_mode: nspActive });
}

function injectAttack(attack) {
    activeAttack = attack;
    postControl({ active_attack: attack });
}

let paramTimeout = null;
let paramUpdates = {};

function updateParam(name, value) {
    const numericVal = parseFloat(value);
    
    // Update local label readout immediately to avoid lag
    const mapping = {
        'stimulation_amplitude_ma': 'lbl-stim-amp',
        'stimulation_frequency_hz': 'lbl-stim-freq',
        'impedance_kohm': 'lbl-impedance',
        'noise_intensity': 'lbl-noise',
        'attenuation_factor': 'lbl-attenuation',
        'battery_level': 'lbl-battery'
    };
    const labelId = mapping[name];
    if (labelId) {
        const precision = name.includes('freq') || name.includes('battery') ? 0 : (name.includes('attenuation') ? 2 : 1);
        document.getElementById(labelId).textContent = numericVal.toFixed(precision);
    }

    paramUpdates[name] = numericVal;
    if (paramTimeout) {
        clearTimeout(paramTimeout);
    }
    paramTimeout = setTimeout(() => {
        postControl(paramUpdates);
        paramUpdates = {};
    }, 100);
}

function updateControlButtons(context) {
    currentMode = context.dbs_mode ? 'dbs' : 'eeg';
    securityActive = context.secure_mode;
    nspActive = context.nsp_mode;
    activeAttack = context.active_attack;
    // Update mode buttons
    document.getElementById('btn-mode-eeg').classList.toggle('active', !context.dbs_mode);
    document.getElementById('btn-mode-dbs').classList.toggle('active', context.dbs_mode);

    // Update hardware mode buttons
    const hwMode = context.hardware_mode || false;
    document.getElementById('btn-mode-sim').classList.toggle('active', !hwMode);
    document.getElementById('btn-mode-hw').classList.toggle('active', hwMode);

    // Update active attack
    activeAttack = context.active_attack || 'none';
    const dropdown = document.getElementById('attack-dropdown');
    if (dropdown) {
        dropdown.value = activeAttack;
    }

    // 2. Security Shield button styling
    const secureBtn = document.getElementById('btn-secure');
    const secureLbl = document.getElementById('lbl-secure-status');
    if (context.secure_mode) {
        secureBtn.className = 'w-full py-3 px-4 rounded-xl font-bold tracking-wide transition-all duration-300 bg-white/10 border border-neonBlue text-neonBlue shadow-[0_0_15px_rgba(0,243,255,0.3)]';
        secureLbl.textContent = 'ON';
    } else {
        secureBtn.className = 'w-full py-3 px-4 rounded-xl font-bold tracking-wide transition-all duration-300 bg-black/40 border border-white/10 text-gray-400 hover:bg-white/5';
        secureLbl.textContent = 'OFF';
    }

    const nspBtn = document.getElementById('btn-nsp');
    const nspLbl = document.getElementById('lbl-nsp-status');
    if (context.nsp_mode) {
        nspBtn.className = 'w-full mt-2 py-3 px-4 rounded-xl font-bold tracking-wide transition-all duration-300 bg-white/10 border border-neonPurple text-neonPurple shadow-[0_0_15px_rgba(183,0,255,0.3)]';
        nspLbl.textContent = 'ON';
    } else {
        nspBtn.className = 'w-full mt-2 py-3 px-4 rounded-xl font-bold tracking-wide transition-all duration-300 bg-black/40 border border-white/10 text-gray-400 hover:bg-white/5';
        nspLbl.textContent = 'OFF';
    }

    // 3. Attack button highlights
    const attackMap = {
        'none': 'btn-attack-none',
        'noise': 'btn-attack-noise',
        'drift': 'btn-attack-drift',
        'impedance': 'btn-attack-impedance',
        'suppression': 'btn-attack-suppression',
        'stimulation_leak': 'btn-attack-leak',
        'phase_shift': 'btn-attack-phase'
    };
    
    for (const [key, id] of Object.entries(attackMap)) {
        const btn = document.getElementById(id);
        if (btn) {
            btn.classList.toggle('active', activeAttack === key);
        }
    }
}

function syncSliders(state, context) {
    const activeEl = document.activeElement;
    
    const mapping = [];
    if (state) {
        mapping.push({ id: 'slide-stim-amp', lbl: 'lbl-stim-amp', val: state.stimulation_amplitude_ma, precision: 1 });
        mapping.push({ id: 'slide-stim-freq', lbl: 'lbl-stim-freq', val: state.stimulation_frequency_hz, precision: 0 });
        mapping.push({ id: 'slide-battery', lbl: 'lbl-battery', val: state.battery_level, precision: 0 });
    }
    if (context) {
        mapping.push({ id: 'slide-impedance', lbl: 'lbl-impedance', val: context.impedance_kohm, precision: 1 });
        mapping.push({ id: 'slide-noise', lbl: 'lbl-noise', val: context.noise_intensity, precision: 1 });
        mapping.push({ id: 'slide-attenuation', lbl: 'lbl-attenuation', val: context.attenuation_factor, precision: 2 });
    }

    for (const item of mapping) {
        const input = document.getElementById(item.id);
        const label = document.getElementById(item.lbl);
        if (input && label) {
            if (activeEl !== input) {
                input.value = item.val;
                label.textContent = item.val.toFixed(item.precision);
            }
        }
    }
}

// Telemetry & Waveform state
let ws = null;
let signalBuffer = [];

function handleTelemetryState(state) {
    // Update connection tag
    const connTag = document.getElementById('lbl-connection');
    if (state.connected) {
        connTag.className = 'text-xs font-bold text-neonGreen';
        connTag.textContent = 'CONNECTED';
    } else {
        connTag.className = 'text-xs font-bold text-gray-500';
        connTag.textContent = 'DISCONNECTED';
    }

    const nspChip = document.getElementById('lbl-nsp-chip');
    if (state.nsp_active) {
        nspChip.classList.remove('hidden');
    } else {
        nspChip.classList.add('hidden');
    }

    // Update Severity Risk card styles
    const severityCard = document.getElementById('card-severity');
    const severityVal = document.getElementById('val-severity');
    const hazardVal = document.getElementById('val-hazard-state');
    
    if (state.niss_score !== undefined) {
        severityVal.textContent = state.iso_severity;
        hazardVal.textContent = `NISS: ${state.niss_score.toFixed(1)} | ${state.hazard_state}`;
        severityCard.className = 'glass-panel p-6 rounded-2xl transition-all duration-300 border-l-4';
        if (state.iso_severity === 'CRITICAL') {
            severityCard.classList.add('border-l-neonRed');
            severityVal.style.color = '#ff0055';
        } else if (state.iso_severity === 'MARGINAL') {
            severityCard.classList.add('border-l-yellow-400');
            severityVal.style.color = '#facc15'; // yellow-400
        } else {
            severityCard.classList.add('border-l-neonGreen');
            severityVal.style.color = '#00ff9d';
        }
    } else {
        severityVal.textContent = state.iso_severity;
        hazardVal.textContent = state.hazard_state;
        severityCard.className = 'glass-panel p-6 rounded-2xl transition-all duration-300 border-l-4';
        if (state.iso_severity === 'CATASTROPHIC') {
            severityCard.classList.add('border-l-neonRed', 'pulse-red');
            severityVal.style.color = '#ff0055';
        } else if (state.iso_severity === 'CRITICAL') {
            severityCard.classList.add('border-l-neonRed');
            severityVal.style.color = '#ff0055';
        } else if (state.iso_severity === 'MARGINAL') {
            severityCard.classList.add('border-l-yellow-400');
            severityVal.style.color = '#facc15';
        } else {
            severityCard.classList.add('border-l-neonGreen');
            severityVal.style.color = '#00ff9d';
        }
    }

    if (state.temperature_celsius !== undefined) {
        const tempVal = document.getElementById('val-temperature');
        const tempState = document.getElementById('val-temp-state');
        const tempCard = document.getElementById('card-temperature');
        if (tempVal && tempState && tempCard) {
            tempVal.textContent = `${state.temperature_celsius.toFixed(1)} °C`;
            tempCard.className = 'glass-panel p-6 rounded-2xl transition-all duration-300 border-l-4';
            if (state.temperature_celsius >= 40.0) {
                tempCard.classList.add('border-l-neonRed', 'pulse-red');
                tempState.textContent = "THERMAL HAZARD";
                tempVal.style.color = '#ff0055';
            } else if (state.temperature_celsius >= 39.0) {
                tempCard.classList.add('border-l-yellow-400');
                tempState.textContent = "ELEVATED";
                tempVal.style.color = '#facc15';
            } else {
                tempCard.classList.add('border-l-neonGreen');
                tempState.textContent = "NOMINAL";
                tempVal.style.color = '#00ff9d';
            }
        }
    }

    // Update Stimulation Card
    const stimCard = document.getElementById('card-stimulation');
    const stimVal = document.getElementById('val-stimulation');
    const stimParams = document.getElementById('val-stimulation-params');
    
    if (state.stimulation_enabled) {
        stimVal.textContent = 'ACTIVE';
        stimVal.style.color = '#00f3ff';
        stimParams.textContent = `${state.stimulation_amplitude_ma.toFixed(1)} mA @ ${state.stimulation_frequency_hz.toFixed(1)} Hz`;
        stimCard.style.boxShadow = '0 0 15px rgba(0, 243, 255, 0.2)';
        stimCard.className = 'glass-panel p-6 rounded-2xl transition-all duration-300 border-l-4 border-l-neonBlue';
    } else {
        stimVal.textContent = 'SUSPENDED';
        stimVal.style.color = '#9ca3af';
        stimParams.textContent = '0.0 mA @ 0.0 Hz';
        stimCard.style.boxShadow = 'none';
        stimCard.className = 'glass-panel p-6 rounded-2xl transition-all duration-300 border-l-4 border-l-gray-600';
    }

    // Update Decoder Confidence Card
    const confVal = document.getElementById('val-confidence');
    confVal.textContent = state.decoder_confidence.toFixed(2);
    if (state.decoder_confidence < 0.7) {
        confVal.style.color = '#ff0055';
    } else if (state.decoder_confidence < 0.9) {
        confVal.style.color = '#facc15';
    } else {
        confVal.style.color = '#00f3ff';
    }

    // Update electrode contact impedances
    if (state.electrode_impedances && state.num_channels) {
        const gridContainer = document.getElementById('electrode-grid-container');
        if (gridContainer && gridContainer.children.length !== state.num_channels) {
            // Rebuild the grid
            gridContainer.innerHTML = '';
            for (let ch = 0; ch < state.num_channels; ch++) {
                const elDiv = document.createElement('div');
                elDiv.className = 'bg-black/40 border border-white/5 rounded-lg p-3 flex flex-col items-center justify-center gap-1';
                elDiv.id = `el-${ch}`;
                elDiv.innerHTML = `
                    <span class="text-xs text-gray-400">Ch ${ch}</span>
                    <span class="font-mono text-neonGreen text-sm font-bold el-val">5.0 kΩ</span>
                `;
                gridContainer.appendChild(elDiv);
            }
        }

        for (let ch = 0; ch < state.num_channels; ch++) {
            const el = document.getElementById(`el-${ch}`);
            if (el) {
                const valSpan = el.querySelector('.el-val');
                if (valSpan) {
                    const imp = state.electrode_impedances[ch] !== undefined ? state.electrode_impedances[ch] : 5.0;
                    valSpan.textContent = `${imp.toFixed(1)} kΩ`;
                    valSpan.className = 'font-mono text-sm font-bold el-val '; 
                    if (imp < 15.0) {
                        valSpan.className += 'text-neonGreen';
                    } else if (imp < 50.0) {
                        valSpan.className += 'text-yellow-400';
                    } else {
                        valSpan.className += 'text-neonRed';
                    }
                }
            }
        }
    }

    // Update Diagnostics stats
    document.getElementById('lbl-blocked-attacks').textContent = state.blocked_attacks_count;
    document.getElementById('lbl-blocked-mtu').textContent = state.blocked_mtu_abuses;
    document.getElementById('lbl-tissue-risk').textContent = state.tissue_damage_risk;
    
    const clampBadge = document.getElementById('lbl-clamp-active');
    if (state.clamping_active) {
        clampBadge.textContent = 'ACTIVE';
        clampBadge.className = 'px-2 py-1 rounded bg-neonRed/20 font-mono text-neonRed font-bold';
    } else {
        clampBadge.textContent = 'INACTIVE';
        clampBadge.className = 'px-2 py-1 rounded bg-white/5 font-mono text-gray-400 font-bold';
    }

    // Sync slider positions from live telemetry values
    syncSliders(state, null);

    // Accumulate confidence history
    confidenceHistory.push(state.decoder_confidence);
    if (confidenceHistory.length > 100) {
        confidenceHistory.shift();
    }

    // Accumulate streamed signal chunk for the oscilloscope visualizer
    if (state.signal_chunk && Array.isArray(state.signal_chunk)) {
        signalBuffer = signalBuffer.concat(state.signal_chunk);
        // Cap buffer to double the width of the oscilloscope to conserve RAM
        const maxSamples = oscCanvas.width * 2;
        if (signalBuffer.length > maxSamples) {
            signalBuffer.splice(0, signalBuffer.length - maxSamples);
        }
    }
}

// WebSocket Connection Handlers
function connectWebSocket() {
    // Establish connection to adjacent port (location.port + 1)
    const wsPort = parseInt(location.port) + 1;
    const wsToken = window.WS_TOKEN || "";
    const wsUrl = `ws://${location.hostname}:${wsPort}/?token=${wsToken}`;
    ws = new WebSocket(wsUrl);

    ws.onopen = () => {
        const connTag = document.getElementById('lbl-connection');
        connTag.className = 'conn-tag tag-connected';
        connTag.textContent = 'Connected';
    };

    ws.onmessage = (event) => {
        try {
            const state = JSON.parse(event.data);
            handleTelemetryState(state);
        } catch (e) {
            console.error("Failed to parse telemetry event message:", e);
        }
    };

    ws.onclose = () => {
        const connTag = document.getElementById('lbl-connection');
        connTag.className = 'conn-tag tag-disconnected';
        connTag.textContent = 'Disconnected';
        // Try reconnecting after 2 seconds
        setTimeout(connectWebSocket, 2000);
    };

    ws.onerror = (err) => {
        console.error("WebSocket server connection error:", err);
    };
}

// Oscilloscope Generator Waveform loop (Canvas animation)
function animateOscilloscope() {
    requestAnimationFrame(animateOscilloscope);
    
    oscCtx.clearRect(0, 0, oscCanvas.width, oscCanvas.height);
    
    // Draw background horizontal center line
    oscCtx.beginPath();
    oscCtx.strokeStyle = 'rgba(255, 255, 255, 0.05)';
    oscCtx.lineWidth = 1;
    oscCtx.moveTo(0, oscCanvas.height / 2);
    oscCtx.lineTo(oscCanvas.width, oscCanvas.height / 2);
    oscCtx.stroke();

    oscCtx.beginPath();
    oscCtx.lineWidth = 2.5;
    
    // Select oscilloscope waveform styling based on active attacks
    if (activeAttack === 'suppression') {
        oscCtx.strokeStyle = '#9ca3af'; // gray
        oscCtx.moveTo(0, oscCanvas.height / 2);
        oscCtx.lineTo(oscCanvas.width, oscCanvas.height / 2);
        oscCtx.stroke();
        return; // Flatline
    }
    
    if (activeAttack === 'noise' || activeAttack.startsWith('qif-')) {
        // Generic red alert for injected dynamic attacks
        oscCtx.strokeStyle = '#ff0055'; // neonRed
    } else if (activeAttack === 'phase_shift') {
        oscCtx.strokeStyle = '#b700ff'; // neonPurple
    } else {
        oscCtx.strokeStyle = '#00f3ff'; // neonBlue
    }

    const midY = oscCanvas.height / 2;
    const w = oscCanvas.width;
    
    if (signalBuffer.length > 0) {
        // Draw real-time streamed signal points
        const samplesToShow = Math.min(signalBuffer.length, w);
        const startIndex = signalBuffer.length - samplesToShow;
        
        for (let x = 0; x < samplesToShow; x++) {
            const val = signalBuffer[startIndex + x];
            // Scale raw microvolts visually
            const y = val * 1.5;
            
            if (x === 0) {
                oscCtx.moveTo(x, midY + y);
            } else {
                oscCtx.lineTo(x, midY + y);
            }
        }
    } else {
        // Flatline placeholder if connection is dead/empty
        oscCtx.moveTo(0, midY);
        oscCtx.lineTo(w, midY);
    }
    
    oscCtx.stroke();
}

// Rolling Confidence Line Chart Loop
function animateConfidenceChart() {
    requestAnimationFrame(animateConfidenceChart);
    
    chartCtx.clearRect(0, 0, chartCanvas.width, chartCanvas.height);
    
    const w = chartCanvas.width;
    const h = chartCanvas.height;
    
    // Draw Y safety boundary limit line (0.70 threshold)
    const limitY = h - (0.70 * h);
    chartCtx.beginPath();
    chartCtx.strokeStyle = '#facc15'; // yellow
    chartCtx.lineWidth = 1.5;
    chartCtx.setLineDash([5, 5]);
    chartCtx.moveTo(0, limitY);
    chartCtx.lineTo(w, limitY);
    chartCtx.stroke();
    chartCtx.setLineDash([]); // Reset
    
    // Draw safety limit text
    chartCtx.fillStyle = '#facc15';
    chartCtx.font = '10px Space Grotesk';
    chartCtx.fillText('0.70 Safety Limit', 10, limitY - 5);

    // Draw Rolling confidence line
    chartCtx.beginPath();
    chartCtx.strokeStyle = '#00f3ff'; // neonBlue
    chartCtx.lineWidth = 3;
    
    const step = w / 99;
    for (let i = 0; i < confidenceHistory.length; i++) {
        const x = i * step;
        const y = h - (confidenceHistory[i] * h * 0.9 + h * 0.05); // Keep padding
        
        if (i === 0) {
            chartCtx.moveTo(x, y);
        } else {
            chartCtx.lineTo(x, y);
        }
    }
    chartCtx.stroke();
}

// Initial initialization loads the current server-side configurations
async function init() {
    // 1. Fetch QIF data to populate attack dropdown
    try {
        const qifRes = await fetch('/api/qif.json');
        if (qifRes.ok) {
            const qifData = await qifRes.json();
            const techniques = qifData.threats?.techniques || [];
            const dropdown = document.getElementById('attack-dropdown');
            
            // Group by tactic/category
            const optgroups = {};
            
            techniques.forEach(tech => {
                const cat = tech.category || "Other";
                if (!optgroups[cat]) {
                    const group = document.createElement('optgroup');
                    group.label = `Category: ${cat}`;
                    optgroups[cat] = group;
                    dropdown.appendChild(group);
                }
                const option = document.createElement('option');
                option.value = tech.id.toLowerCase();
                option.textContent = `${tech.id} - ${tech.name}`;
                optgroups[cat].appendChild(option);
            });
        }
    } catch (e) {
        console.error("Failed to fetch QIF data:", e);
    }

    // 2. Poll context initially to align buttons
    try {
        const res = await fetch('/api/control', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({})
        });
        const data = await res.json();
        updateControlButtons(data.context);
        syncSliders(null, data.context); // Sync slider inputs initially
    } catch (e) {
        console.error("Failed to connect to BCI REST API server on launch:", e);
    }

    // Launch WebSockets and animations
    connectWebSocket();
    animateOscilloscope();
    animateConfidenceChart();
}

init();
