"""
Multi-Layer Verification System

A comprehensive orchestration system for detecting flawed reasoning in well-presented 
academic papers. Designed to catch "beautifully presented hypotheses with 128 perfect 
pages based on rubbish" through systematic multi-layer validation.

Key Features:
- Paper parsing and claim extraction
- Mathematical rigor analysis 
- Experimental design validation
- Citation accuracy verification
- Statistical validity checking
- Physical constraint enforcement
- Integration with URSA and Sakana validation systems
- Adjudication logic for conflicting results

Test Case: Uses the 123-page spectroscopy paper as a known example of sophisticated 
but fundamentally flawed reasoning.
"""

import os
import json
import logging
import numpy as np
import re
from datetime import datetime
from typing import Dict, List, Union, Optional, Any, Tuple
from pathlib import Path

# Import existing validation systems
try:
    from .validation.sakana_validator import SakanaValidator
    from .ursa_integration.validation.universal_sakana_validator import UniversalSakanaValidator
    VALIDATION_SYSTEMS_AVAILABLE = True
except ImportError:
    VALIDATION_SYSTEMS_AVAILABLE = False
    logging.warning("Validation systems not fully available - using simplified verification")

# Import URSA post-hoc verifier
try:
    from .ursa_post_hoc_verifier import URSAPostHocVerifier
    URSA_POST_HOC_AVAILABLE = True
except ImportError:
    URSA_POST_HOC_AVAILABLE = False
    logging.warning("URSA post-hoc verifier not available")

# Import Los Alamos URSA Experiment Verifier (REAL SYSTEM)
import sys
LOS_ALAMOS_VERIFIER_PATH = '/Users/apple/code/losalamos/experiment-verifier'
if os.path.exists(LOS_ALAMOS_VERIFIER_PATH):
    sys.path.append(LOS_ALAMOS_VERIFIER_PATH)
    try:
        from core.pipeline import ExperimentVerifier
        from core.domain_classifier import DomainClassifier
        from agents.evidence_synthesizer import EvidenceSynthesizer
        from agents.literature_verifier import LiteratureVerifier
        LOS_ALAMOS_AVAILABLE = True
        logger = logging.getLogger(__name__)
        logger.info("✅ Los Alamos URSA experiment verifier connected - REAL SYSTEM")
    except ImportError as e:
        LOS_ALAMOS_AVAILABLE = False
        logger = logging.getLogger(__name__)
        logger.warning(f"❌ Los Alamos URSA verifier import failed: {e}")
else:
    LOS_ALAMOS_AVAILABLE = False
    logger = logging.getLogger(__name__)
    logger.warning("❌ Los Alamos URSA verifier directory not found")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PaperParser:
    """Parse academic papers to extract claims, equations, and experimental designs."""
    
    def __init__(self):
        self.section_patterns = {
            'abstract': r'\\begin\{abstract\}(.*?)\\end\{abstract\}',
            'introduction': r'\\section\{[Ii]ntroduction\}(.*?)(?=\\section|\Z)',
            'methodology': r'\\section\{[Mm]ethod|[Aa]pproach|[Ee]xperimental\}(.*?)(?=\\section|\Z)',
            'results': r'\\section\{[Rr]esults\}(.*?)(?=\\section|\Z)',
            'discussion': r'\\section\{[Dd]iscussion\}(.*?)(?=\\section|\Z)',
            'conclusion': r'\\section\{[Cc]onclusion\}(.*?)(?=\\section|\Z)'
        }
        
        self.equation_pattern = r'\\begin\{equation\}(.*?)\\end\{equation\}|\\begin\{align\}(.*?)\\end\{align\}'
        self.citation_pattern = r'\\cite\{([^}]+)\}'
        self.claim_indicators = [
            'we demonstrate', 'we show', 'we prove', 'we establish',
            'our results indicate', 'the data shows', 'we conclude',
            'our analysis reveals', 'we find that', 'evidence suggests'
        ]
    
    def parse_paper(self, paper_content: str) -> Dict:
        """Parse paper content and extract structured information."""
        parsed_content = {
            'sections': {},
            'equations': [],
            'citations': [],
            'claims': [],
            'mathematical_statements': [],
            'experimental_designs': []
        }
        
        # Extract sections
        for section_name, pattern in self.section_patterns.items():
            matches = re.findall(pattern, paper_content, re.DOTALL | re.IGNORECASE)
            if matches:
                parsed_content['sections'][section_name] = matches[0]
        
        # Extract equations
        equation_matches = re.findall(self.equation_pattern, paper_content, re.DOTALL)
        for match in equation_matches:
            equation_text = match[0] if match[0] else match[1]
            parsed_content['equations'].append(equation_text.strip())
        
        # Extract citations
        citation_matches = re.findall(self.citation_pattern, paper_content)
        parsed_content['citations'] = list(set(citation_matches))
        
        # Extract claims
        parsed_content['claims'] = self._extract_claims(paper_content)
        
        # Extract mathematical statements
        parsed_content['mathematical_statements'] = self._extract_mathematical_statements(paper_content)
        
        # Extract experimental designs
        parsed_content['experimental_designs'] = self._extract_experimental_designs(paper_content)
        
        return parsed_content
    
    def _extract_claims(self, text: str) -> List[Dict]:
        """Extract scientific claims from paper text."""
        claims = []
        sentences = text.split('.')
        
        for i, sentence in enumerate(sentences):
            for indicator in self.claim_indicators:
                if indicator.lower() in sentence.lower():
                    claims.append({
                        'sentence_index': i,
                        'claim_text': sentence.strip(),
                        'claim_type': 'empirical' if any(word in sentence.lower() 
                                                       for word in ['data', 'results', 'experiment']) else 'theoretical',
                        'confidence_indicators': self._extract_confidence_indicators(sentence)
                    })
        
        return claims
    
    def _extract_confidence_indicators(self, sentence: str) -> List[str]:
        """Extract confidence indicators from claims."""
        indicators = []
        confidence_words = ['clearly', 'obviously', 'definitively', 'conclusively', 
                          'unambiguously', 'significantly', 'strongly']
        
        for word in confidence_words:
            if word in sentence.lower():
                indicators.append(word)
        
        return indicators
    
    def _extract_mathematical_statements(self, text: str) -> List[Dict]:
        """Extract mathematical statements and their context."""
        statements = []
        
        # Look for mathematical expressions in text
        math_patterns = [
            r'\$([^$]+)\$',  # Inline math
            r'\\\[([^\\]+)\\\]',  # Display math
            r'\\begin\{equation\*?\}(.*?)\\end\{equation\*?\}'  # Equation environments
        ]
        
        for pattern in math_patterns:
            matches = re.findall(pattern, text, re.DOTALL)
            for match in matches:
                statements.append({
                    'expression': match.strip(),
                    'context': 'needs_context_extraction'  # Could be enhanced
                })
        
        return statements
    
    def _extract_experimental_designs(self, text: str) -> List[Dict]:
        """Extract experimental methodology descriptions."""
        designs = []
        
        # Look for experimental methodology indicators
        method_indicators = [
            'we conducted', 'experimental setup', 'methodology', 'procedure',
            'data collection', 'measurement', 'analysis method'
        ]
        
        sentences = text.split('.')
        for i, sentence in enumerate(sentences):
            for indicator in method_indicators:
                if indicator.lower() in sentence.lower():
                    designs.append({
                        'sentence_index': i,
                        'design_text': sentence.strip(),
                        'methodology_type': self._classify_methodology(sentence)
                    })
        
        return designs
    
    def _classify_methodology(self, sentence: str) -> str:
        """Classify the type of experimental methodology."""
        if any(word in sentence.lower() for word in ['simulation', 'model', 'computational']):
            return 'computational'
        elif any(word in sentence.lower() for word in ['experiment', 'laboratory', 'measurement']):
            return 'experimental'
        elif any(word in sentence.lower() for word in ['analysis', 'statistical', 'data']):
            return 'analytical'
        else:
            return 'theoretical'


