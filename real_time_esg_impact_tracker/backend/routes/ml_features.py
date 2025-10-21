"""
Additional ML Features Routes
Advanced machine learning and data collection endpoints
"""
from flask import Blueprint, jsonify, request
from backend.services.data_collector import get_data_collector
from backend.services.ml_analyzer import get_ml_analyzer
from backend.database.models import Company, ESGScore
from backend.app import db
from datetime import datetime

ml_bp = Blueprint('ml', __name__)


@ml_bp.route('/', methods=['GET'])
def index():
    """
    Root endpoint for ML features blueprint
    """
    return jsonify({
        "message": "ML Features endpoint",
        "available_routes": [
            "/collect - Collect data for a company",
            "/train - Train custom ML models",
            "/predict - Make predictions using trained models",
            "/trends - Analyze ESG trends over time",
            "/benchmark - Benchmark company against industry"
        ]
    }), 200


@ml_bp.route('/collect', methods=['POST'])
def collect_data():
    """
    Collect ESG data for a company from various sources
    
    Request body:
    {
        "company_name": "string (required)",
        "max_articles": int (optional, default 20),
        "include_content": bool (optional, default false)
    }
    """
    data = request.get_json()
    
    if not data or 'company_name' not in data:
        return jsonify({"error": "company_name is required"}), 400
    
    company_name = data.get('company_name')
    max_articles = data.get('max_articles', 20)
    include_content = data.get('include_content', False)
    
    try:
        collector = get_data_collector()
        collected_data = collector.collect_company_data(company_name, max_articles)
        
        # Optionally fetch full content from URLs
        if include_content:
            for article in collected_data.get('news_articles', [])[:5]:
                url = article.get('url')
                if url:
                    content = collector.extract_text_from_url(url)
                    article['full_content'] = content[:1000] if content else None
        
        return jsonify({
            "status": "success",
            "company_name": company_name,
            "collected_data": collected_data,
            "timestamp": datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500


@ml_bp.route('/train', methods=['POST'])
def train_models():
    """
    Train or retrain ML models with custom data
    
    Request body:
    {
        "training_data": [{"text": "string", "label": "string"}] (required),
        "model_type": "string (classifier/sentiment)"
    }
    """
    data = request.get_json()
    
    if not data or 'training_data' not in data:
        return jsonify({"error": "training_data is required"}), 400
    
    training_data = data.get('training_data')
    model_type = data.get('model_type', 'classifier')
    
    try:
        # Extract texts and labels
        texts = [item['text'] for item in training_data if 'text' in item]
        labels = [item['label'] for item in training_data if 'label' in item]
        
        if len(texts) != len(labels):
            return jsonify({"error": "Each training item must have 'text' and 'label'"}), 400
        
        # Train the model (simplified version)
        ml_analyzer = get_ml_analyzer()
        
        if model_type == 'classifier':
            from sklearn.feature_extraction.text import TfidfVectorizer
            from sklearn.ensemble import RandomForestClassifier
            import pickle
            import os
            
            vectorizer = TfidfVectorizer(max_features=1000)
            X = vectorizer.fit_transform(texts)
            
            classifier = RandomForestClassifier(n_estimators=100, random_state=42)
            classifier.fit(X, labels)
            
            # Save models
            models_dir = ml_analyzer.models_dir
            with open(os.path.join(models_dir, "esg_classifier.pkl"), 'wb') as f:
                pickle.dump(classifier, f)
            with open(os.path.join(models_dir, "vectorizer.pkl"), 'wb') as f:
                pickle.dump(vectorizer, f)
            
            # Update analyzer's models
            ml_analyzer.esg_classifier = classifier
            ml_analyzer.vectorizer = vectorizer
        
        return jsonify({
            "status": "success",
            "message": f"{model_type} model trained successfully",
            "training_samples": len(texts),
            "timestamp": datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500


@ml_bp.route('/predict', methods=['POST'])
def predict():
    """
    Make predictions using trained models
    
    Request body:
    {
        "texts": ["string array"] (required),
        "prediction_type": "string (category/sentiment/scores)"
    }
    """
    data = request.get_json()
    
    if not data or 'texts' not in data:
        return jsonify({"error": "texts array is required"}), 400
    
    texts = data.get('texts')
    prediction_type = data.get('prediction_type', 'category')
    
    if not isinstance(texts, list):
        return jsonify({"error": "texts must be an array"}), 400
    
    try:
        ml_analyzer = get_ml_analyzer()
        predictions = []
        
        for text in texts:
            if prediction_type == 'sentiment':
                result = ml_analyzer.analyze_sentiment(text)
            elif prediction_type == 'category':
                result = ml_analyzer.classify_esg_category(text)
            elif prediction_type == 'scores':
                result = ml_analyzer.calculate_esg_scores([text])
            else:
                result = {"error": "Unknown prediction type"}
            
            predictions.append({
                "text": text[:100],
                "prediction": result
            })
        
        return jsonify({
            "status": "success",
            "prediction_type": prediction_type,
            "predictions": predictions,
            "timestamp": datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500


@ml_bp.route('/trends', methods=['POST'])
def analyze_trends():
    """
    Analyze ESG trends for a company over time
    
    Request body:
    {
        "company_name": "string (required)",
        "days_back": int (optional, default 30)
    }
    """
    data = request.get_json()
    
    if not data or 'company_name' not in data:
        return jsonify({"error": "company_name is required"}), 400
    
    company_name = data.get('company_name')
    days_back = data.get('days_back', 30)
    
    try:
        # Get historical data from database
        company = Company.query.filter_by(name=company_name).first()
        
        if company:
            # Get historical scores
            scores = ESGScore.query.filter_by(company_id=company.id).order_by(ESGScore.created_at.desc()).all()
            
            historical_scores = [
                {
                    "date": score.created_at.isoformat(),
                    "e_score": score.e_score,
                    "s_score": score.s_score,
                    "g_score": score.g_score,
                    "overall_score": score.overall_score
                }
                for score in scores
            ]
        else:
            historical_scores = []
        
        # Get recent news trends
        collector = get_data_collector()
        recent_news = collector.get_recent_company_news(company_name, days_back)
        
        # Analyze sentiment trends
        ml_analyzer = get_ml_analyzer()
        news_texts = [f"{n.get('title', '')} {n.get('summary', '')}" for n in recent_news]
        
        sentiment_trend = []
        if news_texts:
            for text in news_texts[:20]:  # Limit analysis
                sentiment = ml_analyzer.analyze_sentiment(text)
                sentiment_trend.append({
                    "score": sentiment.get('score', 0.5),
                    "label": sentiment.get('label', 'neutral')
                })
        
        # Calculate average sentiment
        avg_sentiment = sum(s['score'] for s in sentiment_trend) / len(sentiment_trend) if sentiment_trend else 0.5
        
        return jsonify({
            "status": "success",
            "company_name": company_name,
            "trends": {
                "historical_scores": historical_scores,
                "recent_news_count": len(recent_news),
                "sentiment_trend": sentiment_trend,
                "average_sentiment": avg_sentiment,
                "trend_direction": "positive" if avg_sentiment > 0.6 else "negative" if avg_sentiment < 0.4 else "neutral"
            },
            "timestamp": datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500


@ml_bp.route('/benchmark', methods=['POST'])
def benchmark_company():
    """
    Benchmark a company against industry averages
    
    Request body:
    {
        "company_name": "string (required)",
        "industry": "string (optional)",
        "peers": ["string array"] (optional)
    }
    """
    data = request.get_json()
    
    if not data or 'company_name' not in data:
        return jsonify({"error": "company_name is required"}), 400
    
    company_name = data.get('company_name')
    industry = data.get('industry')
    peers = data.get('peers', [])
    
    try:
        # Get company scores
        company = Company.query.filter_by(name=company_name).first()
        
        if not company:
            return jsonify({"error": "Company not found in database"}), 404
        
        latest_score = ESGScore.query.filter_by(company_id=company.id).order_by(ESGScore.created_at.desc()).first()
        
        if not latest_score:
            return jsonify({"error": "No ESG scores found for company"}), 404
        
        company_scores = {
            "e_score": latest_score.e_score,
            "s_score": latest_score.s_score,
            "g_score": latest_score.g_score,
            "overall_score": latest_score.overall_score
        }
        
        # Calculate industry averages (from database or default)
        if industry:
            industry_companies = Company.query.filter_by(industry=industry).all()
            industry_scores = []
            for ic in industry_companies:
                score = ESGScore.query.filter_by(company_id=ic.id).order_by(ESGScore.created_at.desc()).first()
                if score:
                    industry_scores.append({
                        "e_score": score.e_score or 50,
                        "s_score": score.s_score or 50,
                        "g_score": score.g_score or 50,
                        "overall_score": score.overall_score or 50
                    })
            
            if industry_scores:
                industry_avg = {
                    "e_score": sum(s["e_score"] for s in industry_scores) / len(industry_scores),
                    "s_score": sum(s["s_score"] for s in industry_scores) / len(industry_scores),
                    "g_score": sum(s["g_score"] for s in industry_scores) / len(industry_scores),
                    "overall_score": sum(s["overall_score"] for s in industry_scores) / len(industry_scores)
                }
            else:
                industry_avg = {"e_score": 50, "s_score": 50, "g_score": 50, "overall_score": 50}
        else:
            industry_avg = {"e_score": 50, "s_score": 50, "g_score": 50, "overall_score": 50}
        
        # Calculate differences
        benchmark = {
            "company_scores": company_scores,
            "industry_average": industry_avg,
            "difference": {
                "e_score": company_scores["e_score"] - industry_avg["e_score"] if company_scores["e_score"] else 0,
                "s_score": company_scores["s_score"] - industry_avg["s_score"] if company_scores["s_score"] else 0,
                "g_score": company_scores["g_score"] - industry_avg["g_score"] if company_scores["g_score"] else 0,
                "overall_score": company_scores["overall_score"] - industry_avg["overall_score"] if company_scores["overall_score"] else 0
            }
        }
        
        # Add peer comparison if peers provided
        if peers:
            peer_scores = []
            for peer_name in peers:
                peer = Company.query.filter_by(name=peer_name).first()
                if peer:
                    peer_score = ESGScore.query.filter_by(company_id=peer.id).order_by(ESGScore.created_at.desc()).first()
                    if peer_score:
                        peer_scores.append({
                            "company": peer_name,
                            "e_score": peer_score.e_score,
                            "s_score": peer_score.s_score,
                            "g_score": peer_score.g_score,
                            "overall_score": peer_score.overall_score
                        })
            benchmark["peer_comparison"] = peer_scores
        
        return jsonify({
            "status": "success",
            "company_name": company_name,
            "industry": industry,
            "benchmark": benchmark,
            "timestamp": datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500
