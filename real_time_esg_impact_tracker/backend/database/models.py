"""
SQLAlchemy ORM Models for ESG Impact Tracker
"""
from datetime import datetime
from backend.app import db


class Company(db.Model):
    """
    Company model to store company information
    """
    __tablename__ = 'companies'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    industry = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    esg_scores = db.relationship('ESGScore', backref='company', lazy=True, cascade='all, delete-orphan')
    alerts = db.relationship('Alert', backref='company', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Company {self.name}>'
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'industry': self.industry,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class ESGScore(db.Model):
    """
    ESG Score model to track Environmental, Social, and Governance scores
    """
    __tablename__ = 'esg_scores'
    
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    
    # Individual ESG metrics (scale 0-100)
    e_score = db.Column(db.Float, nullable=True)  # Environmental score
    s_score = db.Column(db.Float, nullable=True)  # Social score
    g_score = db.Column(db.Float, nullable=True)  # Governance score
    overall_score = db.Column(db.Float, nullable=True)  # Weighted average
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<ESGScore company_id={self.company_id} overall={self.overall_score}>'
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'company_id': self.company_id,
            'e_score': self.e_score,
            's_score': self.s_score,
            'g_score': self.g_score,
            'overall_score': self.overall_score,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class Alert(db.Model):
    """
    Alert model to track ESG-related alerts for companies
    """
    __tablename__ = 'alerts'
    
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    severity = db.Column(db.String(20), default='info')  # info, warning, critical
    is_resolved = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Alert id={self.id} company_id={self.company_id}>'
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'company_id': self.company_id,
            'message': self.message,
            'severity': self.severity,
            'is_resolved': self.is_resolved,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