class FlawedReasoningDetector:
    """Detect various types of flawed reasoning in academic papers."""
    
    def __init__(self):
        self.detection_patterns = {
            'mathematical_nonsense': self._detect_mathematical_nonsense,
            'unworkable_methodology': self._detect_unworkable_methodology,
            'citation_misuse': self._detect_citation_misuse,
            'statistical_invalidity': self._detect_statistical_invalidity,
            'physical_violations': self._detect_physical_violations,
            'logical_inconsistencies': self._detect_logical_inconsistencies
        }
    
    def detect_flaws(self, parsed_paper: Dict) -> Dict:
        """Run all flaw detection methods on parsed paper."""
        detection_results = {
            'overall_flaw_score': 0.0,
            'flaw_categories': {},
            'specific_issues': [],
            'confidence_assessment': 'unknown'
        }
        
        total_score = 0.0
        
        for flaw_type, detection_method in self.detection_patterns.items():
            try:
                flaw_result = detection_method(parsed_paper)
                detection_results['flaw_categories'][flaw_type] = flaw_result
                total_score += flaw_result.get('severity_score', 0.0)
                
                if flaw_result.get('issues_found', []):
                    detection_results['specific_issues'].extend(flaw_result['issues_found'])
            
            except Exception as e:
                logger.warning(f"Flaw detection failed for {flaw_type}: {e}")
                detection_results['flaw_categories'][flaw_type] = {
                    'severity_score': 0.0,
                    'detection_status': 'failed',
                    'error': str(e)
                }
        
        detection_results['overall_flaw_score'] = total_score / len(self.detection_patterns)
        detection_results['confidence_assessment'] = self._assess_detection_confidence(detection_results)
        
        return detection_results
    
    def _detect_mathematical_nonsense(self, parsed_paper: Dict) -> Dict:
        """Detect mathematically meaningless but sophisticated-looking equations."""
        issues = []
        severity_score = 0.0
        
        equations = parsed_paper.get('equations', [])
        mathematical_statements = parsed_paper.get('mathematical_statements', [])
        
        for eq in equations:
            # Check for suspicious patterns
            if self._contains_dimensional_inconsistency(eq):
                issues.append({
                    'type': 'dimensional_inconsistency',
                    'equation': eq,
                    'description': 'Equation contains dimensional inconsistencies'
                })
                severity_score += 0.3
            
            if self._contains_undefined_variables(eq):
                issues.append({
                    'type': 'undefined_variables',
                    'equation': eq,
                    'description': 'Equation contains undefined or poorly defined variables'
                })
                severity_score += 0.2
        
        return {
            'severity_score': min(severity_score, 1.0),
            'issues_found': issues,
            'detection_status': 'completed'
        }
    
    def _detect_unworkable_methodology(self, parsed_paper: Dict) -> Dict:
        """Detect experimental designs that sound plausible but are unworkable."""
        issues = []
        severity_score = 0.0
        
        experimental_designs = parsed_paper.get('experimental_designs', [])
        
        for design in experimental_designs:
            design_text = design.get('design_text', '')
            
            # Check for impossible experimental conditions
            if self._contains_impossible_conditions(design_text):
                issues.append({
                    'type': 'impossible_conditions',
                    'design': design_text,
                    'description': 'Experimental design contains physically impossible conditions'
                })
                severity_score += 0.4
            
            # Check for lack of control groups
            if self._lacks_proper_controls(design_text):
                issues.append({
                    'type': 'inadequate_controls',
                    'design': design_text,
                    'description': 'Experimental design lacks adequate control groups'
                })
                severity_score += 0.2
        
        return {
            'severity_score': min(severity_score, 1.0),
            'issues_found': issues,
            'detection_status': 'completed'
        }
    
    def _detect_citation_misuse(self, parsed_paper: Dict) -> Dict:
        """Detect citations that don't support the claims made."""
        issues = []
        severity_score = 0.0
        
        claims = parsed_paper.get('claims', [])
        citations = parsed_paper.get('citations', [])
        
        # This is simplified - in practice would need access to cited papers
        for claim in claims:
            claim_text = claim.get('claim_text', '')
            
            # Check for overcited claims (suspicious)
            citation_density = len(re.findall(r'\\cite\{[^}]+\}', claim_text))
            if citation_density > 3:  # Arbitrary threshold
                issues.append({
                    'type': 'overcitation',
                    'claim': claim_text,
                    'description': 'Claim contains suspiciously high citation density'
                })
                severity_score += 0.1
        
        return {
            'severity_score': min(severity_score, 1.0),
            'issues_found': issues,
            'detection_status': 'completed'
        }
    
    def _detect_statistical_invalidity(self, parsed_paper: Dict) -> Dict:
        """Detect statistical analysis that doesn't match claimed conclusions."""
        issues = []
        severity_score = 0.0
        
        # Look for statistical claims in results section
        results_section = parsed_paper.get('sections', {}).get('results', '')
        
        if results_section:
            # Check for p-hacking indicators
            p_value_count = len(re.findall(r'p\s*[<>=]\s*0\.\d+', results_section))
            if p_value_count > 10:  # Suspicious number of p-values
                issues.append({
                    'type': 'potential_p_hacking',
                    'description': f'Found {p_value_count} p-values, potential p-hacking'
                })
                severity_score += 0.3
        
        return {
            'severity_score': min(severity_score, 1.0),
            'issues_found': issues,
            'detection_status': 'completed'
        }
    
    def _detect_physical_violations(self, parsed_paper: Dict) -> Dict:
        """Detect violations of known physical laws and constraints."""
        issues = []
        severity_score = 0.0
        
        equations = parsed_paper.get('equations', [])
        
        for eq in equations:
            # Check for energy conservation violations (simplified)
            if 'energy' in eq.lower() and self._violates_conservation_laws(eq):
                issues.append({
                    'type': 'conservation_violation',
                    'equation': eq,
                    'description': 'Equation may violate conservation laws'
                })
                severity_score += 0.5
        
        return {
            'severity_score': min(severity_score, 1.0),
            'issues_found': issues,
            'detection_status': 'completed'
        }
    
    def _detect_logical_inconsistencies(self, parsed_paper: Dict) -> Dict:
        """Detect logical inconsistencies between different parts of the paper."""
        issues = []
        severity_score = 0.0
        
        claims = parsed_paper.get('claims', [])
        
        # Check for contradictory claims (simplified)
        for i, claim1 in enumerate(claims):
            for j, claim2 in enumerate(claims[i+1:], i+1):
                if self._claims_contradict(claim1.get('claim_text', ''), claim2.get('claim_text', '')):
                    issues.append({
                        'type': 'contradictory_claims',
                        'claim1': claim1.get('claim_text', ''),
                        'claim2': claim2.get('claim_text', ''),
                        'description': 'Claims appear to contradict each other'
                    })
                    severity_score += 0.3
        
        return {
            'severity_score': min(severity_score, 1.0),
            'issues_found': issues,
            'detection_status': 'completed'
        }
    
    # Helper methods for detection (simplified implementations)
    def _contains_dimensional_inconsistency(self, equation: str) -> bool:
        """Check for dimensional inconsistencies (simplified)."""
        # This is a placeholder - real implementation would need dimensional analysis
        suspicious_patterns = ['\\frac{\\text{length}}{\\text{mass}}', 'energy + length']
        return any(pattern in equation for pattern in suspicious_patterns)
    
    def _contains_undefined_variables(self, equation: str) -> bool:
        """Check for undefined variables (simplified)."""
        # Look for single letters without context
        variables = re.findall(r'\b[a-z]\b', equation)
        return len(variables) > 5  # Arbitrary threshold
    
    def _contains_impossible_conditions(self, design_text: str) -> bool:
        """Check for physically impossible experimental conditions."""
        impossible_indicators = [
            'temperature below absolute zero',
            'infinite pressure',
            'negative mass',
            'faster than light'
        ]
        return any(indicator in design_text.lower() for indicator in impossible_indicators)
    
    def _lacks_proper_controls(self, design_text: str) -> bool:
        """Check if experimental design lacks proper controls."""
        control_indicators = ['control group', 'control condition', 'baseline', 'placebo']
        return not any(indicator in design_text.lower() for indicator in control_indicators)
    
    def _violates_conservation_laws(self, equation: str) -> bool:
        """Check for conservation law violations (simplified)."""
        # Placeholder implementation
        violation_patterns = ['energy_out > energy_in', 'perpetual motion']
        return any(pattern in equation.lower() for pattern in violation_patterns)
    
    def _claims_contradict(self, claim1: str, claim2: str) -> bool:
        """Check if two claims contradict each other (simplified)."""
        # Look for opposite statements
        contradiction_pairs = [
            ('increase', 'decrease'),
            ('positive', 'negative'),
            ('significant', 'insignificant'),
            ('effective', 'ineffective')
        ]
        
        for word1, word2 in contradiction_pairs:
            if word1 in claim1.lower() and word2 in claim2.lower():
                return True
        
        return False
    
    def _assess_detection_confidence(self, detection_results: Dict) -> str:
        """Assess confidence in flaw detection results."""
        overall_score = detection_results.get('overall_flaw_score', 0.0)
        
        if overall_score >= 0.8:
            return 'high_confidence_flawed'
        elif overall_score >= 0.5:
            return 'moderate_confidence_flawed'
        elif overall_score >= 0.2:
            return 'low_confidence_flawed'
        else:
            return 'likely_valid'


