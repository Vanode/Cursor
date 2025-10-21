# 🌍 Real-Time ESG Impact Tracker

A hackathon MVP for tracking and analyzing Environmental, Social, and Governance (ESG) metrics for companies using Flask, SQLite, and Ollama LLM integration.

## 📋 Project Overview

This is the baseline project structure for the ESG Impact Tracker. The application provides:
- RESTful API endpoints for ESG analysis and alerts
- SQLite database for storing company data, ESG scores, and alerts
- Integration hooks for Ollama LLM (local language model)
- Modular architecture ready for expansion

## 🏗️ Project Structure

```
real_time_esg_impact_tracker/
│
├── backend/
│   ├── app.py                  # Flask application factory
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── analyze.py          # ESG analysis endpoints
│   │   └── alerts.py           # Alert management endpoints
│   ├── database/
│   │   ├── __init__.py
│   │   └── models.py           # SQLAlchemy ORM models
│   ├── services/
│   │   ├── __init__.py
│   │   └── ollama_client.py    # Ollama LLM integration (stub)
│   └── utils/
│       ├── __init__.py
│       └── db_init.py          # Database initialization script
│
├── config.py                   # Application configuration
├── .env.example                # Environment variables template
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Ollama (optional, for LLM integration)

### Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd real_time_esg_impact_tracker
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration if needed
   ```

5. **Initialize the database:**
   ```bash
   python backend/utils/db_init.py
   ```

### Running the Application

```bash
python backend/app.py
```

The application will start on `http://localhost:5000`

## 🧪 Testing the API

### Health Check
```bash
curl http://localhost:5000/health
```

Expected response:
```json
{
  "status": "ok"
}
```

### Analyze Company
```bash
curl -X POST http://localhost:5000/api/analyze/company \
  -H "Content-Type: application/json" \
  -d '{"company_name": "GreenTech Inc."}'
```

### Get Alerts
```bash
curl http://localhost:5000/api/alerts/
```

### Create Alert
```bash
curl -X POST http://localhost:5000/api/alerts/ \
  -H "Content-Type: application/json" \
  -d '{"company_id": 1, "message": "New ESG alert"}'
```

## 📊 Database Models

### Company
- `id`: Primary key
- `name`: Company name (unique)
- `industry`: Industry sector
- `created_at`: Timestamp

### ESGScore
- `id`: Primary key
- `company_id`: Foreign key to Company
- `e_score`: Environmental score (0-100)
- `s_score`: Social score (0-100)
- `g_score`: Governance score (0-100)
- `overall_score`: Weighted average score
- `created_at`, `updated_at`: Timestamps

### Alert
- `id`: Primary key
- `company_id`: Foreign key to Company
- `message`: Alert message
- `severity`: Alert level (info, warning, critical)
- `is_resolved`: Boolean flag
- `created_at`: Timestamp

## 🔧 Configuration

Key configuration options in `config.py`:

- `DATABASE_URI`: SQLite database path
- `OLLAMA_HOST`: Ollama API endpoint (default: http://localhost:11434)
- `OLLAMA_MODEL`: LLM model to use (default: llama2)
- `SECRET_KEY`: Flask secret key
- `DEBUG`: Debug mode flag

## 🤖 Ollama Integration

The Ollama integration is currently a stub implementation. To enable actual LLM functionality:

1. Install Ollama from https://ollama.ai
2. Pull a model: `ollama pull llama2`
3. The application will connect to Ollama at `http://localhost:11434`

Stub functions in `backend/services/ollama_client.py`:
- `query_ollama()`: Send prompts to Ollama
- `query_ollama_streaming()`: Stream responses
- `analyze_esg_with_ollama()`: ESG-specific analysis

## 📝 Next Steps

This baseline structure is ready for expansion:

- [ ] Implement actual Ollama LLM integration
- [ ] Add web scraping for company data
- [ ] Implement NLP for ESG metric extraction
- [ ] Create a frontend dashboard
- [ ] Add authentication and authorization
- [ ] Implement real-time data streaming
- [ ] Add more comprehensive ESG metrics
- [ ] Create data visualization endpoints

## 🧑‍💻 Development

### Running Tests
```bash
pytest
```

### Database Management

Reset database:
```bash
python backend/utils/db_init.py
```

## 📄 License

This is a hackathon MVP project.

## 🙏 Acknowledgments

Built for the ESG Impact Tracker Hackathon
