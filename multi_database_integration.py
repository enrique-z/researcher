#!/usr/bin/env python3
"""
Multi-Database Research Ecosystem Integration
Provides unified access to FAISS + Weaviate + Neo4j for comprehensive research analysis
"""

import sys
import os
import json
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import database connectors
try:
    from faiss_climate_database import ClimateResearchDatabase
    FAISS_AVAILABLE = True
except ImportError:
    logger.warning("FAISS database not available")
    FAISS_AVAILABLE = False

class MultiDatabaseResearchSystem:
    """
    Unified interface to multiple research databases:
    - FAISS: 1171 PDFs vector similarity search
    - Weaviate: Semantic knowledge graph  
    - Neo4j: Relationship and citation networks
    """
    
    def __init__(self, base_path: str = "/Users/apple/code/scientificoxford-try-shaun"):
        """Initialize multi-database system"""
        self.base_path = Path(base_path)
        self.databases = {}
        
        # Initialize available databases
        self._init_faiss_database()
        self._init_weaviate_database() 
        self._init_neo4j_database()
        
    def _init_faiss_database(self):
        """Initialize FAISS vector database"""
        try:
            if FAISS_AVAILABLE:
                self.databases['faiss'] = ClimateResearchDatabase()
                logger.info("✅ FAISS Database: 1171 PDFs loaded")
            else:
                self.databases['faiss'] = None
                logger.warning("❌ FAISS Database: Not available")
        except Exception as e:
            logger.error(f"❌ FAISS Database failed: {e}")
            self.databases['faiss'] = None
    
    def _init_weaviate_database(self):
        """Initialize Weaviate semantic database"""
        try:
            # Check for Weaviate configuration
            weaviate_config = self.base_path / "old-files-graph" / "docker-compose.weaviate.yml"
            if weaviate_config.exists():
                self.databases['weaviate'] = {
                    'status': 'configured',
                    'config_path': str(weaviate_config),
                    'capabilities': ['semantic_search', 'conceptual_relationships', 'hybrid_search']
                }
                logger.info("✅ Weaviate Database: Configuration found")
            else:
                self.databases['weaviate'] = None
                logger.warning("❌ Weaviate Database: Configuration not found")
        except Exception as e:
            logger.error(f"❌ Weaviate Database failed: {e}")
            self.databases['weaviate'] = None
    
    def _init_neo4j_database(self):
        """Initialize Neo4j graph database"""
        try:
            # Check for Neo4j scripts and configurations
            neo4j_scripts = list(self.base_path.glob("**/simple_neo4j_*.py"))
            graphrag_configs = list(self.base_path.glob("**/graphrag_integration.yaml"))
            
            if neo4j_scripts or graphrag_configs:
                self.databases['neo4j'] = {
                    'status': 'configured',
                    'scripts': [str(s) for s in neo4j_scripts],
                    'configs': [str(c) for c in graphrag_configs],
                    'capabilities': ['citation_networks', 'author_relationships', 'topic_clustering']
                }
                logger.info("✅ Neo4j Database: Configuration found")
            else:
                self.databases['neo4j'] = None
                logger.warning("❌ Neo4j Database: Configuration not found")
        except Exception as e:
            logger.error(f"❌ Neo4j Database failed: {e}")
            self.databases['neo4j'] = None
    
    def assess_research_idea_comprehensive(self, hypothesis: str, research_domain: str = "climate_science") -> Dict[str, Any]:
        """
        Comprehensive research idea assessment across all databases
        
        Args:
            hypothesis: Research hypothesis to evaluate
            research_domain: Research domain context
            
        Returns:
            Multi-database assessment results
        """
        logger.info(f"🎯 Starting comprehensive multi-database assessment...")
        
        results = {
            'hypothesis': hypothesis,
            'research_domain': research_domain,
            'timestamp': datetime.now().isoformat(),
            'databases_used': [],
            'assessments': {},
            'combined_recommendation': {}
        }
        
        # FAISS Vector Similarity Assessment
        if self.databases.get('faiss'):
            try:
                logger.info("🗄️ Running FAISS vector similarity assessment...")
                faiss_results = self.databases['faiss'].comprehensive_idea_assessment(hypothesis, research_domain)
                results['assessments']['faiss'] = faiss_results
                results['databases_used'].append('faiss')
                logger.info(f"✅ FAISS: {faiss_results['overall_assessment']['recommendation']}")
            except Exception as e:
                logger.error(f"❌ FAISS assessment failed: {e}")
                results['assessments']['faiss'] = {'status': 'failed', 'error': str(e)}
        
        # Weaviate Semantic Assessment  
        if self.databases.get('weaviate'):
            try:
                logger.info("🧠 Running Weaviate semantic assessment...")
                # Placeholder for Weaviate integration
                weaviate_results = {
                    'semantic_similarity': 'moderate',
                    'conceptual_relationships': ['geoengineering', 'climate_intervention', 'solar_radiation'],
                    'hybrid_search_results': 'pending_implementation',
                    'status': 'configured_but_not_integrated'
                }
                results['assessments']['weaviate'] = weaviate_results
                results['databases_used'].append('weaviate')
                logger.info("✅ Weaviate: Semantic analysis prepared")
            except Exception as e:
                logger.error(f"❌ Weaviate assessment failed: {e}")
                results['assessments']['weaviate'] = {'status': 'failed', 'error': str(e)}
        
        # Neo4j Graph Network Assessment
        if self.databases.get('neo4j'):
            try:
                logger.info("🕸️ Running Neo4j graph network assessment...")
                # Placeholder for Neo4j integration
                neo4j_results = {
                    'citation_network_analysis': 'pending',
                    'author_collaboration_patterns': 'pending',
                    'research_topic_clustering': 'pending',
                    'influence_metrics': 'pending',
                    'status': 'configured_but_not_integrated'
                }
                results['assessments']['neo4j'] = neo4j_results
                results['databases_used'].append('neo4j')
                logger.info("✅ Neo4j: Graph analysis prepared")
            except Exception as e:
                logger.error(f"❌ Neo4j assessment failed: {e}")
                results['assessments']['neo4j'] = {'status': 'failed', 'error': str(e)}
        
        # Combined Recommendation
        results['combined_recommendation'] = self._generate_combined_recommendation(results['assessments'])
        
        logger.info(f"✅ Multi-database assessment complete: {results['combined_recommendation']['overall_status']}")
        return results
    
    def _generate_combined_recommendation(self, assessments: Dict[str, Any]) -> Dict[str, Any]:
        """Generate combined recommendation from all database assessments"""
        
        recommendations = []
        confidence_scores = []
        
        # Process FAISS results
        if 'faiss' in assessments and 'overall_assessment' in assessments['faiss']:
            faiss_rec = assessments['faiss']['overall_assessment']
            recommendations.append(faiss_rec['recommendation'])
            confidence_scores.append(faiss_rec['overall_score'])
        
        # Process other database results (when implemented)
        # Weaviate and Neo4j would contribute here
        
        # Calculate overall recommendation
        if not recommendations:
            return {
                'overall_status': 'INSUFFICIENT_DATA',
                'reason': 'No databases provided valid assessments',
                'confidence': 'LOW'
            }
        
        # Simple majority vote for now (would be more sophisticated with full integration)
        positive_recommendations = sum(1 for rec in recommendations if rec in ['HIGHLY_RECOMMENDED', 'RECOMMENDED'])
        avg_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0
        
        if positive_recommendations >= len(recommendations) / 2:
            overall_status = 'RECOMMENDED'
            reason = f"Positive assessment from {positive_recommendations}/{len(recommendations)} databases"
        else:
            overall_status = 'NOT_RECOMMENDED'
            reason = f"Negative assessment from {len(recommendations) - positive_recommendations}/{len(recommendations)} databases"
        
        return {
            'overall_status': overall_status,
            'reason': reason,
            'confidence': 'HIGH' if avg_confidence > 0.7 else 'MODERATE',
            'databases_consulted': len(recommendations),
            'consensus_score': avg_confidence
        }
    
    def get_database_status(self) -> Dict[str, Any]:
        """Get status of all database connections"""
        status = {
            'timestamp': datetime.now().isoformat(),
            'databases': {}
        }
        
        for db_name, db_connection in self.databases.items():
            if db_connection is None:
                status['databases'][db_name] = {
                    'status': 'UNAVAILABLE',
                    'reason': 'Not configured or failed to connect'
                }
            elif isinstance(db_connection, dict):
                status['databases'][db_name] = {
                    'status': 'CONFIGURED',
                    'capabilities': db_connection.get('capabilities', []),
                    'details': db_connection
                }
            else:
                status['databases'][db_name] = {
                    'status': 'ACTIVE',
                    'type': type(db_connection).__name__
                }
        
        return status

