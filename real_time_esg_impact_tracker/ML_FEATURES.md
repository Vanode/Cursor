# 🤖 Machine Learning Features - ESG Impact Tracker

## Overview

This ESG Impact Tracker now includes comprehensive machine learning and NLP capabilities for automated ESG analysis, data collection, and risk detection.

---

## 🎯 Key ML Components

### 1. **ML Analyzer Service** (`ml_analyzer.py`)
Advanced sentiment analysis, ESG classification, and scoring

**Features:**
- **Sentiment Analysis**: Using FinBERT (financial sentiment model) or TextBlob
- **ESG Category Classification**: Automatically classify text into Environmental, Social, or Governance categories
- **ESG Score Calculation**: Generate E, S, G, and overall scores (0-100) from text data
- **Risk Detection**: Identify potential ESG risks with severity levels (low, medium, high, critical)
- **Insight Generation**: Create human-readable insights from analysis results

**Key Methods:**
```python
analyzer = get_ml_analyzer()

# Sentiment analysis
sentiment = analyzer.analyze_sentiment("Company reduces carbon emissions by 30%")

# ESG category classification
category = analyzer.classify_esg_category("New diversity program launched")

# Calculate ESG scores
scores = analyzer.calculate_esg_scores(text_list)

# Detect risks
risks = analyzer.detect_esg_risks(text_list, threshold=0.3)
```

---

### 2. **Data Collector Service** (`data_collector.py`)
Automated collection of ESG-related data from various sources

**Features:**
- **News Collection**: Gather company news from RSS feeds and Google News
- **ESG-Specific Search**: Find articles related to specific ESG topics
- **Text Extraction**: Extract full text content from URLs
- **Smart Caching**: Cache results to reduce API calls

**Data Sources:**
- Google News RSS feeds
- Reuters Business News
- BBC Business News
- Financial Times RSS

**Key Methods:**
```python
collector = get_data_collector()

# Collect comprehensive company data
data = collector.collect_company_data("Tesla Inc.", max_articles=20)

# Search specific ESG topics
results = collector.search_specific_esg_topic("Apple", "carbon emissions")

# Get recent news
recent = collector.get_recent_company_news("Microsoft", days_back=30)
```

---

### 3. **NLP Pipeline** (`nlp_pipeline.py`)
End-to-end pipeline combining data collection and ML analysis

**Features:**
- **Complete Company Analysis**: Full ESG analysis workflow
- **Aspect-Specific Analysis**: Analyze specific ESG aspects
- **Company Comparison**: Compare multiple companies
- **Trend Analysis**: Track ESG performance over time
- **Report Generation**: Generate formatted reports (JSON, text, summary)

**Key Methods:**
```python
pipeline = get_nlp_pipeline()

# Full company analysis
analysis = pipeline.analyze_company("Google")

# Compare companies
comparison = pipeline.compare_companies(["Amazon", "Microsoft", "Apple"])

# Generate report
report = pipeline.generate_report("Tesla", format='text')
```

---

## 📡 API Endpoints

### **Analysis Endpoints** (`/api/analyze`)

#### 1. Full Company Analysis
```bash
POST /api/analyze/company
Content-Type: application/json

{
  "company_name": "Tesla Inc.",
  "max_articles": 20,
  "save_to_db": true
}
```

**Response:**
```json
{
  "status": "success",
  "company": "Tesla Inc.",
  "analysis": {
    "esg_scores": {
      "e_score": 72.5,
      "s_score": 65.3,
      "g_score": 68.9,
      "overall_score": 69.2,
      "confidence": 0.85
    },
    "risks": [...],
    "insights": [...],
    "recommendations": [...]
  }
}
```

#### 2. Sentiment Analysis
```bash
POST /api/analyze/sentiment

{
  "text": "Company announces major sustainability initiative"
}
```

#### 3. ESG Category Classification
```bash
POST /api/analyze/category

{
  "text": "Board of directors enhances transparency"
}
```

#### 4. Calculate ESG Scores
```bash
POST /api/analyze/scores

{
  "texts": ["text1", "text2", "text3"],
  "company_name": "Apple",
  "save_to_db": false
}
```

#### 5. Compare Companies
```bash
POST /api/analyze/compare

{
  "companies": ["Apple", "Microsoft", "Google"]
}
```

#### 6. Generate Report
```bash
POST /api/analyze/report

{
  "company_name": "Amazon",
  "format": "text"  // or "json" or "summary"
}
```

#### 7. Analyze Specific Aspect
```bash
POST /api/analyze/aspect

{
  "company_name": "Tesla",
  "aspect": "carbon emissions"
}
```

---