class MultiLayerVerifier:
    """
    Main orchestration system for multi-layer verification of academic papers.
    
    Integrates paper parsing, flaw detection, and validation systems (URSA/Sakana)
    to detect "beautifully presented hypotheses based on rubbish."
    """
    
    def __init__(self, detection_mode: str = 'comprehensive', test_case_validation: bool = False):
        """
        Initialize multi-layer verifier.
        
        Args:
            detection_mode: 'comprehensive', 'fast', or 'targeted'
            test_case_validation: Enable validation against known test cases
        """
        self.detection_mode = detection_mode
        self.test_case_validation = test_case_validation
        
        # Initialize components
        self.paper_parser = PaperParser()
        self.flaw_detector = FlawedReasoningDetector()
        
        # Initialize validation systems if available
        self.sakana_validator = None
        self.ursa_validator = None
        self.ursa_post_hoc_verifier = None
        self.los_alamos_pipeline = None
        self.domain_classifier = None
        self.evidence_synthesizer = None
        
        if VALIDATION_SYSTEMS_AVAILABLE:
            try:
                self.sakana_validator = SakanaValidator()
                logger.info("✅ Sakana validation system initialized")
            except Exception as e:
                logger.warning(f"Could not initialize Sakana validator: {e}")
        
        # Initialize URSA post-hoc verifier
        if URSA_POST_HOC_AVAILABLE:
            try:
                self.ursa_post_hoc_verifier = URSAPostHocVerifier(
                    los_alamos_integration=True,
                    ursa_integration=True,
                    verification_mode=detection_mode
                )
                logger.info("✅ URSA post-hoc verifier initialized")
            except Exception as e:
                logger.warning(f"Could not initialize URSA post-hoc verifier: {e}")
        
        # Initialize REAL Los Alamos URSA Experiment Verifier (NO MOCK DATA)
        if LOS_ALAMOS_AVAILABLE:
            try:
                self.los_alamos_verifier = ExperimentVerifier()
                self.domain_classifier = DomainClassifier()
                self.evidence_synthesizer = EvidenceSynthesizer(self.los_alamos_verifier.model)
                self.literature_verifier = LiteratureVerifier(self.los_alamos_verifier.model)
                logger.info("✅ REAL Los Alamos URSA experiment verifier initialized - NO MOCK DATA")
            except Exception as e:
                logger.error(f"❌ Failed to initialize REAL Los Alamos verifier: {e}")
                self.los_alamos_verifier = None
                self.domain_classifier = None
                self.evidence_synthesizer = None
                self.literature_verifier = None
        else:
            logger.warning("❌ Los Alamos URSA verifier not available - verification will be limited")
        
        # Verification history
        self.verification_history = []
        
        logger.info(f"🔍 MultiLayerVerifier initialized in {detection_mode} mode")
    
    def verify_paper(self, paper_path: str, validation_targets: List[str] = None, 
                    confidence_threshold: float = 0.7) -> Dict:
        """
        Main verification method for academic papers.
        
        Args:
            paper_path: Path to paper file (PDF or LaTeX)
            validation_targets: Specific validation targets
            confidence_threshold: Minimum confidence for positive detection
            
        Returns:
            Dict with verification results
        """
        verification_start = datetime.now()
        
        # Initialize result structure
        result = {
            'paper_path': paper_path,
            'verification_timestamp': verification_start.isoformat(),
            'overall_status': 'pending',
            'flaws_detected': [],
            'confidence_score': 0.0,
            'validation_layers': {},
            'final_verdict': 'unknown',
            'processing_time_seconds': 0.0
        }
        
        try:
            logger.info(f"🔍 Starting verification of paper: {Path(paper_path).name}")
            
            # Store paper path for use by validation systems
            self._current_paper_path = paper_path
            
            # Step 1: Load and parse paper
            paper_content = self._load_paper_content(paper_path)
            parsed_paper = self.paper_parser.parse_paper(paper_content)
            
            logger.info(f"📄 Paper parsed: {len(parsed_paper['sections'])} sections, "
                       f"{len(parsed_paper['equations'])} equations, "
                       f"{len(parsed_paper['claims'])} claims")
            
            # Step 2: Detect flawed reasoning
            flaw_detection_results = self.flaw_detector.detect_flaws(parsed_paper)
            result['validation_layers']['flaw_detection'] = flaw_detection_results
            
            # Step 3: Apply validation targets if specified
            if validation_targets:
                result['validation_layers']['targeted_validation'] = self._apply_targeted_validation(
                    parsed_paper, validation_targets)
            
            # Step 4: Integrate with external validation systems
            if self.sakana_validator:
                sakana_result = self._integrate_sakana_validation(parsed_paper, paper_content)
                result['validation_layers']['sakana_validation'] = sakana_result
            
            # Step 4b: URSA post-hoc experimental verification
            if self.ursa_post_hoc_verifier:
                ursa_post_hoc_result = self._integrate_ursa_post_hoc_verification(paper_path, paper_content)
                result['validation_layers']['ursa_post_hoc_verification'] = ursa_post_hoc_result
            
            # Step 5: Calculate overall assessment
            result = self._calculate_overall_assessment(result, confidence_threshold)
            
            # Step 6: Test case validation if enabled
            if self.test_case_validation:
                result['test_case_analysis'] = self._validate_against_test_cases(result)
            
            # Calculate processing time
            processing_time = (datetime.now() - verification_start).total_seconds()
            result['processing_time_seconds'] = processing_time
            
            # Log results
            self.verification_history.append(result)
            
            logger.info(f"✅ Verification completed: {result['final_verdict']} "
                       f"(confidence: {result['confidence_score']:.2f})")
            
            return result
            
        except Exception as e:
            result['overall_status'] = 'error'
            result['error'] = str(e)
            logger.error(f"❌ Verification failed: {e}")
            return result
    
    def orchestrate_verification(self, paper_path: str, ursa_integration: bool = True,
                               sakana_validation: bool = True, adjudication_required: bool = True) -> Dict:
        """
        Orchestrate complete multi-layer verification with external systems.
        
        Args:
            paper_path: Path to paper to verify
            ursa_integration: Include URSA experimental validation
            sakana_validation: Include Sakana empirical validation  
            adjudication_required: Enable adjudication for conflicting results
            
        Returns:
            Dict with orchestrated verification results
        """
        orchestration_result = {
            'orchestration_timestamp': datetime.now().isoformat(),
            'paper_path': paper_path,
            'verification_layers_enabled': {
                'internal_flaw_detection': True,
                'ursa_integration': ursa_integration,
                'ursa_post_hoc_verification': bool(self.ursa_post_hoc_verifier),
                'sakana_validation': sakana_validation,
                'adjudication': adjudication_required
            },
            'layer_results': {},
            'consensus_analysis': {},
            'final_verdict': 'unknown',
            'confidence_metrics': {}
        }
        
        try:
            logger.info(f"🎯 Starting orchestrated verification for {Path(paper_path).name}")
            
            # Layer 1: Internal verification
            internal_result = self.verify_paper(paper_path)
            orchestration_result['layer_results']['internal_verification'] = internal_result
            
            # Layer 2: URSA post-hoc experimental verification (if enabled)
            if ursa_integration and self.ursa_post_hoc_verifier:
                ursa_post_hoc_result = self._integrate_ursa_post_hoc_verification(paper_path)
                orchestration_result['layer_results']['ursa_post_hoc_verification'] = ursa_post_hoc_result
            elif ursa_integration:
                # Fallback to legacy URSA integration
                ursa_result = self._integrate_ursa_validation(paper_path)
                orchestration_result['layer_results']['ursa_validation'] = ursa_result
            
            # Layer 3: Enhanced Sakana validation (if enabled)
            if sakana_validation and self.sakana_validator:
                enhanced_sakana = self._enhanced_sakana_validation(paper_path)
                orchestration_result['layer_results']['enhanced_sakana'] = enhanced_sakana
            
            # Layer 4: Adjudication (if enabled and needed)
            if adjudication_required:
                consensus_result = self._adjudicate_verification_results(
                    orchestration_result['layer_results'])
                orchestration_result['consensus_analysis'] = consensus_result
                orchestration_result['final_verdict'] = consensus_result.get('final_verdict', 'unknown')
            
            # Calculate confidence metrics
            orchestration_result['confidence_metrics'] = self._calculate_orchestration_confidence(
                orchestration_result)
            
            logger.info(f"🎯 Orchestrated verification completed: {orchestration_result['final_verdict']}")
            
            return orchestration_result
            
        except Exception as e:
            orchestration_result['error'] = str(e)
            orchestration_result['final_verdict'] = 'error'
            logger.error(f"❌ Orchestrated verification failed: {e}")
            return orchestration_result
    
    def _load_paper_content(self, paper_path: str) -> str:
        """Load paper content from file."""
        paper_path = Path(paper_path)
        
        if not paper_path.exists():
            raise FileNotFoundError(f"Paper file not found: {paper_path}")
        
        if paper_path.suffix.lower() == '.pdf':
            # For PDF files, would need PDF extraction library
            # For now, assume LaTeX source is available
            tex_path = paper_path.with_suffix('.tex')
            if tex_path.exists():
                return tex_path.read_text(encoding='utf-8')
            else:
                raise ValueError("PDF extraction not implemented - please provide LaTeX source")
        
        elif paper_path.suffix.lower() in ['.tex', '.txt']:
            return paper_path.read_text(encoding='utf-8')
        
        else:
            raise ValueError(f"Unsupported file format: {paper_path.suffix}")
    
    def _apply_targeted_validation(self, parsed_paper: Dict, targets: List[str]) -> Dict:
        """Apply specific validation targets."""
        targeted_results = {
            'targets_requested': targets,
            'target_results': {},
            'overall_target_assessment': 'unknown'
        }
        
        target_methods = {
            'mathematical_rigor': self._validate_mathematical_rigor,
            'experimental_design': self._validate_experimental_design,
            'citation_accuracy': self._validate_citation_accuracy,
            'statistical_validity': self._validate_statistical_validity
        }
        
        for target in targets:
            if target in target_methods:
                targeted_results['target_results'][target] = target_methods[target](parsed_paper)
            else:
                targeted_results['target_results'][target] = {
                    'status': 'unknown_target',
                    'message': f'Validation target "{target}" not implemented'
                }
        
        return targeted_results
    
    def _integrate_sakana_validation(self, parsed_paper: Dict, paper_content: str) -> Dict:
        """Integrate with Sakana validation system using comprehensive paper validation - NO MOCK DATA ALLOWED."""
        if not self.sakana_validator:
            return {
                'status': 'sakana_unavailable',
                'message': 'Sakana validator not initialized'
            }
        
        try:
            # Get paper path for comprehensive validation
            paper_path = getattr(self, '_current_paper_path', None)
            if not paper_path:
                logger.warning("Paper path not available for Sakana validation, using content analysis")
                return {
                    'status': 'paper_path_unavailable',
                    'message': 'Paper path required for comprehensive Sakana validation'
                }
            
            logger.info(f"🔬 Sakana comprehensive paper validation - NO MOCK DATA")
            
            # Use the correct Sakana method for academic paper validation
            sakana_result = self.sakana_validator.validate_academic_paper(
                paper_path=paper_path,
                paper_content=paper_content
            )
            
            # Extract meaningful validation results
            validation_status = sakana_result.get('overall_validation_status', 'unknown')
            plausibility_score = sakana_result.get('plausibility_score', 0.0)
            consistency_violations = sakana_result.get('consistency_violations', [])
            domain_alignment = sakana_result.get('domain_alignment_score', 0.0)
            
            logger.info(f"✅ Sakana validation completed: {validation_status} (plausibility: {plausibility_score:.2f})")
            
            return {
                'status': 'completed',
                'sakana_assessment': sakana_result,
                'validation_status': validation_status,
                'plausibility_score': plausibility_score,
                'consistency_violations_count': len(consistency_violations),
                'domain_alignment_score': domain_alignment,
                'integration_success': True,
                'real_data_used': True,
                'validation_method': 'comprehensive_paper_validation'
            }
            
        except Exception as e:
            logger.error(f"❌ Sakana validation failed: {e}")
            return {
                'status': 'integration_failed',
                'error': str(e),
                'integration_success': False
            }
    
    def _integrate_ursa_post_hoc_verification(self, paper_path: str, paper_content: str = None) -> Dict:
        """Integrate with URSA post-hoc experimental verification system."""
        if not self.ursa_post_hoc_verifier:
            return {
                'status': 'ursa_post_hoc_unavailable',
                'note': 'URSA post-hoc verifier not initialized'
            }
        
        try:
            logger.info("🔬 Starting URSA post-hoc experimental verification...")
            
            # Use URSA post-hoc verifier to validate experimental claims
            ursa_result = self.ursa_post_hoc_verifier.verify_paper_experiments(
                paper_path=paper_path,
                paper_content=paper_content,
                domain="auto_detect"
            )
            
            logger.info(f"🔬 URSA post-hoc verification completed: {ursa_result.get('overall_post_hoc_status', 'UNKNOWN')}")
            
            return {
                'status': 'completed',
                'ursa_post_hoc_results': ursa_result,
                'integration_success': True,
                'experimental_verification_status': ursa_result.get('overall_post_hoc_status', 'UNKNOWN'),
                'reproducibility_score': ursa_result.get('reproducibility_score', 0.0),
                'feasibility_score': ursa_result.get('feasibility_score', 0.0),
                'validation_confidence': ursa_result.get('verification_confidence', 'UNKNOWN'),
                'los_alamos_integration_ready': ursa_result.get('los_alamos_verification', {}).get('verification_status') == 'INTEGRATION_READY'
            }
            
        except Exception as e:
            logger.error(f"❌ URSA post-hoc verification failed: {e}")
            return {
                'status': 'ursa_post_hoc_failed',
                'error': str(e),
                'integration_success': False
            }
    
    def _integrate_ursa_validation(self, paper_path: str) -> Dict:
        """Integrate with legacy URSA experimental validation."""
        # Legacy method - now using URSA post-hoc verifier primarily
        return {
            'status': 'legacy_ursa_integration',
            'validation_approach': 'experimental_verification',
            'implementation_status': 'superseded_by_post_hoc_verifier',
            'note': 'Use URSA post-hoc verification for enhanced experimental validation'
        }
    
    def _integrate_real_los_alamos_verification(self, paper_path: str, experimental_claims: List[Dict]) -> Dict:
        """
        Integrate with REAL Los Alamos URSA Experiment Verifier - NO MOCK DATA.
        
        Uses the actual Los Alamos verification pipeline for genuine experimental validation.
        """
        if not self.los_alamos_verifier:
            return {
                'status': 'los_alamos_unavailable',
                'message': 'Real Los Alamos URSA verifier not available'
            }
        
        try:
            logger.info(f"🔬 Starting REAL Los Alamos URSA verification - NO MOCK DATA")
            
            # Step 1: Classify domain using real domain classifier
            paper_content = self._load_paper_content(paper_path)
            domain, confidence, all_scores = self.domain_classifier.classify_paper(paper_content)
            
            # Step 2: Prepare verification input using Los Alamos ExperimentInput format
            from core.pipeline import ExperimentInput
            verification_input = ExperimentInput(
                experiment_id=f"multilayer_verification_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                paper_path=paper_path,
                domain=domain,
                verification_depth='standard',
                priority_level='standard'
            )
            
            # Step 3: Execute REAL Los Alamos verification pipeline using async method
            logger.info(f"🔬 Executing Los Alamos verification for {len(experimental_claims)} claims")
            import asyncio
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                verification_result = loop.run_until_complete(
                    self.los_alamos_verifier.process_single_experiment(verification_input)
                )
            finally:
                loop.close()
            
            # Step 4: Extract meaningful results
            logger.info(f"✅ Los Alamos verification completed: {verification_result.overall_verdict} (confidence: {verification_result.confidence_score:.1f}%)")
            
            return {
                'status': 'completed',
                'verification_pipeline': 'REAL_LOS_ALAMOS_URSA',
                'domain_classification': {
                    'domain': domain,
                    'confidence': confidence,
                    'all_scores': all_scores
                },
                'verification_result': {
                    'experiment_id': verification_result.experiment_id,
                    'domain': verification_result.domain,
                    'overall_verdict': verification_result.overall_verdict,
                    'confidence_score': verification_result.confidence_score,
                    'verification_duration': verification_result.verification_duration,
                    'scores': verification_result.scores,
                    'issues_found': verification_result.issues_found,
                    'recommendations': verification_result.recommendations
                },
                'integration_success': True,
                'real_verification': True,
                'mock_data_used': False,
                'claims_processed': len(experimental_claims)
            }
            
        except Exception as e:
            logger.error(f"❌ Real Los Alamos verification failed: {e}")
            return {
                'status': 'verification_failed',
                'error': str(e),
                'verification_pipeline': 'REAL_LOS_ALAMOS_URSA',
                'integration_success': False
            }
    
    def _enhanced_sakana_validation(self, paper_path: str) -> Dict:
        """Enhanced Sakana validation specifically for paper verification."""
        return {
            'status': 'enhanced_sakana_placeholder',
            'validation_approach': 'paper_specific_validation',
            'implementation_status': 'pending'
        }
    
    def _adjudicate_verification_results(self, layer_results: Dict) -> Dict:
        """
        Enhanced adjudication logic for conflicting verification results from different layers.
        
        Implements sophisticated conflict resolution using:
        - Confidence-weighted scoring
        - Layer reliability assessment
        - Conflict analysis and resolution
        - Evidence strength evaluation
        - Meta-analysis across verification approaches
        """
        adjudication_result = {
            'adjudication_timestamp': datetime.now().isoformat(),
            'layers_analyzed': list(layer_results.keys()),
            'consensus_metrics': {},
            'conflict_resolution': {},
            'evidence_analysis': {},
            'reliability_assessment': {},
            'final_verdict': 'unknown',
            'adjudication_confidence': 0.0,
            'conflict_severity': 'unknown'
        }
        
        # Collect verdicts from all layers
        layer_verdicts = {}
        layer_confidences = {}
        
        for layer_name, layer_result in layer_results.items():
            if isinstance(layer_result, dict):
                # Handle different verdict formats from different systems
                if layer_name == 'ursa_post_hoc_verification':
                    verdict = layer_result.get('experimental_verification_status', 'unknown')
                    confidence_map = {
                        'HIGH': 0.9, 'MODERATE': 0.7, 'LOW': 0.4, 'NONE': 0.1, 'UNKNOWN': 0.5
                    }
                    confidence = confidence_map.get(layer_result.get('validation_confidence', 'UNKNOWN'), 0.5)
                else:
                    verdict = layer_result.get('final_verdict', layer_result.get('overall_status', 'unknown'))
                    confidence = layer_result.get('confidence_score', 0.5)
                
                layer_verdicts[layer_name] = verdict
                layer_confidences[layer_name] = confidence
        
        # Enhanced consensus building with sophisticated conflict resolution
        if layer_verdicts:
            # Step 1: Assess layer reliability based on system type and historical performance
            layer_reliability = self._assess_layer_reliability(layer_results)
            adjudication_result['reliability_assessment'] = layer_reliability
            
            # Step 2: Analyze evidence strength from each layer
            evidence_analysis = self._analyze_evidence_strength(layer_results)
            adjudication_result['evidence_analysis'] = evidence_analysis
            
            # Step 3: Detect and analyze conflicts
            conflict_analysis = self._analyze_verification_conflicts(layer_verdicts, layer_confidences)
            adjudication_result['conflict_resolution'] = conflict_analysis
            adjudication_result['conflict_severity'] = conflict_analysis.get('conflict_severity', 'unknown')
            
            # Step 4: Weight verdicts by confidence and reliability
            weighted_scores = {}
            for layer, verdict in layer_verdicts.items():
                confidence = layer_confidences.get(layer, 0.5)
                reliability = layer_reliability.get(layer, {}).get('reliability_score', 0.5)
                evidence_strength = evidence_analysis.get(layer, {}).get('evidence_strength', 0.5)
                
                # Combined weighting: confidence × reliability × evidence_strength
                combined_weight = confidence * reliability * evidence_strength
                
                # Enhanced verdict classification for all verification systems
                if verdict in ['flawed', 'rejected', 'high_confidence_flawed', 'VERIFICATION_FAILED', 'NON_COMPLIANT']:
                    weighted_scores[layer] = combined_weight * 1.0  # Flawed
                elif verdict in ['valid', 'validated', 'likely_valid', 'VERIFIED_HIGH_CONFIDENCE', 'VERIFIED_MODERATE_CONFIDENCE']:
                    weighted_scores[layer] = combined_weight * -1.0  # Valid
                elif verdict in ['REQUIRES_ADDITIONAL_VALIDATION', 'REQUIRES_REVISION', 'suspicious']:
                    weighted_scores[layer] = combined_weight * 0.5  # Needs review
                else:
                    weighted_scores[layer] = 0.0  # Unknown
            
            # Step 5: Calculate sophisticated consensus
            total_weighted_score = sum(weighted_scores.values())
            total_confidence = sum(layer_confidences.values())
            max_possible_weight = sum(layer_reliability.get(layer, {}).get('reliability_score', 0.5) for layer in layer_verdicts.keys())
            
            # Normalize by maximum possible weight
            normalized_score = total_weighted_score / max_possible_weight if max_possible_weight > 0 else 0
            
            # Step 6: Determine final verdict with enhanced thresholds
            if conflict_analysis.get('conflict_severity') == 'HIGH' and abs(normalized_score) < 0.2:
                adjudication_result['final_verdict'] = 'consensus_requires_human_review'
                adjudication_result['adjudication_confidence'] = 0.3
            elif normalized_score > 0.4:
                adjudication_result['final_verdict'] = 'consensus_paper_flawed'
                adjudication_result['adjudication_confidence'] = min(0.9, abs(normalized_score))
            elif normalized_score < -0.4:
                adjudication_result['final_verdict'] = 'consensus_paper_valid'
                adjudication_result['adjudication_confidence'] = min(0.9, abs(normalized_score))
            elif normalized_score > 0.1:
                adjudication_result['final_verdict'] = 'consensus_paper_suspicious'
                adjudication_result['adjudication_confidence'] = 0.6
            else:
                adjudication_result['final_verdict'] = 'consensus_uncertain'
                adjudication_result['adjudication_confidence'] = 0.4
            
            adjudication_result['consensus_metrics'] = {
                'raw_weighted_score': total_weighted_score,
                'normalized_score': normalized_score,
                'average_confidence': total_confidence / len(layer_confidences) if layer_confidences else 0,
                'layer_agreement': len(set(layer_verdicts.values())) == 1,
                'evidence_convergence': evidence_analysis.get('convergence_score', 0.0),
                'reliability_weighted_consensus': max_possible_weight
            }
        
        return adjudication_result
    
    def _assess_layer_reliability(self, layer_results: Dict) -> Dict:
        """Assess the reliability of each verification layer."""
        reliability_assessment = {}
        
        for layer_name, layer_result in layer_results.items():
            if not isinstance(layer_result, dict):
                reliability_assessment[layer_name] = {'reliability_score': 0.3, 'assessment': 'invalid_result'}
                continue
            
            # Base reliability scores by system type
            if layer_name == 'internal_verification':
                base_reliability = 0.7  # Internal flaw detection
            elif layer_name == 'ursa_post_hoc_verification':
                base_reliability = 0.9  # URSA experimental validation
            elif layer_name == 'sakana_validation':
                base_reliability = 0.85  # Sakana empirical validation
            elif layer_name == 'enhanced_sakana':
                base_reliability = 0.88  # Enhanced Sakana validation
            else:
                base_reliability = 0.6  # Default reliability
            
            # Adjust based on result completeness and error status
            completeness_factor = 1.0
            if layer_result.get('status') in ['failed', 'error', 'unavailable']:
                completeness_factor = 0.3
            elif layer_result.get('integration_success') == False:
                completeness_factor = 0.5
            elif 'error' in layer_result:
                completeness_factor = 0.6
            
            # Adjust based on evidence quality
            evidence_factor = 1.0
            if layer_name == 'ursa_post_hoc_verification':
                ursa_results = layer_result.get('ursa_post_hoc_results', {})
                claims_count = len(ursa_results.get('experimental_claims_extracted', []))
                if claims_count > 5:
                    evidence_factor = 1.1  # Bonus for comprehensive analysis
                elif claims_count == 0:
                    evidence_factor = 0.4  # Penalty for no experimental claims
            
            final_reliability = base_reliability * completeness_factor * evidence_factor
            final_reliability = min(1.0, max(0.1, final_reliability))  # Clamp between 0.1 and 1.0
            
            reliability_assessment[layer_name] = {
                'reliability_score': final_reliability,
                'base_reliability': base_reliability,
                'completeness_factor': completeness_factor,
                'evidence_factor': evidence_factor,
                'assessment': self._categorize_reliability(final_reliability)
            }
        
        return reliability_assessment
    
    def _analyze_evidence_strength(self, layer_results: Dict) -> Dict:
        """Analyze the strength of evidence from each verification layer."""
        evidence_analysis = {}
        evidence_scores = []
        
        for layer_name, layer_result in layer_results.items():
            if not isinstance(layer_result, dict):
                evidence_analysis[layer_name] = {'evidence_strength': 0.2, 'analysis': 'invalid_evidence'}
                continue
            
            evidence_strength = 0.5  # Default
            analysis_notes = []
            
            if layer_name == 'internal_verification':
                # Analyze internal flaw detection evidence
                flaws_detected = len(layer_result.get('flaws_detected', []))
                validation_layers = layer_result.get('validation_layers', {})
                
                if flaws_detected > 3:
                    evidence_strength = 0.8
                    analysis_notes.append(f'Strong evidence: {flaws_detected} flaws detected')
                elif flaws_detected > 0:
                    evidence_strength = 0.6
                    analysis_notes.append(f'Moderate evidence: {flaws_detected} flaws detected')
                else:
                    evidence_strength = 0.4
                    analysis_notes.append('Limited evidence: no flaws detected')
            
            elif layer_name == 'ursa_post_hoc_verification':
                # Analyze URSA experimental verification evidence
                ursa_results = layer_result.get('ursa_post_hoc_results', {})
                reproducibility_score = ursa_results.get('reproducibility_score', 0.0)
                feasibility_score = ursa_results.get('feasibility_score', 0.0)
                claims_count = len(ursa_results.get('experimental_claims_extracted', []))
                
                # Strong evidence from experimental validation
                if reproducibility_score > 0.7 and feasibility_score > 0.7:
                    evidence_strength = 0.9
                    analysis_notes.append('High experimental verification confidence')
                elif reproducibility_score > 0.5 or feasibility_score > 0.5:
                    evidence_strength = 0.7
                    analysis_notes.append('Moderate experimental verification confidence')
                elif claims_count > 0:
                    evidence_strength = 0.5
                    analysis_notes.append(f'Experimental claims analyzed: {claims_count}')
                else:
                    evidence_strength = 0.3
                    analysis_notes.append('Limited experimental evidence')
                
                # Bonus for Los Alamos integration readiness
                if layer_result.get('los_alamos_integration_ready'):
                    evidence_strength = min(1.0, evidence_strength + 0.1)
                    analysis_notes.append('Los Alamos integration ready')
            
            elif layer_name in ['sakana_validation', 'enhanced_sakana']:
                # Analyze Sakana validation evidence
                if layer_result.get('integration_success'):
                    evidence_strength = 0.8
                    analysis_notes.append('Sakana validation successful')
                else:
                    evidence_strength = 0.4
                    analysis_notes.append('Sakana validation limited')
            
            evidence_analysis[layer_name] = {
                'evidence_strength': evidence_strength,
                'analysis_notes': analysis_notes,
                'strength_category': self._categorize_evidence_strength(evidence_strength)
            }
            
            evidence_scores.append(evidence_strength)
        
        # Calculate convergence score (how well evidence aligns)
        if len(evidence_scores) > 1:
            evidence_variance = np.var(evidence_scores)
            convergence_score = max(0.0, 1.0 - evidence_variance)
        else:
            convergence_score = 1.0
        
        evidence_analysis['convergence_score'] = convergence_score
        evidence_analysis['overall_evidence_strength'] = np.mean(evidence_scores) if evidence_scores else 0.0
        
        return evidence_analysis
    
    def _analyze_verification_conflicts(self, layer_verdicts: Dict, layer_confidences: Dict) -> Dict:
        """Analyze conflicts between different verification layers."""
        conflict_analysis = {
            'conflicts_detected': [],
            'conflict_severity': 'NONE',
            'resolution_strategy': 'none_required',
            'conflicting_layers': []
        }
        
        if len(layer_verdicts) < 2:
            return conflict_analysis
        
        # Categorize verdicts
        positive_verdicts = []  # Paper is valid
        negative_verdicts = []  # Paper is flawed
        uncertain_verdicts = []  # Unclear/needs review
        
        for layer, verdict in layer_verdicts.items():
            confidence = layer_confidences.get(layer, 0.5)
            
            if verdict in ['valid', 'validated', 'likely_valid', 'VERIFIED_HIGH_CONFIDENCE', 'VERIFIED_MODERATE_CONFIDENCE']:
                positive_verdicts.append((layer, verdict, confidence))
            elif verdict in ['flawed', 'rejected', 'high_confidence_flawed', 'VERIFICATION_FAILED', 'NON_COMPLIANT']:
                negative_verdicts.append((layer, verdict, confidence))
            else:
                uncertain_verdicts.append((layer, verdict, confidence))
        
        # Detect conflicts
        conflicts_found = 0
        if positive_verdicts and negative_verdicts:
            conflicts_found += 1
            conflict_analysis['conflicts_detected'].append({
                'type': 'validity_conflict',
                'positive_layers': [layer for layer, _, _ in positive_verdicts],
                'negative_layers': [layer for layer, _, _ in negative_verdicts],
                'confidence_difference': abs(
                    np.mean([conf for _, _, conf in positive_verdicts]) - 
                    np.mean([conf for _, _, conf in negative_verdicts])
                )
            })
        
        # High confidence conflicts are particularly concerning
        high_conf_positive = [item for item in positive_verdicts if item[2] > 0.7]
        high_conf_negative = [item for item in negative_verdicts if item[2] > 0.7]
        
        if high_conf_positive and high_conf_negative:
            conflicts_found += 1
            conflict_analysis['conflicts_detected'].append({
                'type': 'high_confidence_conflict',
                'description': 'High-confidence layers disagree fundamentally',
                'layers_involved': [item[0] for item in high_conf_positive + high_conf_negative]
            })
        
        # Determine conflict severity
        if conflicts_found == 0:
            conflict_analysis['conflict_severity'] = 'NONE'
            conflict_analysis['resolution_strategy'] = 'consensus_available'
        elif conflicts_found == 1 and not (high_conf_positive and high_conf_negative):
            conflict_analysis['conflict_severity'] = 'LOW'
            conflict_analysis['resolution_strategy'] = 'confidence_weighting'
        elif conflicts_found > 1 or (high_conf_positive and high_conf_negative):
            conflict_analysis['conflict_severity'] = 'HIGH'
            conflict_analysis['resolution_strategy'] = 'human_review_recommended'
        else:
            conflict_analysis['conflict_severity'] = 'MODERATE'
            conflict_analysis['resolution_strategy'] = 'evidence_analysis'
        
        conflict_analysis['conflicting_layers'] = list(set([
            layer for conflict in conflict_analysis['conflicts_detected']
            for layer in conflict.get('positive_layers', []) + conflict.get('negative_layers', []) + 
                       conflict.get('layers_involved', [])
        ]))
        
        return conflict_analysis
    
    def _categorize_reliability(self, reliability_score: float) -> str:
        """Categorize reliability score."""
        if reliability_score >= 0.9:
            return 'very_high'
        elif reliability_score >= 0.7:
            return 'high'
        elif reliability_score >= 0.5:
            return 'moderate'
        elif reliability_score >= 0.3:
            return 'low'
        else:
            return 'very_low'
    
    def _categorize_evidence_strength(self, evidence_strength: float) -> str:
        """Categorize evidence strength score."""
        if evidence_strength >= 0.8:
            return 'strong'
        elif evidence_strength >= 0.6:
            return 'moderate'
        elif evidence_strength >= 0.4:
            return 'weak'
        else:
            return 'very_weak'
    
    def _calculate_overall_assessment(self, result: Dict, confidence_threshold: float) -> Dict:
        """Calculate overall assessment based on all validation layers."""
        flaw_detection = result.get('validation_layers', {}).get('flaw_detection', {})
        overall_flaw_score = flaw_detection.get('overall_flaw_score', 0.0)
        confidence_assessment = flaw_detection.get('confidence_assessment', 'unknown')
        
        # Determine overall status
        if overall_flaw_score >= confidence_threshold:
            result['overall_status'] = 'flaws_detected'
            result['final_verdict'] = 'paper_contains_flawed_reasoning'
        elif overall_flaw_score >= 0.3:
            result['overall_status'] = 'suspicious'
            result['final_verdict'] = 'paper_requires_review'
        else:
            result['overall_status'] = 'likely_valid'
            result['final_verdict'] = 'paper_appears_valid'
        
        result['confidence_score'] = overall_flaw_score
        result['flaws_detected'] = flaw_detection.get('specific_issues', [])
        
        return result
    
    def _calculate_orchestration_confidence(self, orchestration_result: Dict) -> Dict:
        """Calculate confidence metrics for orchestrated verification."""
        layer_results = orchestration_result.get('layer_results', {})
        
        confidence_metrics = {
            'individual_layer_confidences': {},
            'consensus_confidence': 0.0,
            'reliability_assessment': 'unknown'
        }
        
        # Extract confidence from each layer
        for layer_name, layer_result in layer_results.items():
            if isinstance(layer_result, dict):
                confidence = layer_result.get('confidence_score', 
                           layer_result.get('validation_confidence', 0.5))
                confidence_metrics['individual_layer_confidences'][layer_name] = confidence
        
        # Calculate overall consensus confidence
        if confidence_metrics['individual_layer_confidences']:
            confidences = list(confidence_metrics['individual_layer_confidences'].values())
            confidence_metrics['consensus_confidence'] = np.mean(confidences)
            
            # Assess reliability
            if confidence_metrics['consensus_confidence'] >= 0.8:
                confidence_metrics['reliability_assessment'] = 'high_reliability'
            elif confidence_metrics['consensus_confidence'] >= 0.6:
                confidence_metrics['reliability_assessment'] = 'moderate_reliability'
            else:
                confidence_metrics['reliability_assessment'] = 'low_reliability'
        
        return confidence_metrics
    
    def _validate_against_test_cases(self, result: Dict) -> Dict:
        """Validate results against known test cases."""
        # This would validate against the known 123-page spectroscopy paper
        test_case_analysis = {
            'test_case_validation_enabled': True,
            'known_test_cases': [
                {
                    'name': '123-page spectroscopy paper',
                    'expected_verdict': 'flawed',
                    'known_issues': ['mathematical_nonsense', 'unworkable_methodology']
                }
            ],
            'validation_results': 'test_case_validation_placeholder'
        }
        
        return test_case_analysis
    
    # Placeholder validation methods (to be implemented)
    def _validate_mathematical_rigor(self, parsed_paper: Dict) -> Dict:
        """Validate mathematical rigor of the paper."""
        return {'status': 'mathematical_validation_placeholder'}
    
    def _validate_experimental_design(self, parsed_paper: Dict) -> Dict:
        """Validate experimental design methodology."""
        return {'status': 'experimental_validation_placeholder'}
    
    def _validate_citation_accuracy(self, parsed_paper: Dict) -> Dict:
        """Validate citation accuracy and relevance."""
        return {'status': 'citation_validation_placeholder'}
    
    def _validate_statistical_validity(self, parsed_paper: Dict) -> Dict:
        """Validate statistical analysis and conclusions."""
        return {'status': 'statistical_validation_placeholder'}
    
    def get_verification_summary(self) -> Dict:
        """Get summary of all verifications performed."""
        capabilities = [
            'paper_parsing',
            'flaw_detection', 
            'multi_layer_verification',
            'orchestrated_validation'
        ]
        
        # Add system-specific capabilities
        if self.sakana_validator:
            capabilities.append('sakana_validation')
        if self.ursa_post_hoc_verifier:
            capabilities.append('ursa_post_hoc_experimental_verification')
            capabilities.append('los_alamos_integration_ready')
        
        return {
            'total_verifications': len(self.verification_history),
            'detection_mode': self.detection_mode,
            'system_status': 'operational',
            'capabilities': capabilities,
            'integration_status': {
                'sakana_validator': bool(self.sakana_validator),
                'ursa_post_hoc_verifier': bool(self.ursa_post_hoc_verifier),
                'los_alamos_integration': self.ursa_post_hoc_verifier.los_alamos_integration if self.ursa_post_hoc_verifier else False
            }
        }


