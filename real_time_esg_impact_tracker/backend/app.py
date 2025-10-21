"""
Flask Application Factory for ESG Impact Tracker
"""
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from config import DATABASE_URI

# Initialize SQLAlchemy instance
db = SQLAlchemy()


def create_app():
    """
    Application factory pattern for Flask app.
    """
    app = Flask(__name__)
    
    # Load configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize database with app
    db.init_app(app)
    
    # Register blueprints
    from backend.routes.analyze import analyze_bp
    from backend.routes.alerts import alerts_bp
    
    app.register_blueprint(analyze_bp, url_prefix='/api/analyze')
    app.register_blueprint(alerts_bp, url_prefix='/api/alerts')
    
    # Health check route
    @app.route('/health', methods=['GET'])
    def health():
        return jsonify({"status": "ok"}), 200
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
