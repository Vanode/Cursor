"""
Configuration file for ESG Impact Tracker
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database Configuration
DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///esg_tracker.db')

# Ollama Configuration
OLLAMA_HOST = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'llama2')

# Flask Configuration
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
DEBUG = os.getenv('DEBUG', 'True').lower() in ('true', '1', 'yes')

# API Configuration
API_VERSION = 'v1'
API_PREFIX = '/api'

# ESG Score Configuration
ESG_SCORE_MIN = 0
ESG_SCORE_MAX = 100

# Alert Severity Levels
ALERT_SEVERITY_LEVELS = ['info', 'warning', 'critical']

# Logging Configuration
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
