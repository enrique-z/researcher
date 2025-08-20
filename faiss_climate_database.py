#!/usr/bin/env python3
"""
Direct FAISS Climate Science Database Integration
Provides idea-agnostic novelty and feasibility assessment for ANY research hypothesis
"""

import sys
import os
import pickle
import json
import numpy as np
from pathlib import Path
from typing import List, Dict, Any, Tuple
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    import faiss
except ImportError:
    logger.error("FAISS not available. Install with: pip install faiss-cpu")
    sys.exit(1)

try:
    import openai
    from openai import OpenAI
except ImportError:
    logger.error("OpenAI not available. Install with: pip install openai")
    sys.exit(1)

class ClimateResearchDatabase:
    """Direct access to 1171-PDF FAISS climate science database for novelty assessment"""
    
    def __init__(self, database_path: str = None):
        """Initialize with path to FAISS database"""
        if database_path is None:
            # Use the largest complete database
            database_path = "/Users/apple/code/scientificoxford-try-shaun/databases/faiss_complete_1171pdfs_final"
        
        self.database_path = Path(database_path)
        self.client = None
        self.index = None
        self.metadata = None
        self.summary = None
        
        # Initialize OpenAI client
        self._init_openai()
        
        # Load database
        self._load_database()
    
    def _init_openai(self):
        """Initialize OpenAI client with API key from environment"""
        try:
            # Load API key from .env
            env_file = Path("/Users/apple/code/Researcher/.env")
            if env_file.exists():
                with open(env_file, 'r') as f:
                    for line in f:
                        if line.startswith('OPENAI_API_KEY='):
                            api_key = line.split('=', 1)[1].strip()
                            os.environ['OPENAI_API_KEY'] = api_key
                            break
            
            self.client = OpenAI()
            logger.info("✅ OpenAI client initialized")
        except Exception as e:
            logger.error(f"❌ Failed to initialize OpenAI: {e}")
            raise
    
    def _load_database(self):
        """Load FAISS index and metadata"""
        try:
            # Load FAISS index
            index_path = self.database_path / "index.faiss"
            if index_path.exists():
                self.index = faiss.read_index(str(index_path))
                logger.info(f"✅ Loaded FAISS index: {self.index.ntotal} vectors")
            else:
                raise FileNotFoundError(f"FAISS index not found at {index_path}")
            
            # Load metadata
            metadata_path = self.database_path / "metadata.pkl"
            if metadata_path.exists():
                with open(metadata_path, 'rb') as f:
                    self.metadata = pickle.load(f)
                logger.info(f"✅ Loaded metadata: {len(self.metadata)} entries")
            else:
                logger.warning("⚠️ No metadata file found")
                self.metadata = []
            
            # Load summary
            summary_path = self.database_path / "summary.json"
            if summary_path.exists():
                with open(summary_path, 'r') as f:
                    self.summary = json.load(f)
                logger.info(f"✅ Database: {self.summary.get('total_vectors', 0)} vectors from {self.summary.get('database_name', 'Unknown')}")
            
        except Exception as e:
            logger.error(f"❌ Failed to load database: {e}")
            raise
    
    def embed_hypothesis(self, hypothesis_text: str) -> np.ndarray:
        """Convert hypothesis text to embedding vector"""
        try:
            response = self.client.embeddings.create(
                input=hypothesis_text,
                model="text-embedding-3-large"  # Same model as database
            )
            
            embedding = np.array(response.data[0].embedding, dtype=np.float32)
            return embedding.reshape(1, -1)  # FAISS expects 2D array
            
        except Exception as e:
            logger.error(f"❌ Failed to embed hypothesis: {e}")
            raise
    
    def assess_novelty(self, hypothesis_text: str, k: int = 50) -> Dict[str, Any]:
        """
        Assess novelty of research hypothesis against 1171 climate science papers
        
        Args:
            hypothesis_text: Research hypothesis to evaluate
            k: Number of similar papers to retrieve
            
        Returns:
            Dictionary with novelty assessment results
        """
        try:
            logger.info(f"🔍 Assessing novelty for hypothesis: {hypothesis_text[:100]}...")
            
            # Embed the hypothesis
            query_vector = self.embed_hypothesis(hypothesis_text)
            
            # Search for similar content
            distances, indices = self.index.search(query_vector, k)
            
            # Process results
            similar_papers = []
            for i, (distance, idx) in enumerate(zip(distances[0], indices[0])):
                if idx < len(self.metadata):
                    paper_info = self.metadata[idx]
                    similar_papers.append({
                        'rank': i + 1,
                        'distance': float(distance),
                        'similarity_score': max(0, 1 - (distance / 2)),  # Convert distance to similarity
                        'source': paper_info.get('source', 'Unknown'),
                        'content_snippet': paper_info.get('content', '')[:200],
                        'metadata': paper_info
                    })
            
            # Calculate novelty metrics
            avg_distance = np.mean(distances[0])
            min_distance = np.min(distances[0])
            max_similarity = max(paper['similarity_score'] for paper in similar_papers) if similar_papers else 0
            
            # Novelty assessment
            if max_similarity > 0.85:
                novelty_level = "LOW"
                novelty_reason = "Very similar research already exists"
            elif max_similarity > 0.70:
                novelty_level = "MODERATE" 
                novelty_reason = "Some similar research exists, but hypothesis has novel aspects"
            elif max_similarity > 0.50:
                novelty_level = "HIGH"
                novelty_reason = "Limited similar research, hypothesis appears novel"
            else:
                novelty_level = "VERY_HIGH"
                novelty_reason = "No similar research found, highly novel hypothesis"
            
            novelty_score = 1.0 - max_similarity  # Higher score = more novel
            
            results = {
                'hypothesis': hypothesis_text,
                'novelty_level': novelty_level,
                'novelty_score': round(novelty_score, 3),
                'novelty_reason': novelty_reason,
                'database_coverage': {
                    'total_papers': self.summary.get('total_vectors', 0) if self.summary else 0,
                    'papers_searched': k,
                    'embedding_model': 'text-embedding-3-large'
                },
                'similarity_metrics': {
                    'max_similarity': round(max_similarity, 3),
                    'avg_distance': round(float(avg_distance), 3),
                    'min_distance': round(float(min_distance), 3)
                },
                'most_similar_papers': similar_papers[:10],  # Top 10 most similar
                'assessment_timestamp': None  # Will be set by caller
            }
            
            logger.info(f"✅ Novelty assessment complete: {novelty_level} ({novelty_score:.3f})")
            return results
            
        except Exception as e:
            logger.error(f"❌ Novelty assessment failed: {e}")
            raise
    
    def assess_feasibility(self, hypothesis_text: str, research_domain: str = "climate_science") -> Dict[str, Any]:
        """
        Assess feasibility based on similar research methodologies and outcomes
        
        Args:
            hypothesis_text: Research hypothesis to evaluate  
            research_domain: Domain for feasibility context
            
        Returns:
            Dictionary with feasibility assessment results
        """
        try:
            logger.info(f"🔬 Assessing feasibility for: {hypothesis_text[:100]}...")
            
            # Get novelty assessment first (includes similar papers)
            novelty_results = self.assess_novelty(hypothesis_text, k=30)
            similar_papers = novelty_results['most_similar_papers']
            
            # Analyze methodologies in similar papers
            methodology_success_indicators = 0
            methodology_challenges = []
            precedent_count = 0
            
            for paper in similar_papers[:15]:  # Focus on top 15 most similar
                content = paper.get('content_snippet', '').lower()
                similarity = paper.get('similarity_score', 0)
                
                # Weight by similarity
                weight = similarity
                
                # Look for success indicators
                success_keywords = ['successful', 'effective', 'significant', 'validated', 'confirmed', 'demonstrated']
                challenge_keywords = ['failed', 'ineffective', 'limited', 'challenging', 'difficult', 'unfeasible']
                
                success_count = sum(1 for keyword in success_keywords if keyword in content)
                challenge_count = sum(1 for keyword in challenge_keywords if keyword in content)
                
                methodology_success_indicators += (success_count - challenge_count) * weight
                
                if challenge_count > success_count:
                    methodology_challenges.append({
                        'paper_rank': paper['rank'],
                        'challenge_indicators': challenge_count,
                        'similarity': similarity
                    })
                
                if similarity > 0.6:  # Strong precedent
                    precedent_count += 1
            
            # Calculate feasibility score
            base_feasibility = 0.7  # Default moderate feasibility
            
            # Adjust based on precedents
            if precedent_count > 5:
                precedent_bonus = 0.2
            elif precedent_count > 2:
                precedent_bonus = 0.1
            else:
                precedent_bonus = -0.1  # Lower feasibility if no precedents
            
            # Adjust based on methodology success indicators
            if methodology_success_indicators > 3:
                methodology_bonus = 0.2
            elif methodology_success_indicators > 0:
                methodology_bonus = 0.1
            else:
                methodology_bonus = -0.15
            
            # Adjust based on challenges
            challenge_penalty = min(0.25, len(methodology_challenges) * 0.05)
            
            final_feasibility_score = max(0.1, min(1.0, 
                base_feasibility + precedent_bonus + methodology_bonus - challenge_penalty
            ))
            
            # Feasibility level
            if final_feasibility_score > 0.8:
                feasibility_level = "HIGH"
                feasibility_reason = "Strong precedents and methodology success indicators"
            elif final_feasibility_score > 0.6:
                feasibility_level = "MODERATE"
                feasibility_reason = "Some precedents exist with mixed success indicators"
            elif final_feasibility_score > 0.4:
                feasibility_level = "LOW"
                feasibility_reason = "Limited precedents and/or significant challenges identified"
            else:
                feasibility_level = "VERY_LOW"
                feasibility_reason = "No precedents and significant methodology challenges"
            
            results = {
                'hypothesis': hypothesis_text,
                'research_domain': research_domain,
                'feasibility_level': feasibility_level,
                'feasibility_score': round(final_feasibility_score, 3),
                'feasibility_reason': feasibility_reason,
                'precedent_analysis': {
                    'precedent_count': precedent_count,
                    'methodology_success_indicators': round(methodology_success_indicators, 2),
                    'identified_challenges': len(methodology_challenges),
                    'top_challenges': methodology_challenges[:3]
                },
                'recommendation': {
                    'proceed': final_feasibility_score > 0.5,
                    'confidence': "High" if final_feasibility_score > 0.75 or final_feasibility_score < 0.25 else "Moderate",
                    'suggested_modifications': []
                }
            }
            
            # Add suggested modifications for low feasibility
            if final_feasibility_score < 0.5:
                results['recommendation']['suggested_modifications'] = [
                    "Consider smaller-scale pilot study first",
                    "Review methodology challenges from similar studies",
                    "Seek collaboration with researchers who have tackled similar problems"
                ]
            
            logger.info(f"✅ Feasibility assessment complete: {feasibility_level} ({final_feasibility_score:.3f})")
            return results
            
        except Exception as e:
            logger.error(f"❌ Feasibility assessment failed: {e}")
            raise
    
    def comprehensive_idea_assessment(self, hypothesis_text: str, research_domain: str = "climate_science") -> Dict[str, Any]:
        """
        Complete idea assessment: novelty + feasibility + recommendations
        
        Args:
            hypothesis_text: Research hypothesis to evaluate
            research_domain: Research domain context
            
        Returns:
            Comprehensive assessment results
        """
        try:
            logger.info(f"🎯 Starting comprehensive assessment for: {hypothesis_text[:50]}...")
            
            # Run both assessments
            novelty_results = self.assess_novelty(hypothesis_text, k=50)
            feasibility_results = self.assess_feasibility(hypothesis_text, research_domain)
            
            # Calculate overall recommendation
            novelty_score = novelty_results['novelty_score']
            feasibility_score = feasibility_results['feasibility_score']
            
            # Weighted overall score (novelty 40%, feasibility 60%)
            overall_score = (novelty_score * 0.4) + (feasibility_score * 0.6)
            
            # Overall recommendation
            if overall_score > 0.75:
                recommendation = "HIGHLY_RECOMMENDED"
                reason = "High novelty and feasibility - excellent research opportunity"
            elif overall_score > 0.6:
                recommendation = "RECOMMENDED" 
                reason = "Good balance of novelty and feasibility"
            elif overall_score > 0.45:
                recommendation = "CONDITIONAL"
                reason = "Some concerns about novelty or feasibility - proceed with caution"
            else:
                recommendation = "NOT_RECOMMENDED"
                reason = "Significant issues with novelty and/or feasibility"
            
            comprehensive_results = {
                'hypothesis': hypothesis_text,
                'research_domain': research_domain,
                'assessment_timestamp': None,  # Will be set by caller
                'overall_assessment': {
                    'recommendation': recommendation,
                    'overall_score': round(overall_score, 3),
                    'reason': reason,
                    'confidence': "High" if overall_score > 0.8 or overall_score < 0.3 else "Moderate"
                },
                'novelty_assessment': novelty_results,
                'feasibility_assessment': feasibility_results,
                'database_info': {
                    'database_path': str(self.database_path),
                    'total_papers': self.summary.get('total_vectors', 0) if self.summary else 0,
                    'database_name': self.summary.get('database_name', 'Unknown') if self.summary else 'Unknown',
                    'embedding_model': 'text-embedding-3-large'
                }
            }
            
            logger.info(f"✅ Comprehensive assessment complete: {recommendation} ({overall_score:.3f})")
            return comprehensive_results
            
        except Exception as e:
            logger.error(f"❌ Comprehensive assessment failed: {e}")
            raise

def test_database_connection():
    """Test database connectivity and basic functionality"""
    try:
        logger.info("🧪 Testing FAISS Climate Database connection...")
        
        db = ClimateResearchDatabase()
        
        # Test with a sample climate hypothesis
        test_hypothesis = "Stratospheric aerosol injection could reduce global temperatures by 2°C through enhanced solar reflection"
        
        results = db.comprehensive_idea_assessment(test_hypothesis)
        
        logger.info(f"✅ Test successful!")
        logger.info(f"📊 Novelty: {results['novelty_assessment']['novelty_level']}")
        logger.info(f"🔬 Feasibility: {results['feasibility_assessment']['feasibility_level']}")
        logger.info(f"🎯 Overall: {results['overall_assessment']['recommendation']}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    test_database_connection()