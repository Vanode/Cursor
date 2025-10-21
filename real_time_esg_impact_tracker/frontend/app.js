// ESG Impact Tracker Frontend JavaScript

const API_BASE_URL = 'http://localhost:5000';

// DOM Elements
const analyzeForm = document.getElementById('analyzeForm');
const companyNameInput = document.getElementById('companyName');
const analyzeBtn = document.getElementById('analyzeBtn');
const analysisResult = document.getElementById('analysisResult');
const companiesList = document.getElementById('companiesList');
const alertsList = document.getElementById('alertsList');
const refreshBtn = document.getElementById('refreshBtn');
const statusText = document.getElementById('statusText');

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    loadInitialData();
    setupEventListeners();
});

// Event Listeners
function setupEventListeners() {
    analyzeForm.addEventListener('submit', handleAnalyze);
    refreshBtn.addEventListener('click', loadInitialData);
    
    // Risk threshold slider
    const riskThreshold = document.getElementById('riskThreshold');
    const thresholdValue = document.getElementById('thresholdValue');
    if (riskThreshold && thresholdValue) {
        riskThreshold.addEventListener('input', (e) => {
            thresholdValue.textContent = `(${parseFloat(e.target.value).toFixed(2)})`;
        });
    }
}

// Load initial data
async function loadInitialData() {
    await Promise.all([
        loadCompanies(),
        loadAlerts(),
        checkHealth()
    ]);
    updateAverageScores();
}

// Check API health
async function checkHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        const data = await response.json();
        
        if (data.status === 'ok') {
            updateStatus('Connected', true);
        } else {
            updateStatus('Disconnected', false);
        }
    } catch (error) {
        console.error('Health check failed:', error);
        updateStatus('Disconnected', false);
    }
}

// Update status indicator
function updateStatus(text, isConnected) {
    statusText.textContent = text;
    const statusDot = document.querySelector('.status-dot');
    statusDot.style.background = isConnected ? 'var(--success)' : 'var(--danger)';
}

// Handle company analysis
async function handleAnalyze(e) {
    e.preventDefault();
    
    const companyName = companyNameInput.value.trim();
    if (!companyName) return;
    
    // Get advanced settings
    const riskThreshold = parseFloat(document.getElementById('riskThreshold')?.value || 0.3);
    const maxArticles = parseInt(document.getElementById('maxArticles')?.value || 20);
    const autoCreateAlerts = document.getElementById('autoCreateAlerts')?.checked || false;
    
    setLoading(analyzeBtn, true);
    hideResult();
    
    try {
        // First, analyze the company
        const analyzeResponse = await fetch(`${API_BASE_URL}/api/analyze/company`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                company_name: companyName,
                max_articles: maxArticles
            })
        });
        
        const analyzeData = await analyzeResponse.json();
        
        if (!analyzeResponse.ok) {
            showResult(analyzeData, false);
            return;
        }
        
        // Then, detect risks with the specified threshold
        const detectResponse = await fetch(`${API_BASE_URL}/api/alerts/detect`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                company_name: companyName,
                threshold: riskThreshold,
                auto_create: autoCreateAlerts
            })
        });
        
        const detectData = await detectResponse.json();
        
        // Show combined results
        const resultMessage = `
            <strong>Analysis Complete</strong><br>
            ESG Scores calculated: ${analyzeData.analysis?.esg_scores ? 'Yes' : 'In Progress'}<br>
            Risks detected: ${detectData.risks_detected || 0}<br>
            Alerts created: ${detectData.alerts_created || 0}
        `;
        
        showResult({ 
            company_name: companyName, 
            message: resultMessage,
            risks: detectData.risks || []
        }, true);
        
        // Refresh lists
        await Promise.all([
            loadCompanies(),
            loadAlerts()
        ]);
        updateAverageScores();
        
    } catch (error) {
        console.error('Analysis failed:', error);
        showResult({ error: 'Failed to connect to server. Please ensure the backend is running.' }, false);
    } finally {
        setLoading(analyzeBtn, false);
    }
}

// Load companies
async function loadCompanies() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/alerts/companies`);
        const companies = await response.json();
        
        displayCompanies(companies);
        
    } catch (error) {
        console.error('Failed to load companies:', error);
        companiesList.innerHTML = '<div class="empty-state">Failed to load companies</div>';
    }
}

// Display companies
function displayCompanies(companies) {
    if (companies.length === 0) {
        companiesList.innerHTML = '<div class="empty-state">No companies tracked yet. Analyze a company to get started!</div>';
        return;
    }
    
    companiesList.innerHTML = companies.map(company => `
        <div class="company-item">
            <div class="company-header">
                <div>
                    <div class="company-name">${company.name}</div>
                </div>
                <span class="company-industry">${company.industry || 'N/A'}</span>
            </div>
            <div class="esg-scores">
                <div class="score-item">
                    <span class="score-label">Environmental</span>
                    <span class="score-value environmental">${company.e_score || '--'}</span>
                </div>
                <div class="score-item">
                    <span class="score-label">Social</span>
                    <span class="score-value social">${company.s_score || '--'}</span>
                </div>
                <div class="score-item">
                    <span class="score-label">Governance</span>
                    <span class="score-value governance">${company.g_score || '--'}</span>
                </div>
                <div class="score-item">
                    <span class="score-label">Overall</span>
                    <span class="score-value overall">${company.overall_score || '--'}</span>
                </div>
            </div>
        </div>
    `).join('');
}

// Load alerts
async function loadAlerts() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/alerts/`);
        const alerts = await response.json();
        
        displayAlerts(alerts);
    } catch (error) {
        console.error('Failed to load alerts:', error);
        alertsList.innerHTML = '<div class="empty-state">Failed to load alerts</div>';
    }
}