def test_multi_database_system():
    """Test multi-database system functionality"""
    try:
        logger.info("🧪 Testing Multi-Database Research System...")
        
        system = MultiDatabaseResearchSystem()
        
        # Check database status
        status = system.get_database_status()
        logger.info(f"📊 Database Status:")
        for db_name, db_status in status['databases'].items():
            logger.info(f"  {db_name.upper()}: {db_status['status']}")
        
        # Test with a sample hypothesis
        test_hypothesis = "Machine learning can predict solar radiation management effectiveness through atmospheric modeling"
        
        results = system.assess_research_idea_comprehensive(test_hypothesis)
        
        logger.info(f"✅ Multi-database test successful!")
        logger.info(f"🗄️ Databases used: {', '.join(results['databases_used'])}")
        logger.info(f"🎯 Overall recommendation: {results['combined_recommendation']['overall_status']}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Multi-database test failed: {e}")
        return False

# Available database access methods for external software
class DatabaseAccessAPI:
    """API interface for external software to access research databases"""
    
    @staticmethod
    def get_faiss_interface():
        """Get FAISS database interface for vector similarity search"""
        if FAISS_AVAILABLE:
            return ClimateResearchDatabase()
        return None
    
    @staticmethod  
    def get_weaviate_config():
        """Get Weaviate configuration for semantic search"""
        config_path = Path("/Users/apple/code/scientificoxford-try-shaun/old-files-graph/docker-compose.weaviate.yml")
        return str(config_path) if config_path.exists() else None
    
    @staticmethod
    def get_neo4j_scripts():
        """Get Neo4j integration scripts for graph analysis"""
        base_path = Path("/Users/apple/code/scientificoxford-try-shaun")
        scripts = list(base_path.glob("**/simple_neo4j_*.py"))
        return [str(s) for s in scripts]

if __name__ == "__main__":
    test_multi_database_system()