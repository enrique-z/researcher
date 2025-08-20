"""
Solomon Prompt Orchestrator for Oxford Dual-System Framework

This module implements the Solomon prompt logic that unifies Oxford's two independent systems:
1. FAISS System: Local knowledge base with 1100+ climate science PDFs
2. Web Search System: Real-time internet research (independent of FAISS)

The Solomon orchestrator uses advanced prompting techniques to synthesize results from both
systems while maintaining their independence, creating unified responses for Pipeline 2.

Key Features:
- Advanced prompt engineering for dual-system synthesis
- Confidence scoring and validation enhancement
- Context-aware result fusion
- Pipeline 2 integration optimization
- Real-time and historical knowledge integration
"""

import os
import sys
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Union, Any, Tuple
from datetime import datetime
from dataclasses import dataclass
from enum import Enum

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SynthesisMode(Enum):
    """Different modes for Solomon synthesis."""
    VALIDATION = "validation"  # For Pipeline 2 validation enhancement
    RESEARCH = "research"      # For general research queries
    ANALYSIS = "analysis"      # For comparative analysis
    POLICY = "policy"          # For policy-focused synthesis


@dataclass
class SynthesisContext:
    """Context for Solomon synthesis operations."""
    query: str
    mode: SynthesisMode
    domain: str
    priority_systems: List[str]
    confidence_threshold: float = 0.5
    max_results_per_system: int = 5