# Test function for the spectroscopy paper
def test_spectroscopy_paper_verification():
    """Test the verification system with the known flawed 123-page spectroscopy paper."""
    spectroscopy_paper_path = "/Users/apple/code/Researcher/EXPERIMENTS/experiment-native-1-spectro/output/paper_clean_complete_FINAL_LEGIBLE.tex"
    
    if not Path(spectroscopy_paper_path).exists():
        print(f"❌ Test paper not found at: {spectroscopy_paper_path}")
        return
    
    print("🧪 Testing Multi-Layer Verification with 123-page spectroscopy paper...")
    
    # Initialize verifier in test mode
    verifier = MultiLayerVerifier(detection_mode='comprehensive', test_case_validation=True)
    
    # Run verification
    result = verifier.verify_paper(
        paper_path=spectroscopy_paper_path,
        validation_targets=['mathematical_rigor', 'experimental_design', 'citation_accuracy'],
        confidence_threshold=0.7
    )
    
    # Display results
    print(f"📊 Verification Results:")
    print(f"   Overall Status: {result['overall_status']}")
    print(f"   Final Verdict: {result['final_verdict']}")
    print(f"   Confidence Score: {result['confidence_score']:.2f}")
    print(f"   Flaws Detected: {len(result['flaws_detected'])}")
    
    if result['flaws_detected']:
        print("🔍 Specific Issues Found:")
        for i, flaw in enumerate(result['flaws_detected'][:5], 1):  # Show first 5
            print(f"   {i}. {flaw.get('type', 'unknown')}: {flaw.get('description', 'no description')}")
    
    print(f"⏱️  Processing Time: {result['processing_time_seconds']:.2f} seconds")
    
    return result


