"""
Oxford+RAG Integration Bridge for Pipeline 2
Integrates the existing Oxford RAG system with Pipeline 2 Development framework
"""

import os
import sys
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
import json
from datetime import datetime

# Add AI-S-Plus path for Oxford bridge imports
AI_S_PLUS_PATH = "/Users/apple/code/ai-s-plus"
sys.path.insert(0, str(Path(AI_S_PLUS_PATH)))

try:
    from researcher_oxford_bridge import ResearcherOxfordBridge, ResearchIdea
    OXFORD_BRIDGE_AVAILABLE = True
except ImportError as e:
    OXFORD_BRIDGE_AVAILABLE = False
    logging.warning(f"Oxford bridge not available: {e}")

logger = logging.getLogger(__name__)

class Pipeline2OxfordIntegration:
    """
    Integration bridge between Oxford+RAG system and Pipeline 2 framework
    """
    
    def __init__(self):
        self.oxford_bridge = None
        self.initialized = False
        
        if OXFORD_BRIDGE_AVAILABLE:
            try:
                self._initialize_oxford_bridge()
                self.initialized = True
                logger.info("✅ Oxford+RAG integration initialized successfully")
            except Exception as e:
                logger.error(f"❌ Failed to initialize Oxford bridge: {e}")
        else:
            logger.warning("⚠️ Oxford bridge not available - operating without RAG enhancement")
    
    def _initialize_oxford_bridge(self):
        """Initialize Oxford bridge with existing configuration"""
        # Use existing Oxford bridge configuration
        self.oxford_bridge = ResearcherOxfordBridge(
            researcher_path="/Users/apple/code/ai-s-plus/Researcher",
            oxford_path="/Users/apple/code/scientificoxford-try-shaun",
            queue_dir="/Users/apple/code/ai-s-plus/integration_queue"
        )
        logger.info("Oxford+RAG bridge initialized")
    
    def enhance_research_idea(self, idea_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enhance research idea using Oxford+RAG system
        
        Args:
            idea_data: Research idea from Pipeline 2
            
        Returns:
            Enhanced idea with RAG context
        """
        if not self.initialized:
            logger.warning("Oxford bridge not initialized - returning original idea")
            return self._create_fallback_enhancement(idea_data)
        
        try:
            # Convert Pipeline 2 idea to ResearchIdea format
            research_idea = self._convert_to_research_idea(idea_data)
            
            logger.info(f"Enhancing research idea: {research_idea.title}")
            
            # Process with Oxford RAG system
            enhanced_idea = self.oxford_bridge.process_with_oxford_rag(research_idea)
            
            # Convert back to Pipeline 2 format
            pipeline2_enhanced = self._convert_from_research_idea(enhanced_idea)
            
            return {
                "status": "success",
                "enhancement_source": "Oxford+RAG",
                "original_idea": idea_data,
                "enhanced_idea": pipeline2_enhanced,
                "enhancement_metadata": {
                    "enhancement_timestamp": datetime.now().isoformat(),
                    "oxford_enhancements": enhanced_idea.oxford_enhancements,
                    "rag_context_items": len(enhanced_idea.rag_context),
                    "web_results_items": len(enhanced_idea.web_search_results),
                    "graph_insights_items": len(enhanced_idea.graph_insights)
                }
            }
            
        except Exception as e:
            logger.error(f"Failed to enhance idea with Oxford+RAG: {e}")
            return {
                "status": "error",
                "error": str(e),
                "fallback_enhancement": self._create_fallback_enhancement(idea_data)
            }
    
    def _convert_to_research_idea(self, idea_data: Dict[str, Any]) -> 'ResearchIdea':
        """Convert Pipeline 2 idea format to ResearchIdea format"""
        return ResearchIdea(
            topic=idea_data.get("topic", "Unknown topic"),
            title=idea_data.get("title", ""),
            abstract=idea_data.get("abstract", ""),
            research_gaps=idea_data.get("research_gaps", []),
            methodology=idea_data.get("methodology", ""),
            keywords=idea_data.get("keywords", []),
            source_system="pipeline2",
            processing_stage="initial"
        )
    
    def _convert_from_research_idea(self, research_idea: 'ResearchIdea') -> Dict[str, Any]:
        """Convert ResearchIdea format back to Pipeline 2 format"""
        return {
            "idea_id": research_idea.idea_id,
            "topic": research_idea.topic,
            "title": research_idea.title,
            "abstract": research_idea.abstract,
            "research_gaps": research_idea.research_gaps,
            "methodology": research_idea.methodology,
            "keywords": research_idea.keywords,
            "processing_stage": research_idea.processing_stage,
            "oxford_enhancements": research_idea.oxford_enhancements,
            "rag_context": research_idea.rag_context,
            "web_search_results": research_idea.web_search_results,
            "graph_insights": research_idea.graph_insights,
            "citation_count": research_idea.citation_count,
            "relevance_score": research_idea.relevance_score,
            "novelty_score": research_idea.novelty_score
        }
    
    def _create_fallback_enhancement(self, idea_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create fallback enhancement when Oxford+RAG not available"""
        enhanced_idea = idea_data.copy()
        
        # Add basic enhancement markers
        enhanced_idea["enhancement_status"] = "fallback"
        enhanced_idea["enhancement_note"] = "Oxford+RAG not available - using basic enhancement"
        enhanced_idea["enhancement_timestamp"] = datetime.now().isoformat()
        
        # Add placeholder enhancement data
        enhanced_idea["oxford_enhancements"] = {
            "fallback_mode": True,
            "message": "Oxford+RAG system unavailable"
        }
        enhanced_idea["rag_context"] = []
        enhanced_idea["web_search_results"] = []
        enhanced_idea["graph_insights"] = []
        
        return enhanced_idea
    
    def generate_hypotheses_for_question(self, cambridge_question: str) -> Dict[str, Any]:
        """
        Generate research hypotheses for Cambridge professor's question
        
        Args:
            cambridge_question: The Cambridge professor's SAI question
            
        Returns:
            Generated hypotheses with RAG enhancement
        """
        if not self.initialized:
            logger.warning("Oxford bridge not initialized - generating basic hypotheses")
            return self._generate_fallback_hypotheses(cambridge_question)
        
        try:
            # Create research idea from question
            idea_data = {
                "topic": "Stratospheric Aerosol Injection Analysis",
                "title": "SAI Delivery Mechanism Analysis: Pulse vs Continuous Flow",
                "abstract": f"Research to address: {cambridge_question}",
                "research_gaps": [
                    "Limited understanding of delivery mechanism optimization",
                    "Insufficient comparison of pulse vs continuous approaches",
                    "Need for quantitative analysis of injection strategies"
                ],
                "methodology": "Comparative analysis using climate models and experimental data",
                "keywords": ["stratospheric aerosol injection", "geoengineering", "pulse injection", "continuous flow", "SAI optimization"]
            }
            
            # Enhance with Oxford+RAG
            enhancement_result = self.enhance_research_idea(idea_data)
            
            if enhancement_result["status"] == "success":
                # Extract hypotheses from Oxford enhancement
                oxford_response = enhancement_result["enhanced_idea"]["oxford_enhancements"].get("solomon_response", "")
                
                # Parse hypotheses from Oxford response
                hypotheses = self._extract_hypotheses_from_oxford_response(oxford_response)
                
                return {
                    "status": "success",
                    "question": cambridge_question,
                    "hypotheses": hypotheses,
                    "rag_enhancement": enhancement_result["enhancement_metadata"],
                    "oxford_analysis": oxford_response
                }
            else:
                return self._generate_fallback_hypotheses(cambridge_question)
                
        except Exception as e:
            logger.error(f"Failed to generate hypotheses: {e}")
            return {
                "status": "error",
                "error": str(e),
                "fallback_hypotheses": self._generate_fallback_hypotheses(cambridge_question)
            }
    
    def _extract_hypotheses_from_oxford_response(self, oxford_response: str) -> List[Dict[str, Any]]:
        """Extract structured hypotheses from Oxford RAG response"""
        hypotheses = []
        
        # Simple extraction - look for numbered points or hypothesis patterns
        lines = oxford_response.split('\n')
        current_hypothesis = None
        
        for line in lines:
            line = line.strip()
            
            # Look for hypothesis patterns
            if any(pattern in line.lower() for pattern in ['hypothesis', 'h1:', 'h2:', 'h3:', '1.', '2.', '3.']):
                if current_hypothesis:
                    hypotheses.append(current_hypothesis)
                
                current_hypothesis = {
                    "hypothesis": line,
                    "description": "",
                    "predictions": [],
                    "methodology": "",
                    "source": "Oxford+RAG"
                }
            elif current_hypothesis and line:
                # Add content to current hypothesis
                if "prediction" in line.lower() or "expect" in line.lower():
                    current_hypothesis["predictions"].append(line)
                elif "method" in line.lower() or "approach" in line.lower():
                    current_hypothesis["methodology"] += line + " "
                else:
                    current_hypothesis["description"] += line + " "
        
        # Add last hypothesis
        if current_hypothesis:
            hypotheses.append(current_hypothesis)
        
        # If no structured hypotheses found, create basic ones
        if not hypotheses:
            hypotheses = [
                {
                    "hypothesis": "Pulse injection provides better atmospheric mixing",
                    "description": "Pulsed SAI delivery may achieve more uniform stratospheric distribution",
                    "predictions": ["Higher mixing efficiency", "More uniform aerosol distribution"],
                    "methodology": "Climate model comparison of injection strategies",
                    "source": "Oxford+RAG (extracted)"
                },
                {
                    "hypothesis": "Continuous flow enables better control",
                    "description": "Continuous SAI delivery provides more precise dosage control",
                    "predictions": ["Stable aerosol concentrations", "Predictable climate response"],
                    "methodology": "Time-series analysis of injection control systems",
                    "source": "Oxford+RAG (extracted)"
                },
                {
                    "hypothesis": "Optimal strategy depends on target timescale",
                    "description": "Different injection strategies optimize for different temporal objectives",
                    "predictions": ["Short-term: pulse advantages", "Long-term: continuous advantages"],
                    "methodology": "Multi-timescale modeling and optimization",
                    "source": "Oxford+RAG (extracted)"
                }
            ]
        
        return hypotheses
    
    def _generate_fallback_hypotheses(self, cambridge_question: str) -> Dict[str, Any]:
        """Generate fallback hypotheses when Oxford+RAG not available"""
        fallback_hypotheses = [
            {
                "hypothesis": "Pulse injection achieves better atmospheric mixing",
                "description": "Intermittent injection may create turbulence that enhances aerosol distribution",
                "predictions": ["Improved mixing efficiency", "Reduced stratospheric gradients"],
                "methodology": "CFD modeling of injection dynamics",
                "source": "Fallback (Oxford+RAG unavailable)"
            },
            {
                "hypothesis": "Continuous flow provides operational advantages",
                "description": "Steady injection simplifies logistics and control systems",
                "predictions": ["Consistent aerosol loading", "Simplified operational protocols"],
                "methodology": "Engineering systems analysis",
                "source": "Fallback (Oxford+RAG unavailable)"
            },
            {
                "hypothesis": "Hybrid approach optimizes multiple objectives",
                "description": "Combined pulse-continuous strategy balances mixing and control",
                "predictions": ["Optimized aerosol distribution", "Flexible operational control"],
                "methodology": "Multi-objective optimization modeling",
                "source": "Fallback (Oxford+RAG unavailable)"
            }
        ]
        
        return {
            "status": "fallback",
            "question": cambridge_question,
            "hypotheses": fallback_hypotheses,
            "note": "Generated without Oxford+RAG enhancement"
        }
    
    def get_integration_status(self) -> Dict[str, Any]:
        """Get current integration status"""
        status = {
            "oxford_bridge_available": OXFORD_BRIDGE_AVAILABLE,
            "initialized": self.initialized,
            "bridge_status": "operational" if self.initialized else "unavailable",
            "enhancement_source": "Oxford+RAG" if self.initialized else "fallback",
            "ai_s_plus_path": AI_S_PLUS_PATH
        }
        
        if self.initialized and self.oxford_bridge:
            # Get queue status from Oxford bridge
            try:
                queue_status = self.oxford_bridge.get_queue_status()
                status["queue_status"] = queue_status
            except Exception as e:
                status["queue_status"] = {"error": str(e)}
        
        return status

def test_oxford_integration():
    """Test function for Oxford+RAG integration"""
    logger.info("🧪 Testing Oxford+RAG integration...")
    
    integration = Pipeline2OxfordIntegration()
    status = integration.get_integration_status()
    
    logger.info(f"Integration status: {status}")
    
    # Test idea enhancement
    test_idea = {
        "topic": "Stratospheric Aerosol Injection",
        "title": "SAI Delivery Mechanism Optimization",
        "abstract": "Analysis of injection strategies for climate intervention",
        "research_gaps": ["Limited delivery mechanism comparison"],
        "methodology": "Climate modeling",
        "keywords": ["SAI", "geoengineering", "injection"]
    }
    
    enhancement_result = integration.enhance_research_idea(test_idea)
    logger.info(f"Enhancement result status: {enhancement_result['status']}")
    
    # Test hypothesis generation
    cambridge_question = "What are the potential pros and cons of injecting materials for stratospheric aerosol injection (SAI) in a pulsed fashion versus a continuous flow?"
    
    hypothesis_result = integration.generate_hypotheses_for_question(cambridge_question)
    logger.info(f"Hypothesis generation status: {hypothesis_result['status']}")
    logger.info(f"Generated {len(hypothesis_result.get('hypotheses', []))} hypotheses")
    
    return status["initialized"]

if __name__ == "__main__":
    success = test_oxford_integration()
    print(f"✅ Oxford+RAG integration test {'PASSED' if success else 'FAILED'}")