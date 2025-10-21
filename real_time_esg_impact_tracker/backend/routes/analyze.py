"""
ESG Analysis Routes
Machine Learning-powered ESG analysis endpoints
"""
from flask import Blueprint, jsonify, request
from backend.services.ollama_client import query_ollama
from backend.services.nlp_pipeline import get_nlp_pipeline
from backend.services.ml_analyzer import get_ml_analyzer
from backend.services.data_collector import get_data_collector
from backend.database.models import Company, ESGScore
from backend.app import db
from datetime import datetime

analyze_bp = Blueprint('analyze', __name__)


@analyze_bp.route('/', methods=['GET'])
def index():
    """
    Root endpoint for analyze blueprint
    """
    return jsonify({
        "message": "ESG Analysis endpoint - ML Powered",
        "available_routes": [
            "/company - Full company ESG analysis",
            "/sentiment - Sentiment analysis",
            "/category - ESG category classification",
            "/scores - Calculate ESG scores",
            "/compare - Compare multiple companies",
            "/report - Generate comprehensive report",
            "/aspect - Analyze specific ESG aspect"
        ]
    }), 200


@analyze_bp.route('/company', methods=['POST'])
def analyze_company():
    """
    Analyze ESG metrics for a company using ML/NLP pipeline.
    Expects JSON payload with company information.
    
    Request body:
    {
        "company_name": "string (required)",
        "max_articles": int (optional, default 20),
        "save_to_db": bool (optional, default true)
    }
    """
    data = request.get_json()
    
    if not data or 'company_name' not in data:
        return jsonify({"error": "company_name is required"}), 400
    
    company_name = data.get('company_name')
    max_articles = data.get('max_articles', 20)
    save_to_db = data.get('save_to_db', True)
    
    try:
        # Use NLP pipeline for comprehensive analysis
        pipeline = get_nlp_pipeline()
        analysis_results = pipeline.analyze_company(company_name, max_articles)
        
        # Save to database if requested
        if save_to_db:
            _save_analysis_to_db(company_name, analysis_results)
        
        # Optional: Get additional insights from Ollama if available
        ollama_insights = None
        try:
            prompt = f"Provide additional ESG insights for {company_name} based on recent performance"
            ollama_insights = query_ollama(prompt)
        except Exception as e:
            print(f"Ollama integration error: {e}")
        
        return jsonify({
            "status": "success",
            "company_name": company_name,
            "analysis": analysis_results,
            "ollama_insights": ollama_insights,
            "timestamp": datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e),
            "company_name": company_name
        }), 500


