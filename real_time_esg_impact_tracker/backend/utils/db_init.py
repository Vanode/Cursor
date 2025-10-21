"""
Database Initialization Script
Creates all tables defined in the models
"""
import sys
import os

# Add the parent directory to the path to allow imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.app import create_app, db
from backend.database.models import Company, ESGScore, Alert


def init_database():
    """
    Initialize the database by creating all tables.
    """
    app = create_app()
    
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("Database tables created successfully!")
        
        # Optionally add some seed data
        add_seed_data()


def add_seed_data():
    """
    Add some initial seed data for testing purposes.
    """
    # Check if data already exists
    if Company.query.first():
        print("Database already contains data. Skipping seed data.")
        return
    
    print("Adding seed data...")
    
    # Create sample companies
    company1 = Company(name="GreenTech Inc.", industry="Technology")
    company2 = Company(name="EcoEnergy Corp.", industry="Energy")
    company3 = Company(name="SustainableGoods Ltd.", industry="Retail")
    
    db.session.add_all([company1, company2, company3])
    db.session.commit()
    
    # Create sample ESG scores
    score1 = ESGScore(
        company_id=company1.id,
        e_score=85.5,
        s_score=78.2,
        g_score=92.0,
        overall_score=85.2
    )
    score2 = ESGScore(
        company_id=company2.id,
        e_score=90.0,
        s_score=82.5,
        g_score=88.0,
        overall_score=86.8
    )
    
    db.session.add_all([score1, score2])
    db.session.commit()
    
    # Create sample alerts
    alert1 = Alert(
        company_id=company1.id,
        message="High carbon emissions detected in Q3 report",
        severity="warning"
    )
    alert2 = Alert(
        company_id=company2.id,
        message="Improved renewable energy adoption",
        severity="info"
    )
    
    db.session.add_all([alert1, alert2])
    db.session.commit()
    
    print("Seed data added successfully!")


def drop_all_tables():
    """
    Drop all tables (use with caution!)
    """
    app = create_app()
    
    with app.app_context():
        print("Dropping all database tables...")
        db.drop_all()
        print("All tables dropped successfully!")


if __name__ == '__main__':
    init_database()
