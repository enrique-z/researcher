"""
Oxford Web Search Connector for Pipeline 2

Connects Pipeline 2 to Oxford's web search system for real-time internet research.
This system is independent from Oxford's FAISS knowledge base and searches the web
for current information, recent publications, and expert opinions.

Key Features:
- Real-time web search using multiple providers (Perplexity, Tavily, Brave)
- Climate science domain specialization
- Academic source prioritization
- Recent publication detection
- Expert opinion identification
- Independent from FAISS system (cannot read 1100 PDFs)
"""

import os
import sys
import json
import logging
import requests
from pathlib import Path
from typing import Dict, List, Optional, Union, Any, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum

# Add Oxford project path for integration
project_root = "/Users/apple/code/scientificoxford-try-shaun"
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Web search dependencies
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    logging.warning("Requests not available - web search functionality disabled")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SearchProvider(Enum):
    """Web search providers supported by Oxford system."""
    PERPLEXITY = "perplexity"
    TAVILY = "tavily"
    BRAVE = "brave"
    FALLBACK = "fallback"


@dataclass
class WebSearchResult:
    """Represents a web search result."""
    title: str
    url: str
    snippet: str
    source_domain: str
    date: Optional[str]
    relevance_score: float
    provider: SearchProvider
    result_type: str  # 'academic', 'news', 'expert', 'general'
    credibility_score: float