@analyze_bp.route('/sentiment', methods=['POST'])
def analyze_sentiment():
    """
    Analyze sentiment of provided text
    
    Request body:
    {
        "text": "string (required)"
    }
    """
    data = request.get_json()
    
    if not data or 'text' not in data:
        return jsonify({"error": "text is required"}), 400
    
    text = data.get('text')
    
    try:
        ml_analyzer = get_ml_analyzer()
        sentiment_result = ml_analyzer.analyze_sentiment(text)
        
        return jsonify({
            "status": "success",
            "text": text[:100] + "..." if len(text) > 100 else text,
            "sentiment": sentiment_result,
            "timestamp": datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500


@analyze_bp.route('/category', methods=['POST'])
def classify_category():
    """
    Classify text into ESG categories
    
    Request body:
    {
        "text": "string (required)"
    }
    """
    data = request.get_json()
    
    if not data or 'text' not in data:
        return jsonify({"error": "text is required"}), 400
    
    text = data.get('text')
    
    try:
        ml_analyzer = get_ml_analyzer()
        category_result = ml_analyzer.classify_esg_category(text)
        
        return jsonify({
            "status": "success",
            "text": text[:100] + "..." if len(text) > 100 else text,
            "classification": category_result,
            "timestamp": datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500


@analyze_bp.route('/scores', methods=['POST'])
def calculate_scores():
    """
    Calculate ESG scores from text data
    
    Request body:
    {
        "texts": ["string array (required)"],
        "company_name": "string (optional)",
        "save_to_db": bool (optional, default false)
    }
    """
    data = request.get_json()
    
    if not data or 'texts' not in data:
        return jsonify({"error": "texts array is required"}), 400
    
    texts = data.get('texts')
    company_name = data.get('company_name')
    save_to_db = data.get('save_to_db', False)
    
    if not isinstance(texts, list):
        return jsonify({"error": "texts must be an array"}), 400
    
    try:
        ml_analyzer = get_ml_analyzer()
        scores = ml_analyzer.calculate_esg_scores(texts)
        
        # Save to database if requested and company name provided
        if save_to_db and company_name:
            _save_scores_to_db(company_name, scores)
        
        return jsonify({
            "status": "success",
            "company_name": company_name,
            "scores": scores,
            "texts_analyzed": len(texts),
            "timestamp": datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500


@analyze_bp.route('/compare', methods=['POST'])
def compare_companies():
    """
    Compare ESG performance across multiple companies
    
    Request body:
    {
        "companies": ["string array (required, 2-5 companies)"]
    }
    """
    data = request.get_json()
    
    if not data or 'companies' not in data:
        return jsonify({"error": "companies array is required"}), 400
    
    companies = data.get('companies')
    
    if not isinstance(companies, list) or len(companies) < 2:
        return jsonify({"error": "At least 2 companies required for comparison"}), 400
    
    if len(companies) > 5:
        return jsonify({"error": "Maximum 5 companies allowed for comparison"}), 400
    
    try:
        pipeline = get_nlp_pipeline()
        comparison_results = pipeline.compare_companies(companies)
        
        return jsonify({
            "status": "success",
            "comparison": comparison_results,
            "timestamp": datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500


@analyze_bp.route('/report', methods=['POST'])
def generate_report():
    """
    Generate comprehensive ESG report
    
    Request body:
    {
        "company_name": "string (required)",
        "format": "string (optional: json, text, summary)"
    }
    """
    data = request.get_json()
    
    if not data or 'company_name' not in data:
        return jsonify({"error": "company_name is required"}), 400
    
    company_name = data.get('company_name')
    format_type = data.get('format', 'json')
    
    try:
        pipeline = get_nlp_pipeline()
        report = pipeline.generate_report(company_name, format_type)
        
        if format_type in ['text', 'summary']:
            return report, 200, {'Content-Type': 'text/plain; charset=utf-8'}
        else:
            return jsonify({
                "status": "success",
                "company_name": company_name,
                "report": report,
                "format": format_type,
                "timestamp": datetime.utcnow().isoformat()
            }), 200
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500


@analyze_bp.route('/aspect', methods=['POST'])
def analyze_aspect():
    """
    Analyze specific ESG aspect
    
    Request body:
    {
        "company_name": "string (required)",
        "aspect": "string (required, e.g., 'carbon emissions', 'diversity')"
    }
    """
    data = request.get_json()
    
    if not data or 'company_name' not in data or 'aspect' not in data:
        return jsonify({"error": "company_name and aspect are required"}), 400
    
    company_name = data.get('company_name')
    aspect = data.get('aspect')
    
    try:
        pipeline = get_nlp_pipeline()
        aspect_analysis = pipeline.analyze_specific_aspect(company_name, aspect)
        
        return jsonify({
            "status": "success",
            "analysis": aspect_analysis,
            "timestamp": datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500


def _save_analysis_to_db(company_name: str, analysis: dict):
    """Save analysis results to database"""
    try:
        # Get or create company
        company = Company.query.filter_by(name=company_name).first()
        if not company:
            company = Company(name=company_name)
            db.session.add(company)
            db.session.flush()
        
        # Save ESG scores
        scores = analysis.get('esg_scores', {})
        esg_score = ESGScore(
            company_id=company.id,
            e_score=scores.get('e_score'),
            s_score=scores.get('s_score'),
            g_score=scores.get('g_score'),
            overall_score=scores.get('overall_score')
        )
        db.session.add(esg_score)
        db.session.commit()
        
    except Exception as e:
        db.session.rollback()
        print(f"Error saving to database: {e}")


def _save_scores_to_db(company_name: str, scores: dict):
    """Save ESG scores to database"""
    try:
        # Get or create company
        company = Company.query.filter_by(name=company_name).first()
        if not company:
            company = Company(name=company_name)
            db.session.add(company)
            db.session.flush()
        
        # Save ESG scores
        esg_score = ESGScore(
            company_id=company.id,
            e_score=scores.get('e_score'),
            s_score=scores.get('s_score'),
            g_score=scores.get('g_score'),
            overall_score=scores.get('overall_score')
        )
        db.session.add(esg_score)
        db.session.commit()
        
    except Exception as e:
        db.session.rollback()
        print(f"Error saving scores to database: {e}")