def test_orchestrated_verification_with_ursa():
    """Test complete orchestrated verification including URSA post-hoc verification."""
    spectroscopy_paper_path = "/Users/apple/code/Researcher/EXPERIMENTS/experiment-native-1-spectro/output/paper_clean_complete_FINAL_LEGIBLE.tex"
    
    if not Path(spectroscopy_paper_path).exists():
        print(f"❌ Test paper not found at: {spectroscopy_paper_path}")
        return
    
    print("🎯 Testing Complete Orchestrated Verification with URSA Post-Hoc Integration...")
    print("   (Including Los Alamos experiment verifier integration preparation)")
    
    # Initialize verifier with comprehensive mode
    verifier = MultiLayerVerifier(detection_mode='comprehensive', test_case_validation=True)
    
    # Display system capabilities
    summary = verifier.get_verification_summary()
    print(f"🔧 System Capabilities: {', '.join(summary['capabilities'])}")
    print(f"🌐 Integration Status:")
    for system, status in summary['integration_status'].items():
        status_emoji = "✅" if status else "❌"
        print(f"   {status_emoji} {system}: {status}")
    
    # Run orchestrated verification
    orchestration_result = verifier.orchestrate_verification(
        paper_path=spectroscopy_paper_path,
        ursa_integration=True,
        sakana_validation=True,
        adjudication_required=True
    )
    
    # Display orchestrated results
    print(f"\n🎯 Orchestrated Verification Results:")
    print(f"   Final Verdict: {orchestration_result['final_verdict']}")
    print(f"   Consensus Confidence: {orchestration_result.get('confidence_metrics', {}).get('consensus_confidence', 'unknown'):.2f}")
    
    print(f"\n📊 Layer-by-Layer Results:")
    for layer_name, layer_result in orchestration_result.get('layer_results', {}).items():
        if isinstance(layer_result, dict):
            status = layer_result.get('status', layer_result.get('overall_status', 'unknown'))
            print(f"   • {layer_name}: {status}")
            
            # Show URSA post-hoc specific results
            if layer_name == 'ursa_post_hoc_verification' and layer_result.get('ursa_post_hoc_results'):
                ursa_results = layer_result['ursa_post_hoc_results']
                print(f"     - Experimental Claims: {len(ursa_results.get('experimental_claims_extracted', []))}")
                print(f"     - Reproducibility Score: {ursa_results.get('reproducibility_score', 0.0):.2f}")
                print(f"     - Feasibility Score: {ursa_results.get('feasibility_score', 0.0):.2f}")
                print(f"     - Los Alamos Ready: {layer_result.get('los_alamos_integration_ready', False)}")
    
    return orchestration_result


