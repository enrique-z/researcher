#!/usr/bin/env python3
"""
Research Service Client - Unified Oxford RAG + Gemini 2.5 Pro Integration
Provides a single interface for accessing Oxford 1100 PDFs knowledge base and Gemini deep research capabilities.
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Union, Any
from pathlib import Path

# Gemini integration
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    logging.warning("Gemini not available - install with: pip install google-generativeai")

# Oxford RAG integration
try:
    import sys
    sys.path.append('PIPELINE_2_DEVELOPMENT')
    from ai_researcher_enhanced.integration.oxford_rag_faiss_connector import create_oxford_faiss_connector, search_oxford_knowledge
    OXFORD_AVAILABLE = True
except ImportError:
    OXFORD_AVAILABLE = False
    logging.warning("Oxford RAG not available - check PIPELINE_2_DEVELOPMENT path")

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ResearchServiceClient:
    """
    Unified client for Oxford RAG knowledge base and Gemini 2.5 Pro deep research.
    
    Provides seamless integration between literature search and AI analysis for
    enhanced experiment information enrichment.
    """
    
    def __init__(self):
        """Initialize the research service client."""
        self.oxford_connector = None
        self.gemini_model = None
        
        # Service availability
        self.oxford_ready = False
        self.gemini_ready = False
        
        # Performance tracking
        self.query_stats = {
            'oxford_queries': 0,
            'gemini_queries': 0,
            'combined_queries': 0,
            'total_response_time_ms': 0
        }
        
        logger.info("🔬 Research Service Client initializing...")
        
        # Initialize services
        self._initialize_oxford_connection()
        self._initialize_gemini_connection()
        
        # Report readiness
        services_ready = []
        if self.oxford_ready:
            services_ready.append("Oxford RAG (1100+ PDFs)")
        if self.gemini_ready:
            services_ready.append("Gemini 2.5 Pro")
            
        if services_ready:
            logger.info(f"✅ Research Service Client ready with: {', '.join(services_ready)}")
        else:
            logger.warning("⚠️ Research Service Client initialized but no services available")
    
    def _initialize_oxford_connection(self):
        """Initialize connection to Oxford RAG system."""
        if not OXFORD_AVAILABLE:
            logger.warning("Oxford RAG not available")
            return
        
        try:
            self.oxford_connector = create_oxford_faiss_connector()
            self.oxford_ready = self.oxford_connector.is_ready
            
            if self.oxford_ready:
                status = self.oxford_connector.get_system_status()
                logger.info(f"✅ Oxford RAG connected: {status['knowledge_base']['total_pdfs']} PDFs, "
                           f"{status['knowledge_base']['total_vectors']} vectors")
            else:
                logger.warning("⚠️ Oxford RAG connector not ready")
                
        except Exception as e:
            logger.error(f"❌ Oxford RAG initialization failed: {e}")
            self.oxford_ready = False
    
    def _initialize_gemini_connection(self):
        """Initialize connection to Gemini 2.5 Pro."""
        if not GEMINI_AVAILABLE:
            logger.warning("Gemini not available")
            return
        
        try:
            api_key = os.getenv('GEMINI_API_KEY')
            if not api_key:
                logger.warning("GEMINI_API_KEY not found")
                return
            
            genai.configure(api_key=api_key)
            self.gemini_model = genai.GenerativeModel('gemini-2.5-pro')
            self.gemini_ready = True
            logger.info("✅ Gemini 2.5 Pro connected")
            
        except Exception as e:
            logger.error(f"❌ Gemini initialization failed: {e}")
            self.gemini_ready = False
    
    def query_literature(self, 
                        query: str, 
                        context: str = "research",
                        k: int = 5,
                        similarity_threshold: float = 0.3) -> Dict[str, Any]:
        """
        Query Oxford literature knowledge base.
        
        Args:
            query: Research query
            context: Context for the query (research, validation, etc.)
            k: Number of results to return
            similarity_threshold: Minimum similarity score
            
        Returns:
            Dict with literature search results
        """
        query_start = datetime.now()
        self.query_stats['oxford_queries'] += 1
        
        result = {
            'query': query,
            'context': context,
            'timestamp': query_start.isoformat(),
            'service': 'oxford_rag',
            'success': False,
            'literature_found': [],
            'summary': '',
            'error': None
        }
        
        try:
            # Search Oxford knowledge base
            search_result = self.oxford_connector.search_knowledge_base(
                query, k=k, similarity_threshold=similarity_threshold
            )
            
            if search_result['success']:
                result['success'] = True
                result['literature_found'] = search_result['results']
                result['search_stats'] = search_result['search_stats']
                
                # Create summary of findings
                if search_result['results']:
                    sources = [r['source'] for r in search_result['results'][:3]]
                    result['summary'] = f"Found {len(search_result['results'])} relevant sources from Oxford knowledge base including: {', '.join(sources)}"
                else:
                    result['summary'] = "No relevant literature found in Oxford knowledge base"
            else:
                result['error'] = search_result.get('error', 'Oxford search failed')
        
        except Exception as e:
            logger.error(f"Literature query failed: {e}")
            result['error'] = str(e)
        
        # Calculate response time
        query_duration = (datetime.now() - query_start).total_seconds() * 1000
        result['response_time_ms'] = query_duration
        self.query_stats['total_response_time_ms'] += query_duration
        
        return result
    
    def deep_research_analysis(self, 
                             topic: str,
                             context: str = "",
                             literature_context: List[Dict] = None,
                             analysis_type: str = "comprehensive",
                             manual_mode: bool = True) -> Dict[str, Any]:
        """
        Perform deep research analysis using Gemini 2.5 Pro.
        
        MANUAL MODE: Prepares content for manual copy/paste to Gemini 2.5 Pro website
        and waits for user input of the response.
        
        Args:
            topic: Research topic to analyze
            context: Additional context for the analysis
            literature_context: Literature findings from Oxford search
            analysis_type: Type of analysis (comprehensive, focused, validation)
            manual_mode: If True, uses manual workflow instead of API calls
            
        Returns:
            Dict with deep research analysis results
        """
        query_start = datetime.now()
        self.query_stats['gemini_queries'] += 1
        
        result = {
            'topic': topic,
            'context': context,
            'analysis_type': analysis_type,
            'timestamp': query_start.isoformat(),
            'service': 'gemini_2.5_pro_manual' if manual_mode else 'gemini_2.5_pro_api',
            'success': False,
            'analysis': '',
            'key_insights': [],
            'recommendations': [],
            'manual_prompt_prepared': '',
            'error': None
        }
        
        try:
            # Construct analysis prompt based on literature context
            literature_summary = ""
            if literature_context:
                literature_summary = "\n\nRELEVANT LITERATURE CONTEXT:\n"
                for i, lit in enumerate(literature_context[:5]):
                    literature_summary += f"{i+1}. {lit.get('source', 'Unknown')}: {lit.get('content', '')[:200]}...\n"
            
            analysis_prompt = f"""Perform a {analysis_type} research analysis on the following topic:

