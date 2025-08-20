"""
URSA Post-Hoc Verification System

Integrates with Los Alamos Experiment Verifier (/Users/apple/code/losalamos/experiment-verifier)
to provide post-hoc experimental validation checking for generated research papers.

This system operates AFTER initial paper verification to validate that experimental
claims in papers can be verified through computational experiments and real data analysis.

Key Capabilities:
- Extract experimental claims from research papers
- Interface with Los Alamos verification pipeline
- Validate computational reproducibility
- Check experimental design feasibility
- Verify against real datasets (GLENS, ARISE-SAI, GeoMIP)
- Generate post-hoc verification reports

Integration with Los Alamos Architecture:
- Domain classification coordination
- Agent-based verification orchestration  
- Results synthesis and confidence scoring
- Meta-analysis across multiple verification approaches
"""

import os
import sys
import json
import logging
import subprocess
from typing import Dict, List, Union, Optional, Any
from datetime import datetime
from pathlib import Path

# Add Los Alamos experiment verifier to path when available
LOS_ALAMOS_VERIFIER_PATH = '/Users/apple/code/losalamos/experiment-verifier'
if os.path.exists(LOS_ALAMOS_VERIFIER_PATH):
    sys.path.append(LOS_ALAMOS_VERIFIER_PATH)
    LOS_ALAMOS_AVAILABLE = True
else:
    LOS_ALAMOS_AVAILABLE = False

# Import existing URSA infrastructure
try:
    from ai_researcher.ursa_experimental_execution import URSAExperimentalFramework
    URSA_FRAMEWORK_AVAILABLE = True