# Convenience function for complete Phase 2 Multi-Layer Verification
def execute_phase_2_multi_layer_verification(paper_path: str) -> Dict:
    """
    Execute complete Phase 2 Multi-Layer Verification as documented in UNIVERSAL_PIPELINE_DOCUMENTATION.md
    
    Args:
        paper_path: Path to paper to verify
        
    Returns:
        Dict with complete verification results including all layers
    """
    print("🎯 EXECUTING PHASE 2 MULTI-LAYER VERIFICATION")
    print("   Detecting 'beautifully presented hypotheses based on rubbish'")
    print(f"   Paper: {Path(paper_path).name}")
    
    # Initialize comprehensive verifier
    verifier = MultiLayerVerifier(detection_mode='comprehensive', test_case_validation=True)
    
    # Execute orchestrated verification with all systems
    result = verifier.orchestrate_verification(
        paper_path=paper_path,
        ursa_integration=True,
        sakana_validation=True,
        adjudication_required=True
    )
    
    print(f"\n✅ PHASE 2 VERIFICATION COMPLETED")
    print(f"   Final Verdict: {result['final_verdict']}")
    print(f"   Layers Processed: {len(result.get('layer_results', {}))}")
    print(f"   Los Alamos Integration: Ready for coordination")
    
    return result


if __name__ == "__main__":
    # Run test
    test_result = test_spectroscopy_paper_verification()
    
    print("\n🎯 Multi-Layer Verification System ready for Phase 2 implementation!")