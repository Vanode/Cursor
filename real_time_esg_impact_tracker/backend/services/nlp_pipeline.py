"""
NLP Processing Pipeline for ESG Text Analysis
Combines data collection, ML analysis, and report generation
"""
from typing import Dict, List, Optional
from datetime import datetime
import json

from backend.services.data_collector import get_data_collector
from backend.services.ml_analyzer import get_ml_analyzer


class ESGNLPPipeline:
    """
    Complete NLP pipeline for ESG analysis
    """
    
    def __init__(self):
        """Initialize the NLP pipeline"""
        self.data_collector = get_data_collector()
        self.ml_analyzer = get_ml_analyzer()
    
    def analyze_company(self, company_name: str, max_articles: int = 20) -> Dict:
        """
        Complete analysis of a company's ESG performance
        
        Args:
            company_name: Name of the company to analyze
            max_articles: Maximum number of articles to collect
            
        Returns:
            Complete analysis results
        """
        # Step 1: Collect data
        print(f"Collecting data for {company_name}...")
        collected_data = self.data_collector.collect_company_data(company_name, max_articles)
        
        # Step 2: Aggregate text for analysis
        print(f"Aggregating text data...")
        text_data = self.data_collector.aggregate_text_for_analysis(collected_data)
        
        # Step 3: Perform sentiment analysis on each text
        print(f"Analyzing sentiment...")
        sentiment_results = []
        for text in text_data[:50]:  # Limit to prevent overload
            sentiment = self.ml_analyzer.analyze_sentiment(text)
            sentiment_results.append({
                'text': text[:100],  # First 100 chars
                'sentiment': sentiment
            })
        
        # Step 4: Classify ESG categories
        print(f"Classifying ESG categories...")
        category_results = []
        for text in text_data[:50]:
            category = self.ml_analyzer.classify_esg_category(text)
            category_results.append({
                'text': text[:100],
                'category': category
            })
        
        # Step 5: Calculate ESG scores
        print(f"Calculating ESG scores...")
        esg_scores = self.ml_analyzer.calculate_esg_scores(text_data)
        
        # Step 6: Detect risks
        print(f"Detecting risks...")
        risks = self.ml_analyzer.detect_esg_risks(text_data)
        
        # Step 7: Generate insights
        analysis_results = {
            'esg_scores': esg_scores,
            'risks': risks
        }
        insights = self.ml_analyzer.generate_insights(analysis_results)
        
        # Compile complete results
        results = {
            'company_name': company_name,
            'analysis_timestamp': datetime.utcnow().isoformat(),
            'data_collection': {
                'articles_collected': len(collected_data.get('news_articles', [])),
                'esg_mentions': len(collected_data.get('esg_mentions', [])),
                'sources': collected_data.get('sources', []),
                'total_texts_analyzed': len(text_data)
            },
            'sentiment_analysis': {
                'results': sentiment_results[:10],  # Top 10 for brevity
                'summary': self._summarize_sentiments(sentiment_results)
            },
            'category_classification': {
                'results': category_results[:10],  # Top 10 for brevity
                'distribution': self._get_category_distribution(category_results)
            },
            'esg_scores': esg_scores,
            'risks': risks[:10],  # Top 10 risks
            'insights': insights,
            'recommendations': self._generate_recommendations(esg_scores, risks),
            'raw_data': {
                'news_articles': collected_data.get('news_articles', [])[:5],  # Sample
                'esg_mentions': collected_data.get('esg_mentions', [])[:5]  # Sample
            }
        }
        
        return results
    
    def analyze_specific_aspect(self, company_name: str, aspect: str) -> Dict:
        """
        Analyze a specific ESG aspect for a company
        
        Args:
            company_name: Name of the company
            aspect: Specific aspect to analyze (e.g., 'environmental', 'carbon emissions')
            
        Returns:
            Analysis results for the specific aspect
        """
        # Collect data specific to the aspect
        results = self.data_collector.search_specific_esg_topic(company_name, aspect)
        
        # Extract text
        texts = [r.get('title', '') + ' ' + r.get('summary', '') for r in results]
        
        # Analyze
        sentiments = [self.ml_analyzer.analyze_sentiment(t) for t in texts if t.strip()]
        categories = [self.ml_analyzer.classify_esg_category(t) for t in texts if t.strip()]
        
        return {
            'company_name': company_name,
            'aspect': aspect,
            'timestamp': datetime.utcnow().isoformat(),
            'articles_found': len(results),
            'sentiment_summary': self._summarize_sentiments(
                [{'sentiment': s} for s in sentiments]
            ),
            'category_distribution': self._get_category_distribution(
                [{'category': c} for c in categories]
            ),
            'articles': results[:10]  # Top 10
        }
    
    def compare_companies(self, company_names: List[str]) -> Dict:
        """
        Compare ESG performance across multiple companies
        
        Args:
            company_names: List of company names to compare
            
        Returns:
            Comparative analysis results
        """
        comparisons = {}
        
        for company in company_names:
            # Quick analysis for each company
            analysis = self.analyze_company(company, max_articles=10)
            comparisons[company] = {
                'esg_scores': analysis.get('esg_scores', {}),
                'risk_count': len(analysis.get('risks', [])),
                'sentiment_summary': analysis.get('sentiment_analysis', {}).get('summary', {}),
                'insights': analysis.get('insights', [])
            }
        
        # Generate comparative insights
        comparative_insights = self._generate_comparative_insights(comparisons)
        
        return {
            'companies': company_names,
            'timestamp': datetime.utcnow().isoformat(),
            'individual_analysis': comparisons,
            'comparative_insights': comparative_insights,
            'rankings': self._rank_companies(comparisons)
        }
    
    def _summarize_sentiments(self, sentiment_results: List[Dict]) -> Dict:
        """Summarize sentiment analysis results"""
        if not sentiment_results:
            return {'positive': 0, 'negative': 0, 'neutral': 0, 'average_score': 0.5}
        
        sentiments = [r.get('sentiment', {}) for r in sentiment_results]
        labels = [s.get('label', 'neutral') for s in sentiments]
        scores = [s.get('score', 0.5) for s in sentiments]
        
        return {
            'positive': labels.count('positive'),
            'negative': labels.count('negative'),
            'neutral': labels.count('neutral'),
            'average_score': sum(scores) / len(scores) if scores else 0.5,
            'total_analyzed': len(sentiment_results)
        }
    
    def _get_category_distribution(self, category_results: List[Dict]) -> Dict:
        """Get distribution of ESG categories"""
        if not category_results:
            return {'environmental': 0, 'social': 0, 'governance': 0, 'general': 0}
        
        categories = [r.get('category', {}).get('category', 'general') for r in category_results]
        
        return {
            'environmental': categories.count('environmental'),
            'social': categories.count('social'),
            'governance': categories.count('governance'),
            'general': categories.count('general'),
            'total': len(categories)
        }
    
    def _generate_recommendations(self, esg_scores: Dict, risks: List[Dict]) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        e_score = esg_scores.get('e_score', 50)
        s_score = esg_scores.get('s_score', 50)
        g_score = esg_scores.get('g_score', 50)
        
        # Score-based recommendations
        if e_score < 50:
            recommendations.append("Enhance environmental initiatives and transparent reporting")
        if s_score < 50:
            recommendations.append("Improve social responsibility programs and stakeholder engagement")
        if g_score < 50:
            recommendations.append("Strengthen governance practices and compliance frameworks")
        
        # Risk-based recommendations
        critical_risks = [r for r in risks if r.get('severity') == 'critical']
        if critical_risks:
            recommendations.append(f"Address {len(critical_risks)} critical risk(s) immediately")
        
        high_risks = [r for r in risks if r.get('severity') == 'high']
        if high_risks:
            recommendations.append(f"Develop mitigation plans for {len(high_risks)} high-priority risk(s)")
        
        # General recommendations
        if not recommendations:
            recommendations.append("Maintain current ESG practices and continue monitoring")
        
        return recommendations
    
    def _generate_comparative_insights(self, comparisons: Dict) -> List[str]:
        """Generate insights from company comparisons"""
        insights = []
        
        # Find best performer
        best_overall = max(
            comparisons.keys(),
            key=lambda c: comparisons[c]['esg_scores'].get('overall_score', 0)
        )
        best_score = comparisons[best_overall]['esg_scores'].get('overall_score', 0)
        insights.append(f"{best_overall} leads with overall ESG score of {best_score}")
        
        # Find most environmental
        best_env = max(
            comparisons.keys(),
            key=lambda c: comparisons[c]['esg_scores'].get('e_score', 0)
        )
        insights.append(f"{best_env} has strongest environmental performance")
        
        # Risk comparison
        company_risks = {c: comparisons[c]['risk_count'] for c in comparisons.keys()}
        safest = min(company_risks, key=company_risks.get)
        insights.append(f"{safest} has lowest risk profile with {company_risks[safest]} identified risks")
        
        return insights
    
    def _rank_companies(self, comparisons: Dict) -> List[Dict]:
        """Rank companies by ESG performance"""
        rankings = []
        
        for company, data in comparisons.items():
            overall_score = data['esg_scores'].get('overall_score', 0)
            rankings.append({
                'company': company,
                'overall_score': overall_score,
                'e_score': data['esg_scores'].get('e_score', 0),
                's_score': data['esg_scores'].get('s_score', 0),
                'g_score': data['esg_scores'].get('g_score', 0),
                'risk_count': data['risk_count']
            })
        
        # Sort by overall score descending
        rankings.sort(key=lambda x: x['overall_score'], reverse=True)
        
        # Add rank
        for i, item in enumerate(rankings, 1):
            item['rank'] = i
        
        return rankings
    
    def generate_report(self, company_name: str, format: str = 'json') -> str:
        """
        Generate a comprehensive ESG report
        
        Args:
            company_name: Name of the company
            format: Report format ('json', 'text', 'summary')
            
        Returns:
            Formatted report string
        """
        analysis = self.analyze_company(company_name)
        
        if format == 'json':
            return json.dumps(analysis, indent=2)
        
        elif format == 'text':
            return self._format_text_report(analysis)
        
        elif format == 'summary':
            return self._format_summary_report(analysis)
        
        else:
            return json.dumps(analysis, indent=2)
    
    def _format_text_report(self, analysis: Dict) -> str:
        """Format analysis as text report"""
        company = analysis.get('company_name', 'Unknown')
        timestamp = analysis.get('analysis_timestamp', '')
        scores = analysis.get('esg_scores', {})
        
        report = f"""
ESG ANALYSIS REPORT
{'=' * 50}

Company: {company}
Analysis Date: {timestamp}

ESG SCORES
{'-' * 50}
Environmental Score:  {scores.get('e_score', 'N/A')}/100
Social Score:         {scores.get('s_score', 'N/A')}/100  
Governance Score:     {scores.get('g_score', 'N/A')}/100
Overall Score:        {scores.get('overall_score', 'N/A')}/100
Confidence:           {scores.get('confidence', 'N/A')}

KEY INSIGHTS
{'-' * 50}
"""
        for insight in analysis.get('insights', []):
            report += f"• {insight}\n"
        
        report += f"""
RECOMMENDATIONS
{'-' * 50}
"""
        for rec in analysis.get('recommendations', []):
            report += f"• {rec}\n"
        
        risks = analysis.get('risks', [])
        if risks:
            report += f"""
TOP RISKS IDENTIFIED
{'-' * 50}
"""
            for i, risk in enumerate(risks[:5], 1):
                report += f"{i}. [{risk.get('severity', 'unknown').upper()}] "
                report += f"{risk.get('category', 'general')}: {risk.get('text', 'N/A')[:100]}...\n"
        
        return report
    
    def _format_summary_report(self, analysis: Dict) -> str:
        """Format analysis as brief summary"""
        company = analysis.get('company_name', 'Unknown')
        scores = analysis.get('esg_scores', {})
        overall = scores.get('overall_score', 0)
        
        summary = f"{company} ESG Summary:\n"
        summary += f"Overall Score: {overall}/100\n"
        summary += f"Top Insights:\n"
        
        for insight in analysis.get('insights', [])[:3]:
            summary += f"  • {insight}\n"
        
        return summary


# Global instance
_nlp_pipeline = None


def get_nlp_pipeline() -> ESGNLPPipeline:
    """Get or create the global NLP pipeline instance"""
    global _nlp_pipeline
    if _nlp_pipeline is None:
        _nlp_pipeline = ESGNLPPipeline()
    return _nlp_pipeline
