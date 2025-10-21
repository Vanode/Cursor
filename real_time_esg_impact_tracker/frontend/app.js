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
    
    setLoading(analyzeBtn, true);
    hideResult();
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/analyze/company`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ company_name: companyName })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showResult(data, true);
            await loadCompanies(); // Refresh companies list
            updateAverageScores();
        } else {
            showResult(data, false);
        }
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
        // For now, we'll fetch from the database through a custom endpoint
        // Since we don't have a direct GET companies endpoint, we'll use the alert data
        // In a production app, you'd want a dedicated companies endpoint
        const response = await fetch(`${API_BASE_URL}/api/alerts/`);
        const alerts = await response.json();
        
        // Get unique companies from alerts
        const companyIds = [...new Set(alerts.map(alert => alert.company_id))];
        
        // Display placeholder companies or fetch from database
        displayCompanies([]);
        
    } catch (error) {
        console.error('Failed to load companies:', error);
        companiesList.innerHTML = '<div class="empty-state">Failed to load companies</div>';
    }
}

// Display companies
function displayCompanies(companies) {
    if (companies.length === 0) {
        // Show sample companies for demo
        companiesList.innerHTML = `
            <div class="company-item">
                <div class="company-header">
                    <div>
                        <div class="company-name">GreenTech Solutions</div>
                    </div>
                    <span class="company-industry">Technology</span>
                </div>
                <div class="esg-scores">
                    <div class="score-item">
                        <span class="score-label">Environmental</span>
                        <span class="score-value environmental">85</span>
                    </div>
                    <div class="score-item">
                        <span class="score-label">Social</span>
                        <span class="score-value social">78</span>
                    </div>
                    <div class="score-item">
                        <span class="score-label">Governance</span>
                        <span class="score-value governance">92</span>
                    </div>
                    <div class="score-item">
                        <span class="score-label">Overall</span>
                        <span class="score-value overall">85</span>
                    </div>
                </div>
            </div>
            <div class="company-item">
                <div class="company-header">
                    <div>
                        <div class="company-name">EcoEnergy Corp</div>
                    </div>
                    <span class="company-industry">Energy</span>
                </div>
                <div class="esg-scores">
                    <div class="score-item">
                        <span class="score-label">Environmental</span>
                        <span class="score-value environmental">92</span>
                    </div>
                    <div class="score-item">
                        <span class="score-label">Social</span>
                        <span class="score-value social">88</span>
                    </div>
                    <div class="score-item">
                        <span class="score-label">Governance</span>
                        <span class="score-value governance">85</span>
                    </div>
                    <div class="score-item">
                        <span class="score-label">Overall</span>
                        <span class="score-value overall">88.3</span>
                    </div>
                </div>
            </div>
            <div class="company-item">
                <div class="company-header">
                    <div>
                        <div class="company-name">SustainableFoods Inc</div>
                    </div>
                    <span class="company-industry">Food & Beverage</span>
                </div>
                <div class="esg-scores">
                    <div class="score-item">
                        <span class="score-label">Environmental</span>
                        <span class="score-value environmental">72</span>
                    </div>
                    <div class="score-item">
                        <span class="score-label">Social</span>
                        <span class="score-value social">95</span>
                    </div>
                    <div class="score-item">
                        <span class="score-label">Governance</span>
                        <span class="score-value governance">80</span>
                    </div>
                    <div class="score-item">
                        <span class="score-label">Overall</span>
                        <span class="score-value overall">82.3</span>
                    </div>
                </div>
            </div>
        `;
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
function updateAverageScores() {
    // For demo purposes, using sample data
    document.getElementById('avgEnvironmental').textContent = '83.0';
    document.getElementById('avgSocial').textContent = '87.0';
    document.getElementById('avgGovernance').textContent = '85.7';
    document.getElementById('avgOverall').textContent = '85.2';
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