// Display alerts
function displayAlerts(alerts) {
    if (alerts.length === 0) {
        alertsList.innerHTML = `
            <div class="empty-state">
                <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <path d="M9 12L11 14L15 10M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke-width="2"/>
                </svg>
                <p>No alerts at this time</p>
            </div>
        `;
        return;
    }
    
    alertsList.innerHTML = alerts.map(alert => `
        <div class="alert-item ${alert.severity}">
            <div class="alert-content">
                <div class="alert-header">
                    <span class="alert-company">Company ID: ${alert.company_id}</span>
                    <span class="alert-severity ${alert.severity}">${alert.severity}</span>
                </div>
                <p class="alert-message">${alert.message}</p>
                <div class="alert-time">${formatDate(alert.created_at)}</div>
            </div>
            <span class="alert-status ${alert.is_resolved ? 'resolved' : 'active'}">
                ${alert.is_resolved ? 'Resolved' : 'Active'}
            </span>
        </div>
    `).join('');
}

// Update average scores
async function updateAverageScores() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/alerts/companies`);
        const companies = await response.json();
        
        if (companies.length === 0) {
            document.getElementById('avgEnvironmental').textContent = '--';
            document.getElementById('avgSocial').textContent = '--';
            document.getElementById('avgGovernance').textContent = '--';
            document.getElementById('avgOverall').textContent = '--';
            return;
        }
        
        // Calculate averages from real data
        let eSum = 0, sSum = 0, gSum = 0, oSum = 0;
        let eCount = 0, sCount = 0, gCount = 0, oCount = 0;
        
        companies.forEach(company => {
            if (company.e_score !== null) { eSum += company.e_score; eCount++; }
            if (company.s_score !== null) { sSum += company.s_score; sCount++; }
            if (company.g_score !== null) { gSum += company.g_score; gCount++; }
            if (company.overall_score !== null) { oSum += company.overall_score; oCount++; }
        });
        
        document.getElementById('avgEnvironmental').textContent = eCount > 0 ? (eSum / eCount).toFixed(1) : '--';
        document.getElementById('avgSocial').textContent = sCount > 0 ? (sSum / sCount).toFixed(1) : '--';
        document.getElementById('avgGovernance').textContent = gCount > 0 ? (gSum / gCount).toFixed(1) : '--';
        document.getElementById('avgOverall').textContent = oCount > 0 ? (oSum / oCount).toFixed(1) : '--';
        
    } catch (error) {
        console.error('Failed to update average scores:', error);
    }
}

// Show analysis result
function showResult(data, success) {
    analysisResult.style.display = 'block';
    
    if (success) {
        analysisResult.innerHTML = `
            <div class="success-message">
                ✓ Analysis complete for "${data.company_name}"
            </div>
            <p style="margin-top: 0.5rem; color: var(--text-secondary);">
                ${data.message || 'Company has been added to the tracker.'}
            </p>
        `;
    } else {
        analysisResult.innerHTML = `
            <div class="error-message">
                ✗ ${data.error || 'Analysis failed'}
            </div>
        `;
    }
    
    // Clear form
    companyNameInput.value = '';
}

// Hide result
function hideResult() {
    analysisResult.style.display = 'none';
}

// Set loading state
function setLoading(button, isLoading) {
    const btnText = button.querySelector('.btn-text');
    const btnLoader = button.querySelector('.btn-loader');
    
    if (isLoading) {
        btnText.style.display = 'none';
        btnLoader.style.display = 'inline-block';
        button.disabled = true;
    } else {
        btnText.style.display = 'inline';
        btnLoader.style.display = 'none';
        button.disabled = false;
    }
}

// Format date
function formatDate(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const diff = now - date;
    
    // Less than a minute
    if (diff < 60000) {
        return 'Just now';
    }
    
    // Less than an hour
    if (diff < 3600000) {
        const minutes = Math.floor(diff / 60000);
        return `${minutes} minute${minutes > 1 ? 's' : ''} ago`;
    }
    
    // Less than a day
    if (diff < 86400000) {
        const hours = Math.floor(diff / 3600000);
        return `${hours} hour${hours > 1 ? 's' : ''} ago`;
    }
    
    // Default format
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
}

// Auto-refresh every 30 seconds
setInterval(loadAlerts, 30000);
