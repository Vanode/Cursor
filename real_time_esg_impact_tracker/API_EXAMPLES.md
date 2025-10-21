# 🔌 API Examples - ESG Impact Tracker

Complete examples for using the ML-powered ESG API endpoints.

---

## 📋 Table of Contents

1. [Company Analysis](#company-analysis)
2. [Alert Detection](#alert-detection)
3. [Data Collection](#data-collection)
4. [Sentiment & Classification](#sentiment--classification)
5. [Trends & Benchmarking](#trends--benchmarking)
6. [Company Comparison](#company-comparison)

---

## Company Analysis

### Full ESG Analysis

**Request:**
```bash
curl -X POST http://localhost:5000/api/analyze/company \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "Tesla Inc.",
    "max_articles": 25,
    "save_to_db": true
  }'
```

**Response:**
```json
{
  "status": "success",
  "company": "Tesla Inc.",
  "analysis": {
    "company_name": "Tesla Inc.",
    "analysis_timestamp": "2025-10-21T10:30:00Z",
    "data_collection": {
      "articles_collected": 25,
      "esg_mentions": 15,
      "sources": ["Google News", "Reuters", "BBC"],
      "total_texts_analyzed": 40
    },
    "esg_scores": {
      "e_score": 75.3,
      "s_score": 62.8,
      "g_score": 68.5,
      "overall_score": 69.2,
      "confidence": 0.87,
      "data_points": 40
    },
    "sentiment_analysis": {
      "summary": {
        "positive": 18,
        "negative": 5,
        "neutral": 17,
        "average_score": 0.68
      }
    },
    "category_classification": {
      "distribution": {
        "environmental": 22,
        "social": 10,
        "governance": 8,
        "general": 0
      }
    },
    "risks": [
      {
        "category": "social",
        "severity": "medium",
        "text": "Labor issues reported at factory...",
        "sentiment_score": 0.35,
        "confidence": 0.75
      }
    ],
    "insights": [
      "Strong overall ESG performance with a score of 69.2/100",
      "Environmental practices are strong",
      "Social practices need improvement"
    ],
    "recommendations": [
      "Improve social responsibility programs and stakeholder engagement"
    ]
  }
}
```

### Analyze Specific ESG Aspect

**Request:**
```bash
curl -X POST http://localhost:5000/api/analyze/aspect \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "Apple",
    "aspect": "carbon emissions"
  }'
```

**Response:**
```json
{
  "status": "success",
  "analysis": {
    "company_name": "Apple",
    "aspect": "carbon emissions",
    "articles_found": 12,
    "sentiment_summary": {
      "positive": 8,
      "negative": 2,
      "neutral": 2,
      "average_score": 0.72
    },
    "category_distribution": {
      "environmental": 11,
      "social": 0,
      "governance": 1
    },
    "articles": [...]
  }
}
```

### Generate Report

**Text Report:**
```bash
curl -X POST http://localhost:5000/api/analyze/report \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "Microsoft",
    "format": "text"
  }'
```

**Summary Report:**
```bash
curl -X POST http://localhost:5000/api/analyze/report \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "Google",
    "format": "summary"
  }'
```

---

## Alert Detection

### Get All Alerts

**Request:**
```bash
# All alerts
curl http://localhost:5000/api/alerts/

# Filtered by company
curl http://localhost:5000/api/alerts/?company_id=1

# Critical unresolved alerts
curl http://localhost:5000/api/alerts/?severity=critical&is_resolved=false

# Limited results
curl http://localhost:5000/api/alerts/?limit=10
```

**Response:**
```json
{
  "status": "success",
  "count": 5,
  "alerts": [
    {
      "id": 1,
      "company_id": 1,
      "message": "[ENVIRONMENTAL] Pollution incident at manufacturing plant",
      "severity": "critical",
      "is_resolved": false,
      "created_at": "2025-10-21T08:00:00Z"
    }
  ]
}
```

### Create Manual Alert

**Request:**
```bash
curl -X POST http://localhost:5000/api/alerts/ \
  -H "Content-Type: application/json" \
  -d '{
    "company_id": 1,
    "message": "New ESG compliance issue identified",
    "severity": "warning"
  }'
```

### Detect Alerts (ML-Powered)

**Request:**
```bash
curl -X POST http://localhost:5000/api/alerts/detect \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "BP",
    "auto_create": true,
    "threshold": 0.3
  }'
```

**Response:**
```json
{
  "status": "success",
  "company_name": "BP",
  "risks_detected": 8,
  "risks": [
    {
      "text": "Environmental lawsuit filed over oil spill...",
      "category": "environmental",
      "severity": "critical",
      "sentiment_score": 0.15,
      "confidence": 0.92
    },
    {
      "text": "Safety violations reported at refinery...",
      "category": "social",
      "severity": "high",
      "sentiment_score": 0.28,
      "confidence": 0.85
    }
  ],
  "alerts_created": 2,
  "created_alerts": [...]
}
```

### Update Alert

**Request:**
```bash
curl -X PUT http://localhost:5000/api/alerts/123 \
  -H "Content-Type: application/json" \
  -d '{
    "is_resolved": true
  }'
```

### Monitor Company

**Request:**
```bash
curl -X POST http://localhost:5000/api/alerts/monitor \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "Shell",
    "categories": ["environmental", "social", "governance"]
  }'
```

### Get Alerts Summary

**Request:**
```bash
curl http://localhost:5000/api/alerts/summary
```

**Response:**
```json
{
  "status": "success",
  "summary": {
    "total_alerts": 45,
    "unresolved_alerts": 12,
    "critical_alerts": 3,
    "warning_alerts": 9,
    "alerts_by_company": [
      {"company": "BP", "count": 8},
      {"company": "Shell", "count": 5},
      {"company": "Exxon", "count": 3}
    ]
  }
}
```

---

## Data Collection

### Collect Company Data

**Request:**
```bash
curl -X POST http://localhost:5000/api/ml/collect \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "Amazon",
    "max_articles": 30,
    "include_content": false
  }'
```

**Response:**
```json
{
  "status": "success",
  "company_name": "Amazon",
  "collected_data": {
    "timestamp": "2025-10-21T10:30:00Z",
    "news_articles": [
      {
        "title": "Amazon announces carbon neutral by 2040",
        "summary": "Company commits to ambitious climate goals...",
        "url": "https://...",
        "published": "2025-10-20",
        "source": "Reuters"
      }
    ],
    "esg_mentions": [...],
    "sources": ["Google News", "Reuters", "BBC"]
  }
}
```

---

## Sentiment & Classification

### Analyze Sentiment

**Request:**
```bash
curl -X POST http://localhost:5000/api/analyze/sentiment \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Company announces major sustainability initiative and carbon reduction targets"
  }'
```

**Response:**
```json
{
  "status": "success",
  "text": "Company announces major sustainability initiative...",
  "sentiment": {
    "label": "positive",
    "score": 0.87,
    "method": "transformer"
  }
}
```

### Classify ESG Category

**Request:**
```bash
curl -X POST http://localhost:5000/api/analyze/category \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Board of directors implements new ethics and compliance framework"
  }'
```

**Response:**
```json
{
  "status": "success",
  "text": "Board of directors implements new ethics...",
  "classification": {
    "category": "governance",
    "confidence": 0.85,
    "scores": {
      "environmental": 2,
      "social": 1,
      "governance": 15
    },
    "method": "hybrid"
  }
}
```

### Calculate ESG Scores

**Request:**
```bash
curl -X POST http://localhost:5000/api/analyze/scores \
  -H "Content-Type: application/json" \
  -d '{
    "texts": [
      "Company reduces carbon emissions by 30%",
      "New diversity and inclusion program launched",
      "Enhanced board transparency measures",
      "Renewable energy investment increased",
      "Improved workplace safety standards"
    ],
    "company_name": "Apple",
    "save_to_db": true
  }'
```

**Response:**
```json
{
  "status": "success",
  "company_name": "Apple",
  "scores": {
    "e_score": 78.5,
    "s_score": 72.3,
    "g_score": 75.8,
    "overall_score": 75.6,
    "confidence": 0.50,
    "data_points": 5
  },
  "texts_analyzed": 5
}
```

---

## Trends & Benchmarking

### Analyze Trends

**Request:**
```bash
curl -X POST http://localhost:5000/api/ml/trends \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "Microsoft",
    "days_back": 90
  }'
```

**Response:**
```json
{
  "status": "success",
  "company_name": "Microsoft",
  "trends": {
    "historical_scores": [
      {
        "date": "2025-10-15",
        "e_score": 75.0,
        "s_score": 70.0,
        "g_score": 72.0,
        "overall_score": 72.3
      },
      {
        "date": "2025-09-15",
        "e_score": 73.5,
        "s_score": 68.5,
        "g_score": 71.0,
        "overall_score": 71.0
      }
    ],
    "recent_news_count": 45,
    "sentiment_trend": [
      {"score": 0.75, "label": "positive"},
      {"score": 0.68, "label": "positive"}
    ],
    "average_sentiment": 0.71,
    "trend_direction": "positive"
  }
}
```

### Benchmark Company

**Request:**
```bash
curl -X POST http://localhost:5000/api/ml/benchmark \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "Tesla",
    "industry": "Automotive",
    "peers": ["Ford", "GM", "Rivian"]
  }'
```

**Response:**
```json
{
  "status": "success",
  "company_name": "Tesla",
  "industry": "Automotive",
  "benchmark": {
    "company_scores": {
      "e_score": 75.3,
      "s_score": 62.8,
      "g_score": 68.5,
      "overall_score": 69.2
    },
    "industry_average": {
      "e_score": 65.0,
      "s_score": 60.0,
      "g_score": 65.0,
      "overall_score": 63.3
    },
    "difference": {
      "e_score": 10.3,
      "s_score": 2.8,
      "g_score": 3.5,
      "overall_score": 5.9
    },
    "peer_comparison": [
      {
        "company": "Ford",
        "e_score": 62.0,
        "s_score": 58.0,
        "g_score": 64.0,
        "overall_score": 61.3
      }
    ]
  }
}
```

---

## Company Comparison

### Compare Multiple Companies

**Request:**
```bash
curl -X POST http://localhost:5000/api/analyze/compare \
  -H "Content-Type: application/json" \
  -d '{
    "companies": ["Apple", "Microsoft", "Google", "Amazon"]
  }'
```

**Response:**
```json
{
  "status": "success",
  "comparison": {
    "companies": ["Apple", "Microsoft", "Google", "Amazon"],
    "timestamp": "2025-10-21T10:30:00Z",
    "individual_analysis": {
      "Apple": {
        "esg_scores": {
          "e_score": 78.5,
          "s_score": 72.3,
          "g_score": 75.8,
          "overall_score": 75.6
        },
        "risk_count": 3,
        "insights": [...]
      },
      "Microsoft": {
        "esg_scores": {
          "e_score": 76.2,
          "s_score": 74.8,
          "g_score": 77.5,
          "overall_score": 76.2
        },
        "risk_count": 2,
        "insights": [...]
      }
    },
    "comparative_insights": [
      "Microsoft leads with overall ESG score of 76.2",
      "Microsoft has strongest environmental performance",
      "Apple has lowest risk profile with 2 identified risks"
    ],
    "rankings": [
      {
        "rank": 1,
        "company": "Microsoft",
        "overall_score": 76.2,
        "e_score": 76.2,
        "s_score": 74.8,
        "g_score": 77.5,
        "risk_count": 2
      },
      {
        "rank": 2,
        "company": "Apple",
        "overall_score": 75.6,
        "e_score": 78.5,
        "s_score": 72.3,
        "g_score": 75.8,
        "risk_count": 3
      }
    ]
  }
}
```

---

## Python Client Examples

### Using Python Requests

```python
import requests
import json

BASE_URL = "http://localhost:5000/api"

# Full company analysis
def analyze_company(company_name):
    response = requests.post(
        f"{BASE_URL}/analyze/company",
        json={
            "company_name": company_name,
            "max_articles": 25,
            "save_to_db": True
        }
    )
    return response.json()

# Detect and create alerts
def detect_alerts(company_name):
    response = requests.post(
        f"{BASE_URL}/alerts/detect",
        json={
            "company_name": company_name,
            "auto_create": True,
            "threshold": 0.3
        }
    )
    return response.json()

# Compare companies
def compare_companies(companies):
    response = requests.post(
        f"{BASE_URL}/analyze/compare",
        json={"companies": companies}
    )
    return response.json()

# Usage
if __name__ == "__main__":
    # Analyze Tesla
    tesla_analysis = analyze_company("Tesla Inc.")
    print(f"Tesla Overall Score: {tesla_analysis['analysis']['esg_scores']['overall_score']}")
    
    # Detect BP alerts
    bp_alerts = detect_alerts("BP")
    print(f"Risks detected for BP: {bp_alerts['risks_detected']}")
    
    # Compare tech companies
    comparison = compare_companies(["Apple", "Microsoft", "Google"])
    print("Rankings:")
    for rank in comparison['comparison']['rankings']:
        print(f"  {rank['rank']}. {rank['company']}: {rank['overall_score']}")
```

---

## JavaScript/Node.js Examples

```javascript
const axios = require('axios');

const BASE_URL = 'http://localhost:5000/api';

// Analyze company
async function analyzeCompany(companyName) {
  const response = await axios.post(`${BASE_URL}/analyze/company`, {
    company_name: companyName,
    max_articles: 25,
    save_to_db: true
  });
  return response.data;
}

// Detect alerts
async function detectAlerts(companyName) {
  const response = await axios.post(`${BASE_URL}/alerts/detect`, {
    company_name: companyName,
    auto_create: true,
    threshold: 0.3
  });
  return response.data;
}

// Get alerts summary
async function getAlertsSummary() {
  const response = await axios.get(`${BASE_URL}/alerts/summary`);
  return response.data;
}

// Usage
(async () => {
  try {
    const analysis = await analyzeCompany('Tesla Inc.');
    console.log('Tesla ESG Score:', analysis.analysis.esg_scores.overall_score);
    
    const alerts = await detectAlerts('BP');
    console.log('BP Risks:', alerts.risks_detected);
    
    const summary = await getAlertsSummary();
    console.log('Total Alerts:', summary.summary.total_alerts);
  } catch (error) {
    console.error('Error:', error.message);
  }
})();
```

---

## Rate Limiting & Best Practices

1. **Caching**: Data is cached for 1 hour by default
2. **Batch Processing**: Use compare endpoint instead of multiple analyze calls
3. **Pagination**: Use `limit` parameter for large result sets
4. **Error Handling**: Always check `status` field in responses
5. **Timeouts**: Some operations may take 30-60 seconds for large datasets

---

**Happy Analyzing! 🚀**
