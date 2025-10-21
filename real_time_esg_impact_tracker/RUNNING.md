# 🚀 ESG Impact Tracker - Now Running!

## ✅ Current Status

Your ESG Impact Tracker is **LIVE** and running successfully!

- **Backend API**: http://localhost:5000
- **Frontend Dashboard**: http://localhost:5000
- **Health Check**: http://localhost:5000/health
- **Database**: Initialized with seed data

---

## 🌐 Access the Application

### Frontend Dashboard
Open your browser and navigate to:
```
http://localhost:5000
```

You'll see a beautiful, modern dashboard with:
- **Real-time ESG metrics** (Environmental, Social, Governance scores)
- **Company analysis** form
- **Company ESG scores** display
- **ESG alerts** monitoring

### API Endpoints

#### Health Check
```bash
curl http://localhost:5000/health
```

#### Get Alerts
```bash
curl http://localhost:5000/api/alerts/
```

#### Analyze Company
```bash
curl -X POST http://localhost:5000/api/analyze/company \
  -H "Content-Type: application/json" \
  -d '{"company_name": "Tesla Inc."}'
```

---

## 📊 Features

### 1. Dashboard Overview
- **4 Key Metrics Cards**: Environmental, Social, Governance, and Overall scores
- **Real-time Status Indicator**: Shows connection status
- **Modern Dark Theme**: Beautiful gradient backgrounds and smooth animations

### 2. Company Analysis
- **Input any company name** to analyze
- **Mock ESG analysis** (ready for Ollama LLM integration)
- **Instant feedback** with success/error messages

### 3. Company ESG Scores
- **Sample companies** displayed with scores:
  - GreenTech Solutions (Tech)
  - EcoEnergy Corp (Energy)
  - SustainableFoods Inc (Food & Beverage)
- **Visual score breakdown**: E, S, G, and Overall scores

### 4. ESG Alerts
- **Real-time alerts** from the database
- **Severity levels**: Info, Warning, Critical
- **Status tracking**: Active vs Resolved
- **Auto-refresh** every 30 seconds

---

## 🛠️ Technical Stack

- **Backend**: Flask 3.0.0 with SQLAlchemy 2.0.44
- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **Database**: SQLite with seed data
- **API**: RESTful endpoints with CORS enabled
- **UI/UX**: Modern dark theme with Inter font family

---

## 📁 Project Structure

```
real_time_esg_impact_tracker/
├── backend/
│   ├── app.py                    ✅ Running on port 5000
│   ├── routes/
│   │   ├── analyze.py            ✅ /api/analyze/*
│   │   └── alerts.py             ✅ /api/alerts/*
│   ├── database/
│   │   └── models.py             ✅ Company, ESGScore, Alert
│   ├── services/
│   │   └── ollama_client.py      📝 Ready for LLM integration
│   └── utils/
│       └── db_init.py            ✅ Database initialized
├── frontend/
│   ├── index.html                ✅ Main dashboard
│   ├── styles.css                ✅ Modern dark theme
│   └── app.js                    ✅ API integration
├── config.py                     ✅ Configuration loaded
├── .env                          ✅ Environment variables
└── esg_tracker.db                ✅ SQLite database with seed data
```

---

## 🎯 Testing the Application

### Test 1: Health Check
```bash
curl http://localhost:5000/health
```
Expected: `{"status": "ok"}`

### Test 2: View Alerts
```bash
curl http://localhost:5000/api/alerts/
```
Expected: JSON array of alerts

### Test 3: Analyze a Company
```bash
curl -X POST http://localhost:5000/api/analyze/company \
  -H "Content-Type: application/json" \
  -d '{"company_name": "Apple Inc."}'
```
Expected: Analysis response with mock data

### Test 4: Access Frontend
Open browser: http://localhost:5000
- Should see dark-themed dashboard
- Should see 4 metric cards at top
- Should see company analysis form
- Should see sample companies with scores
- Should see alerts section

---

## 🔧 Server Control

### Check if Server is Running
```bash
ps aux | grep "python3.*app.py"
```

### View Server Logs
```bash
tail -f /tmp/flask.log
```

### Stop the Server
```bash
# Find the process ID
ps aux | grep "python3.*app.py" | grep -v grep

# Kill the process (replace PID with actual process ID)
kill <PID>
```

### Restart the Server
```bash
cd /workspace/real_time_esg_impact_tracker
PYTHONPATH=/workspace/real_time_esg_impact_tracker python3 backend/app.py > /tmp/flask.log 2>&1 &
```

---

## 📝 Next Steps for Development

### Immediate Enhancements
1. **Integrate Ollama LLM**
   - Install Ollama: https://ollama.ai
   - Pull a model: `ollama pull llama2`
   - Update `ollama_client.py` with real API calls

2. **Add More Companies**
   - Create a companies endpoint
   - Implement CRUD operations
   - Add search and filter functionality

3. **Enhanced Alerts**
   - Add alert creation from frontend
   - Implement alert resolution
   - Add notification system

4. **Data Visualization**
   - Add charts (using Chart.js or D3.js)
   - Trend analysis over time
   - Comparative company analysis

### Future Features
- [ ] User authentication
- [ ] Real-time WebSocket updates
- [ ] External data integration (news, financial APIs)
- [ ] Export reports (PDF, CSV)
- [ ] Advanced analytics dashboard
- [ ] Mobile responsive improvements

---

## 🐛 Troubleshooting

### Frontend not loading?
- Check if Flask is running: `curl http://localhost:5000/health`
- Check browser console for errors
- Clear browser cache

### API not responding?
- Check server logs: `tail /tmp/flask.log`
- Verify database exists: `ls -la esg_tracker.db`
- Check CORS is enabled in `app.py`

### Database errors?
- Reinitialize: `python3 backend/utils/db_init.py`
- Check permissions: `ls -la esg_tracker.db`

---

## 📊 Sample Data

The database includes:
- **3 Companies**: GreenTech Solutions, EcoEnergy Corp, SustainableFoods Inc
- **3 ESG Score records**: One for each company
- **3 Alerts**: Sample alerts with different severity levels

---

## 🎨 UI Features

- **Responsive Design**: Works on desktop and mobile
- **Dark Theme**: Easy on the eyes
- **Smooth Animations**: Hover effects and transitions
- **Loading States**: Visual feedback for API calls
- **Status Indicators**: Real-time connection status
- **Auto-refresh**: Alerts update every 30 seconds

---

## 🚀 You're All Set!

Your ESG Impact Tracker is now running and ready for use. Open http://localhost:5000 in your browser to see the beautiful dashboard in action!

**Enjoy building amazing ESG analytics!** 🌍📈