### **Alert Endpoints** (`/api/alerts`)

#### 1. Get All Alerts
```bash
GET /api/alerts/?company_id=1&severity=critical&is_resolved=false&limit=50
```

#### 2. Create Alert
```bash
POST /api/alerts/

{
  "company_id": 1,
  "message": "Environmental compliance issue detected",
  "severity": "critical"
}
```

#### 3. Update Alert
```bash
PUT /api/alerts/123

{
  "is_resolved": true
}
```

#### 4. Detect Alerts (ML-Powered)
```bash
POST /api/alerts/detect

{
  "company_name": "BP",
  "auto_create": true,
  "threshold": 0.3
}
```

**This endpoint:**
- Collects recent news about the company
- Uses ML to detect ESG risks
- Automatically creates alerts for high/critical risks

#### 5. Monitor Company
```bash
POST /api/alerts/monitor

{
  "company_name": "Shell",
  "categories": ["environmental", "social", "governance"]
}
```

#### 6. Get Alerts Summary
```bash
GET /api/alerts/summary
```

---

### **ML Features Endpoints** (`/api/ml`)

#### 1. Collect Data
```bash
POST /api/ml/collect

{
  "company_name": "Microsoft",
  "max_articles": 30,
  "include_content": false
}
```

#### 2. Train Models
```bash
POST /api/ml/train

{
  "training_data": [
    {"text": "Carbon emissions reduced", "label": "environmental"},
    {"text": "Diversity program launched", "label": "social"}
  ],
  "model_type": "classifier"
}
```

#### 3. Make Predictions
```bash
POST /api/ml/predict

{
  "texts": ["New sustainability report released"],
  "prediction_type": "category"  // or "sentiment" or "scores"
}
```

#### 4. Analyze Trends
```bash
POST /api/ml/trends

{
  "company_name": "Apple",
  "days_back": 30
}
```

#### 5. Benchmark Company
```bash
POST /api/ml/benchmark

{
  "company_name": "Tesla",
  "industry": "Automotive",
  "peers": ["Ford", "GM", "Rivian"]
}
```

---

## 🧪 Usage Examples

### Example 1: Complete ESG Analysis
```python
import requests

# Analyze a company
response = requests.post('http://localhost:5000/api/analyze/company', json={
    "company_name": "Apple Inc.",
    "max_articles": 25,
    "save_to_db": True
})

results = response.json()
print(f"Overall ESG Score: {results['analysis']['esg_scores']['overall_score']}")
print(f"Insights: {results['analysis']['insights']}")
```

### Example 2: Automated Risk Detection
```python
# Detect ESG risks and auto-create alerts
response = requests.post('http://localhost:5000/api/alerts/detect', json={
    "company_name": "BP",
    "auto_create": True,
    "threshold": 0.3
})

risks = response.json()
print(f"Risks detected: {risks['risks_detected']}")
print(f"Alerts created: {risks['alerts_created']}")
```

### Example 3: Compare Companies
```python
# Compare ESG performance
response = requests.post('http://localhost:5000/api/analyze/compare', json={
    "companies": ["Tesla", "Ford", "GM"]
})

comparison = response.json()
rankings = comparison['comparison']['rankings']
for rank in rankings:
    print(f"{rank['rank']}. {rank['company']} - Score: {rank['overall_score']}")
```

### Example 4: Track Trends
```python
# Analyze ESG trends over time
response = requests.post('http://localhost:5000/api/ml/trends', json={
    "company_name": "Microsoft",
    "days_back": 90
})

trends = response.json()
print(f"Sentiment trend: {trends['trends']['trend_direction']}")
print(f"Average sentiment: {trends['trends']['average_sentiment']}")
```

---

## 🔧 Technical Details

### ML Models Used

1. **Sentiment Analysis**
   - Primary: FinBERT (ProsusAI/finbert) - specialized for financial text
   - Fallback: TextBlob - for basic sentiment when transformers unavailable

2. **ESG Classification**
   - Random Forest Classifier with TF-IDF features
   - Keyword-based scoring for interpretability
   - Hybrid approach combining ML and rule-based methods

3. **Score Prediction**
   - Weighted combination of sentiment and category confidence
   - Historical data blending (70% new, 30% historical)
   - Confidence scoring based on data volume

### Data Processing Pipeline

```
Data Collection → Text Aggregation → ML Analysis → Score Calculation → Insight Generation
       ↓                 ↓                ↓                ↓                   ↓
   RSS Feeds      Deduplication    Sentiment        E/S/G Scores      Recommendations
   Google News    Cleaning         Classification   Overall Score     Risk Alerts
   Web Scraping   Filtering        Risk Detection   Confidence        Reports
```

