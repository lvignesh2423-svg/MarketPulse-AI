// Auto-detect: use localhost for local dev, or the deployed backend URL
const API_BASE = window.location.hostname === 'localhost' 
    ? 'http://localhost:8000' 
    : 'https://finoracle.up.railway.app'; // Change this to your Railway URL after deploy

// Tilt effect for cards
document.querySelectorAll('[data-tilt]').forEach(card => {
    card.addEventListener('mousemove', (e) => {
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        const centerX = rect.width / 2;
        const centerY = rect.height / 2;
        const rotateX = (y - centerY) / 10;
        const rotateY = (centerX - x) / 10;
        
        card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateZ(20px)`;
    });
    
    card.addEventListener('mouseleave', () => {
        card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) translateZ(0)';
    });
});

// Select stock from watchlist
function selectStock(symbol) {
    document.getElementById('symbolInput').value = symbol;
    analyzeStock();
}

// Show/hide elements
function showElement(id) {
    document.getElementById(id).classList.remove('hidden');
}

function hideElement(id) {
    document.getElementById(id).classList.add('hidden');
}

// Load performance metrics
async function loadPerformanceMetrics() {
    try {
        const response = await fetch(`${API_BASE}/api/performance`);
        const data = await response.json();
        
        document.getElementById('perfAccuracy').textContent = data.avg_accuracy + '%';
        document.getElementById('perfLatency').textContent = data.avg_latency + 's';
        document.getElementById('perfRisk').textContent = data.avg_risk_score.toFixed(2);
        document.getElementById('perfAnalyses').textContent = data.total_analyses;
        
        // Update bars
        document.querySelector('.perf-fill').style.width = data.avg_accuracy + '%';
        document.querySelector('.perf-fill.blue').style.width = (data.avg_latency * 50) + '%';
        document.querySelector('.perf-fill.purple').style.width = (data.avg_risk_score * 100) + '%';
    } catch (error) {
        console.error('Error loading performance metrics:', error);
    }
}

// Load RAG context
async function loadRAGContext(query) {
    try {
        const response = await fetch(`${API_BASE}/api/rag/context?q=${encodeURIComponent(query)}`);
        const data = await response.json();
        
        const ragElement = document.getElementById('ragContext');
        if (data.context && data.context !== "No relevant regulatory or analytical context available.") {
            const sources = data.context.split('\n\n');
            ragElement.innerHTML = sources.map(source => {
                const parts = source.split('] ');
                const sourceName = parts[0].replace('[Source: ', '');
                const text = parts.slice(1).join('] ');
                return `
                    <div style="margin-bottom: 12px;">
                        <span class="rag-source">${sourceName}</span>
                        <p class="rag-text">${text}</p>
                    </div>
                `;
            }).join('');
        }
    } catch (error) {
        console.error('Error loading RAG context:', error);
    }
}

// Main analyze function
async function analyzeStock() {
    const symbol = document.getElementById('symbolInput').value.toUpperCase();
    const riskProfile = document.getElementById('riskProfile').value;

    // Show loading
    hideElement('results');
    hideElement('placeholder');
    showElement('loadingScreen');

    try {
        const response = await fetch(`${API_BASE}/api/analyze`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                symbol: symbol,
                user_profile: {
                    user_id: 'demo_user',
                    name: 'Demo User',
                    risk_tolerance: riskProfile,
                    portfolio: [],
                    watchlist: [],
                    investment_horizon: 'medium'
                }
            })
        });

        const data = await response.json();
        
        // Load RAG context for this stock
        loadRAGContext(`${symbol} analysis fundamentals technical`);
        
        // Simulate loading for better UX
        setTimeout(() => {
            hideElement('loadingScreen');
            displayResults(data, symbol);
            loadPerformanceMetrics();
        }, 2000);
        
    } catch (error) {
        hideElement('loadingScreen');
        showElement('placeholder');
        alert('Error connecting to backend. Make sure server is running on port 8000.');
        console.error(error);
    }
}

function displayResults(data, symbol) {
    showElement('results');

    // Market Data
    const md = data.market_data;
    document.getElementById('marketInfo').innerHTML = `
        <div class="metric-3d">
            <span class="metric-label-3d">PRICE</span>
            <span class="metric-value-3d">$${md.current_price.toLocaleString()}</span>
        </div>
        <div class="metric-3d">
            <span class="metric-label-3d">24H CHANGE</span>
            <span class="metric-value-3d" style="color: ${md.price_change >= 0 ? 'var(--green)' : 'var(--red)'}">
                ${md.price_change >= 0 ? '+' : ''}${md.price_change_pct}%
            </span>
        </div>
        <div class="metric-3d">
            <span class="metric-label-3d">RSI (14)</span>
            <span class="metric-value-3d">${md.rsi}</span>
        </div>
        <div class="metric-3d">
            <span class="metric-label-3d">VOLUME RATIO</span>
            <span class="metric-value-3d">${md.volume_ratio}x</span>
        </div>
        <div class="metric-3d">
            <span class="metric-label-3d">SMA 20</span>
            <span class="metric-value-3d">$${md.sma_20.toLocaleString()}</span>
        </div>
        <div class="metric-3d">
            <span class="metric-label-3d">RANGE</span>
            <span class="metric-value-3d" style="font-size: 12px;">$${md.period_low} - $${md.period_high}</span>
        </div>
    `;

    // Recommendation
    const rec = data.recommendation;
    document.getElementById('recommendation').innerHTML = `
        <div style="display: flex; align-items: center; gap: 20px; margin-bottom: 16px;">
            <div class="signal-badge-3d ${rec.recommendation.toLowerCase()}">${rec.recommendation}</div>
            <span style="font-family: 'Orbitron', monospace; font-size: 24px; font-weight: 700;">
                ${(rec.confidence * 100).toFixed(1)}%
            </span>
            ${data.response_time ? `<span style="font-size: 11px; color: rgba(255,255,255,0.4);">Response: ${data.response_time}s</span>` : ''}
        </div>
        <div class="confidence-bar-3d">
            <div class="confidence-fill-3d" style="width: ${rec.confidence * 100}%"></div>
        </div>
        <div style="display: flex; gap: 20px; font-size: 11px; color: rgba(255,255,255,0.5);">
            <span>RISK ADJUSTED: ${rec.risk_adjusted ? 'YES' : 'NO'}</span>
            <span>•</span>
            <span>${symbol}</span>
            ${data.session_id ? `<span>• Session: ${data.session_id}</span>` : ''}
        </div>
    `;

    // Agent Outputs
    data.agent_outputs.forEach(agent => {
        const prefix = agent.agent_name.split(' ')[0].toLowerCase();
        const signalId = prefix === 'technical' ? 'techSignal' : 
                        prefix === 'fundamental' ? 'fundSignal' : 'sentSignal';
        const outputId = prefix + 'Output';
        
        const signalEl = document.getElementById(signalId);
        const outputEl = document.getElementById(outputId);
        
        if (signalEl) {
            const signalType = agent.signal.signal_type.toUpperCase();
            signalEl.textContent = signalType;
            signalEl.className = 'agent-signal signal-badge-3d ' + agent.signal.signal_type.toLowerCase();
        }
        
        if (outputEl) {
            outputEl.innerHTML = `
                <div style="margin-bottom: 8px;">
                    <span class="signal-badge-3d ${agent.signal.signal_type.toLowerCase()}" style="margin-right: 8px;">
                        ${agent.signal.signal_type}
                    </span>
                    <span style="font-family: 'Orbitron', monospace; font-size: 11px; color: rgba(255,255,255,0.5);">
                        ${(agent.signal.confidence * 100).toFixed(1)}% CONFIDENCE
                    </span>
                </div>
                <p style="font-size: 11px; line-height: 1.6; color: rgba(255,255,255,0.4);">
                    ${agent.signal.reasoning.substring(0, 150)}...
                </p>
                ${agent.signal.sources ? `
                    <div style="margin-top: 8px; font-size: 9px; color: var(--orange);">
                        Sources: ${agent.signal.sources.join(', ')}
                    </div>
                ` : ''}
            `;
        }
    });

    // Reasoning Chain
    document.getElementById('reasoningChain').innerHTML = `
        <ul class="reasoning-list">
            ${rec.reasoning_chain.map(r => `<li>${r}</li>`).join('')}
        </ul>
    `;

    // Portfolio
    document.getElementById('portfolio').innerHTML = `
        <div class="portfolio-item-3d">
            <span class="portfolio-symbol">RELIANCE</span>
            <span class="portfolio-qty">10 @ ₹2,450</span>
            <span class="portfolio-change positive">+2.3%</span>
        </div>
        <div class="portfolio-item-3d">
            <span class="portfolio-symbol">TCS</span>
            <span class="portfolio-qty">5 @ ₹3,800</span>
            <span class="portfolio-change negative">-1.1%</span>
        </div>
        <div class="portfolio-item-3d">
            <span class="portfolio-symbol">INFY</span>
            <span class="portfolio-qty">15 @ ₹1,520</span>
            <span class="portfolio-change positive">+1.8%</span>
        </div>
    `;
}

// Initialize
document.getElementById('symbolInput').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') analyzeStock();
});

// Load performance metrics on page load
window.onload = function() {
    loadPerformanceMetrics();
};

// Add some interactivity
document.querySelectorAll('.watch-item-3d').forEach(item => {
    item.addEventListener('mouseenter', function() {
        this.style.boxShadow = '0 0 30px rgba(249, 115, 22, 0.3)';
    });
    item.addEventListener('mouseleave', function() {
        this.style.boxShadow = 'none';
    });
});
