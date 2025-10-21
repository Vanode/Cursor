#!/usr/bin/env python3
"""
Test script for ML features
Verifies that all ML components are working correctly
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

def test_ml_analyzer():
    """Test ML analyzer functionality"""
    print("\n" + "="*60)
    print("Testing ML Analyzer")
    print("="*60)
    
    try:
        from backend.services.ml_analyzer import get_ml_analyzer
        
        analyzer = get_ml_analyzer()
        print("✅ ML Analyzer initialized")
        
        # Test sentiment analysis
        test_text = "Company announces major sustainability initiative and carbon reduction targets"
        sentiment = analyzer.analyze_sentiment(test_text)
        print(f"\n📊 Sentiment Analysis:")
        print(f"   Text: {test_text[:60]}...")
        print(f"   Label: {sentiment.get('label')}")
        print(f"   Score: {sentiment.get('score', 0):.2f}")
        print(f"   Method: {sentiment.get('method')}")
        
        # Test category classification
        test_text2 = "Board of directors implements new ethics and compliance framework"
        category = analyzer.classify_esg_category(test_text2)
        print(f"\n🏷️  Category Classification:")
        print(f"   Text: {test_text2[:60]}...")
        print(f"   Category: {category.get('category')}")
        print(f"   Confidence: {category.get('confidence', 0):.2f}")
        
        # Test ESG scoring
        test_texts = [
            "Company reduces carbon emissions by 30%",
            "New diversity program launched",
            "Enhanced governance transparency"
        ]
        scores = analyzer.calculate_esg_scores(test_texts)
        print(f"\n📈 ESG Scores:")
        print(f"   Environmental: {scores.get('e_score')}")
        print(f"   Social: {scores.get('s_score')}")
        print(f"   Governance: {scores.get('g_score')}")
        print(f"   Overall: {scores.get('overall_score')}")
        print(f"   Confidence: {scores.get('confidence')}")
        
        # Test risk detection
        risk_texts = [
            "Environmental pollution incident at factory",
            "Lawsuit filed over workplace discrimination",
            "Fraud investigation launched by regulators"
        ]
        risks = analyzer.detect_esg_risks(risk_texts)
        print(f"\n⚠️  Risk Detection:")
        print(f"   Risks detected: {len(risks)}")
        for i, risk in enumerate(risks[:3], 1):
            print(f"   {i}. [{risk['severity'].upper()}] {risk['category']}: {risk['text'][:50]}...")
        
        print("\n✅ All ML Analyzer tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ ML Analyzer test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_data_collector():
    """Test data collector functionality"""
    print("\n" + "="*60)
    print("Testing Data Collector")
    print("="*60)
    
    try:
        from backend.services.data_collector import get_data_collector
        
        collector = get_data_collector()
        print("✅ Data Collector initialized")
        
        # Test data collection (limited to avoid long waits)
        print("\n🔍 Collecting sample data for 'Tesla'...")
        data = collector.collect_company_data("Tesla", max_articles=5)
        
        print(f"   Company: {data.get('company_name')}")
        print(f"   News articles: {len(data.get('news_articles', []))}")
        print(f"   ESG mentions: {len(data.get('esg_mentions', []))}")
        print(f"   Sources: {len(data.get('sources', []))}")
        
        if data.get('news_articles'):
            print(f"\n   Sample article:")
            article = data['news_articles'][0]
            print(f"     Title: {article.get('title', 'N/A')[:60]}...")
            print(f"     Source: {article.get('source', 'N/A')}")
        
        # Test text aggregation
        texts = collector.aggregate_text_for_analysis(data)
        print(f"\n📝 Text Aggregation:")
        print(f"   Total texts extracted: {len(texts)}")
        if texts:
            print(f"   Sample: {texts[0][:60]}...")
        
        print("\n✅ All Data Collector tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Data Collector test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_nlp_pipeline():
    """Test NLP pipeline functionality"""
    print("\n" + "="*60)
    print("Testing NLP Pipeline")
    print("="*60)
    
    try:
        from backend.services.nlp_pipeline import get_nlp_pipeline
        
        pipeline = get_nlp_pipeline()
        print("✅ NLP Pipeline initialized")
        
        # Test quick analysis (limited articles to speed up)
        print("\n🔬 Running quick analysis for 'Microsoft'...")
        analysis = pipeline.analyze_company("Microsoft", max_articles=5)
        
        print(f"\n📊 Analysis Results:")
        print(f"   Company: {analysis.get('company_name')}")
        print(f"   Timestamp: {analysis.get('analysis_timestamp')}")
        
        data_collection = analysis.get('data_collection', {})
        print(f"\n📚 Data Collection:")
        print(f"   Articles collected: {data_collection.get('articles_collected')}")
        print(f"   Texts analyzed: {data_collection.get('total_texts_analyzed')}")
        
        scores = analysis.get('esg_scores', {})
        print(f"\n📈 ESG Scores:")
        print(f"   E: {scores.get('e_score')}")
        print(f"   S: {scores.get('s_score')}")
        print(f"   G: {scores.get('g_score')}")
        print(f"   Overall: {scores.get('overall_score')}")
        
        insights = analysis.get('insights', [])
        print(f"\n💡 Insights ({len(insights)}):")
        for insight in insights[:3]:
            print(f"   • {insight}")
        
        recommendations = analysis.get('recommendations', [])
        print(f"\n🎯 Recommendations ({len(recommendations)}):")
        for rec in recommendations[:3]:
            print(f"   • {rec}")
        
        # Test report generation
        print("\n📄 Generating summary report...")
        report = pipeline.generate_report("Microsoft", format='summary')
        print(f"\n{report}")
        
        print("\n✅ All NLP Pipeline tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ NLP Pipeline test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_database_integration():
    """Test database integration"""
    print("\n" + "="*60)
    print("Testing Database Integration")
    print("="*60)
    
    try:
        from backend.app import create_app, db
        from backend.database.models import Company, ESGScore, Alert
        
        app = create_app()
        
        with app.app_context():
            # Test database connection
            print("✅ Database connected")
            
            # Count records
            company_count = Company.query.count()
            score_count = ESGScore.query.count()
            alert_count = Alert.query.count()
            
            print(f"\n📊 Database Statistics:")
            print(f"   Companies: {company_count}")
            print(f"   ESG Scores: {score_count}")
            print(f"   Alerts: {alert_count}")
            
            # Test creating a test company
            test_company = Company.query.filter_by(name="Test ML Company").first()
            if not test_company:
                test_company = Company(name="Test ML Company", industry="Technology")
                db.session.add(test_company)
                db.session.commit()
                print("\n✅ Test company created")
            else:
                print("\n✅ Test company found")
            
            # Test creating ESG score
            test_score = ESGScore(
                company_id=test_company.id,
                e_score=75.5,
                s_score=68.3,
                g_score=72.1,
                overall_score=71.8
            )
            db.session.add(test_score)
            db.session.commit()
            print("✅ Test ESG score created")
            
            # Test creating alert
            test_alert = Alert(
                company_id=test_company.id,
                message="Test ML alert",
                severity="info",
                is_resolved=False
            )
            db.session.add(test_alert)
            db.session.commit()
            print("✅ Test alert created")
        
        print("\n✅ All Database Integration tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Database Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("\n" + "🌍 "*20)
    print("ESG IMPACT TRACKER - ML FEATURES TEST SUITE")
    print("🌍 "*20 + "\n")
    
    tests = [
        ("ML Analyzer", test_ml_analyzer),
        ("Data Collector", test_data_collector),
        ("NLP Pipeline", test_nlp_pipeline),
        ("Database Integration", test_database_integration),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\n{'='*60}")
        print(f"Running: {test_name}")
        print(f"{'='*60}")
        
        try:
            result = test_func()
            results[test_name] = result
        except Exception as e:
            print(f"❌ Test suite '{test_name}' crashed: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name:.<40} {status}")
    
    passed = sum(1 for r in results.values() if r)
    total = len(results)
    
    print(f"\n{passed}/{total} test suites passed")
    
    if passed == total:
        print("\n🎉 All tests passed! ML features are working correctly.")
        print("\n📚 Next steps:")
        print("   1. Start the server: python backend/app.py")
        print("   2. Try the API examples in API_EXAMPLES.md")
        print("   3. Read ML_FEATURES.md for detailed documentation")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
        print("   Make sure all dependencies are installed:")
        print("   pip install -r requirements.txt")
        return 1


if __name__ == '__main__':
    sys.exit(main())