TOPIC: {topic}

CONTEXT: {context}
{literature_summary}

ANALYSIS REQUIREMENTS:
1. Provide comprehensive analysis grounded in the literature context
2. Identify key research gaps and opportunities
3. Suggest specific research directions and methodologies
4. Consider interdisciplinary connections and emerging trends
5. Evaluate feasibility and potential impact

Format your response as:
## Analysis
[Detailed analysis here]

## Key Insights
- [Insight 1]
- [Insight 2]
- [Insight 3]

## Recommendations
- [Recommendation 1]
- [Recommendation 2]
- [Recommendation 3]
"""
            
            if manual_mode:
                # MANUAL MODE: Prepare prompt for copy/paste
                result['manual_prompt_prepared'] = analysis_prompt
                
                # Display instructions to user
                print("\n" + "="*80)
                print("🔴 MANUAL GEMINI 2.5 PRO DEEP RESEARCH REQUIRED")
                print("="*80)
                print("Please follow these steps:")
                print("1. Go to https://aistudio.google.com/app/prompts/new")
                print("2. Copy the prompt below and paste it into Gemini 2.5 Pro:")
                print("3. Wait for Gemini's response")
                print("4. Copy Gemini's complete response")
                print("5. Return here and paste it when prompted")
                print("-"*80)
                print("PROMPT TO COPY:")
                print("-"*80)
                print(analysis_prompt)
                print("-"*80)
                
                # Wait for user input
                print("\nAfter getting Gemini's response, paste it here:")
                user_response = input(">>> Paste Gemini's response (press Enter twice when done): ")
                
                # Allow multi-line input
                lines = [user_response]
                while True:
                    try:
                        line = input()
                        if line.strip() == "":
                            break
                        lines.append(line)
                    except EOFError:
                        break
                
                analysis_text = "\n".join(lines)
                
                if analysis_text.strip():
                    result['analysis'] = analysis_text
                    result['success'] = True
                    
                    # Extract key insights and recommendations
                    result['key_insights'] = self._extract_section(analysis_text, "Key Insights")
                    result['recommendations'] = self._extract_section(analysis_text, "Recommendations")
                    
                    logger.info(f"✅ Manual deep research analysis completed for: {topic[:50]}...")
                    print("✅ Gemini response processed successfully!")
                else:
                    result['error'] = 'No response provided by user'
                    print("❌ No response provided - skipping Gemini analysis")
            
            else:
                # AUTOMATED MODE: Use API if available (fallback)
                if not self.gemini_ready:
                    result['error'] = 'Gemini 2.5 Pro API not available and manual mode disabled'
                    return result
                
                # Generate analysis using Gemini API
                response = self.gemini_model.generate_content(
                    analysis_prompt,
                    generation_config={
                        'temperature': 0.3,
                        'max_output_tokens': 3000,
                    }
                )
                
                analysis_text = response.text
                result['analysis'] = analysis_text
                result['success'] = True
                
                # Extract key insights and recommendations
                result['key_insights'] = self._extract_section(analysis_text, "Key Insights")
                result['recommendations'] = self._extract_section(analysis_text, "Recommendations")
                
                logger.info(f"✅ Automated deep research analysis completed for: {topic[:50]}...")
            
        except Exception as e:
            logger.error(f"Deep research analysis failed: {e}")
            result['error'] = str(e)
        
        # Calculate response time
        query_duration = (datetime.now() - query_start).total_seconds() * 1000
        result['response_time_ms'] = query_duration
        self.query_stats['total_response_time_ms'] += query_duration
        
        return result
    
    def combined_research_query(self, 
                              query: str, 
                              context: str = "research",
                              analysis_type: str = "comprehensive",
                              manual_mode: bool = True) -> Dict[str, Any]:
        """
        Perform combined Oxford literature search + Gemini deep analysis.
        
        Args:
            query: Research query
            context: Context for the research
            analysis_type: Type of analysis to perform
            manual_mode: If True, uses manual Gemini workflow instead of API calls
            
        Returns:
            Dict with combined research results
        """
        query_start = datetime.now()
        self.query_stats['combined_queries'] += 1
        
        combined_result = {
            'query': query,
            'context': context,
            'timestamp': query_start.isoformat(),
            'service': 'combined_oxford_gemini',
            'success': False,
            'literature_search': {},
            'deep_analysis': {},
            'synthesis': {},
            'error': None
        }
        
        try:
            # Step 1: Search Oxford literature
            logger.info(f"🔍 Searching Oxford literature for: {query[:50]}...")
            literature_result = self.query_literature(query, context)
            combined_result['literature_search'] = literature_result
            
            if not literature_result['success']:
                logger.warning(f"Oxford search failed: {literature_result.get('error')}")
            
            # Step 2: Perform Gemini deep analysis with literature context
            logger.info(f"🧠 Performing deep analysis with Gemini 2.5 Pro...")
            analysis_result = self.deep_research_analysis(
                topic=query,
                context=context,
                literature_context=literature_result.get('literature_found', []),
                analysis_type=analysis_type,
                manual_mode=manual_mode
            )
            combined_result['deep_analysis'] = analysis_result
            
            if not analysis_result['success']:
                logger.warning(f"Gemini analysis failed: {analysis_result.get('error')}")
            
            # Step 3: Create synthesis
            synthesis = self._create_synthesis(literature_result, analysis_result)
            combined_result['synthesis'] = synthesis
            
            # Mark as successful if either service worked
            combined_result['success'] = literature_result['success'] or analysis_result['success']
            
            if combined_result['success']:
                logger.info(f"✅ Combined research query completed successfully")
            else:
                combined_result['error'] = "Both Oxford and Gemini services failed"
                
        except Exception as e:
            logger.error(f"Combined research query failed: {e}")
            combined_result['error'] = str(e)
        
        # Calculate total response time
        query_duration = (datetime.now() - query_start).total_seconds() * 1000
        combined_result['response_time_ms'] = query_duration
        
        return combined_result
    
    def _extract_section(self, text: str, section_name: str) -> List[str]:
        """Extract bullet points from a section in the analysis."""
        lines = text.split('\n')
        in_section = False
        items = []
        
        for line in lines:
            if f"## {section_name}" in line or f"# {section_name}" in line:
                in_section = True
                continue
            elif line.startswith('##') or line.startswith('#'):
                in_section = False
            elif in_section and line.strip().startswith('-'):
                items.append(line.strip()[1:].strip())
        
        return items
    
    def _create_synthesis(self, literature_result: Dict, analysis_result: Dict) -> Dict[str, Any]:
        """Create synthesis of literature search and deep analysis results."""
        synthesis = {
            'literature_sources_count': 0,
            'analysis_quality': 'unknown',
            'combined_insights': [],
            'research_directions': [],
            'confidence_score': 0.0
        }
        
        # Literature synthesis
        if literature_result.get('success'):
            synthesis['literature_sources_count'] = len(literature_result.get('literature_found', []))
        
        # Analysis synthesis
        if analysis_result.get('success'):
            synthesis['analysis_quality'] = 'high' if analysis_result.get('analysis') else 'low'
            synthesis['combined_insights'] = analysis_result.get('key_insights', [])
            synthesis['research_directions'] = analysis_result.get('recommendations', [])
        
        # Calculate confidence score
        confidence = 0.0
        if literature_result.get('success'):
            confidence += 0.5
        if analysis_result.get('success'):
            confidence += 0.5
        
        synthesis['confidence_score'] = confidence
        
        return synthesis
    
    def get_service_status(self) -> Dict[str, Any]:
        """Get status of all research services."""
        return {
            'research_service_client': {
                'oxford_rag': {
                    'available': self.oxford_ready,
                    'status': 'READY' if self.oxford_ready else 'NOT_AVAILABLE',
                    'knowledge_base': '1100+ PDFs' if self.oxford_ready else 'N/A'
                },
                'gemini_2_5_pro': {
                    'available': self.gemini_ready,
                    'status': 'READY' if self.gemini_ready else 'NOT_AVAILABLE',
                    'model': 'gemini-2.5-pro' if self.gemini_ready else 'N/A'
                },
                'query_statistics': self.query_stats.copy(),
                'average_response_time_ms': (
                    self.query_stats['total_response_time_ms'] / 
                    max(1, sum([self.query_stats['oxford_queries'], 
                               self.query_stats['gemini_queries'], 
                               self.query_stats['combined_queries']]))
                )
            }
        }


# Convenience functions for easy integration
def create_research_service_client() -> ResearchServiceClient:
    """Create a research service client instance."""
    return ResearchServiceClient()

def quick_literature_search(query: str, k: int = 5) -> Dict[str, Any]:
    """Quick function to search Oxford literature."""
    client = create_research_service_client()
    return client.query_literature(query, k=k)

def quick_deep_analysis(topic: str, context: str = "") -> Dict[str, Any]:
    """Quick function for Gemini deep analysis."""
    client = create_research_service_client()
    return client.deep_research_analysis(topic, context)

def quick_combined_research(query: str, context: str = "research", manual_mode: bool = True) -> Dict[str, Any]:
    """Quick function for combined Oxford + Gemini research."""
    client = create_research_service_client()
    return client.combined_research_query(query, context, manual_mode=manual_mode)


if __name__ == "__main__":
    # Test the research service client
    print("🧪 Testing Research Service Client...")
    
    client = create_research_service_client()
    status = client.get_service_status()
    
    print(f"Service Status: {json.dumps(status, indent=2)}")
    
    # Test literature search if Oxford is available
    if client.oxford_ready:
        print("\n🔍 Testing Oxford literature search...")
        result = client.query_literature("climate modeling validation techniques")
        print(f"Literature search results: {len(result.get('literature_found', []))} sources found")
    
    # Test Gemini analysis if available
    if client.gemini_ready:
        print("\n🧠 Testing Gemini deep analysis...")
        result = client.deep_research_analysis("machine learning applications in climate science")
        print(f"Deep analysis completed: {result['success']}")
    
    # Test combined research if both are available
    if client.oxford_ready and client.gemini_ready:
        print("\n🚀 Testing combined research...")
        result = client.combined_research_query("stratospheric aerosol injection modeling")
        print(f"Combined research completed: {result['success']}")
    
    print("✅ Testing completed!")