"""
Alert Management Routes
ML-powered alert detection and management endpoints
"""
from flask import Blueprint, jsonify, request
from backend.database.models import Alert, Company
from backend.app import db
from backend.services.ml_analyzer import get_ml_analyzer
from backend.services.data_collector import get_data_collector
from datetime import datetime

alerts_bp = Blueprint('alerts', __name__)


@alerts_bp.route('/', methods=['GET'])
def get_alerts():
    """
    Retrieve all alerts with optional filtering.
    
    Query parameters:
    - company_id: Filter by company ID
    - severity: Filter by severity (info, warning, critical)
    - is_resolved: Filter by resolution status (true/false)
    - limit: Maximum number of alerts to return (default: 100)
    """
    try:
        # Get query parameters
        company_id = request.args.get('company_id', type=int)
        severity = request.args.get('severity')
        is_resolved = request.args.get('is_resolved')
        limit = request.args.get('limit', default=100, type=int)
        
        # Build query
        query = Alert.query
        
        if company_id:
            query = query.filter_by(company_id=company_id)
        if severity:
            query = query.filter_by(severity=severity)
        if is_resolved is not None:
            resolved_bool = is_resolved.lower() == 'true'
            query = query.filter_by(is_resolved=resolved_bool)
        
        # Order by most recent first
        query = query.order_by(Alert.created_at.desc()).limit(limit)
        
        alerts = query.all()
        
        # Return array directly for frontend compatibility
        return jsonify([alert.to_dict() for alert in alerts]), 200
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500


