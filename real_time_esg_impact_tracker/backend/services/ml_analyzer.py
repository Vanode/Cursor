"""
Machine Learning Service for ESG Analysis
Provides sentiment analysis, text classification, and ESG scoring capabilities
"""
import re
import numpy as np
from typing import Dict, List, Tuple, Optional
from datetime import datetime
import pickle
import os

try:
    from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
    import torch
    from textblob import TextBlob
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
    from sklearn.preprocessing import StandardScaler
    import nltk
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    print("Warning: Some ML libraries not available. Install requirements.txt for full functionality.")


class ESGMLAnalyzer:
    """
    Machine Learning analyzer for ESG (Environmental, Social, Governance) metrics
    """
    
    def __init__(self, models_dir: str = "models"):
        """
        Initialize the ML analyzer
        
        Args:
            models_dir: Directory to store/load trained models
        """
        self.models_dir = models_dir
        os.makedirs(models_dir, exist_ok=True)
        
        # Initialize components
        self.sentiment_analyzer = None
        self.esg_classifier = None
        self.score_predictor = None
        self.vectorizer = None
        self.scaler = None
        
        # ESG keywords dictionary
        self.esg_keywords = {
            'environmental': [
                'carbon', 'emissions', 'climate', 'renewable', 'sustainable', 
                'pollution', 'waste', 'recycling', 'energy efficiency', 'green',
                'fossil fuel', 'clean energy', 'biodiversity', 'conservation',
                'carbon footprint', 'greenhouse gas', 'solar', 'wind power'
            ],
            'social': [
                'diversity', 'inclusion', 'labor', 'human rights', 'safety',
                'community', 'employee', 'workforce', 'fair trade', 'equity',
                'discrimination', 'working conditions', 'health', 'welfare',
                'stakeholder', 'customer satisfaction', 'training', 'education'
            ],
            'governance': [
                'board', 'ethics', 'compliance', 'transparency', 'accountability',
                'corruption', 'fraud', 'audit', 'shareholder', 'executive compensation',
                'risk management', 'internal controls', 'whistleblower', 'disclosure',
                'corporate governance', 'independence', 'integrity', 'regulation'
            ]
        }
        
        # Load or initialize models
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize or load pre-trained models"""
        if not TRANSFORMERS_AVAILABLE:
            print("Transformers not available, using basic TextBlob for sentiment")
            return
        
        try:
            # Try to load fine-tuned sentiment model or use default
            model_path = os.path.join(self.models_dir, "sentiment_model")
            if os.path.exists(model_path):
                self.sentiment_analyzer = pipeline("sentiment-analysis", model=model_path)
            else:
                # Use pre-trained FinBERT for financial sentiment (good for ESG)
                self.sentiment_analyzer = pipeline(
                    "sentiment-analysis",
                    model="ProsusAI/finbert",
                    tokenizer="ProsusAI/finbert"
                )
        except Exception as e:
            print(f"Could not load transformer model: {e}. Using TextBlob fallback.")
            self.sentiment_analyzer = None
        
        # Load custom ESG classifier if exists
        classifier_path = os.path.join(self.models_dir, "esg_classifier.pkl")
        vectorizer_path = os.path.join(self.models_dir, "vectorizer.pkl")
        
        if os.path.exists(classifier_path) and os.path.exists(vectorizer_path):
            try:
                with open(classifier_path, 'rb') as f:
                    self.esg_classifier = pickle.load(f)
                with open(vectorizer_path, 'rb') as f:
                    self.vectorizer = pickle.load(f)
            except Exception as e:
                print(f"Error loading classifier: {e}")
                self._create_default_classifier()
        else:
            self._create_default_classifier()
    
    def _create_default_classifier(self):
        """Create a default ESG classifier with sample training"""
        self.vectorizer = TfidfVectorizer(max_features=1000, ngram_range=(1, 2))
        self.esg_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
        
        # Sample training data (in production, use real labeled data)
        training_texts = self._get_sample_training_data()
        training_labels = self._get_sample_training_labels()
        
        if training_texts and training_labels:
            X = self.vectorizer.fit_transform(training_texts)
            self.esg_classifier.fit(X, training_labels)
            
            # Save the trained model
            self._save_models()
    
    def _get_sample_training_data(self) -> List[str]:
        """Get sample training data for ESG classification"""
        return [
            "Company reduces carbon emissions by 30%",
            "Improved employee diversity and inclusion programs",
            "Board of directors enhances transparency in reporting",
            "Renewable energy initiative launched",
            "Labor rights violations reported",
            "New sustainability goals announced",
            "Executive compensation linked to ESG metrics",
            "Pollution incident at manufacturing plant",
            "Community outreach program expanded",
            "Enhanced data privacy and security measures",
        ]
    
    def _get_sample_training_labels(self) -> List[str]:
        """Get sample labels for training data"""
        return [
            'environmental', 'social', 'governance',
            'environmental', 'social', 'environmental',
            'governance', 'environmental', 'social', 'governance'
        ]
    
    def _save_models(self):
        """Save trained models to disk"""
        try:
            if self.esg_classifier:
                with open(os.path.join(self.models_dir, "esg_classifier.pkl"), 'wb') as f:
                    pickle.dump(self.esg_classifier, f)
            if self.vectorizer:
                with open(os.path.join(self.models_dir, "vectorizer.pkl"), 'wb') as f:
                    pickle.dump(self.vectorizer, f)
        except Exception as e:
            print(f"Error saving models: {e}")
    
    def analyze_sentiment(self, text: str) -> Dict[str, any]:
        """
        Analyze sentiment of text
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary with sentiment label and score
        """
        if not text or not text.strip():
            return {"label": "neutral", "score": 0.5, "method": "default"}
        
        # Try transformer-based analysis first
        if self.sentiment_analyzer and TRANSFORMERS_AVAILABLE:
            try:
                result = self.sentiment_analyzer(text[:512])[0]  # Limit text length
                return {
                    "label": result['label'].lower(),
                    "score": result['score'],
                    "method": "transformer"
                }
            except Exception as e:
                print(f"Transformer sentiment failed: {e}, falling back to TextBlob")
        
        # Fallback to TextBlob
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        
        if polarity > 0.1:
            label = "positive"
        elif polarity < -0.1:
            label = "negative"
        else:
            label = "neutral"
        
        return {
            "label": label,
            "score": (polarity + 1) / 2,  # Normalize to 0-1
            "polarity": polarity,
            "subjectivity": blob.sentiment.subjectivity,
            "method": "textblob"
        }
    
    def classify_esg_category(self, text: str) -> Dict[str, any]:
        """
        Classify text into ESG categories
        
        Args:
            text: Text to classify
            
        Returns:
            Dictionary with category predictions and scores
        """
        if not text or not text.strip():
            return {"category": "unknown", "confidence": 0.0, "scores": {}}
        
        text_lower = text.lower()
        
        # Keyword-based scoring
        category_scores = {
            'environmental': 0,
            'social': 0,
            'governance': 0
        }
        
        for category, keywords in self.esg_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    category_scores[category] += 1
        
        # ML-based classification if model exists
        ml_prediction = None
        if self.esg_classifier and self.vectorizer:
            try:
                X = self.vectorizer.transform([text])
                ml_prediction = self.esg_classifier.predict(X)[0]
                ml_probabilities = self.esg_classifier.predict_proba(X)[0]
                
                # Combine keyword scores with ML predictions
                for i, category in enumerate(self.esg_classifier.classes_):
                    category_scores[category] += ml_probabilities[i] * 10
            except Exception as e:
                print(f"ML classification error: {e}")
        
        # Determine primary category
        if sum(category_scores.values()) == 0:
            return {
                "category": "general",
                "confidence": 0.0,
                "scores": category_scores,
                "method": "keyword"
            }
        
        primary_category = max(category_scores, key=category_scores.get)
        total_score = sum(category_scores.values())
        confidence = category_scores[primary_category] / total_score if total_score > 0 else 0
        
        return {
            "category": primary_category,
            "confidence": confidence,
            "scores": category_scores,
            "ml_prediction": ml_prediction,
            "method": "hybrid"
        }
    
    def calculate_esg_scores(self, text_data: List[str], historical_data: Optional[Dict] = None) -> Dict[str, float]:
        """
        Calculate ESG scores based on text analysis
        
        Args:
            text_data: List of text snippets to analyze
            historical_data: Optional historical ESG data for the company
            
        Returns:
            Dictionary with E, S, G, and overall scores (0-100)
        """
        if not text_data:
            return {
                "e_score": 50.0,
                "s_score": 50.0,
                "g_score": 50.0,
                "overall_score": 50.0,
                "confidence": 0.0
            }
        
        category_sentiments = {
            'environmental': [],
            'social': [],
            'governance': []
        }
        
        # Analyze each text snippet
        for text in text_data:
            if not text or not text.strip():
                continue
            
            # Get sentiment and category
            sentiment = self.analyze_sentiment(text)
            category_info = self.classify_esg_category(text)
            
            category = category_info['category']
            if category in category_sentiments:
                # Convert sentiment to 0-100 score
                sentiment_score = sentiment['score'] * 100
                confidence = category_info['confidence']
                weighted_score = sentiment_score * confidence
                category_sentiments[category].append(weighted_score)
        
        # Calculate average scores for each category
        e_score = np.mean(category_sentiments['environmental']) if category_sentiments['environmental'] else 50.0
        s_score = np.mean(category_sentiments['social']) if category_sentiments['social'] else 50.0
        g_score = np.mean(category_sentiments['governance']) if category_sentiments['governance'] else 50.0
        
        # Calculate overall score (weighted average)
        overall_score = (e_score * 0.35 + s_score * 0.35 + g_score * 0.30)
        
        # If historical data provided, blend with current analysis
        if historical_data:
            alpha = 0.7  # Weight for new data
            e_score = alpha * e_score + (1 - alpha) * historical_data.get('e_score', e_score)
            s_score = alpha * s_score + (1 - alpha) * historical_data.get('s_score', s_score)
            g_score = alpha * g_score + (1 - alpha) * historical_data.get('g_score', g_score)
            overall_score = alpha * overall_score + (1 - alpha) * historical_data.get('overall_score', overall_score)
        
        # Calculate confidence based on amount of data
        confidence = min(len(text_data) / 10.0, 1.0)  # Max confidence at 10+ texts
        
        return {
            "e_score": round(e_score, 2),
            "s_score": round(s_score, 2),
            "g_score": round(g_score, 2),
            "overall_score": round(overall_score, 2),
            "confidence": round(confidence, 2),
            "data_points": len(text_data)
        }
    
    def detect_esg_risks(self, text_data: List[str], threshold: float = 0.3) -> List[Dict]:
        """
        Detect potential ESG risks from text data
        
        Args:
            text_data: List of text snippets to analyze
            threshold: Threshold for risk detection (0-1)
            
        Returns:
            List of detected risks with severity and category
        """
        risks = []
        
        # Risk keywords
        risk_keywords = {
            'environmental': ['pollution', 'spill', 'contamination', 'violation', 'fine', 'lawsuit'],
            'social': ['discrimination', 'harassment', 'violation', 'lawsuit', 'strike', 'accident'],
            'governance': ['fraud', 'corruption', 'scandal', 'investigation', 'lawsuit', 'breach']
        }
        
        for text in text_data:
            if not text or not text.strip():
                continue
            
            text_lower = text.lower()
            sentiment = self.analyze_sentiment(text)
            category_info = self.classify_esg_category(text)
            
            # Check for negative sentiment
            if sentiment['label'] == 'negative' or sentiment['score'] < 0.4:
                category = category_info['category']
                
                # Check for risk keywords
                risk_found = False
                for risk_category, keywords in risk_keywords.items():
                    for keyword in keywords:
                        if keyword in text_lower:
                            risk_found = True
                            severity = self._calculate_risk_severity(sentiment['score'], keyword)
                            
                            risks.append({
                                'text': text[:200],  # First 200 chars
                                'category': risk_category,
                                'severity': severity,
                                'sentiment_score': sentiment['score'],
                                'confidence': category_info['confidence'],
                                'timestamp': datetime.utcnow().isoformat()
                            })
                            break
                    if risk_found:
                        break
        
        # Sort by severity
        risks.sort(key=lambda x: x['severity'], reverse=True)
        
        return risks
    
    def _calculate_risk_severity(self, sentiment_score: float, keyword: str) -> str:
        """
        Calculate risk severity based on sentiment and keyword
        
        Args:
            sentiment_score: Sentiment score (0-1)
            keyword: Risk keyword found
            
        Returns:
            Severity level: 'low', 'medium', 'high', 'critical'
        """
        critical_keywords = ['fraud', 'corruption', 'lawsuit', 'investigation', 'spill']
        
        if keyword in critical_keywords and sentiment_score < 0.3:
            return 'critical'
        elif sentiment_score < 0.25:
            return 'high'
        elif sentiment_score < 0.4:
            return 'medium'
        else:
            return 'low'
    
    def generate_insights(self, analysis_results: Dict) -> List[str]:
        """
        Generate human-readable insights from analysis results
        
        Args:
            analysis_results: Results from ESG analysis
            
        Returns:
            List of insight strings
        """
        insights = []
        
        scores = analysis_results.get('esg_scores', {})
        e_score = scores.get('e_score', 50)
        s_score = scores.get('s_score', 50)
        g_score = scores.get('g_score', 50)
        overall = scores.get('overall_score', 50)
        
        # Overall performance
        if overall >= 70:
            insights.append(f"Strong overall ESG performance with a score of {overall}/100")
        elif overall >= 50:
            insights.append(f"Moderate ESG performance with room for improvement (score: {overall}/100)")
        else:
            insights.append(f"ESG performance needs significant improvement (score: {overall}/100)")
        
        # Individual category insights
        if e_score >= 70:
            insights.append("Environmental practices are strong")
        elif e_score < 40:
            insights.append("Environmental performance requires immediate attention")
        
        if s_score >= 70:
            insights.append("Social responsibility initiatives are well-executed")
        elif s_score < 40:
            insights.append("Social practices need improvement")
        
        if g_score >= 70:
            insights.append("Governance structure is robust")
        elif g_score < 40:
            insights.append("Governance practices require strengthening")
        
        # Risks
        risks = analysis_results.get('risks', [])
        if risks:
            critical_risks = [r for r in risks if r['severity'] == 'critical']
            high_risks = [r for r in risks if r['severity'] == 'high']
            
            if critical_risks:
                insights.append(f"⚠️ {len(critical_risks)} critical risk(s) detected requiring immediate action")
            if high_risks:
                insights.append(f"⚠️ {len(high_risks)} high-priority risk(s) identified")
        
        return insights


# Global instance
_ml_analyzer = None


def get_ml_analyzer() -> ESGMLAnalyzer:
    """Get or create the global ML analyzer instance"""
    global _ml_analyzer
    if _ml_analyzer is None:
        models_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'models')
        _ml_analyzer = ESGMLAnalyzer(models_dir=models_dir)
    return _ml_analyzer
