#!/usr/bin/env python3
"""
Setup script for ML components
Downloads required models and data
"""
import os
import sys

def setup_nltk():
    """Download required NLTK data"""
    print("📦 Downloading NLTK data...")
    try:
        import nltk
        nltk.download('punkt', quiet=True)
        nltk.download('vader_lexicon', quiet=True)
        nltk.download('stopwords', quiet=True)
        print("✅ NLTK data downloaded successfully")
        return True
    except ImportError:
        print("⚠️  NLTK not installed. Install with: pip install nltk")
        return False
    except Exception as e:
        print(f"❌ Error downloading NLTK data: {e}")
        return False


def create_models_directory():
    """Create models directory if it doesn't exist"""
    print("📁 Creating models directory...")
    try:
        models_dir = os.path.join(os.path.dirname(__file__), 'models')
        os.makedirs(models_dir, exist_ok=True)
        print(f"✅ Models directory created at: {models_dir}")
        return True
    except Exception as e:
        print(f"❌ Error creating models directory: {e}")
        return False


def test_imports():
    """Test if all required packages are installed"""
    print("🔍 Testing imports...")
    
    required_packages = [
        ('sklearn', 'scikit-learn'),
        ('numpy', 'numpy'),
        ('pandas', 'pandas'),
        ('transformers', 'transformers'),
        ('torch', 'torch'),
        ('nltk', 'nltk'),
        ('textblob', 'textblob'),
        ('bs4', 'beautifulsoup4'),
        ('feedparser', 'feedparser'),
    ]
    
    missing_packages = []
    
    for package, install_name in required_packages:
        try:
            __import__(package)
            print(f"  ✅ {install_name}")
        except ImportError:
            print(f"  ❌ {install_name} (missing)")
            missing_packages.append(install_name)
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print(f"Install with: pip install {' '.join(missing_packages)}")
        return False
    else:
        print("\n✅ All required packages are installed")
        return True


def initialize_ml_models():
    """Initialize ML models"""
    print("🤖 Initializing ML models...")
    try:
        from backend.services.ml_analyzer import get_ml_analyzer
        
        analyzer = get_ml_analyzer()
        print("✅ ML analyzer initialized successfully")
        
        # Test basic functionality
        test_text = "Company announces new sustainability initiative"
        sentiment = analyzer.analyze_sentiment(test_text)
        category = analyzer.classify_esg_category(test_text)
        
        print(f"  Test sentiment: {sentiment.get('label')} (score: {sentiment.get('score', 0):.2f})")
        print(f"  Test category: {category.get('category')} (confidence: {category.get('confidence', 0):.2f})")
        
        return True
    except Exception as e:
        print(f"❌ Error initializing ML models: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main setup function"""
    print("\n" + "="*60)
    print("🌍 ESG Impact Tracker - ML Setup")
    print("="*60 + "\n")
    
    steps = [
        ("Testing package imports", test_imports),
        ("Creating models directory", create_models_directory),
        ("Downloading NLTK data", setup_nltk),
        ("Initializing ML models", initialize_ml_models),
    ]
    
    results = []
    for step_name, step_func in steps:
        print(f"\n{step_name}...")
        result = step_func()
        results.append(result)
        if not result:
            print(f"\n⚠️  Setup step '{step_name}' failed, but continuing...")
    
    print("\n" + "="*60)
    if all(results):
        print("✅ ML Setup completed successfully!")
        print("\nYou can now use all ML features:")
        print("  • Sentiment analysis")
        print("  • ESG category classification")
        print("  • Automated data collection")
        print("  • Risk detection")
        print("  • Company comparison")
    else:
        print("⚠️  ML Setup completed with some warnings")
        print("\nSome features may not work without all dependencies.")
        print("Install missing packages with:")
        print("  pip install -r requirements.txt")
    print("="*60 + "\n")
    
    print("📚 For more information, see ML_FEATURES.md")
    print("🚀 Start the server with: python backend/app.py\n")


if __name__ == '__main__':
    main()