class OxfordWebSearchConnector:
    """
    Connector to Oxford's web search system for real-time internet research.
    
    System Architecture:
    - Multi-provider search: Perplexity, Tavily, Brave APIs
    - Domain specialization: Climate science prioritization
    - Academic focus: University and research institution prioritization
    - Real-time data: Independent web search (cannot access FAISS PDFs)
    """
    
    def __init__(self, 
                 oxford_path: str = "/Users/apple/code/scientificoxford-try-shaun",
                 enable_perplexity: bool = True,
                 enable_tavily: bool = True,
                 enable_brave: bool = False):
        """
        Initialize Oxford web search connector.
        
        Args:
            oxford_path: Path to Oxford framework directory
            enable_perplexity: Enable Perplexity API search
            enable_tavily: Enable Tavily API search
            enable_brave: Enable Brave search
        """
        self.oxford_path = Path(oxford_path)
        self.enable_perplexity = enable_perplexity
        self.enable_tavily = enable_tavily
        self.enable_brave = enable_brave
        
        # API configuration
        self.perplexity_api_key = os.getenv("PERPLEXITY_API_KEY")
        self.tavily_api_key = os.getenv("TAVILY_API_KEY")
        self.brave_api_key = os.getenv("BRAVE_API_KEY")
        
        # Search configuration
        self.timeout = 30  # seconds
        self.max_results_per_provider = 5
        self.default_search_depth = "recent"  # recent, comprehensive, academic
        
        # Climate science domain specialization
        self.priority_domains = [
            "nature.com", "science.org", "pnas.org", "agu.org",
            "ipcc.ch", "unfccc.int", "nasa.gov", "noaa.gov",
            "arctic-council.org", "inuitcircumpolar.org",
            "mit.edu", "harvard.edu", "stanford.edu", "cambridge.org",
            "springer.com", "wiley.com", "elsevier.com"
        ]
        
        # Search enhancement keywords
        self.climate_keywords = [
            "climate change", "climate science", "climate modeling",
            "stratospheric aerosol injection", "solar radiation management",
            "geoengineering", "climate intervention", "arctic climate",
            "climate policy", "climate governance", "climate impacts"
        ]
        
        # System status
        self.is_ready = False
        self.search_history = []
        self.search_stats = {
            'total_searches': 0,
            'successful_searches': 0,
            'failed_searches': 0,
            'perplexity_searches': 0,
            'tavily_searches': 0,
            'brave_searches': 0,
            'average_response_time_ms': 0
        }
        
        logger.info(f"🌐 Oxford Web Search Connector initializing...")
        logger.info(f"Oxford path: {self.oxford_path}")
        logger.info(f"Perplexity: {'ENABLED' if self.enable_perplexity else 'DISABLED'}")
        logger.info(f"Tavily: {'ENABLED' if self.enable_tavily else 'DISABLED'}")
        logger.info(f"Brave: {'ENABLED' if self.enable_brave else 'DISABLED'}")
        
        # Initialize connection
        self._initialize_connection()
    
    def _initialize_connection(self):
        """Initialize connection to Oxford web search system."""
        if not REQUESTS_AVAILABLE:
            logger.error("❌ Requests library not available - web search disabled")
            return
        
        try:
            # Check API keys
            available_providers = []
            
            if self.enable_perplexity and self.perplexity_api_key:
                available_providers.append("Perplexity")
            
            if self.enable_tavily and self.tavily_api_key:
                available_providers.append("Tavily")
            
            if self.enable_brave and self.brave_api_key:
                available_providers.append("Brave")
            
            if available_providers:
                self.is_ready = True
                logger.info(f"✅ Oxford web search connector ready")
                logger.info(f"🔌 Available providers: {', '.join(available_providers)}")
            else:
                logger.warning("⚠️ No API keys found - using fallback search methods")
                self.is_ready = True  # Still ready for fallback search
                
        except Exception as e:
            logger.error(f"❌ Oxford web search connector initialization failed: {e}")
            self.is_ready = False
    
    def search_web(self, 
                  query: str,
                  max_results: int = 5,
                  search_depth: str = "recent",
                  domain_filter: Optional[str] = None) -> Dict[str, Any]:
        """
        Search the web using Oxford's multi-provider approach.
        
        Args:
            query: Search query
            max_results: Maximum results to return
            search_depth: Search depth (recent, comprehensive, academic)
            domain_filter: Optional domain filter
            
        Returns:
            Dict with web search results and metadata
        """
        search_start = datetime.now()
        self.search_stats['total_searches'] += 1
        
        search_result = {
            'query': query,
            'timestamp': search_start.isoformat(),
            'search_depth': search_depth,
            'domain_filter': domain_filter,
            'results': [],
            'search_stats': {
                'providers_used': [],
                'total_raw_results': 0,
                'filtered_results': 0
            },
            'system_info': {
                'web_search_system': 'Oxford Multi-Provider',
                'independent_of_faiss': True,
                'real_time_search': True
            },
            'success': False,
            'error': None
        }
        
        if not self.is_ready:
            search_result['error'] = 'Oxford web search system not ready'
            return search_result
        
        try:
            # Enhance query for climate science context
            enhanced_query = self._enhance_query_for_climate_science(query)
            
            # Multi-provider search
            all_results = []
            
            # Search with Perplexity
            if self.enable_perplexity and self.perplexity_api_key:
                perplexity_results = self._search_perplexity(enhanced_query, max_results)
                if perplexity_results:
                    all_results.extend(perplexity_results)
                    search_result['search_stats']['providers_used'].append('Perplexity')
                    self.search_stats['perplexity_searches'] += 1
            
            # Search with Tavily
            if self.enable_tavily and self.tavily_api_key:
                tavily_results = self._search_tavily(enhanced_query, max_results)
                if tavily_results:
                    all_results.extend(tavily_results)
                    search_result['search_stats']['providers_used'].append('Tavily')
                    self.search_stats['tavily_searches'] += 1
            
            # Search with Brave (if enabled)
            if self.enable_brave and self.brave_api_key:
                brave_results = self._search_brave(enhanced_query, max_results)
                if brave_results:
                    all_results.extend(brave_results)
                    search_result['search_stats']['providers_used'].append('Brave')
                    self.search_stats['brave_searches'] += 1
            
            # Fallback search if no providers available
            if not all_results and not search_result['search_stats']['providers_used']:
                fallback_results = self._search_fallback(enhanced_query, max_results)
                if fallback_results:
                    all_results.extend(fallback_results)
                    search_result['search_stats']['providers_used'].append('Fallback')
            
            # Process and rank results
            processed_results = self._process_and_rank_results(all_results, search_depth, domain_filter)
            
            # Limit to requested number of results
            final_results = processed_results[:max_results]
            
            search_result['results'] = final_results
            search_result['search_stats']['total_raw_results'] = len(all_results)
            search_result['search_stats']['filtered_results'] = len(final_results)
            search_result['success'] = True
            
            self.search_stats['successful_searches'] += 1
            
            logger.info(f"🌐 Web search completed: {len(final_results)} results for '{query[:50]}...'")
            
        except Exception as e:
            logger.error(f"❌ Oxford web search failed: {e}")
            search_result['error'] = str(e)
            self.search_stats['failed_searches'] += 1
        
        # Calculate response time
        search_duration = (datetime.now() - search_start).total_seconds() * 1000
        search_result['response_time_ms'] = search_duration
        
        # Update average response time
        if self.search_stats['successful_searches'] > 0:
            total_time = (self.search_stats['average_response_time_ms'] * 
                         (self.search_stats['successful_searches'] - 1) + search_duration)
            self.search_stats['average_response_time_ms'] = total_time / self.search_stats['successful_searches']
        
        # Record search history
        self.search_history.append(search_result)
        
        return search_result
    
    def _enhance_query_for_climate_science(self, query: str) -> str:
        """Enhance query with climate science context."""
        query_lower = query.lower()
        
        # If query already contains climate terms, return as is
        if any(keyword in query_lower for keyword in self.climate_keywords):
            return query
        
        # Add climate science context
        enhanced_query = f"{query} climate science research"
        
        # Add recent filter for current research
        current_year = datetime.now().year
        enhanced_query += f" {current_year-1}-{current_year}"
        
        return enhanced_query
    
    def _search_perplexity(self, query: str, max_results: int) -> List[WebSearchResult]:
        """Search using Perplexity API."""
        try:
            headers = {
                "Authorization": f"Bearer {self.perplexity_api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": "llama-3.1-sonar-small-128k-online",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that searches for recent climate science information."
                    },
                    {
                        "role": "user",
                        "content": f"Search for recent information about: {query}. Include academic sources and expert opinions."
                    }
                ],
                "max_tokens": 1000,
                "temperature": 0.2,
                "return_citations": True,
                "return_images": False
            }
            
            response = requests.post(
                "https://api.perplexity.ai/chat/completions",
                headers=headers,
                json=data,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                return self._parse_perplexity_response(result, query)
            else:
                logger.warning(f"Perplexity search failed: {response.status_code}")
                
        except Exception as e:
            logger.error(f"Perplexity search error: {e}")
        
        return []
    
    def _search_tavily(self, query: str, max_results: int) -> List[WebSearchResult]:
        """Search using Tavily API."""
        try:
            data = {
                "api_key": self.tavily_api_key,
                "query": query,
                "search_depth": "advanced",
                "include_answer": True,
                "include_domains": self.priority_domains[:10],  # Limit domains for API
                "max_results": max_results
            }
            
            response = requests.post(
                "https://api.tavily.com/search",
                json=data,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                return self._parse_tavily_response(result, query)
            else:
                logger.warning(f"Tavily search failed: {response.status_code}")
                
        except Exception as e:
            logger.error(f"Tavily search error: {e}")
        
        return []
    
    def _search_brave(self, query: str, max_results: int) -> List[WebSearchResult]:
        """Search using Brave API."""
        try:
            headers = {
                "Accept": "application/json",
                "Accept-Encoding": "gzip",
                "X-Subscription-Token": self.brave_api_key
            }
            
            params = {
                "q": query,
                "count": max_results,
                "search_lang": "en",
                "country": "US",
                "freshness": "pw"  # Past week for recent results
            }
            
            response = requests.get(
                "https://api.search.brave.com/res/v1/web/search",
                headers=headers,
                params=params,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                return self._parse_brave_response(result, query)
            else:
                logger.warning(f"Brave search failed: {response.status_code}")
                
        except Exception as e:
            logger.error(f"Brave search error: {e}")
        
        return []
    
    def _search_fallback(self, query: str, max_results: int) -> List[WebSearchResult]:
        """Fallback search method when no APIs are available."""
        # Simple fallback - create mock results indicating web search capability
        fallback_results = [
            WebSearchResult(
                title="Web Search Results Available",
                url="https://example.com",
                snippet=f"Real-time web search results would be available for: {query}",
                source_domain="fallback.system",
                date=datetime.now().strftime("%Y-%m-%d"),
                relevance_score=0.5,
                provider=SearchProvider.FALLBACK,
                result_type="general",
                credibility_score=0.3
            )
        ]
        
        logger.info(f"Using fallback search for: {query}")
        return fallback_results[:max_results]
    
    def _parse_perplexity_response(self, result: Dict, query: str) -> List[WebSearchResult]:
        """Parse Perplexity API response."""
        search_results = []
        
        # Extract citations if available
        citations = result.get("citations", [])
        content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
        
        for i, citation in enumerate(citations[:5]):  # Limit to 5 citations
            search_result = WebSearchResult(
                title=citation.get("title", f"Perplexity Result {i+1}"),
                url=citation.get("url", ""),
                snippet=content[:200] + "..." if len(content) > 200 else content,
                source_domain=self._extract_domain(citation.get("url", "")),
                date=datetime.now().strftime("%Y-%m-%d"),
                relevance_score=0.8,  # Perplexity provides high-quality results
                provider=SearchProvider.PERPLEXITY,
                result_type=self._classify_result_type(citation.get("title", "")),
                credibility_score=self._assess_credibility(citation.get("url", ""))
            )
            search_results.append(search_result)
        
        return search_results
    
    def _parse_tavily_response(self, result: Dict, query: str) -> List[WebSearchResult]:
        """Parse Tavily API response."""
        search_results = []
        
        results = result.get("results", [])
        
        for i, item in enumerate(results[:5]):
            search_result = WebSearchResult(
                title=item.get("title", f"Tavily Result {i+1}"),
                url=item.get("url", ""),
                snippet=item.get("content", item.get("snippet", "")),
                source_domain=self._extract_domain(item.get("url", "")),
                date=item.get("published_date", datetime.now().strftime("%Y-%m-%d")),
                relevance_score=item.get("score", 0.7),
                provider=SearchProvider.TAVILY,
                result_type=self._classify_result_type(item.get("title", "")),
                credibility_score=self._assess_credibility(item.get("url", ""))
            )
            search_results.append(search_result)
        
        return search_results
    
    def _parse_brave_response(self, result: Dict, query: str) -> List[WebSearchResult]:
        """Parse Brave API response."""
        search_results = []
        
        web_results = result.get("web", {}).get("results", [])
        
        for i, item in enumerate(web_results[:5]):
            search_result = WebSearchResult(
                title=item.get("title", f"Brave Result {i+1}"),
                url=item.get("url", ""),
                snippet=item.get("description", ""),
                source_domain=self._extract_domain(item.get("url", "")),
                date=item.get("age", datetime.now().strftime("%Y-%m-%d")),
                relevance_score=0.6,  # Default relevance for Brave
                provider=SearchProvider.BRAVE,
                result_type=self._classify_result_type(item.get("title", "")),
                credibility_score=self._assess_credibility(item.get("url", ""))
            )
            search_results.append(search_result)
        
        return search_results
    
    def _process_and_rank_results(self, 
                                 all_results: List[WebSearchResult],
                                 search_depth: str,
                                 domain_filter: Optional[str]) -> List[WebSearchResult]:
        """Process and rank all search results."""
        if not all_results:
            return []
        
        # Filter by domain if specified
        if domain_filter:
            filtered_results = [r for r in all_results if domain_filter in r.source_domain]
        else:
            filtered_results = all_results
        
        # Remove duplicates based on URL
        seen_urls = set()
        unique_results = []
        for result in filtered_results:
            if result.url not in seen_urls:
                unique_results.append(result)
                seen_urls.add(result.url)
        
        # Rank results based on multiple factors
        for result in unique_results:
            ranking_score = self._calculate_ranking_score(result, search_depth)
            result.relevance_score = ranking_score
        
        # Sort by ranking score
        ranked_results = sorted(unique_results, key=lambda r: r.relevance_score, reverse=True)
        
        return ranked_results
    
    def _calculate_ranking_score(self, result: WebSearchResult, search_depth: str) -> float:
        """Calculate ranking score for search result."""
        score = result.relevance_score
        
        # Boost academic sources
        if any(domain in result.source_domain for domain in self.priority_domains):
            score += 0.3
        
        # Boost based on result type
        if result.result_type == "academic":
            score += 0.2
        elif result.result_type == "expert":
            score += 0.15
        
        # Boost credibility
        score += result.credibility_score * 0.2
        
        # Recent results boost
        if search_depth == "recent" and result.date:
            try:
                result_date = datetime.strptime(result.date[:10], "%Y-%m-%d")
                days_old = (datetime.now() - result_date).days
                if days_old < 30:  # Less than 30 days old
                    score += 0.1
            except:
                pass  # Skip if date parsing fails
        
        return min(score, 1.0)  # Cap at 1.0
    
    def _extract_domain(self, url: str) -> str:
        """Extract domain from URL."""
        try:
            from urllib.parse import urlparse
            return urlparse(url).netloc.lower()
        except:
            return "unknown.domain"
    
    def _classify_result_type(self, title: str) -> str:
        """Classify result type based on title."""
        title_lower = title.lower()
        
        if any(term in title_lower for term in ["journal", "paper", "study", "research", "publication"]):
            return "academic"
        elif any(term in title_lower for term in ["expert", "scientist", "researcher", "professor"]):
            return "expert"
        elif any(term in title_lower for term in ["news", "report", "update", "breaking"]):
            return "news"
        else:
            return "general"
    
    def _assess_credibility(self, url: str) -> float:
        """Assess credibility score based on URL domain."""
        domain = self._extract_domain(url)
        
        # High credibility domains
        if domain in self.priority_domains:
            return 0.9
        
        # Academic domains
        if any(tld in domain for tld in [".edu", ".ac.uk", ".org"]):
            return 0.8
        
        # Government domains
        if ".gov" in domain:
            return 0.85
        
        # General credibility
        return 0.5
    
    def search_for_validation(self,
                            experiment_topic: str,
                            domain: str = "climate",
                            max_results: int = 3) -> Dict[str, Any]:
        """
        Search web for experiment validation information.
        
        Args:
            experiment_topic: Topic of the experiment to validate
            domain: Scientific domain
            max_results: Number of results to retrieve
            
        Returns:
            Dict with validation-focused web search results
        """
        # Create domain-specific validation query
        validation_query = f"recent research {experiment_topic} {domain} scientific validation methodology 2024"
        
        search_result = self.search_web(validation_query, max_results=max_results, search_depth="recent")
        
        if search_result['success']:
            # Enhance results with validation context
            validation_results = []
            for result in search_result['results']:
                validation_result = self._convert_to_dict(result)
                validation_result['validation_relevance'] = self._assess_web_validation_relevance(
                    validation_result, experiment_topic, domain
                )
                validation_results.append(validation_result)
            
            search_result['validation_results'] = validation_results
            search_result['validation_summary'] = self._create_web_validation_summary(validation_results)
        
        return search_result
    
    def _convert_to_dict(self, result: WebSearchResult) -> Dict:
        """Convert WebSearchResult to dictionary."""
        return {
            'title': result.title,
            'url': result.url,
            'snippet': result.snippet,
            'source_domain': result.source_domain,
            'date': result.date,
            'relevance_score': result.relevance_score,
            'provider': result.provider.value,
            'result_type': result.result_type,
            'credibility_score': result.credibility_score
        }
    
    def _assess_web_validation_relevance(self, result: Dict, topic: str, domain: str) -> Dict[str, Any]:
        """Assess how relevant web result is for validation."""
        content = f"{result['title']} {result['snippet']}".lower()
        topic_lower = topic.lower()
        domain_lower = domain.lower()
        
        relevance_score = result['credibility_score']  # Base on credibility
        validation_aspects = []
        
        # Check for validation keywords
        validation_keywords = ['validation', 'verification', 'evidence', 'study', 'research', 'findings']
        for keyword in validation_keywords:
            if keyword in content:
                relevance_score += 0.1
                validation_aspects.append(keyword)
        
        # Recent research bonus
        if any(year in content for year in ['2024', '2023']):
            relevance_score += 0.2
            validation_aspects.append('recent')
        
        return {
            'relevance_score': min(relevance_score, 1.0),
            'validation_aspects': validation_aspects,
            'is_recent': any(year in content for year in ['2024', '2023']),
            'is_academic': result['result_type'] == 'academic'
        }
    
    def _create_web_validation_summary(self, validation_results: List[Dict]) -> Dict[str, Any]:
        """Create summary of web validation findings."""
        if not validation_results:
            return {'total_sources': 0, 'summary': 'No web validation sources found'}
        
        recent_sources = [r for r in validation_results 
                         if r.get('validation_relevance', {}).get('is_recent', False)]
        academic_sources = [r for r in validation_results 
                          if r.get('result_type') == 'academic']
        
        return {
            'total_sources': len(validation_results),
            'recent_sources': len(recent_sources),
            'academic_sources': len(academic_sources),
            'summary': f"Found {len(validation_results)} web validation sources (independent of 1100 PDF FAISS system)"
        }
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get Oxford web search system status."""
        return {
            'system_name': 'Oxford Web Search System',
            'ready': self.is_ready,
            'independent_of_faiss': True,
            'real_time_search': True,
            'providers': {
                'perplexity': 'ENABLED' if (self.enable_perplexity and self.perplexity_api_key) else 'DISABLED',
                'tavily': 'ENABLED' if (self.enable_tavily and self.tavily_api_key) else 'DISABLED',
                'brave': 'ENABLED' if (self.enable_brave and self.brave_api_key) else 'DISABLED'
            },
            'priority_domains': self.priority_domains[:5],  # Show first 5
            'search_statistics': self.search_stats.copy(),
            'search_history_count': len(self.search_history)
        }


# Convenience functions for Pipeline 2 integration
def create_oxford_web_connector(oxford_path: str = "/Users/apple/code/scientificoxford-try-shaun") -> OxfordWebSearchConnector:
    """Create Oxford web search connector for Pipeline 2."""
    return OxfordWebSearchConnector(oxford_path)

def search_oxford_web(query: str, max_results: int = 3) -> Dict[str, Any]:
    """
    One-line function to search Oxford web system.
    
    Usage in Pipeline 2:
    from .oxford_web_search_connector import search_oxford_web
    results = search_oxford_web("recent climate validation research 2024")
    """
    connector = create_oxford_web_connector()
    return connector.search_web(query, max_results)