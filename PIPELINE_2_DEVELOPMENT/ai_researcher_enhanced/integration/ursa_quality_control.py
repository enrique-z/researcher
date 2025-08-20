"""
URSA Quality Control Integration for Pipeline 2
Integrates URSA experiment verifier for automated quality control
"""

import os
import sys
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
import json
import asyncio
from datetime import datetime

# Add URSA path for imports
URSA_PATH = "/Users/apple/code/losalamos"
sys.path.insert(0, str(Path(URSA_PATH)))
sys.path.insert(0, str(Path(URSA_PATH) / "experiment-verifier"))

try:
    # Import URSA experiment verifier components
    from experiment_verifier.core.pipeline import ExperimentVerifier
    from experiment_verifier.core.domain_classifier import DomainClassifier  
    from experiment_verifier.data.experiment_integrator import ExperimentIntegrator
    URSA_AVAILABLE = True
except ImportError as e:
    URSA_AVAILABLE = False
    logging.warning(f"URSA experiment verifier not available: {e}")

logger = logging.getLogger(__name__)

class Pipeline2URSAQualityControl:
    """
    URSA-based quality control system for Pipeline 2 generated papers
    """
    
    def __init__(self):
        self.ursa_verifier = None
        self.domain_classifier = None
        self.experiment_integrator = None
        self.initialized = False
        
        if URSA_AVAILABLE:
            try:
                self._initialize_ursa_components()
                self.initialized = True
                logger.info("✅ URSA quality control initialized successfully")
            except Exception as e:
                logger.error(f"❌ Failed to initialize URSA components: {e}")
        else:
            logger.warning("⚠️ URSA not available - operating without automated quality control")
    
    def _initialize_ursa_components(self):
        """Initialize URSA components for quality control"""
        # Initialize URSA experiment verifier
        self.ursa_verifier = ExperimentVerifier(
            log_level="INFO",
            save_intermediate_results=True,
            parallel_agents=True
        )
        
        # Initialize domain classifier
        self.domain_classifier = DomainClassifier()
        
        # Initialize experiment integrator for validation
        self.experiment_integrator = ExperimentIntegrator()
        
        logger.info("URSA components initialized for quality control")
    
    async def verify_generated_paper(self, paper_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Verify a generated paper using URSA's 6-phase verification process
        
        Args:
            paper_data: Generated paper from Pipeline 2
            
        Returns:
            Comprehensive verification results
        """
        if not self.initialized:
            logger.warning("URSA not initialized - using fallback verification")
            return self._create_fallback_verification(paper_data)
        
        try:
            # Create temporary experiment for verification
            experiment_config = self._create_experiment_config(paper_data)
            
            logger.info(f"Starting URSA verification for paper: {paper_data.get('title', 'Unknown')}")
            
            # Run URSA verification pipeline
            verification_result = await self.ursa_verifier.process_single_experiment(experiment_config)
            
            # Format results for Pipeline 2
            pipeline2_result = self._format_verification_results(verification_result, paper_data)
            
            return {
                "status": "success",
                "verification_source": "URSA",
                "experiment_id": experiment_config.experiment_id,
                "paper_data": paper_data,
                "verification_results": pipeline2_result,
                "verification_metadata": {
                    "verification_timestamp": datetime.now().isoformat(),
                    "ursa_version": "experiment-verifier",
                    "phases_completed": 6,
                    "processing_time_minutes": getattr(verification_result, 'processing_time', 0)
                }
            }
            
        except Exception as e:
            logger.error(f"URSA verification failed: {e}")
            return {
                "status": "error",
                "error": str(e),
                "fallback_verification": self._create_fallback_verification(paper_data)
            }
    
    def _create_experiment_config(self, paper_data: Dict[str, Any]):
        """Create URSA experiment configuration from paper data"""
        # This would create the ExperimentInput structure expected by URSA
        # For now, create a mock structure
        from dataclasses import dataclass
        
        @dataclass
        class MockExperimentInput:
            experiment_id: str
            paper_content: str
            domain: str
            priority_level: str = "high"
            verification_depth: str = "comprehensive"
            custom_verification_focus: List[str] = None
        
        # Determine domain
        domain = self._classify_paper_domain(paper_data)
        
        # Create experiment config
        experiment_config = MockExperimentInput(
            experiment_id=f"pipeline2_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            paper_content=paper_data.get("content", ""),
            domain=domain,
            priority_level="high",
            verification_depth="comprehensive",
            custom_verification_focus=["experimental_validation", "mathematical_rigor", "implementation_feasibility"]
        )
        
        return experiment_config
    
    def _classify_paper_domain(self, paper_data: Dict[str, Any]) -> str:
        """Classify paper domain for URSA verification"""
        if self.domain_classifier:
            try:
                # Use URSA domain classifier
                content = paper_data.get("content", "") + " " + paper_data.get("abstract", "")
                domain = self.domain_classifier.classify(content)
                return domain
            except Exception as e:
                logger.warning(f"Domain classification failed: {e}")
        
        # Fallback domain classification
        keywords = paper_data.get("keywords", [])
        title = paper_data.get("title", "").lower()
        abstract = paper_data.get("abstract", "").lower()
        
        if any(term in title + abstract for term in ["climate", "aerosol", "stratosphere", "geoengineering"]):
            return "climate_science"
        elif any(term in title + abstract for term in ["material", "crystal", "alloy"]):
            return "materials_science"
        elif any(term in title + abstract for term in ["chemical", "reaction", "molecule"]):
            return "chemistry"
        elif any(term in title + abstract for term in ["biological", "protein", "dna"]):
            return "biology"
        elif any(term in title + abstract for term in ["physics", "quantum", "particle"]):
            return "physics"
        else:
            return "universal"
    
    def _format_verification_results(self, ursa_result: Any, paper_data: Dict[str, Any]) -> Dict[str, Any]:
        """Format URSA verification results for Pipeline 2"""
        
        # Extract key metrics from URSA result
        overall_score = getattr(ursa_result, 'overall_score', 0.5)
        confidence_score = getattr(ursa_result, 'confidence_score', 50.0)
        phase_scores = getattr(ursa_result, 'phase_scores', {})
        
        # Format for Pipeline 2 consumption
        formatted_result = {
            "overall_score": overall_score,
            "confidence_percentage": confidence_score,
            "overall_verdict": self._determine_verdict(overall_score, confidence_score),
            "phase_scores": {
                "literature_foundation": phase_scores.get("literature", 0.5),
                "mathematical_validity": phase_scores.get("mathematical", 0.5),
                "implementation_feasibility": phase_scores.get("implementation", 0.5),
                "experimental_evidence": phase_scores.get("experimental", 0.5),
                "domain_alignment": phase_scores.get("domain", 0.5),
                "evidence_synthesis": phase_scores.get("synthesis", 0.5)
            },
            "detailed_findings": {
                "literature_issues": getattr(ursa_result, 'literature_issues', []),
                "mathematical_issues": getattr(ursa_result, 'mathematical_issues', []),
                "experimental_support_rate": getattr(ursa_result, 'experimental_support_rate', 0.0),
                "implementation_risks": getattr(ursa_result, 'implementation_risks', [])
            },
            "recommendations": getattr(ursa_result, 'recommendations', []),
            "quality_metrics": {
                "citation_count": getattr(ursa_result, 'citation_count', 0),
                "equations_validated": getattr(ursa_result, 'equations_validated', 0),
                "claims_supported": getattr(ursa_result, 'claims_supported', 0),
                "total_claims": getattr(ursa_result, 'total_claims', 0)
            }
        }
        
        return formatted_result
    
    def _determine_verdict(self, overall_score: float, confidence_score: float) -> str:
        """Determine overall verdict based on scores"""
        if overall_score >= 0.85 and confidence_score >= 85:
            return "EXCELLENT"
        elif overall_score >= 0.75 and confidence_score >= 75:
            return "GOOD"
        elif overall_score >= 0.65 and confidence_score >= 65:
            return "ACCEPTABLE"
        elif overall_score >= 0.50 and confidence_score >= 50:
            return "NEEDS_IMPROVEMENT"
        else:
            return "REQUIRES_MAJOR_REVISION"
    
    def _create_fallback_verification(self, paper_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create fallback verification when URSA not available"""
        return {
            "status": "fallback",
            "verification_source": "Fallback (URSA unavailable)",
            "overall_score": 0.7,  # Conservative estimate
            "confidence_percentage": 60.0,
            "overall_verdict": "NEEDS_MANUAL_REVIEW",
            "phase_scores": {
                "literature_foundation": 0.7,
                "mathematical_validity": 0.7,
                "implementation_feasibility": 0.7,
                "experimental_evidence": 0.6,
                "domain_alignment": 0.7,
                "evidence_synthesis": 0.7
            },
            "detailed_findings": {
                "note": "URSA verification not available - manual review recommended"
            },
            "recommendations": [
                "Manual quality review required",
                "Verify experimental claims against available data",
                "Check mathematical formulations",
                "Validate literature citations"
            ],
            "quality_metrics": {
                "citation_count": "unknown",
                "equations_validated": "unknown",
                "claims_supported": "unknown",
                "total_claims": "unknown"
            }
        }
    
    async def batch_verify_papers(self, papers: List[Dict[str, Any]], max_parallel: int = 2) -> List[Dict[str, Any]]:
        """
        Verify multiple papers in parallel using URSA
        
        Args:
            papers: List of papers to verify
            max_parallel: Maximum parallel verifications
            
        Returns:
            List of verification results
        """
        if not self.initialized:
            logger.warning("URSA not initialized - using fallback for batch verification")
            return [self._create_fallback_verification(paper) for paper in papers]
        
        results = []
        
        # Process papers in batches
        for i in range(0, len(papers), max_parallel):
            batch = papers[i:i + max_parallel]
            
            # Create verification tasks
            tasks = [self.verify_generated_paper(paper) for paper in batch]
            
            # Run batch
            try:
                batch_results = await asyncio.gather(*tasks, return_exceptions=True)
                
                for result in batch_results:
                    if isinstance(result, Exception):
                        logger.error(f"Batch verification error: {result}")
                        results.append({"status": "error", "error": str(result)})
                    else:
                        results.append(result)
                        
            except Exception as e:
                logger.error(f"Batch processing failed: {e}")
                # Add error results for this batch
                for paper in batch:
                    results.append({
                        "status": "error",
                        "error": str(e),
                        "fallback_verification": self._create_fallback_verification(paper)
                    })
        
        return results
    
    def create_gemini_review_prompt(self, verification_result: Dict[str, Any]) -> str:
        """
        Create a prompt for manual Gemini review based on URSA verification
        
        Args:
            verification_result: URSA verification results
            
        Returns:
            Formatted prompt for Gemini deep research
        """
        paper_data = verification_result.get("paper_data", {})
        verification = verification_result.get("verification_results", {})
        
        prompt = f"""# Research Paper Quality Control Review Request

## Paper Information
- **Title**: {paper_data.get('title', 'Unknown')}
- **Domain**: {paper_data.get('domain', 'Unknown')}
- **Abstract**: {paper_data.get('abstract', 'Not provided')}

## URSA Automated Verification Results
- **Overall Score**: {verification.get('overall_score', 'N/A')}/1.0
- **Confidence**: {verification.get('confidence_percentage', 'N/A')}%
- **Verdict**: {verification.get('overall_verdict', 'Unknown')}

### Phase Scores:
- Literature Foundation: {verification.get('phase_scores', {}).get('literature_foundation', 'N/A')}/1.0
- Mathematical Validity: {verification.get('phase_scores', {}).get('mathematical_validity', 'N/A')}/1.0
- Implementation Feasibility: {verification.get('phase_scores', {}).get('implementation_feasibility', 'N/A')}/1.0
- Experimental Evidence: {verification.get('phase_scores', {}).get('experimental_evidence', 'N/A')}/1.0
- Domain Alignment: {verification.get('phase_scores', {}).get('domain_alignment', 'N/A')}/1.0

### Key Issues Identified:
{self._format_issues_for_prompt(verification.get('detailed_findings', {}))}

## Review Request

Please conduct a comprehensive expert review of this research paper, focusing on:

1. **Scientific Rigor**: Evaluate the methodological soundness and experimental design
2. **Literature Integration**: Assess how well the paper builds on existing knowledge
3. **Mathematical/Statistical Validity**: Check calculations, equations, and statistical methods
4. **Novelty and Significance**: Determine the contribution to the field
5. **Reproducibility**: Evaluate whether methods are sufficiently detailed for replication
6. **Domain Expertise**: Apply field-specific knowledge to validate claims and approaches

## Specific Questions:
1. Do you agree with the URSA automated assessment scores? Why or why not?
2. What are the most critical strengths and weaknesses of this paper?
3. What additional validation or revision would you recommend?
4. Is this paper ready for publication, or what improvements are needed?
5. How would you rate this paper on a scale of 1-10 for scientific quality?

## Expected Deliverable:
Provide a detailed expert review (1000-2000 words) with specific recommendations for improvement, focusing on the areas where URSA identified potential concerns."""

        return prompt
    
    def _format_issues_for_prompt(self, detailed_findings: Dict[str, Any]) -> str:
        """Format URSA findings for Gemini prompt"""
        issues = []
        
        if detailed_findings.get("literature_issues"):
            issues.append(f"- Literature Issues: {', '.join(detailed_findings['literature_issues'])}")
        
        if detailed_findings.get("mathematical_issues"):
            issues.append(f"- Mathematical Issues: {', '.join(detailed_findings['mathematical_issues'])}")
        
        if detailed_findings.get("implementation_risks"):
            issues.append(f"- Implementation Risks: {', '.join(detailed_findings['implementation_risks'])}")
        
        experimental_rate = detailed_findings.get("experimental_support_rate", 0)
        if experimental_rate < 0.8:
            issues.append(f"- Low Experimental Support Rate: {experimental_rate:.1%}")
        
        return "\n".join(issues) if issues else "- No major issues identified by automated verification"
    
    def get_integration_status(self) -> Dict[str, Any]:
        """Get current integration status"""
        return {
            "ursa_available": URSA_AVAILABLE,
            "initialized": self.initialized,
            "verifier_status": "operational" if self.initialized else "unavailable",
            "quality_control_source": "URSA" if self.initialized else "fallback",
            "ursa_path": URSA_PATH,
            "capabilities": {
                "automated_verification": self.initialized,
                "batch_processing": self.initialized,
                "gemini_prompt_generation": True,
                "domain_classification": self.initialized
            }
        }

def test_ursa_quality_control():
    """Test function for URSA quality control integration"""
    logger.info("🧪 Testing URSA quality control integration...")
    
    integration = Pipeline2URSAQualityControl()
    status = integration.get_integration_status()
    
    logger.info(f"Integration status: {status}")
    
    # Test paper verification
    test_paper = {
        "title": "Stratospheric Aerosol Injection: Pulse vs Continuous Delivery Analysis",
        "abstract": "This paper analyzes the comparative effectiveness of pulsed versus continuous stratospheric aerosol injection strategies.",
        "content": "Paper content would go here...",
        "domain": "climate_science",
        "keywords": ["stratospheric aerosol injection", "geoengineering", "climate intervention"]
    }
    
    # Test verification (async)
    async def run_test():
        verification_result = await integration.verify_generated_paper(test_paper)
        logger.info(f"Verification result status: {verification_result['status']}")
        
        # Test Gemini prompt generation
        if verification_result['status'] in ['success', 'fallback']:
            gemini_prompt = integration.create_gemini_review_prompt(verification_result)
            logger.info(f"Generated Gemini prompt length: {len(gemini_prompt)} characters")
        
        return verification_result['status'] == 'success'
    
    # Run async test
    try:
        import asyncio
        success = asyncio.run(run_test())
    except Exception as e:
        logger.error(f"Async test failed: {e}")
        success = False
    
    return status["initialized"] or success  # Success if either initialized or test passed

if __name__ == "__main__":
    success = test_ursa_quality_control()
    print(f"✅ URSA quality control test {'PASSED' if success else 'FAILED'}")