# Quick Start Guide

## Start the Server

```bash
cd /workspace/real_time_esg_impact_tracker
python3 -m backend.app
```

## Access the Application

Open your browser to: **http://localhost:5000**

## What You'll See

### ✅ Dashboard Cards (Top Row)
- **Environmental:** ~82.6 (average across companies)
- **Social:** ~82.1
- **Governance:** ~86.5
- **Overall Score:** ~83.7

### ✅ Company ESG Scores Section
Three companies with full ESG metrics:
1. **GreenTech Inc.** (Technology) - Overall: 85.2
2. **EcoEnergy Corp.** (Energy) - Overall: 86.8
3. **SustainableGoods Ltd.** (Retail) - Overall: 79.2

### ✅ ESG Alerts Section
Four alerts showing:
- Critical alert about water usage
- Warning about carbon emissions
- Info alerts about renewable energy and supply chain

## Test the Analysis Feature

1. Enter a company name (e.g., "Microsoft", "Tesla", "Apple")
2. Click "Analyze Company"
3. Wait for analysis to complete
4. View results in the dashboard

## Troubleshooting

If you still see errors:
1. Ensure the server is running
2. Check that `esg_tracker.db` exists in the project root
3. Verify the browser console for specific error messages
4. Try refreshing the page (F5)

## Database Info

- **Location:** `/workspace/real_time_esg_impact_tracker/esg_tracker.db`
- **Companies:** 3
- **Alerts:** 4  
- **ESG Scores:** 3

All data is ready to load!