### Model Storage

Models are stored in `/models` directory:
- `sentiment_model/` - Fine-tuned sentiment model (if available)
- `esg_classifier.pkl` - Trained ESG classifier
- `vectorizer.pkl` - TF-IDF vectorizer

---

## 📊 ESG Scoring Methodology

### Score Calculation
Each category (E, S, G) is scored 0-100 based on:
1. **Sentiment Analysis** (60% weight)
   - Positive sentiment → Higher score
   - Negative sentiment → Lower score

2. **Category Confidence** (40% weight)
   - How relevant the text is to that ESG category

### Overall Score
```
Overall = (E_score × 0.35) + (S_score × 0.35) + (G_score × 0.30)
```

### Confidence Score
Based on:
- Number of data points analyzed
- Consistency of signals
- Recency of data

---

## 🚨 Risk Detection

### Severity Levels

1. **Critical** (Red Flag)
   - Keywords: fraud, corruption, lawsuit, investigation
   - Very negative sentiment (< 0.3)
   - Immediate action required

2. **High** (Warning)
   - Negative sentiment (< 0.25)
   - Multiple negative mentions
   - Should be monitored closely

3. **Medium** (Caution)
   - Moderately negative sentiment (0.25-0.4)
   - Minor concerns identified

4. **Low** (Informational)
   - Slightly negative sentiment (0.4-0.5)
   - Worth tracking

### Risk Categories
- **Environmental**: Pollution, emissions, compliance violations
- **Social**: Labor issues, discrimination, safety incidents
- **Governance**: Ethics violations, fraud, transparency issues

---

## 🎓 Best Practices

1. **Data Collection**
   - Use `max_articles=20-50` for balanced analysis
   - Enable caching to reduce API calls
   - Collect data regularly for trend analysis

2. **Analysis**
   - Combine multiple data sources
   - Use historical data for context
   - Set appropriate confidence thresholds

3. **Risk Detection**
   - Set threshold=0.2-0.4 depending on sensitivity
   - Auto-create alerts for critical/high risks only
   - Review and validate ML-detected risks

4. **Model Training**
   - Retrain models with domain-specific data
   - Use at least 100+ labeled examples
   - Validate on held-out test set

---

## 🔄 Continuous Improvement

The ML models improve over time through:
1. **Custom Training**: Add domain-specific training data
2. **Feedback Loop**: Mark false positives/negatives
3. **Model Updates**: Regularly retrain with new data
4. **Fine-tuning**: Adjust hyperparameters based on performance

---

## 🐛 Troubleshooting

### Issue: Low confidence scores
**Solution**: Increase `max_articles` to collect more data

### Issue: No risks detected
**Solution**: Lower the `threshold` parameter (e.g., 0.2)

### Issue: Too many false positives
**Solution**: Increase threshold or retrain classifier with better data

### Issue: Slow performance
**Solution**: 
- Enable caching
- Reduce `max_articles`
- Use async processing for multiple companies

---

## 📦 Dependencies

All ML dependencies are in `requirements.txt`:
- `transformers` - For advanced NLP models
- `torch` - PyTorch backend for transformers
- `scikit-learn` - ML algorithms
- `nltk` - Natural language processing
- `textblob` - Sentiment analysis
- `beautifulsoup4` - Web scraping
- `feedparser` - RSS feed parsing
- `newspaper3k` - Article extraction

---

## 🚀 Quick Start

1. **Install dependencies:**
```bash
cd real_time_esg_impact_tracker
pip install -r requirements.txt
```

2. **Download NLTK data (first time only):**
```python
python -c "import nltk; nltk.download('punkt'); nltk.download('vader_lexicon')"
```

3. **Start the server:**
```bash
python backend/app.py
```

4. **Test ML features:**
```bash
# Analyze a company
curl -X POST http://localhost:5000/api/analyze/company \
  -H "Content-Type: application/json" \
  -d '{"company_name": "Tesla Inc."}'

# Detect risks
curl -X POST http://localhost:5000/api/alerts/detect \
  -H "Content-Type: application/json" \
  -d '{"company_name": "BP", "auto_create": true}'
```

---

## 📈 Future Enhancements

- [ ] Real-time streaming analysis
- [ ] Advanced NER (Named Entity Recognition) for extracting specific ESG metrics
- [ ] Time-series forecasting for ESG trends
- [ ] Integration with ESG databases (MSCI, Bloomberg ESG)
- [ ] Multi-language support
- [ ] Custom model fine-tuning interface
- [ ] Automated report scheduling
- [ ] Webhook notifications for critical alerts

---

**Built with ❤️ for ESG Analytics** | **Powered by Machine Learning**
