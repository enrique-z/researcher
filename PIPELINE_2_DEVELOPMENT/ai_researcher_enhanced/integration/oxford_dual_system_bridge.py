"""
Oxford Dual-System Bridge for Pipeline 2

This module provides the bridge between Pipeline 2 and the existing Oxford framework
which consists of two independent systems unified by Solomon prompt:
1. FAISS System: 1100+ PDFs local knowledge base (71,047 vectors)
2. Web Search System: Real-time internet research (cannot read FAISS PDFs)
3. Solomon Prompt: Orchestrates both systems while keeping them independent

Pipeline 2 uses this bridge to enhance validation with both local knowledge (FAISS)
and real-time research (web search) without disrupting Pipeline 1.
"""

import os
import sys
import json
import pickle
import logging
from pathlib import Path
from typing import Dict, List, Optional, Union, Any, Tuple
from datetime import datetime
import numpy as np

# FAISS integration
try:
    import faiss
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False
    logging.warning("FAISS not available - Oxford FAISS system connection disabled")

# Pipeline 2 imports
from ..validation.experiment_validator import ExperimentValidator
from .sakana_bridge import SakanaBridge

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OxfordDualSystemBridge:
    """
    Bridge connecting Pipeline 2 to Oxford's dual-system framework.
    
    Architecture:
    - FAISS System: Local knowledge base with 1100+ climate science PDFs
    - Web Search System: Real-time internet research (independent of FAISS)
    - Solomon Orchestration: Unifies both systems via prompts
    - Pipeline 2 Integration: Enhances validation without Pipeline 1 changes
    """
    
    def __init__(self, 
                 oxford_path: str = "/Users/apple/code/scientificoxford-try-shaun",
                 enable_faiss: bool = True,
                 enable_web_search: bool = True):
        """
        Initialize Oxford dual-system bridge.
        
        Args:
            oxford_path: Path to Oxford framework directory
            enable_faiss: Enable FAISS system connection
            enable_web_search: Enable web search system connection
        """
        self.oxford_path = Path(oxford_path)
        self.enable_faiss = enable_faiss and FAISS_AVAILABLE
        self.enable_web_search = enable_web_search
        
        # System status tracking
        self.faiss_system_ready = False
        self.web_search_system_ready = False
        self.solomon_orchestrator_ready = False
        
        # Connection components
        self.faiss_connector = None
        self.web_search_connector = None
        self.solomon_orchestrator = None
        
        # Integration history
        self.query_history = []
        self.system_stats = {
            'total_queries': 0,
            'faiss_queries': 0,
            'web_search_queries': 0,
            'dual_queries': 0,
            'solomon_orchestrations': 0
        }
        
        logger.info(f"🌉 Oxford Dual-System Bridge initializing...")
        logger.info(f"Oxford path: {self.oxford_path}")
        logger.info(f"FAISS enabled: {self.enable_faiss}")
        logger.info(f"Web Search enabled: {self.enable_web_search}")
        
        # Initialize systems
        self._initialize_systems()
    
    def _initialize_systems(self):
        """Initialize Oxford dual-system components."""
        try:
            # Initialize FAISS system
            if self.enable_faiss:
                self._initialize_faiss_system()
            
            # Initialize web search system
            if self.enable_web_search:
                self._initialize_web_search_system()
            
            # Initialize Solomon orchestrator
            self._initialize_solomon_orchestrator()
            
            logger.info(f"✅ Oxford Dual-System Bridge initialized")
            logger.info(f"FAISS system: {'READY' if self.faiss_system_ready else 'DISABLED'}")
            logger.info(f"Web search system: {'READY' if self.web_search_system_ready else 'DISABLED'}")
            logger.info(f"Solomon orchestrator: {'READY' if self.solomon_orchestrator_ready else 'DISABLED'}")
            
        except Exception as e:
            logger.error(f"❌ Oxford Dual-System Bridge initialization failed: {e}")
    
    def _initialize_faiss_system(self):
        """Initialize connection to Oxford FAISS system (1100+ PDFs)."""
        try:
            # Import FAISS connector
            from .oxford_rag_faiss_connector import OxfordRAGFAISSConnector
            
            self.faiss_connector = OxfordRAGFAISSConnector(self.oxford_path)
            self.faiss_system_ready = True
            
            logger.info("✅ Oxford FAISS system connected (1100+ PDFs)")
            
        except Exception as e:
            logger.error(f"❌ Oxford FAISS system initialization failed: {e}")
            self.faiss_system_ready = False
    
    def _initialize_web_search_system(self):
        """Initialize connection to Oxford web search system."""
        try:
            # Import web search connector
            from .oxford_web_search_connector import OxfordWebSearchConnector
            
            self.web_search_connector = OxfordWebSearchConnector(self.oxford_path)
            self.web_search_system_ready = True
            
            logger.info("✅ Oxford web search system connected")
            
        except Exception as e:
            logger.error(f"❌ Oxford web search system initialization failed: {e}")
            self.web_search_system_ready = False
    
    def _initialize_solomon_orchestrator(self):
        """Initialize Solomon prompt orchestrator for dual system coordination."""
        try:
            # Import Solomon orchestrator
            from .solomon_prompt_orchestrator import SolomonPromptOrchestrator
            
            self.solomon_orchestrator = SolomonPromptOrchestrator()
            self.solomon_orchestrator_ready = True
            
            logger.info("✅ Solomon orchestrator initialized")
            
        except Exception as e:
            logger.error(f"❌ Solomon orchestrator initialization failed: {e}")
            self.solomon_orchestrator_ready = False
    
    def query_dual_system(self, 
                         query: str,
                         use_faiss: bool = True,
                         use_web_search: bool = True,
                         max_faiss_results: int = 5,
                         max_web_results: int = 3) -> Dict[str, Any]:
        """
        Query Oxford dual-system with Solomon orchestration.
        
        Args:
            query: Research question or validation query
            use_faiss: Query FAISS system (1100 PDFs)
            use_web_search: Query web search system
            max_faiss_results: Maximum FAISS results
            max_web_results: Maximum web search results
            
        Returns:
            Dict with unified results from both systems
        """
        query_start = datetime.now()
        self.system_stats['total_queries'] += 1
        
        query_result = {
            'query': query,
            'timestamp': query_start.isoformat(),
            'systems_used': [],
            'faiss_results': None,
            'web_search_results': None,
            'solomon_synthesis': None,
            'unified_response': None,
            'success': False,
            'error': None
        }
        
        try:
            # Query FAISS system (local 1100 PDFs)
            if use_faiss and self.faiss_system_ready:
                faiss_results = self._query_faiss_system(query, max_faiss_results)
                query_result['faiss_results'] = faiss_results
                query_result['systems_used'].append('faiss')
                self.system_stats['faiss_queries'] += 1
                
                logger.info(f"📚 FAISS query completed: {len(faiss_results.get('results', []))} results")
            
            # Query web search system (independent)
            if use_web_search and self.web_search_system_ready:
                web_results = self._query_web_search_system(query, max_web_results)
                query_result['web_search_results'] = web_results
                query_result['systems_used'].append('web_search')
                self.system_stats['web_search_queries'] += 1
                
                logger.info(f"🌐 Web search query completed: {len(web_results.get('results', []))} results")
            
            # Solomon orchestration (unify independent systems)
            if len(query_result['systems_used']) > 0 and self.solomon_orchestrator_ready:
                solomon_synthesis = self._orchestrate_with_solomon(query_result)
                query_result['solomon_synthesis'] = solomon_synthesis
                query_result['unified_response'] = solomon_synthesis.get('unified_response')
                self.system_stats['solomon_orchestrations'] += 1
                
                logger.info("🎭 Solomon orchestration completed")
            
            # Track dual system usage
            if len(query_result['systems_used']) > 1:
                self.system_stats['dual_queries'] += 1
            
            query_result['success'] = True
            logger.info(f"✅ Oxford dual-system query completed: {query[:50]}...")
            
        except Exception as e:
            logger.error(f"❌ Oxford dual-system query failed: {e}")
            query_result['error'] = str(e)
            query_result['success'] = False
        
        # Record query history
        query_result['duration_ms'] = (datetime.now() - query_start).total_seconds() * 1000
        self.query_history.append(query_result)
        
        return query_result
    
    def _query_faiss_system(self, query: str, max_results: int) -> Dict[str, Any]:
        """Query Oxford FAISS system (1100+ PDFs)."""
        if not self.faiss_connector:
            return {'results': [], 'error': 'FAISS connector not available'}
        
        return self.faiss_connector.search_knowledge_base(query, max_results)
    
    def _query_web_search_system(self, query: str, max_results: int) -> Dict[str, Any]:
        """Query Oxford web search system (independent of FAISS)."""
        if not self.web_search_connector:
            return {'results': [], 'error': 'Web search connector not available'}
        
        return self.web_search_connector.search_web(query, max_results)
    
    def _orchestrate_with_solomon(self, query_result: Dict[str, Any]) -> Dict[str, Any]:
        """Use Solomon prompt to orchestrate and unify both independent systems."""
        if not self.solomon_orchestrator:
            return {'error': 'Solomon orchestrator not available'}
        
        return self.solomon_orchestrator.synthesize_dual_results(query_result)
    
    def enhance_pipeline2_validation(self, 
                                   experiment: Dict[str, Any],
                                   validation_context: str = "general") -> Dict[str, Any]:
        """
        Enhance Pipeline 2 validation using Oxford dual-system knowledge.
        
        Args:
            experiment: Pipeline 2 experiment data
            validation_context: Context for validation (chemical, climate, etc.)
            
        Returns:
            Dict with Oxford-enhanced validation results
        """
        enhancement_start = datetime.now()
        
        enhancement_result = {
            'experiment_id': experiment.get('id', 'unknown'),
            'validation_context': validation_context,
            'enhancement_timestamp': enhancement_start.isoformat(),
            'oxford_faiss_validation': {},
            'oxford_web_validation': {},
            'solomon_unified_validation': {},
            'enhancement_successful': False,
            'validation_improvements': [],
            'knowledge_gaps_identified': [],
            'recommendations': []
        }
        
        try:
            # Extract validation queries from experiment
            validation_queries = self._extract_validation_queries(experiment, validation_context)
            
            # Enhance with FAISS knowledge (1100 PDFs)
            if self.faiss_system_ready and validation_queries:
                faiss_validation = self._enhance_with_faiss_knowledge(validation_queries)
                enhancement_result['oxford_faiss_validation'] = faiss_validation
            
            # Enhance with web search (real-time research)
            if self.web_search_system_ready and validation_queries:
                web_validation = self._enhance_with_web_search(validation_queries)
                enhancement_result['oxford_web_validation'] = web_validation
            
            # Solomon unified validation
            if self.solomon_orchestrator_ready:
                unified_validation = self._create_unified_validation(enhancement_result)
                enhancement_result['solomon_unified_validation'] = unified_validation
                enhancement_result['validation_improvements'] = unified_validation.get('improvements', [])
                enhancement_result['recommendations'] = unified_validation.get('recommendations', [])
            
            enhancement_result['enhancement_successful'] = True
            logger.info("✅ Oxford dual-system validation enhancement completed")
            
        except Exception as e:
            logger.error(f"❌ Oxford validation enhancement failed: {e}")
            enhancement_result['error'] = str(e)
        
        return enhancement_result
    
    def _extract_validation_queries(self, experiment: Dict, context: str) -> List[str]:
        """Extract validation queries from experiment based on context."""
        queries = []
        
        # Base validation query
        experiment_topic = experiment.get('topic', experiment.get('title', 'unknown experiment'))
        queries.append(f"Scientific validation for {experiment_topic} in {context} domain")
        
        # Domain-specific queries
        if context == "chemical":
            queries.extend([
                f"Chemical composition validation for {experiment_topic}",
                f"Thermodynamic properties of {experiment_topic}",
                f"Safety considerations for {experiment_topic}"
            ])
        elif context == "climate":
            queries.extend([
                f"Climate response patterns for {experiment_topic}",
                f"Environmental impacts of {experiment_topic}",
                f"Climate modeling validation for {experiment_topic}"
            ])
        
        # Extract specific parameters for validation
        if 'parameters' in experiment:
            for param_name, param_value in experiment['parameters'].items():
                queries.append(f"Validation of {param_name} value {param_value} in {context} experiments")
        
        return queries[:5]  # Limit to 5 queries for efficiency
    
    def _enhance_with_faiss_knowledge(self, queries: List[str]) -> Dict[str, Any]:
        """Enhance validation with FAISS knowledge base (1100 PDFs)."""
        faiss_enhancement = {
            'queries_processed': len(queries),
            'knowledge_found': [],
            'validation_support': [],
            'literature_references': []
        }
        
        for query in queries:
            faiss_result = self._query_faiss_system(query, max_results=3)
            
            if faiss_result.get('results'):
                faiss_enhancement['knowledge_found'].extend(faiss_result['results'])
                
                # Extract validation support
                for result in faiss_result['results']:
                    if result.get('relevance_score', 0) > 0.7:
                        faiss_enhancement['validation_support'].append({
                            'source': result.get('source', 'Unknown'),
                            'content': result.get('content', ''),
                            'relevance': result.get('relevance_score', 0)
                        })
        
        return faiss_enhancement
    
    def _enhance_with_web_search(self, queries: List[str]) -> Dict[str, Any]:
        """Enhance validation with web search (real-time research)."""
        web_enhancement = {
            'queries_processed': len(queries),
            'current_research': [],
            'recent_publications': [],
            'expert_opinions': []
        }
        
        for query in queries:
            web_result = self._query_web_search_system(query, max_results=2)
            
            if web_result.get('results'):
                web_enhancement['current_research'].extend(web_result['results'])
                
                # Categorize web results
                for result in web_result['results']:
                    if 'publication' in result.get('title', '').lower():
                        web_enhancement['recent_publications'].append(result)
                    elif any(term in result.get('snippet', '').lower() 
                            for term in ['expert', 'researcher', 'scientist']):
                        web_enhancement['expert_opinions'].append(result)
        
        return web_enhancement
    
    def _create_unified_validation(self, enhancement_result: Dict) -> Dict[str, Any]:
        """Create unified validation using Solomon orchestration."""
        faiss_data = enhancement_result.get('oxford_faiss_validation', {})
        web_data = enhancement_result.get('oxford_web_validation', {})
        
        unified_validation = {
            'knowledge_sources': {
                'literature_count': len(faiss_data.get('validation_support', [])),
                'web_sources_count': len(web_data.get('current_research', [])),
                'total_sources': len(faiss_data.get('validation_support', [])) + len(web_data.get('current_research', []))
            },
            'improvements': [],
            'recommendations': []
        }
        
        # Analyze validation coverage
        if unified_validation['knowledge_sources']['total_sources'] > 0:
            unified_validation['improvements'].append("Enhanced validation with Oxford dual-system knowledge")
            
            if faiss_data.get('validation_support'):
                unified_validation['improvements'].append("Literature validation from 1100+ PDF knowledge base")
            
            if web_data.get('current_research'):
                unified_validation['improvements'].append("Real-time research validation from web search")
            
            # Generate recommendations
            unified_validation['recommendations'].extend([
                "Validation enhanced with Oxford dual-system approach",
                "Consider both historical literature and current research",
                f"Total knowledge sources: {unified_validation['knowledge_sources']['total_sources']}"
            ])
        else:
            unified_validation['recommendations'].append("Limited validation data available - consider expanding query scope")
        
        return unified_validation
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get Oxford dual-system bridge status."""
        return {
            'bridge_active': True,
            'oxford_path': str(self.oxford_path),
            'systems_status': {
                'faiss_system': 'READY' if self.faiss_system_ready else 'DISABLED',
                'web_search_system': 'READY' if self.web_search_system_ready else 'DISABLED',
                'solomon_orchestrator': 'READY' if self.solomon_orchestrator_ready else 'DISABLED'
            },
            'statistics': self.system_stats.copy(),
            'faiss_info': {
                'total_pdfs': 1171,  # From Oxford system
                'total_vectors': 71047,  # From FAISS summary
                'embedding_dimension': 3072
            } if self.faiss_system_ready else None,
            'query_history_count': len(self.query_history)
        }


# Convenience functions for Pipeline 2 integration
def create_oxford_bridge(oxford_path: str = "/Users/apple/code/scientificoxford-try-shaun") -> OxfordDualSystemBridge:
    """Create Oxford dual-system bridge for Pipeline 2."""
    return OxfordDualSystemBridge(oxford_path)

def enhance_pipeline2_with_oxford(experiment: Dict, 
                                 validation_context: str = "general") -> Dict[str, Any]:
    """
    One-line function to enhance Pipeline 2 validation with Oxford dual-system.
    
    Usage in Pipeline 2:
    from .oxford_dual_system_bridge import enhance_pipeline2_with_oxford
    oxford_enhancement = enhance_pipeline2_with_oxford(experiment, "chemical")
    """
    bridge = create_oxford_bridge()
    return bridge.enhance_pipeline2_validation(experiment, validation_context)