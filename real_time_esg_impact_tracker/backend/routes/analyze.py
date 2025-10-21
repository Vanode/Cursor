"""
ESG Analysis Routes
Placeholder for ESG analysis endpoints
"""
from flask import Blueprint, jsonify, request
from backend.services.ollama_client import query_ollama

analyze_bp = Blueprint('analyze', __name__)


@analyze_bp.route('/', methods=['GET'])
def index():
    """
    Root endpoint for analyze blueprint
    """
    return jsonify({
        "message": "ESG Analysis endpoint",
        "available_routes": ["/company"]
    }), 200


@analyze_bp.route('/company', methods=['POST'])
def analyze_company():
    """
    Analyze ESG metrics for a company.
    Expects JSON payload with company information.
    """
    data = request.get_json()
    
    if not data or 'company_name' not in data:
        return jsonify({"error": "company_name is required"}), 400
    
    company_name = data.get('company_name')
    
    # Placeholder for ESG analysis logic
    # In the future, this will use NLP and Ollama LLM
    prompt = f"Analyze ESG metrics for {company_name}"
    ollama_response = query_ollama(prompt)
    
    return jsonify({
        "company": company_name,
        "status": "analysis_pending",
        "message": "ESG analysis endpoint is ready for integration",
        "ollama_response": ollama_response
    }), 200
