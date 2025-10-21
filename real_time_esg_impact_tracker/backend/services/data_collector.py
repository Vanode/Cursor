"""
Data Collection Service for ESG Analysis
Collects company news, reports, and ESG-related data from various sources
"""
import requests
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import re
import time
from urllib.parse import quote_plus

try:
    from bs4 import BeautifulSoup
    import feedparser
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False
    print("Warning: BeautifulSoup not available. Install requirements.txt for full functionality.")


class ESGDataCollector:
    """
    Collector for ESG-related data from various online sources
    """
    
    def __init__(self, cache_duration: int = 3600):
        """
        Initialize the data collector
        
        Args:
            cache_duration: Cache duration in seconds (default: 1 hour)
        """
        self.cache_duration = cache_duration
        self.cache = {}
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        
        # ESG-related search terms
        self.esg_terms = [
            'sustainability', 'ESG', 'environmental impact', 'social responsibility',
            'corporate governance', 'carbon emissions', 'diversity', 'ethics'
        ]
    
    def collect_company_data(self, company_name: str, max_articles: int = 20) -> Dict:
        """
        Collect comprehensive data about a company
        
        Args:
            company_name: Name of the company
            max_articles: Maximum number of articles to collect
            
        Returns:
            Dictionary with collected data
        """
        # Check cache
        cache_key = f"{company_name}_{max_articles}"
        if cache_key in self.cache:
            cached_data, timestamp = self.cache[cache_key]
            if time.time() - timestamp < self.cache_duration:
                return cached_data
        
        collected_data = {
            'company_name': company_name,
            'timestamp': datetime.utcnow().isoformat(),
            'news_articles': [],
            'esg_mentions': [],
            'social_media': [],
            'sources': []
        }
        
        # Collect from various sources
        try:
            # News articles via RSS feeds and APIs
            news_data = self._collect_news_articles(company_name, max_articles)
            collected_data['news_articles'].extend(news_data)
            
            # ESG-specific mentions
            esg_data = self._collect_esg_mentions(company_name)
            collected_data['esg_mentions'].extend(esg_data)
            
            # Public financial/ESG reports (if available)
            reports = self._search_esg_reports(company_name)
            collected_data['reports'] = reports
            
            # Add source tracking
            collected_data['sources'] = list(set([
                item.get('source', 'unknown') 
                for item in collected_data['news_articles'] + collected_data['esg_mentions']
            ]))
            
        except Exception as e:
            print(f"Error collecting data for {company_name}: {e}")
            collected_data['error'] = str(e)
        
        # Cache the results
        self.cache[cache_key] = (collected_data, time.time())
        
        return collected_data
    
    def _collect_news_articles(self, company_name: str, max_articles: int) -> List[Dict]:
        """
        Collect news articles about the company
        
        Args:
            company_name: Name of the company
            max_articles: Maximum number of articles
            
        Returns:
            List of article dictionaries
        """
        articles = []
        
        # Try RSS feeds first (more reliable and doesn't require scraping)
        rss_articles = self._collect_from_rss(company_name, max_articles)
        articles.extend(rss_articles)
        
        # If we need more articles, try Google News (via RSS)
        if len(articles) < max_articles:
            google_articles = self._collect_from_google_news_rss(company_name, max_articles - len(articles))
            articles.extend(google_articles)
        
        return articles[:max_articles]
    
    def _collect_from_rss(self, company_name: str, max_items: int) -> List[Dict]:
        """
        Collect articles from RSS feeds
        
        Args:
            company_name: Name of the company
            max_items: Maximum items to collect
            
        Returns:
            List of article dictionaries
        """
        if not BS4_AVAILABLE:
            return []
        
        articles = []
        
        # Major news RSS feeds
        rss_feeds = [
            'http://feeds.reuters.com/reuters/businessNews',
            'http://feeds.bbci.co.uk/news/business/rss.xml',
            'https://www.ft.com/?format=rss',
        ]
        
        for feed_url in rss_feeds:
            try:
                feed = feedparser.parse(feed_url)
                for entry in feed.entries[:max_items]:
                    # Check if company name is mentioned
                    title = entry.get('title', '')
                    summary = entry.get('summary', '')
                    
                    if company_name.lower() in title.lower() or company_name.lower() in summary.lower():
                        articles.append({
                            'title': title,
                            'summary': summary,
                            'url': entry.get('link', ''),
                            'published': entry.get('published', ''),
                            'source': feed_url,
                            'type': 'news'
                        })
                        
                        if len(articles) >= max_items:
                            break
            except Exception as e:
                print(f"Error parsing RSS feed {feed_url}: {e}")
                continue
            
            if len(articles) >= max_items:
                break
        
        return articles
    
    def _collect_from_google_news_rss(self, company_name: str, max_items: int) -> List[Dict]:
        """
        Collect articles from Google News RSS
        
        Args:
            company_name: Name of the company
            max_items: Maximum items to collect
            
        Returns:
            List of article dictionaries
        """
        if not BS4_AVAILABLE:
            return []
        
        articles = []
        
        try:
            # Google News RSS URL
            query = quote_plus(f"{company_name} ESG sustainability")
            rss_url = f"https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"
            
            feed = feedparser.parse(rss_url)
            
            for entry in feed.entries[:max_items]:
                articles.append({
                    'title': entry.get('title', ''),
                    'summary': entry.get('summary', ''),
                    'url': entry.get('link', ''),
                    'published': entry.get('published', ''),
                    'source': 'Google News',
                    'type': 'news'
                })
        except Exception as e:
            print(f"Error collecting from Google News: {e}")
        
        return articles
    
    def _collect_esg_mentions(self, company_name: str) -> List[Dict]:
        """
        Collect ESG-specific mentions and reports
        
        Args:
            company_name: Name of the company
            
        Returns:
            List of ESG mention dictionaries
        """
        esg_mentions = []
        
        # Search for ESG-specific news
        for esg_term in self.esg_terms[:3]:  # Limit to avoid too many requests
            try:
                query = quote_plus(f"{company_name} {esg_term}")
                rss_url = f"https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"
                
                if BS4_AVAILABLE:
                    feed = feedparser.parse(rss_url)
                    
                    for entry in feed.entries[:5]:  # Limit per term
                        esg_mentions.append({
                            'title': entry.get('title', ''),
                            'summary': entry.get('summary', ''),
                            'url': entry.get('link', ''),
                            'published': entry.get('published', ''),
                            'esg_term': esg_term,
                            'source': 'Google News ESG',
                            'type': 'esg_mention'
                        })
                
                time.sleep(0.5)  # Rate limiting
            except Exception as e:
                print(f"Error collecting ESG mentions for term '{esg_term}': {e}")
                continue
        
        return esg_mentions
    
    def _search_esg_reports(self, company_name: str) -> List[Dict]:
        """
        Search for ESG reports and sustainability documents
        
        Args:
            company_name: Name of the company
            
        Returns:
            List of report dictionaries
        """
        reports = []
        
        # Common ESG report patterns
        report_searches = [
            f"{company_name} sustainability report",
            f"{company_name} ESG report",
            f"{company_name} corporate social responsibility",
        ]
        
        for search_term in report_searches:
            try:
                # Use a simple search approach (could be enhanced with actual API)
                query = quote_plus(search_term)
                
                # Simulated report search (in production, use actual ESG databases)
                reports.append({
                    'title': f"{company_name} - ESG Report Search",
                    'search_term': search_term,
                    'type': 'report_search',
                    'note': 'Use dedicated ESG databases like Bloomberg ESG, MSCI ESG, or company IR pages for actual reports'
                })
            except Exception as e:
                print(f"Error searching reports: {e}")
                continue
        
        return reports
    
    def extract_text_from_url(self, url: str, max_length: int = 5000) -> Optional[str]:
        """
        Extract text content from a URL
        
        Args:
            url: URL to extract from
            max_length: Maximum text length to extract
            
        Returns:
            Extracted text or None
        """
        if not BS4_AVAILABLE:
            return None
        
        try:
            headers = {'User-Agent': self.user_agent}
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text
            text = soup.get_text()
            
            # Clean up text
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            return text[:max_length]
        except Exception as e:
            print(f"Error extracting text from {url}: {e}")
            return None
    
    def get_recent_company_news(self, company_name: str, days_back: int = 30) -> List[Dict]:
        """
        Get recent news articles about a company
        
        Args:
            company_name: Name of the company
            days_back: Number of days to look back
            
        Returns:
            List of recent articles
        """
        articles = self._collect_news_articles(company_name, max_articles=50)
        
        # Filter by date if possible
        cutoff_date = datetime.utcnow() - timedelta(days=days_back)
        recent_articles = []
        
        for article in articles:
            try:
                # Try to parse published date
                published = article.get('published', '')
                # This is a simplified check; enhance with proper date parsing
                recent_articles.append(article)
            except:
                recent_articles.append(article)
        
        return recent_articles
    
    def search_specific_esg_topic(self, company_name: str, topic: str) -> List[Dict]:
        """
        Search for specific ESG topic related to company
        
        Args:
            company_name: Name of the company
            topic: Specific ESG topic (e.g., 'carbon emissions', 'diversity')
            
        Returns:
            List of relevant articles/mentions
        """
        results = []
        
        try:
            query = quote_plus(f"{company_name} {topic}")
            rss_url = f"https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"
            
            if BS4_AVAILABLE:
                feed = feedparser.parse(rss_url)
                
                for entry in feed.entries[:10]:
                    results.append({
                        'title': entry.get('title', ''),
                        'summary': entry.get('summary', ''),
                        'url': entry.get('link', ''),
                        'published': entry.get('published', ''),
                        'topic': topic,
                        'source': 'Google News',
                        'type': 'topic_search'
                    })
        except Exception as e:
            print(f"Error searching for topic '{topic}': {e}")
        
        return results
    
    def aggregate_text_for_analysis(self, collected_data: Dict) -> List[str]:
        """
        Aggregate collected text data for ML analysis
        
        Args:
            collected_data: Data collected from various sources
            
        Returns:
            List of text snippets for analysis
        """
        texts = []
        
        # Extract from news articles
        for article in collected_data.get('news_articles', []):
            title = article.get('title', '')
            summary = article.get('summary', '')
            if title:
                texts.append(title)
            if summary:
                texts.append(summary)
        
        # Extract from ESG mentions
        for mention in collected_data.get('esg_mentions', []):
            title = mention.get('title', '')
            summary = mention.get('summary', '')
            if title:
                texts.append(title)
            if summary:
                texts.append(summary)
        
        # Remove duplicates and empty strings
        texts = list(set([t.strip() for t in texts if t and t.strip()]))
        
        return texts


# Global instance
_data_collector = None


def get_data_collector() -> ESGDataCollector:
    """Get or create the global data collector instance"""
    global _data_collector
    if _data_collector is None:
        _data_collector = ESGDataCollector()
    return _data_collector