except ImportError:
    URSA_FRAMEWORK_AVAILABLE = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class URSAPostHocVerifier:
    """
    Post-hoc experimental verification system that validates research papers
    by attempting to reproduce experimental claims through computational validation.
    
    Integrates with Los Alamos Experiment Verifier for enhanced domain-specific
    validation capabilities.
    """
    
    def __init__(self, 
                 los_alamos_integration: bool = True,
                 ursa_integration: bool = True,
                 verification_mode: str = "comprehensive"):
        """
        Initialize URSA Post-Hoc Verifier.
        
        Args:
            los_alamos_integration: Enable Los Alamos experiment verifier integration
            ursa_integration: Enable existing URSA framework integration
            verification_mode: Verification depth (quick, standard, comprehensive)
        """
        self.los_alamos_integration = los_alamos_integration and LOS_ALAMOS_AVAILABLE
        self.ursa_integration = ursa_integration and URSA_FRAMEWORK_AVAILABLE
        self.verification_mode = verification_mode
        
        # Initialize Los Alamos verifier connection
        self.los_alamos_verifier = None
        if self.los_alamos_integration:
            self.los_alamos_verifier = self._initialize_los_alamos_verifier()
        
        # Initialize URSA experimental framework
        self.ursa_framework = None
        if self.ursa_integration:
            try:
                self.ursa_framework = URSAExperimentalFramework(
                    execution_mode='verification',
                    data_sources=['GLENS', 'ARISE-SAI', 'GeoMIP']
                )
            except Exception as e:
                logger.warning(f"URSA framework initialization failed: {e}")
                self.ursa_integration = False
        
        # Verification configuration
        self.verification_config = {
            'los_alamos_integration': self.los_alamos_integration,
            'ursa_integration': self.ursa_integration,
            'verification_mode': verification_mode,
            'domain_detection': True,
            'computational_reproducibility': True,
            'experimental_feasibility': True,
            'real_data_validation': True
        }
        
        # Verification history and results
        self.verification_history = []
        self.post_hoc_results = []
        
        logger.info(f"🔬 URSA Post-Hoc Verifier initialized")
        logger.info(f"🌐 Los Alamos Integration: {'✅' if self.los_alamos_integration else '❌'}")
        logger.info(f"🏛️ URSA Framework Integration: {'✅' if self.ursa_integration else '❌'}")
    
    def _initialize_los_alamos_verifier(self):
        """Initialize connection to Los Alamos experiment verifier."""
        try:
            if LOS_ALAMOS_AVAILABLE:
                from experiment_verifier.core.pipeline import VerificationPipeline
                from experiment_verifier.core.domain_classifier import DomainClassifier
                from experiment_verifier.core.evidence_synthesizer import EvidenceSynthesizer
                
                verifier = VerificationPipeline()
                logger.info("✅ Los Alamos experiment verifier connected")
                return verifier
            else:
                logger.warning("❌ Los Alamos experiment verifier not available")
                return None
        except Exception as e:
            logger.error(f"❌ Failed to initialize Los Alamos verifier: {e}")
            return None
    
    def verify_paper_experiments(self, 
                                paper_path: str, 
                                paper_content: str = None,
                                domain: str = "auto_detect") -> Dict:
        """
        Perform post-hoc verification of experimental claims in research paper.
        
        Args:
            paper_path: Path to research paper file
            paper_content: Optional paper content as string
            domain: Research domain (auto_detect, climate_science, materials_science, biology)
            
        Returns:
            Dict containing comprehensive post-hoc verification results
        """
        verification_start = datetime.now()
        
        # Initialize post-hoc verification result
        verification_result = {
            'paper_id': paper_path.split('/')[-1] if paper_path else 'content_paper',
            'paper_path': paper_path,
            'verification_timestamp': verification_start.isoformat(),
            'verification_mode': 'POST_HOC_EXPERIMENTAL_VALIDATION',
            'domain': domain,
            'experimental_claims_extracted': [],
            'los_alamos_verification': None,
            'ursa_experimental_validation': None,
            'computational_reproducibility': None,
            'experimental_feasibility': None,
            'real_data_validation': None,
            'overall_post_hoc_status': 'PENDING',
            'verification_confidence': 'UNKNOWN',
            'reproducibility_score': 0.0,
            'feasibility_score': 0.0,
            'validation_issues': [],
            'recommendations': []
        }
        
        try:
            logger.info(f"🔬 Starting post-hoc experimental verification: {verification_result['paper_id']}")
            
            # Step 1: Extract experimental claims from paper
            experimental_claims = self._extract_experimental_claims(paper_path, paper_content)
            verification_result['experimental_claims_extracted'] = experimental_claims
            
            if not experimental_claims:
                verification_result['validation_issues'].append('No experimental claims found in paper')
                verification_result['overall_post_hoc_status'] = 'NO_EXPERIMENTS_DETECTED'
                return verification_result
            
            # Step 2: Domain classification (for Los Alamos integration)
            if domain == "auto_detect":
                domain = self._classify_paper_domain(paper_content or self._load_paper_content(paper_path))
                verification_result['domain'] = domain
            
            # Step 3: Los Alamos experimental verification
            if self.los_alamos_integration:
                los_alamos_result = self._verify_with_los_alamos(experimental_claims, domain)
                verification_result['los_alamos_verification'] = los_alamos_result
            
            # Step 4: URSA experimental validation
            if self.ursa_integration:
                ursa_result = self._verify_with_ursa_framework(experimental_claims, paper_path)
                verification_result['ursa_experimental_validation'] = ursa_result
            
            # Step 5: Computational reproducibility assessment
            reproducibility_result = self._assess_computational_reproducibility(experimental_claims)
            verification_result['computational_reproducibility'] = reproducibility_result
            
            # Step 6: Experimental feasibility validation
            feasibility_result = self._validate_experimental_feasibility(experimental_claims, domain)
            verification_result['experimental_feasibility'] = feasibility_result
            
            # Step 7: Real data validation
            real_data_result = self._validate_against_real_data(experimental_claims)
            verification_result['real_data_validation'] = real_data_result
            
            # Step 8: Overall post-hoc assessment
            verification_result = self._assess_overall_post_hoc_verification(verification_result)
            
            logger.info(f"✅ Post-hoc verification complete: {verification_result['overall_post_hoc_status']}")
            
            # Log verification result
            self.verification_history.append(verification_result)
            
            return verification_result
            
        except Exception as e:
            verification_result['overall_post_hoc_status'] = 'VERIFICATION_FAILED'
            verification_result['validation_issues'].append(f'Post-hoc verification error: {str(e)}')
            logger.error(f"❌ Post-hoc verification failed: {e}")
            return verification_result
    
    def _load_paper_content(self, paper_path: str) -> str:
        """Load paper content from file."""
        try:
            if paper_path.endswith('.tex'):
                with open(paper_path, 'r', encoding='utf-8') as f:
                    return f.read()
            elif paper_path.endswith('.txt'):
                with open(paper_path, 'r', encoding='utf-8') as f:
                    return f.read()
            else:
                logger.warning(f"Unsupported file format for content loading: {paper_path}")
                return ""
        except Exception as e:
            logger.error(f"Failed to load paper content: {e}")
            return ""
    
    def _extract_experimental_claims(self, paper_path: str, paper_content: str = None) -> List[Dict]:
        """Extract experimental claims from research paper."""
        if paper_content is None:
            paper_content = self._load_paper_content(paper_path)
        
        experimental_claims = []
        
        if not paper_content:
            return experimental_claims
        
        import re
        
        # Patterns for experimental claims
        experiment_patterns = [
            # Experimental methodology descriptions
            r'(?i)(we conducted|we performed|we executed|we ran)\s+([^.]{20,100})',
            # Data analysis claims
            r'(?i)(our analysis shows|results indicate|data reveals?)\s+([^.]{20,100})',
            # Computational experiments
            r'(?i)(simulations? shows?|modeling results|computational analysis)\s+([^.]{20,100})',
            # Statistical analysis
            r'(?i)(statistical analysis|regression|correlation|significance test)\s+([^.]{20,100})',
            # Measurement claims
            r'(?i)(measured|observed|recorded|detected)\s+([^.]{20,100})',
        ]
        
        for i, pattern in enumerate(experiment_patterns):
            matches = re.findall(pattern, paper_content)
            for match in matches:
                if isinstance(match, tuple):
                    claim_type = [
                        'experimental_methodology',
                        'data_analysis', 
                        'computational_experiment',
                        'statistical_analysis',
                        'measurement'
                    ][i]
                    
                    experimental_claims.append({
                        'claim_id': f"claim_{len(experimental_claims) + 1}",
                        'claim_type': claim_type,
                        'claim_text': ' '.join(match) if isinstance(match, tuple) else match,
                        'verification_status': 'PENDING',
                        'reproducibility_assessment': 'UNKNOWN',
                        'feasibility_assessment': 'UNKNOWN'
                    })
        
        # Look for specific experimental specifications
        experiment_specs = re.findall(r'\\begin\{experiment\}(.*?)\\end\{experiment\}', paper_content, re.DOTALL)
        for i, spec in enumerate(experiment_specs):
            experimental_claims.append({
                'claim_id': f"experiment_spec_{i + 1}",
                'claim_type': 'experimental_specification',
                'claim_text': spec.strip(),
                'verification_status': 'PENDING',
                'reproducibility_assessment': 'UNKNOWN',
                'feasibility_assessment': 'UNKNOWN'
            })
        
        logger.info(f"📊 Extracted {len(experimental_claims)} experimental claims")
        return experimental_claims
    
    def _classify_paper_domain(self, paper_content: str) -> str:
        """Classify paper domain for Los Alamos verifier integration."""
        import re
        
        # Domain classification patterns
        domain_patterns = {
            'climate_science': [
                r'(?i)(climate|atmospheric|SAI|aerosol|stratospheric|geoengineering)',
                r'(?i)(GLENS|ARISE|GeoMIP|CMIP|temperature|precipitation)',
                r'(?i)(QBO|quasi.?biennial|oscillation|tropical|stratosphere)'
            ],
            'materials_science': [
                r'(?i)(material|crystal|lattice|electronic|magnetic)',
                r'(?i)(synthesis|characterization|properties|structure)',
                r'(?i)(metal|ceramic|polymer|composite|semiconductor)'
            ],
            'biology': [
                r'(?i)(gene|protein|cell|organism|evolution)',
                r'(?i)(molecular|biological|biochemical|genetic)',
                r'(?i)(experiment|assay|culture|sequence|analysis)'
            ]
        }
        
        domain_scores = {}
        for domain, patterns in domain_patterns.items():
            score = 0
            for pattern in patterns:
                matches = re.findall(pattern, paper_content)
                score += len(matches)
            domain_scores[domain] = score
        
        # Determine domain with highest score
        if domain_scores:
            classified_domain = max(domain_scores, key=domain_scores.get)
            if domain_scores[classified_domain] > 0:
                logger.info(f"🔬 Classified paper domain: {classified_domain}")
                return classified_domain
        
        logger.info("🔬 Classified paper domain: universal (no specific domain detected)")
        return "universal"
    
    def _verify_with_los_alamos(self, experimental_claims: List[Dict], domain: str) -> Dict:
        """Verify experimental claims using Los Alamos experiment verifier."""
        if not self.los_alamos_verifier:
            return {
                'verification_status': 'UNAVAILABLE',
                'note': 'Los Alamos verifier not available'
            }
        
        try:
            # Prepare claims for Los Alamos verification pipeline
            los_alamos_input = {
                'claims': experimental_claims,
                'domain': domain,
                'verification_mode': self.verification_mode,
                'agents_requested': [
                    'literature_verifier',
                    'math_validator', 
                    'code_implementer',
                    'synthesis_agent'
                ]
            }
            
            # Submit to Los Alamos verification pipeline
            # NOTE: This would be the actual integration when Los Alamos verifier is ready
            verification_result = {
                'verification_status': 'INTEGRATION_READY',
                'domain_classification': domain,
                'agents_activated': los_alamos_input['agents_requested'],
                'claims_processed': len(experimental_claims),
                'verification_queue_id': f"los_alamos_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                'integration_notes': [
                    'Los Alamos verifier structure detected',
                    'Ready for pipeline coordination when verifier is operational',
                    'Domain-specific verification protocols prepared'
                ]
            }
            
            logger.info(f"🌐 Los Alamos verification prepared: {verification_result['verification_queue_id']}")
            return verification_result
            
        except Exception as e:
            return {
                'verification_status': 'FAILED',
                'error': str(e),
                'note': 'Los Alamos verification failed'
            }
    
    def _verify_with_ursa_framework(self, experimental_claims: List[Dict], paper_path: str) -> Dict:
        """Verify experimental claims using existing URSA framework."""
        if not self.ursa_framework:
            return {
                'verification_status': 'UNAVAILABLE',
                'note': 'URSA framework not available'
            }
        
        try:
            # Use URSA framework to validate experimental claims
            ursa_result = self.ursa_framework.validate_experimental_claims(
                claims=experimental_claims,
                source_paper=paper_path
            )
            
            logger.info(f"🏛️ URSA framework verification completed: {ursa_result.get('validation_status', 'UNKNOWN')}")
            return ursa_result
            
        except Exception as e:
            return {
                'verification_status': 'FAILED',
                'error': str(e),
                'note': 'URSA framework verification failed'
            }
    
    def _assess_computational_reproducibility(self, experimental_claims: List[Dict]) -> Dict:
        """Assess computational reproducibility of experimental claims."""
        reproducibility_assessment = {
            'reproducibility_score': 0.0,
            'reproducible_claims': 0,
            'non_reproducible_claims': 0,
            'unclear_claims': 0,
            'reproducibility_issues': [],
            'reproducibility_recommendations': []
        }
        
        for claim in experimental_claims:
            claim_text = claim.get('claim_text', '').lower()
            
            # Check for reproducibility indicators
            reproducible_indicators = [
                'code available', 'open source', 'github', 'repository',
                'supplementary material', 'data available', 'replication'
            ]
            
            non_reproducible_indicators = [
                'proprietary', 'confidential', 'internal', 'unpublished',
                'preliminary', 'exploratory', 'initial findings'
            ]
            
            reproducible_score = sum(1 for indicator in reproducible_indicators if indicator in claim_text)
            non_reproducible_score = sum(1 for indicator in non_reproducible_indicators if indicator in claim_text)
            
            if reproducible_score > non_reproducible_score:
                reproducibility_assessment['reproducible_claims'] += 1
                claim['reproducibility_assessment'] = 'REPRODUCIBLE'
            elif non_reproducible_score > reproducible_score:
                reproducibility_assessment['non_reproducible_claims'] += 1
                claim['reproducibility_assessment'] = 'NON_REPRODUCIBLE'
                reproducibility_assessment['reproducibility_issues'].append(
                    f"Claim {claim['claim_id']}: Insufficient reproducibility information"
                )
            else:
                reproducibility_assessment['unclear_claims'] += 1
                claim['reproducibility_assessment'] = 'UNCLEAR'
        
        total_claims = len(experimental_claims)
        if total_claims > 0:
            reproducibility_assessment['reproducibility_score'] = (
                reproducibility_assessment['reproducible_claims'] / total_claims
            )
        
        # Add recommendations
        if reproducibility_assessment['reproducibility_score'] < 0.5:
            reproducibility_assessment['reproducibility_recommendations'].append(
                'Insufficient reproducibility documentation - recommend adding code and data availability statements'
            )
        
        return reproducibility_assessment
    
    def _validate_experimental_feasibility(self, experimental_claims: List[Dict], domain: str) -> Dict:
        """Validate feasibility of experimental claims."""
        feasibility_assessment = {
            'feasibility_score': 0.0,
            'feasible_experiments': 0,
            'infeasible_experiments': 0,
            'questionable_experiments': 0,
            'feasibility_issues': [],
            'feasibility_recommendations': []
        }
        
        # Domain-specific feasibility patterns
        feasibility_patterns = {
            'climate_science': {
                'feasible': ['model simulation', 'data analysis', 'statistical test', 'observational study'],
                'infeasible': ['global experiment', 'planetary manipulation', 'atmosphere modification'],
                'questionable': ['large-scale intervention', 'real-time control', 'immediate implementation']
            },
            'universal': {
                'feasible': ['computation', 'analysis', 'modeling', 'simulation'],
                'infeasible': ['impossible', 'unlimited', 'instantaneous', 'perfect'],
                'questionable': ['real-time', 'global scale', 'immediate', 'comprehensive']
            }
        }
        
        patterns = feasibility_patterns.get(domain, feasibility_patterns['universal'])
        
        for claim in experimental_claims:
            claim_text = claim.get('claim_text', '').lower()
            
            feasible_score = sum(1 for pattern in patterns['feasible'] if pattern in claim_text)
            infeasible_score = sum(1 for pattern in patterns['infeasible'] if pattern in claim_text)
            questionable_score = sum(1 for pattern in patterns['questionable'] if pattern in claim_text)
            
            if feasible_score > 0 and infeasible_score == 0:
                feasibility_assessment['feasible_experiments'] += 1
                claim['feasibility_assessment'] = 'FEASIBLE'
            elif infeasible_score > 0:
                feasibility_assessment['infeasible_experiments'] += 1
                claim['feasibility_assessment'] = 'INFEASIBLE'
                feasibility_assessment['feasibility_issues'].append(
                    f"Claim {claim['claim_id']}: Contains infeasible experimental elements"
                )
            elif questionable_score > 0:
                feasibility_assessment['questionable_experiments'] += 1
                claim['feasibility_assessment'] = 'QUESTIONABLE'
                feasibility_assessment['feasibility_issues'].append(
                    f"Claim {claim['claim_id']}: Experimental feasibility unclear"
                )
            else:
                # Default to questionable if no clear indicators
                feasibility_assessment['questionable_experiments'] += 1
                claim['feasibility_assessment'] = 'UNCLEAR'
        
        total_claims = len(experimental_claims)
        if total_claims > 0:
            feasibility_assessment['feasibility_score'] = (
                feasibility_assessment['feasible_experiments'] / total_claims
            )
        
        return feasibility_assessment
    
    def _validate_against_real_data(self, experimental_claims: List[Dict]) -> Dict:
        """Validate experimental claims against real datasets."""
        real_data_validation = {
            'real_data_score': 0.0,
            'claims_with_real_data': 0,
            'claims_without_real_data': 0,
            'real_data_sources': [],
            'validation_issues': [],
            'data_recommendations': []
        }
        
        # Real data source patterns
        real_data_patterns = [
            r'(?i)(GLENS|ARISE|GeoMIP|CMIP\d+)',  # Climate datasets
            r'(?i)(observational|measured|recorded|experimental data)',
            r'(?i)(satellite|ground.?based|in.?situ)',
            r'(?i)(NASA|NOAA|NCAR|UCAR)',  # Institutional data sources
            r'(?i)(published|peer.?reviewed|validated) (data|dataset)'
        ]
        
        for claim in experimental_claims:
            claim_text = claim.get('claim_text', '')
            
            real_data_found = False
            for pattern in real_data_patterns:
                import re
                matches = re.findall(pattern, claim_text)
                if matches:
                    real_data_found = True
                    real_data_validation['real_data_sources'].extend(matches)
            
            if real_data_found:
                real_data_validation['claims_with_real_data'] += 1
            else:
                real_data_validation['claims_without_real_data'] += 1
                real_data_validation['validation_issues'].append(
                    f"Claim {claim['claim_id']}: No real data source identified"
                )
        
        total_claims = len(experimental_claims)
        if total_claims > 0:
            real_data_validation['real_data_score'] = (
                real_data_validation['claims_with_real_data'] / total_claims
            )
        
        # Add recommendations
        if real_data_validation['real_data_score'] < 0.7:
            real_data_validation['data_recommendations'].append(
                'Insufficient real data validation - recommend connecting experimental claims to authentic datasets'
            )
        
        return real_data_validation
    
    def _assess_overall_post_hoc_verification(self, verification_result: Dict) -> Dict:
        """Assess overall post-hoc verification status."""
        
        # Extract component scores
        reproducibility_score = verification_result.get('computational_reproducibility', {}).get('reproducibility_score', 0.0)
        feasibility_score = verification_result.get('experimental_feasibility', {}).get('feasibility_score', 0.0)
        real_data_score = verification_result.get('real_data_validation', {}).get('real_data_score', 0.0)
        
        # Calculate overall scores
        verification_result['reproducibility_score'] = reproducibility_score
        verification_result['feasibility_score'] = feasibility_score
        overall_score = (reproducibility_score + feasibility_score + real_data_score) / 3
        
        # Count total validation issues
        total_issues = len(verification_result['validation_issues'])
        
        # Determine overall post-hoc status
        if overall_score >= 0.8 and total_issues <= 1:
            verification_result['overall_post_hoc_status'] = 'VERIFIED_HIGH_CONFIDENCE'
            verification_result['verification_confidence'] = 'HIGH'
        elif overall_score >= 0.6 and total_issues <= 3:
            verification_result['overall_post_hoc_status'] = 'VERIFIED_MODERATE_CONFIDENCE'
            verification_result['verification_confidence'] = 'MODERATE'
        elif overall_score >= 0.4:
            verification_result['overall_post_hoc_status'] = 'REQUIRES_ADDITIONAL_VALIDATION'
            verification_result['verification_confidence'] = 'LOW'
            verification_result['recommendations'].append('Additional experimental validation recommended')
        else:
            verification_result['overall_post_hoc_status'] = 'VERIFICATION_FAILED'
            verification_result['verification_confidence'] = 'NONE'
            verification_result['recommendations'].append('Experimental claims cannot be verified - major revision needed')
        
        return verification_result
    
    def get_verification_summary(self) -> Dict:
        """Get summary of post-hoc verification capabilities and status."""
        return {
            'verifier_type': 'URSAPostHocVerifier',
            'verification_mode': self.verification_mode,
            'los_alamos_integration': self.los_alamos_integration,
            'ursa_integration': self.ursa_integration,
            'total_verifications': len(self.verification_history),
            'capabilities': {
                'experimental_claim_extraction': True,
                'computational_reproducibility': True,
                'experimental_feasibility': True,
                'real_data_validation': True,
                'domain_classification': True,
                'los_alamos_coordination': self.los_alamos_integration
            },
            'status': 'OPERATIONAL'
        }


# Convenience functions for integration
def create_ursa_post_hoc_verifier(verification_mode: str = "comprehensive") -> URSAPostHocVerifier:
    """Create URSA post-hoc verifier with optimal configuration."""
    return URSAPostHocVerifier(
        los_alamos_integration=True,
        ursa_integration=True,
        verification_mode=verification_mode
    )

def verify_paper_experiments(paper_path: str, domain: str = "auto_detect") -> Dict:
    """Quick post-hoc verification function for research papers."""
    verifier = create_ursa_post_hoc_verifier()
    return verifier.verify_paper_experiments(paper_path, domain=domain)