@alerts_bp.route('/', methods=['POST'])
def create_alert():
    """
    Create a new alert for a company.
    
    Request body:
    {
        "company_id": int (required),
        "message": "string (required)",
        "severity": "string (optional: info, warning, critical)"
    }
    """
    data = request.get_json()
    
    if not data or 'company_id' not in data or 'message' not in data:
        return jsonify({"error": "company_id and message are required"}), 400
    
    try:
        company_id = data.get('company_id')
        message = data.get('message')
        severity = data.get('severity', 'info')
        
        # Verify company exists
        company = Company.query.get(company_id)
        if not company:
            return jsonify({"error": "Company not found"}), 404
        
        # Create alert
        alert = Alert(
            company_id=company_id,
            message=message,
            severity=severity,
            is_resolved=False
        )
        
        db.session.add(alert)
        db.session.commit()
        
        return jsonify({
            "status": "created",
            "alert": alert.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500


@alerts_bp.route('/<int:alert_id>', methods=['GET'])
def get_alert(alert_id):
    """
    Retrieve a specific alert by ID.
    """
    try:
        alert = Alert.query.get(alert_id)
        
        if not alert:
            return jsonify({"error": "Alert not found"}), 404
        
        return jsonify({
            "status": "success",
            "alert": alert.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500


@alerts_bp.route('/<int:alert_id>', methods=['PUT'])
def update_alert(alert_id):
    """
    Update an alert (e.g., mark as resolved)
    
    Request body:
    {
        "is_resolved": bool (optional),
        "severity": "string (optional)"
    }
    """
    try:
        alert = Alert.query.get(alert_id)
        
        if not alert:
            return jsonify({"error": "Alert not found"}), 404
        
        data = request.get_json()
        
        if 'is_resolved' in data:
            alert.is_resolved = data['is_resolved']
        if 'severity' in data:
            alert.severity = data['severity']
        
        db.session.commit()
        
        return jsonify({
            "status": "updated",
            "alert": alert.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500


@alerts_bp.route('/<int:alert_id>', methods=['DELETE'])
def delete_alert(alert_id):
    """
    Delete an alert
    """
    try:
        alert = Alert.query.get(alert_id)
        
        if not alert:
            return jsonify({"error": "Alert not found"}), 404
        
        db.session.delete(alert)
        db.session.commit()
        
        return jsonify({
            "status": "deleted",
            "message": f"Alert {alert_id} deleted successfully"
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500


@alerts_bp.route('/detect', methods=['POST'])
def detect_alerts():
    """
    Detect potential ESG alerts for a company using ML
    
    Request body:
    {
        "company_name": "string (required)",
        "auto_create": bool (optional, default false),
        "threshold": float (optional, 0-1, default 0.3)
    }
    """
    data = request.get_json()
    
    if not data or 'company_name' not in data:
        return jsonify({"error": "company_name is required"}), 400
    
    company_name = data.get('company_name')
    auto_create = data.get('auto_create', False)
    threshold = data.get('threshold', 0.3)
    
    try:
        # Collect recent data about the company
        data_collector = get_data_collector()
        collected_data = data_collector.collect_company_data(company_name, max_articles=30)
        
        # Aggregate text for analysis
        texts = data_collector.aggregate_text_for_analysis(collected_data)
        
        # Detect risks using ML
        ml_analyzer = get_ml_analyzer()
        risks = ml_analyzer.detect_esg_risks(texts, threshold)
        
        # Auto-create alerts if requested
        created_alerts = []
        if auto_create and risks:
            # Get or create company
            company = Company.query.filter_by(name=company_name).first()
            if not company:
                company = Company(name=company_name)
                db.session.add(company)
                db.session.flush()
            
            # Create alerts for high and critical risks
            for risk in risks:
                if risk['severity'] in ['high', 'critical']:
                    alert = Alert(
                        company_id=company.id,
                        message=f"[{risk['category'].upper()}] {risk['text'][:200]}",
                        severity='critical' if risk['severity'] == 'critical' else 'warning',
                        is_resolved=False
                    )
                    db.session.add(alert)
                    created_alerts.append(alert)
            
            db.session.commit()
        
        return jsonify({
            "status": "success",
            "company_name": company_name,
            "risks_detected": len(risks),
            "risks": risks,
            "alerts_created": len(created_alerts),
            "created_alerts": [alert.to_dict() for alert in created_alerts] if created_alerts else [],
            "timestamp": datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500


@alerts_bp.route('/monitor', methods=['POST'])
def monitor_company():
    """
    Set up continuous monitoring for a company
    
    Request body:
    {
        "company_name": "string (required)",
        "categories": ["environmental", "social", "governance"] (optional)
    }
    """
    data = request.get_json()
    
    if not data or 'company_name' not in data:
        return jsonify({"error": "company_name is required"}), 400
    
    company_name = data.get('company_name')
    categories = data.get('categories', ['environmental', 'social', 'governance'])
    
    try:
        # Get or create company
        company = Company.query.filter_by(name=company_name).first()
        if not company:
            company = Company(name=company_name)
            db.session.add(company)
            db.session.commit()
        
        return jsonify({
            "status": "success",
            "message": f"Monitoring enabled for {company_name}",
            "company_id": company.id,
            "categories": categories,
            "note": "In production, this would set up background jobs for continuous monitoring"
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500


@alerts_bp.route('/summary', methods=['GET'])
def get_alerts_summary():
    """
    Get summary statistics of alerts
    """
    try:
        total_alerts = Alert.query.count()
        unresolved_alerts = Alert.query.filter_by(is_resolved=False).count()
        critical_alerts = Alert.query.filter_by(severity='critical', is_resolved=False).count()
        warning_alerts = Alert.query.filter_by(severity='warning', is_resolved=False).count()
        
        # Get alerts by company
        alerts_by_company = db.session.query(
            Company.name,
            db.func.count(Alert.id).label('alert_count')
        ).join(Alert).group_by(Company.name).all()
        
        return jsonify({
            "status": "success",
            "summary": {
                "total_alerts": total_alerts,
                "unresolved_alerts": unresolved_alerts,
                "critical_alerts": critical_alerts,
                "warning_alerts": warning_alerts,
                "alerts_by_company": [
                    {"company_name": name, "count": count}
                    for name, count in alerts_by_company
                ]
            },
            "timestamp": datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500


@alerts_bp.route('/companies', methods=['GET'])
def get_companies():
    """
    Get all companies with their latest ESG scores
    """
    try:
        companies = Company.query.all()
        
        result = []
        for company in companies:
            # Get latest ESG score for the company
            latest_score = ESGScore.query.filter_by(company_id=company.id)\
                .order_by(ESGScore.created_at.desc()).first()
            
            company_data = company.to_dict()
            if latest_score:
                company_data.update({
                    'e_score': latest_score.e_score,
                    's_score': latest_score.s_score,
                    'g_score': latest_score.g_score,
                    'overall_score': latest_score.overall_score
                })
            else:
                company_data.update({
                    'e_score': None,
                    's_score': None,
                    'g_score': None,
                    'overall_score': None
                })
            
            result.append(company_data)
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500