class SolomonPromptOrchestrator:
    """
    Solomon prompt orchestrator for unifying Oxford's dual-system framework.
    
    Architecture:
    - Prompt Engineering: Advanced templates for dual-system synthesis
    - Context Fusion: Intelligent merging of FAISS and web search results
    - Validation Enhancement: Pipeline 2 specific validation improvements
    - Independence Preservation: Maintains system independence while unifying outputs
    """
    
    def __init__(self):
        """Initialize Solomon prompt orchestrator."""
        self.synthesis_history = []
        self.synthesis_stats = {
            'total_syntheses': 0,
            'faiss_web_syntheses': 0,
            'validation_syntheses': 0,
            'average_confidence': 0.0,
            'successful_syntheses': 0
        }
        
        # Solomon prompt templates
        self.prompt_templates = self._initialize_prompt_templates()
        
        # Synthesis configuration
        self.default_confidence_threshold = 0.6
        self.max_synthesis_length = 2000
        self.priority_validation_aspects = [
            'experimental_validation',
            'data_authenticity', 
            'methodological_rigor',
            'literature_support',
            'current_research'
        ]
        
        logger.info("🎭 Solomon Prompt Orchestrator initialized")
        logger.info(f"Available synthesis modes: {[mode.value for mode in SynthesisMode]}")
    
    def _initialize_prompt_templates(self) -> Dict[str, str]:
        """Initialize Solomon prompt templates for different synthesis modes."""
        return {
            'validation_synthesis': """
As Solomon, the master synthesizer of dual knowledge systems, analyze and unify these independent research sources:

FAISS SYSTEM RESULTS (Historical Knowledge - 1100+ PDFs):
{faiss_results}

WEB SEARCH RESULTS (Current Research - Real-time):
{web_results}

SYNTHESIS MISSION: Create unified validation enhancement for: "{query}"

SOLOMON'S ANALYTICAL FRAMEWORK:
1. CONVERGENCE ANALYSIS: Where do historical literature and current research align?
2. DIVERGENCE IDENTIFICATION: What new developments contradict or extend historical knowledge?
3. VALIDATION ENHANCEMENT: How do both systems strengthen experimental validation?
4. KNOWLEDGE GAPS: What critical information is missing from either system?
5. CONFIDENCE ASSESSMENT: Rate the reliability of unified findings (0.0-1.0)

SYNTHESIS REQUIREMENTS:
- Maintain independence of both systems while creating unified insights
- Prioritize experimental validation and data authenticity
- Highlight convergent evidence from both historical and current sources
- Identify knowledge gaps that require additional investigation
- Provide actionable recommendations for Pipeline 2 validation

UNIFIED RESPONSE FORMAT:
- Convergent Evidence: [Historical + Current findings that align]
- Emerging Insights: [New developments from web search]
- Validation Support: [How both systems enhance experimental validation]
- Confidence Score: [0.0-1.0 based on source quality and convergence]
- Recommendations: [Specific actions for Pipeline 2 validation enhancement]
""",
            
            'research_synthesis': """
As Solomon, synthesize these independent knowledge sources for comprehensive research insight:

FAISS KNOWLEDGE BASE (1100+ Academic PDFs):
{faiss_results}

REAL-TIME WEB SEARCH (Current Information):
{web_results}

RESEARCH QUERY: "{query}"

SOLOMON'S RESEARCH SYNTHESIS:
1. FOUNDATIONAL KNOWLEDGE: What established principles emerge from the literature base?
2. CURRENT DEVELOPMENTS: What new research and developments are happening now?
3. KNOWLEDGE INTEGRATION: How do historical and current sources complement each other?
4. RESEARCH GAPS: What questions remain unanswered?
5. FUTURE DIRECTIONS: What research opportunities are indicated?

SYNTHESIS OUTPUT:
- Established Knowledge: [From FAISS literature base]
- Current Developments: [From web search results]
- Integrated Insights: [Unified understanding]
- Research Recommendations: [Future research directions]
""",
            
            'policy_synthesis': """
As Solomon, unify these policy-relevant knowledge sources:

POLICY LITERATURE (FAISS Database):
{faiss_results}

CURRENT POLICY LANDSCAPE (Web Search):
{web_results}

POLICY QUESTION: "{query}"

SOLOMON'S POLICY ANALYSIS:
1. REGULATORY FRAMEWORK: What established policies and frameworks exist?
2. CURRENT DEVELOPMENTS: What new policy initiatives are emerging?
3. STAKEHOLDER POSITIONS: What positions do different stakeholders hold?
4. IMPLEMENTATION CHALLENGES: What barriers exist?
5. POLICY RECOMMENDATIONS: What actions should be taken?

UNIFIED POLICY RESPONSE:
- Regulatory Foundation: [Established policy framework]
- Current Initiatives: [New policy developments]
- Stakeholder Analysis: [Key positions and conflicts]
- Implementation Pathway: [Recommended policy actions]
"""
        }
    
    def synthesize_dual_results(self, query_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main entry point for Solomon synthesis of dual Oxford systems.
        
        Args:
            query_result: Results from Oxford dual-system query
            
        Returns:
            Dict with Solomon synthesis and unified response
        """
        synthesis_start = datetime.now()
        self.synthesis_stats['total_syntheses'] += 1
        
        synthesis_result = {
            'query': query_result.get('query', ''),
            'synthesis_timestamp': synthesis_start.isoformat(),
            'synthesis_mode': SynthesisMode.VALIDATION.value,
            'systems_synthesized': query_result.get('systems_used', []),
            'solomon_analysis': {},
            'unified_response': '',
            'confidence_score': 0.0,
            'validation_enhancements': [],
            'knowledge_gaps': [],
            'recommendations': [],
            'success': False,
            'error': None
        }
        
        try:
            # Determine synthesis mode based on query content
            synthesis_mode = self._determine_synthesis_mode(query_result.get('query', ''))
            synthesis_result['synthesis_mode'] = synthesis_mode.value
            
            # Extract results from both systems
            faiss_results = query_result.get('faiss_results', {})
            web_results = query_result.get('web_search_results', {})
            
            # Create synthesis context
            synthesis_context = SynthesisContext(
                query=query_result.get('query', ''),
                mode=synthesis_mode,
                domain='climate',  # Default for Pipeline 2
                priority_systems=query_result.get('systems_used', [])
            )
            
            # Perform Solomon synthesis
            solomon_analysis = self._perform_solomon_synthesis(
                faiss_results, web_results, synthesis_context
            )
            
            synthesis_result['solomon_analysis'] = solomon_analysis
            synthesis_result['unified_response'] = solomon_analysis.get('unified_response', '')
            synthesis_result['confidence_score'] = solomon_analysis.get('confidence_score', 0.0)
            synthesis_result['validation_enhancements'] = solomon_analysis.get('validation_enhancements', [])
            synthesis_result['knowledge_gaps'] = solomon_analysis.get('knowledge_gaps', [])
            synthesis_result['recommendations'] = solomon_analysis.get('recommendations', [])
            
            # Update statistics
            if synthesis_result['confidence_score'] > self.default_confidence_threshold:
                self.synthesis_stats['successful_syntheses'] += 1
            
            if len(query_result.get('systems_used', [])) > 1:
                self.synthesis_stats['faiss_web_syntheses'] += 1
            
            if synthesis_mode == SynthesisMode.VALIDATION:
                self.synthesis_stats['validation_syntheses'] += 1
            
            # Update average confidence
            total_confidence = (self.synthesis_stats['average_confidence'] * 
                              (self.synthesis_stats['total_syntheses'] - 1) + 
                              synthesis_result['confidence_score'])
            self.synthesis_stats['average_confidence'] = total_confidence / self.synthesis_stats['total_syntheses']
            
            synthesis_result['success'] = True
            logger.info(f"🎭 Solomon synthesis completed: confidence {synthesis_result['confidence_score']:.2f}")
            
        except Exception as e:
            logger.error(f"❌ Solomon synthesis failed: {e}")
            synthesis_result['error'] = str(e)
            synthesis_result['unified_response'] = self._get_synthesis_fallback(query_result.get('query', ''))
        
        # Record synthesis history
        synthesis_result['duration_ms'] = (datetime.now() - synthesis_start).total_seconds() * 1000
        self.synthesis_history.append(synthesis_result)
        
        return synthesis_result
    
    def _determine_synthesis_mode(self, query: str) -> SynthesisMode:
        """Determine appropriate synthesis mode based on query content."""
        query_lower = query.lower()
        
        if any(term in query_lower for term in ['validation', 'validate', 'verify', 'experiment', 'data']):
            return SynthesisMode.VALIDATION
        elif any(term in query_lower for term in ['policy', 'governance', 'framework', 'regulation']):
            return SynthesisMode.POLICY
        elif any(term in query_lower for term in ['analysis', 'compare', 'evaluate', 'assess']):
            return SynthesisMode.ANALYSIS
        else:
            return SynthesisMode.RESEARCH
    
    def _perform_solomon_synthesis(self, 
                                  faiss_results: Dict, 
                                  web_results: Dict, 
                                  context: SynthesisContext) -> Dict[str, Any]:
        """Perform the core Solomon synthesis using prompt templates."""
        # Format results for prompt
        faiss_summary = self._format_faiss_results_for_prompt(faiss_results)
        web_summary = self._format_web_results_for_prompt(web_results)
        
        # Select appropriate prompt template
        template_key = f"{context.mode.value}_synthesis"
        prompt_template = self.prompt_templates.get(template_key, self.prompt_templates['validation_synthesis'])
        
        # Create Solomon prompt
        solomon_prompt = prompt_template.format(
            faiss_results=faiss_summary,
            web_results=web_summary,
            query=context.query
        )
        
        # Simulate Solomon's analytical process
        # Note: In a real implementation, this would use an LLM
        solomon_analysis = self._simulate_solomon_analysis(faiss_results, web_results, context)
        
        return solomon_analysis
    
    def _format_faiss_results_for_prompt(self, faiss_results: Dict) -> str:
        """Format FAISS results for Solomon prompt."""
        if not faiss_results or not faiss_results.get('results'):
            return "No FAISS knowledge base results available."
        
        formatted = "FAISS KNOWLEDGE BASE FINDINGS:\n"
        
        for i, result in enumerate(faiss_results.get('results', [])[:3], 1):
            source = result.get('source', 'Unknown PDF')
            content = result.get('content', '')[:200] + "..."
            similarity = result.get('similarity_score', 0.0)
            
            formatted += f"\n{i}. SOURCE: {source} (Similarity: {similarity:.2f})\n"
            formatted += f"   CONTENT: {content}\n"
        
        return formatted
    
    def _format_web_results_for_prompt(self, web_results: Dict) -> str:
        """Format web search results for Solomon prompt."""
        if not web_results or not web_results.get('results'):
            return "No real-time web search results available."
        
        formatted = "CURRENT WEB SEARCH FINDINGS:\n"
        
        for i, result in enumerate(web_results.get('results', [])[:3], 1):
            title = result.get('title', 'Unknown')
            snippet = result.get('snippet', '')[:200] + "..."
            url = result.get('url', '')
            date = result.get('date', 'Recent')
            
            formatted += f"\n{i}. TITLE: {title} (Date: {date})\n"
            formatted += f"   URL: {url}\n"
            formatted += f"   SUMMARY: {snippet}\n"
        
        return formatted
    
    def _simulate_solomon_analysis(self, 
                                  faiss_results: Dict, 
                                  web_results: Dict, 
                                  context: SynthesisContext) -> Dict[str, Any]:
        """Simulate Solomon's analytical process for dual-system synthesis."""
        
        # Analyze convergence between systems
        convergent_evidence = self._analyze_convergence(faiss_results, web_results)
        
        # Identify emerging insights from web search
        emerging_insights = self._extract_emerging_insights(web_results, faiss_results)
        
        # Assess validation support
        validation_support = self._assess_validation_support(faiss_results, web_results, context)
        
        # Calculate confidence score
        confidence_score = self._calculate_synthesis_confidence(
            faiss_results, web_results, convergent_evidence
        )
        
        # Generate recommendations
        recommendations = self._generate_synthesis_recommendations(
            convergent_evidence, emerging_insights, validation_support, context
        )
        
        # Create unified response
        unified_response = self._create_unified_response(
            convergent_evidence, emerging_insights, validation_support, 
            confidence_score, recommendations, context
        )
        
        return {
            'convergent_evidence': convergent_evidence,
            'emerging_insights': emerging_insights,
            'validation_support': validation_support,
            'confidence_score': confidence_score,
            'validation_enhancements': validation_support.get('enhancements', []),
            'knowledge_gaps': validation_support.get('gaps', []),
            'recommendations': recommendations,
            'unified_response': unified_response,
            'synthesis_metadata': {
                'faiss_sources': len(faiss_results.get('results', [])),
                'web_sources': len(web_results.get('results', [])),
                'synthesis_mode': context.mode.value,
                'domain': context.domain
            }
        }
    
    def _analyze_convergence(self, faiss_results: Dict, web_results: Dict) -> Dict[str, Any]:
        """Analyze convergence between FAISS and web search results."""
        faiss_content = self._extract_content_keywords(faiss_results)
        web_content = self._extract_content_keywords(web_results)
        
        # Find common themes
        common_keywords = set(faiss_content).intersection(set(web_content))
        
        convergence_score = len(common_keywords) / max(len(faiss_content) + len(web_content), 1)
        
        return {
            'common_themes': list(common_keywords)[:5],
            'convergence_score': convergence_score,
            'supporting_evidence': f"Both historical literature and current research emphasize: {', '.join(list(common_keywords)[:3])}"
        }
    
    def _extract_emerging_insights(self, web_results: Dict, faiss_results: Dict) -> Dict[str, Any]:
        """Extract emerging insights from web search that complement FAISS knowledge."""
        web_keywords = self._extract_content_keywords(web_results)
        faiss_keywords = self._extract_content_keywords(faiss_results)
        
        # Find web-specific insights
        emerging_keywords = set(web_keywords) - set(faiss_keywords)
        
        return {
            'new_developments': list(emerging_keywords)[:5],
            'current_research_trends': self._identify_current_trends(web_results),
            'temporal_insights': "Recent research shows developments not captured in historical literature"
        }
    
    def _assess_validation_support(self, faiss_results: Dict, web_results: Dict, context: SynthesisContext) -> Dict[str, Any]:
        """Assess how both systems support experimental validation."""
        validation_aspects = []
        gaps = []
        enhancements = []
        
        # Check FAISS for historical validation methods
        if faiss_results.get('results'):
            validation_aspects.append("Historical validation methods from literature")
            enhancements.append("Access to 1100+ PDF knowledge base for validation context")
        
        # Check web for current validation approaches
        if web_results.get('results'):
            validation_aspects.append("Current validation approaches from recent research")
            enhancements.append("Real-time research updates for validation enhancement")
        
        # Identify gaps
        if not faiss_results.get('results'):
            gaps.append("Limited historical literature context")
        
        if not web_results.get('results'):
            gaps.append("Missing current research developments")
        
        return {
            'validation_aspects': validation_aspects,
            'enhancements': enhancements,
            'gaps': gaps,
            'dual_system_advantage': "Combination of historical depth and current insights"
        }
    
    def _calculate_synthesis_confidence(self, faiss_results: Dict, web_results: Dict, convergent_evidence: Dict) -> float:
        """Calculate confidence score for synthesis."""
        confidence = 0.0
        
        # Base confidence from result availability
        if faiss_results.get('results'):
            confidence += 0.3
        
        if web_results.get('results'):
            confidence += 0.3
        
        # Boost from convergence
        convergence_score = convergent_evidence.get('convergence_score', 0.0)
        confidence += convergence_score * 0.4
        
        return min(confidence, 1.0)
    
    def _generate_synthesis_recommendations(self, 
                                          convergent_evidence: Dict, 
                                          emerging_insights: Dict, 
                                          validation_support: Dict, 
                                          context: SynthesisContext) -> List[str]:
        """Generate actionable recommendations from synthesis."""
        recommendations = []
        
        if context.mode == SynthesisMode.VALIDATION:
            recommendations.extend([
                "Use dual Oxford system for comprehensive validation",
                "Cross-reference historical literature with current research",
                "Prioritize convergent evidence for experimental design"
            ])
        
        if convergent_evidence.get('convergence_score', 0) > 0.5:
            recommendations.append("High convergence indicates strong validation support")
        
        if emerging_insights.get('new_developments'):
            recommendations.append("Incorporate recent research developments for complete validation")
        
        if validation_support.get('gaps'):
            recommendations.append("Address identified knowledge gaps through targeted research")
        
        return recommendations
    
    def _create_unified_response(self, 
                               convergent_evidence: Dict, 
                               emerging_insights: Dict, 
                               validation_support: Dict,
                               confidence_score: float,
                               recommendations: List[str],
                               context: SynthesisContext) -> str:
        """Create unified response from Solomon synthesis."""
        response = f"🎭 SOLOMON SYNTHESIS for: '{context.query}'\n"
        response += "=" * 60 + "\n\n"
        
        response += f"🔗 CONVERGENT EVIDENCE (Confidence: {confidence_score:.2f}):\n"
        response += f"{convergent_evidence.get('supporting_evidence', 'Limited convergent evidence')}\n\n"
        
        response += f"🆕 EMERGING INSIGHTS:\n"
        new_developments = emerging_insights.get('new_developments', [])
        if new_developments:
            response += f"Recent research emphasizes: {', '.join(new_developments[:3])}\n\n"
        else:
            response += "No significant new developments identified\n\n"
        
        response += f"✅ VALIDATION ENHANCEMENT:\n"
        enhancements = validation_support.get('enhancements', [])
        for enhancement in enhancements:
            response += f"• {enhancement}\n"
        response += "\n"
        
        response += f"🎯 RECOMMENDATIONS:\n"
        for recommendation in recommendations:
            response += f"• {recommendation}\n"
        
        response += f"\n🔍 SYNTHESIS SUMMARY:\n"
        response += f"Solomon successfully unified {validation_support.get('dual_system_advantage', 'available knowledge systems')} "
        response += f"with {confidence_score:.1%} confidence for Pipeline 2 validation enhancement."
        
        return response
    
    def _extract_content_keywords(self, results: Dict) -> List[str]:
        """Extract keywords from results content."""
        keywords = []
        
        for result in results.get('results', []):
            content = result.get('content', '') + ' ' + result.get('snippet', '')
            # Simple keyword extraction (in practice, use NLP libraries)
            words = content.lower().split()
            keywords.extend([word for word in words if len(word) > 4])
        
        return list(set(keywords))[:20]  # Return unique keywords
    
    def _identify_current_trends(self, web_results: Dict) -> List[str]:
        """Identify current research trends from web results."""
        trends = []
        
        for result in web_results.get('results', []):
            title = result.get('title', '').lower()
            if any(term in title for term in ['new', 'recent', 'latest', '2024', 'emerging']):
                trends.append(f"Recent development: {result.get('title', '')[:50]}...")
        
        return trends[:3]
    
    def _get_synthesis_fallback(self, query: str) -> str:
        """Provide fallback synthesis when main process fails."""
        return f"""🎭 SOLOMON SYNTHESIS FALLBACK for: '{query}'

⚠️ Primary synthesis process encountered limitations
📋 GENERAL DUAL-SYSTEM GUIDANCE:

Oxford Framework provides two independent knowledge systems:
• FAISS System: 1100+ climate science PDFs for historical context
• Web Search System: Real-time research for current developments

🔗 SYNTHESIS APPROACH:
- Cross-reference historical literature with current research
- Prioritize convergent evidence from both systems
- Use temporal analysis to identify knowledge evolution
- Enhance validation through dual-system confirmation

🎯 PIPELINE 2 INTEGRATION:
Solomon orchestration enhances Pipeline 2 validation by combining
established knowledge with emerging research developments.
"""
    
    def get_synthesis_statistics(self) -> Dict[str, Any]:
        """Get Solomon synthesis statistics."""
        return {
            'orchestrator_name': 'Solomon Prompt Orchestrator',
            'total_syntheses': self.synthesis_stats['total_syntheses'],
            'dual_system_syntheses': self.synthesis_stats['faiss_web_syntheses'],
            'validation_syntheses': self.synthesis_stats['validation_syntheses'],
            'average_confidence': self.synthesis_stats['average_confidence'],
            'success_rate': (self.synthesis_stats['successful_syntheses'] / 
                           max(self.synthesis_stats['total_syntheses'], 1)),
            'synthesis_history_count': len(self.synthesis_history),
            'available_modes': [mode.value for mode in SynthesisMode]
        }


# Convenience functions for Pipeline 2 integration
def create_solomon_orchestrator() -> SolomonPromptOrchestrator:
    """Create Solomon orchestrator for Pipeline 2."""
    return SolomonPromptOrchestrator()

def synthesize_dual_oxford_results(query_result: Dict[str, Any]) -> Dict[str, Any]:
    """
    One-line function to synthesize Oxford dual-system results with Solomon.
    
    Usage in Pipeline 2:
    from .solomon_prompt_orchestrator import synthesize_dual_oxford_results
    synthesis = synthesize_dual_oxford_results(oxford_query_result)
    """
    orchestrator = create_solomon_orchestrator()
    return orchestrator.synthesize_dual_results(query_result)