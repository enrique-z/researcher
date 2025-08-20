"""
Oxford RAG FAISS Connector for Pipeline 2

Connects Pipeline 2 to Oxford's FAISS-based knowledge system containing 1100+ climate science PDFs.
This system is independent from Oxford's web search and uses local vector database for retrieval.

Key Features:
- Access to 71,047 embeddings from 1100+ climate science PDFs  
- 3072-dimensional embeddings using text-embedding-3-large
- HNSW index type for efficient similarity search
- Metadata-rich results with source attribution
- Pipeline 2 validation enhancement
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
    logging.warning("FAISS not available - install with: pip install faiss-cpu")

# OpenAI for embedding generation (matching Oxford system)
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    logging.warning("OpenAI not available - embeddings will be disabled")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OxfordRAGFAISSConnector:
    """
    Connector to Oxford's FAISS-based RAG system with 1100+ climate science PDFs.
    
    System Architecture:
    - FAISS Index: 71,047 vectors, 3072 dimensions, HNSW type
    - Knowledge Base: 1171 PDFs (644 + 527 merged collections)
    - Embeddings: OpenAI text-embedding-3-large model
    - Metadata: Rich source attribution and content context
    """
    
    def __init__(self, 
                 oxford_path: str = "/Users/apple/code/scientificoxford-try-shaun",
                 faiss_db_name: str = "faiss_1171pdfs_final_corrected"):
        """
        Initialize Oxford FAISS connector.
        
        Args:
            oxford_path: Path to Oxford framework directory
            faiss_db_name: Name of FAISS database to use
        """
        self.oxford_path = Path(oxford_path)
        self.faiss_db_name = faiss_db_name
        self.faiss_db_path = self.oxford_path / "databases" / faiss_db_name
        
        # System components
        self.faiss_index = None
        self.metadata = None
        self.openai_client = None
        self.system_info = {}
        
        # Search configuration
        self.embedding_model = "text-embedding-3-large"  # Matching Oxford system
        self.embedding_dimension = 3072
        self.default_k = 10  # Default number of results
        
        # System status
        self.is_ready = False
        self.search_history = []
        self.search_stats = {
            'total_searches': 0,
            'successful_searches': 0,
            'average_response_time_ms': 0,
            'total_documents_retrieved': 0
        }
        
        logger.info(f"🔍 Oxford FAISS Connector initializing...")
        logger.info(f"Oxford path: {self.oxford_path}")
        logger.info(f"FAISS DB: {faiss_db_name}")
        
        # Initialize connection
        self._initialize_connection()
    
    def _initialize_connection(self):
        """Initialize connection to Oxford FAISS system."""
        if not FAISS_AVAILABLE:
            logger.error("❌ FAISS not available - cannot connect to Oxford FAISS system")
            return
        
        try:
            # Load FAISS index
            self._load_faiss_index()
            
            # Load metadata
            self._load_metadata()
            
            # Initialize OpenAI client for embedding generation
            self._initialize_openai_client()
            
            # Load system information
            self._load_system_info()
            
            self.is_ready = True
            logger.info("✅ Oxford FAISS connector ready")
            logger.info(f"📚 Knowledge base: {self.system_info.get('total_pdfs', 'unknown')} PDFs")
            logger.info(f"🔢 Vectors: {self.system_info.get('total_vectors', 'unknown')}")
            logger.info(f"📐 Dimensions: {self.system_info.get('embedding_dimension', 'unknown')}")
            
        except Exception as e:
            logger.error(f"❌ Oxford FAISS connector initialization failed: {e}")
            self.is_ready = False
    
    def _load_faiss_index(self):
        """Load FAISS index from Oxford system."""
        index_path = self.faiss_db_path / "index.faiss"
        
        if not index_path.exists():
            raise FileNotFoundError(f"FAISS index not found at {index_path}")
        
        self.faiss_index = faiss.read_index(str(index_path))
        logger.info(f"📂 FAISS index loaded: {self.faiss_index.ntotal} vectors")
    
    def _load_metadata(self):
        """Load metadata from Oxford system."""
        metadata_path = self.faiss_db_path / "metadata.pkl"
        
        if not metadata_path.exists():
            raise FileNotFoundError(f"Metadata not found at {metadata_path}")
        
        with open(metadata_path, 'rb') as f:
            self.metadata = pickle.load(f)
        
        logger.info(f"📋 Metadata loaded: {len(self.metadata)} entries")
    
    def _initialize_openai_client(self):
        """Initialize OpenAI client for embedding generation."""
        if not OPENAI_AVAILABLE:
            logger.warning("OpenAI not available - embedding generation disabled")
            return
        
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            logger.warning("OPENAI_API_KEY not found - embedding generation disabled")
            return
        
        self.openai_client = OpenAI(api_key=api_key)
        logger.info("🤖 OpenAI client initialized for embeddings")
    
    def _load_system_info(self):
        """Load system information from Oxford FAISS summary."""
        summary_path = self.faiss_db_path / "summary.json"
        
        if summary_path.exists():
            with open(summary_path, 'r') as f:
                self.system_info = json.load(f)
        else:
            # Fallback system info
            self.system_info = {
                'total_pdfs': 1171,
                'total_vectors': self.faiss_index.ntotal if self.faiss_index else 0,
                'embedding_dimension': 3072,
                'model': 'text-embedding-3-large',
                'index_type': 'HNSW'
            }
    
    def generate_embedding(self, text: str) -> Optional[np.ndarray]:
        """
        Generate embedding for text using OpenAI (matching Oxford system).
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding vector or None if generation fails
        """
        if not self.openai_client:
            logger.warning("OpenAI client not available for embedding generation")
            return None
        
        try:
            response = self.openai_client.embeddings.create(
                model=self.embedding_model,
                input=text,
                encoding_format="float"
            )
            
            embedding = np.array(response.data[0].embedding, dtype=np.float32)
            
            # Verify dimension matches Oxford system
            if embedding.shape[0] != self.embedding_dimension:
                logger.error(f"Embedding dimension mismatch: {embedding.shape[0]} != {self.embedding_dimension}")
                return None
            
            return embedding
            
        except Exception as e:
            logger.error(f"Embedding generation failed: {e}")
            return None
    
    def search_knowledge_base(self, 
                            query: str,
                            k: int = 5,
                            similarity_threshold: float = 0.0) -> Dict[str, Any]:
        """
        Search Oxford FAISS knowledge base with 1100+ PDFs.
        
        Args:
            query: Search query
            k: Number of results to return
            similarity_threshold: Minimum similarity score
            
        Returns:
            Dict with search results and metadata
        """
        search_start = datetime.now()
        self.search_stats['total_searches'] += 1
        
        search_result = {
            'query': query,
            'timestamp': search_start.isoformat(),
            'results': [],
            'search_stats': {
                'total_candidates': 0,
                'filtered_results': 0,
                'similarity_threshold': similarity_threshold
            },
            'system_info': {
                'database': self.faiss_db_name,
                'total_pdfs': self.system_info.get('total_pdfs', 'unknown'),
                'embedding_model': self.embedding_model
            },
            'success': False,
            'error': None
        }
        
        if not self.is_ready:
            search_result['error'] = 'Oxford FAISS system not ready'
            return search_result
        
        try:
            # Generate query embedding
            query_embedding = self.generate_embedding(query)
            if query_embedding is None:
                search_result['error'] = 'Failed to generate query embedding'
                return search_result
            
            # Search FAISS index
            query_vector = query_embedding.reshape(1, -1)
            distances, indices = self.faiss_index.search(query_vector, k)
            
            # Process results
            results = []
            for i, (distance, idx) in enumerate(zip(distances[0], indices[0])):
                if idx < 0:  # Invalid index
                    continue
                
                # Calculate similarity score (FAISS uses L2 distance)
                similarity_score = 1.0 / (1.0 + distance)
                
                if similarity_score < similarity_threshold:
                    continue
                
                # Get metadata
                metadata_entry = self.metadata[idx] if idx < len(self.metadata) else {}
                
                result = {
                    'rank': i + 1,
                    'similarity_score': float(similarity_score),
                    'distance': float(distance),
                    'content': metadata_entry.get('text', ''),
                    'source': metadata_entry.get('source', 'Unknown PDF'),
                    'document_name': metadata_entry.get('document_name', 'Unknown'),
                    'page': metadata_entry.get('page', 'Unknown'),
                    'chunk_id': metadata_entry.get('chunk_id', idx),
                    'metadata': metadata_entry
                }
                
                results.append(result)
            
            search_result['results'] = results
            search_result['search_stats']['total_candidates'] = len(distances[0])
            search_result['search_stats']['filtered_results'] = len(results)
            search_result['success'] = True
            
            # Update statistics
            self.search_stats['successful_searches'] += 1
            self.search_stats['total_documents_retrieved'] += len(results)
            
            logger.info(f"🔍 FAISS search completed: {len(results)} results for '{query[:50]}...'")
            
        except Exception as e:
            logger.error(f"❌ Oxford FAISS search failed: {e}")
            search_result['error'] = str(e)
        
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
    
    def search_for_validation(self, 
                            experiment_topic: str,
                            domain: str = "climate",
                            k: int = 3) -> Dict[str, Any]:
        """
        Search Oxford knowledge base for experiment validation information.
        
        Args:
            experiment_topic: Topic of the experiment to validate
            domain: Scientific domain (climate, chemical, etc.)
            k: Number of validation sources to retrieve
            
        Returns:
            Dict with validation-focused search results
        """
        # Create domain-specific validation query
        validation_query = f"scientific validation {experiment_topic} {domain} research methodology experimental design"
        
        search_result = self.search_knowledge_base(validation_query, k=k, similarity_threshold=0.3)
        
        if search_result['success']:
            # Enhance results with validation context
            validation_results = []
            for result in search_result['results']:
                validation_result = result.copy()
                validation_result['validation_relevance'] = self._assess_validation_relevance(
                    result['content'], experiment_topic, domain
                )
                validation_results.append(validation_result)
            
            search_result['validation_results'] = validation_results
            search_result['validation_summary'] = self._create_validation_summary(validation_results)
        
        return search_result
    
    def _assess_validation_relevance(self, content: str, topic: str, domain: str) -> Dict[str, Any]:
        """Assess how relevant content is for validation."""
        content_lower = content.lower()
        topic_lower = topic.lower()
        domain_lower = domain.lower()
        
        relevance_score = 0.0
        validation_aspects = []
        
        # Check for validation keywords
        validation_keywords = ['validation', 'verify', 'confirm', 'evidence', 'data', 'measurement', 'experiment']
        for keyword in validation_keywords:
            if keyword in content_lower:
                relevance_score += 0.1
                validation_aspects.append(keyword)
        
        # Check for topic relevance
        topic_words = topic_lower.split()
        for word in topic_words:
            if word in content_lower:
                relevance_score += 0.2
        
        # Check for domain relevance
        if domain_lower in content_lower:
            relevance_score += 0.3
        
        return {
            'relevance_score': min(relevance_score, 1.0),
            'validation_aspects': validation_aspects,
            'topic_match': any(word in content_lower for word in topic_lower.split()),
            'domain_match': domain_lower in content_lower
        }
    
    def _create_validation_summary(self, validation_results: List[Dict]) -> Dict[str, Any]:
        """Create summary of validation findings."""
        if not validation_results:
            return {'total_sources': 0, 'summary': 'No validation sources found'}
        
        high_relevance = [r for r in validation_results 
                         if r.get('validation_relevance', {}).get('relevance_score', 0) > 0.5]
        
        validation_aspects = set()
        for result in validation_results:
            aspects = result.get('validation_relevance', {}).get('validation_aspects', [])
            validation_aspects.update(aspects)
        
        return {
            'total_sources': len(validation_results),
            'high_relevance_sources': len(high_relevance),
            'validation_aspects_found': list(validation_aspects),
            'summary': f"Found {len(validation_results)} validation sources from 1100+ PDF knowledge base"
        }
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get Oxford FAISS system status."""
        return {
            'system_name': 'Oxford FAISS RAG System',
            'database': self.faiss_db_name,
            'ready': self.is_ready,
            'knowledge_base': {
                'total_pdfs': self.system_info.get('total_pdfs', 'unknown'),
                'total_vectors': self.system_info.get('total_vectors', 'unknown'),
                'embedding_dimension': self.system_info.get('embedding_dimension', 'unknown'),
                'model': self.system_info.get('model', 'unknown'),
                'index_type': self.system_info.get('index_type', 'unknown')
            },
            'components': {
                'faiss_index': 'LOADED' if self.faiss_index is not None else 'NOT_LOADED',
                'metadata': 'LOADED' if self.metadata is not None else 'NOT_LOADED',
                'openai_client': 'READY' if self.openai_client is not None else 'NOT_AVAILABLE'
            },
            'search_statistics': self.search_stats.copy(),
            'search_history_count': len(self.search_history)
        }


# Convenience functions for Pipeline 2 integration
def create_oxford_faiss_connector(oxford_path: str = "/Users/apple/code/scientificoxford-try-shaun") -> OxfordRAGFAISSConnector:
    """Create Oxford FAISS connector for Pipeline 2."""
    return OxfordRAGFAISSConnector(oxford_path)

def search_oxford_knowledge(query: str, k: int = 5) -> Dict[str, Any]:
    """
    One-line function to search Oxford 1100 PDF knowledge base.
    
    Usage in Pipeline 2:
    from .oxford_rag_faiss_connector import search_oxford_knowledge
    results = search_oxford_knowledge("climate validation methodology")
    """
    connector = create_oxford_faiss_connector()
    return connector.search_knowledge_base(query, k)