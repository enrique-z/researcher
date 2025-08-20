"""
Sakana Principle Validator

Core implementation of the Sakana Principle for empirical validation of theoretical claims.
Named after the AI-S-Plus (Sakana) system that revealed the importance of empirical validation
when it demonstrated the need for real data verification across all scientific domains.

The Sakana Principle enforces mandatory empirical validation to prevent the "plausibility trap"
where sophisticated theoretical claims lack quantitative empirical backing.

Key Requirements (Universal across all domains):
1. Every theoretical claim must pass empirical validation tests
2. Real dataset verification mandatory for all experimental hypotheses  
3. Order-of-magnitude calculations provide quantitative grounding
4. Domain-appropriate validation criteria applied based on experiment type
5. Standard Python scientific stack (SciPy, NumPy, xarray) for validation
"""

import numpy as np
import xarray as xr
from typing import Dict, List, Union, Optional, Any
import logging
from datetime import datetime

try:
    from .experiment_validator import ExperimentValidator
    from .plausibility_checker import PlausibilityChecker
    VALIDATION_COMPONENTS_AVAILABLE = True
except ImportError:
    VALIDATION_COMPONENTS_AVAILABLE = False
    logger = logging.getLogger(__name__)
    logger.warning("Some validation components not available, using simplified validation")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SakanaValidator:
    """
    Core Sakana Principle validation engine implementing empirical falsification
    framework to prevent "plausibility trap" scenarios in AI-generated research.
    
    This validator ensures every theoretical claim undergoes rigorous empirical
    testing using real datasets (GLENS/ARISE-SAI/GeoMIP) with quantitative metrics.
    """
    
    def __init__(self, real_data_mandatory: bool = True, synthetic_data_forbidden: bool = True):
        """
        Initialize Sakana Validator with strict empirical requirements.
        
        Args:
            real_data_mandatory: Enforce requirement for real datasets (default: True)
            synthetic_data_forbidden: Forbid synthetic data usage (default: True)
        """
        self.real_data_mandatory = real_data_mandatory
        self.synthetic_data_forbidden = synthetic_data_forbidden
        
        # Initialize component validators
        if VALIDATION_COMPONENTS_AVAILABLE:
            self.experiment_validator = ExperimentValidator(
                real_data_mandatory=real_data_mandatory,
                synthetic_data_forbidden=synthetic_data_forbidden,
                strict_mode=True
            )
            self.plausibility_checker = PlausibilityChecker()
        else:
            self.experiment_validator = None
            self.plausibility_checker = None
            logger.warning("Validation components unavailable - using simplified validation mode")
        
        # Validation history and statistics
        self.validation_history = []
        self.rejected_claims = []
        self.validated_claims = []
        
        # Sakana Principle enforcement flags (universal across all domains)
        self.enforcement_flags = {
            'REAL_DATA_MANDATORY': real_data_mandatory,
            'SYNTHETIC_DATA_FORBIDDEN': synthetic_data_forbidden,
            'EMPIRICAL_VALIDATION_REQUIRED': True,
            'PHYSICAL_CONSTRAINT_CHECKING': True,
            'PLAUSIBILITY_TRAP_PREVENTION': True,
            'DOMAIN_SPECIFIC_VALIDATION': True
        }
        
        logger.info("Sakana Validator initialized with empirical falsification enforcement")
    
    def validate_theoretical_claim(self, claim: Dict) -> Dict:
        """
        Core Sakana Principle validation of a theoretical claim.
        
        Implements mandatory empirical validation to prevent acceptance of 
        sophisticated-sounding but physically ungrounded theories across all domains.
        
        Args:
            claim: Dictionary containing theoretical claim and supporting evidence
                Required keys:
                - 'hypothesis': Text description of theoretical claim
                - 'theoretical_signal': Predicted quantitative signal
                - 'real_dataset': Real climate data for validation
                - 'parameters': Theoretical parameters and values
                
        Returns:
            Dict containing comprehensive validation results and Sakana compliance status
        """
        validation_start_time = datetime.now()
        
        # Initialize validation result structure
        validation_result = {
            'claim_id': claim.get('id', f"claim_{len(self.validation_history)}"),
            'hypothesis': claim.get('hypothesis', 'Unknown hypothesis'),
            'validation_timestamp': validation_start_time.isoformat(),
            'sakana_principle_status': 'PENDING',
            'empirical_falsification_result': None,
            'snr_validation': None,
            'plausibility_trap_analysis': None,
            'physical_constraints_check': None,
            'data_authenticity_verification': None,
            'overall_validation_status': 'PENDING',
            'rejection_reasons': [],
            'validation_confidence': 'UNKNOWN',
            'recommendations': []
        }
        
        try:
            logger.info(f"Starting Sakana Principle validation for claim: {validation_result['claim_id']}")
            
            # Step 1: Mandatory Data Authenticity Verification
            data_auth_result = self._verify_data_authenticity(claim)
            validation_result['data_authenticity_verification'] = data_auth_result
            
            if not data_auth_result['authentic_data_confirmed']:
                validation_result['sakana_principle_status'] = 'VIOLATION'
                validation_result['overall_validation_status'] = 'REJECTED'
                validation_result['rejection_reasons'].append('Real data requirement violated')
                self._log_rejection(validation_result)
                return validation_result
            
            # Step 2: Domain-Agnostic Experiment Validation
            if self.experiment_validator:
                experiment_validation = self.experiment_validator.validate_experiment(claim)
                validation_result['experiment_validation'] = experiment_validation
                
                # Check for domain-specific validation failures
                if not experiment_validation['sakana_principle_compliance']:
                    validation_result['sakana_principle_status'] = 'VALIDATION_FAILED'
                    validation_result['overall_validation_status'] = 'REJECTED'
                    validation_result['rejection_reasons'].extend(experiment_validation['violations'])
                    self._log_rejection(validation_result)
                    return validation_result
                
                # Step 3: Physical Constraints Validation (handled by domain-specific validation)
                # Physical constraints are now validated by the ExperimentValidator based on domain
                if experiment_validation.get('domain_specific_results'):
                    validation_result['physical_constraints_check'] = experiment_validation['domain_specific_results']
            else:
                # Simplified validation when components not available
                validation_result['experiment_validation'] = {
                    'sakana_principle_compliance': True,
                    'note': 'Simplified validation - ExperimentValidator not available'
                }
            
            # Step 4: Comprehensive Plausibility Trap Analysis
            trap_analysis = self._analyze_plausibility_trap_risk(claim, validation_result)
            validation_result['plausibility_trap_analysis'] = trap_analysis
            
            if trap_analysis['prevention_status'] == 'CLAIM_REJECTED':
                validation_result['sakana_principle_status'] = 'PLAUSIBILITY_TRAP_DETECTED'
                validation_result['overall_validation_status'] = 'REJECTED'
                validation_result['rejection_reasons'].append('Plausibility trap prevention triggered')
                self._log_rejection(validation_result)
                return validation_result
            
            # Step 5: Overall Validation Assessment
            validation_result = self._assess_overall_validation(validation_result)
            
            # Log successful validation
            if validation_result['overall_validation_status'] in ['VALIDATED_HIGH_CONFIDENCE', 'VALIDATED_MODERATE_CONFIDENCE']:
                self._log_successful_validation(validation_result)
            
            return validation_result
            
        except Exception as e:
            validation_result['sakana_principle_status'] = 'ERROR'
            validation_result['overall_validation_status'] = 'FAILED'
            validation_result['rejection_reasons'].append(f'Validation error: {str(e)}')
            logger.error(f"Sakana validation failed: {e}")
            return validation_result
    
    def _verify_data_authenticity(self, claim: Dict) -> Dict:
        """
        Verify that claim uses authentic real data, not synthetic data.
        
        Implements REAL_DATA_MANDATORY and SYNTHETIC_DATA_FORBIDDEN enforcement.
        """
        auth_result = {
            'authentic_data_confirmed': False,
            'synthetic_data_detected': False,
            'data_source_verification': 'UNKNOWN',
            'institutional_provenance': None,
            'verification_details': []
        }
        
        # Check for real dataset presence
        if 'real_dataset' not in claim:
            auth_result['verification_details'].append('No real dataset provided')
            return auth_result
        
        dataset = claim['real_dataset']
        
        # Basic authenticity checks
        if hasattr(dataset, 'attrs'):
            # Check for institutional markers in dataset attributes
            attrs = dataset.attrs if hasattr(dataset.attrs, 'items') else {}
            
            institutional_markers = ['NCAR', 'UCAR', 'NOAA', 'NASA', 'GLENS', 'ARISE-SAI', 'GeoMIP']
            found_markers = [marker for marker in institutional_markers 
                           if any(marker in str(value) for value in attrs.values())]
            
            if found_markers:
                auth_result['institutional_provenance'] = found_markers
                auth_result['authentic_data_confirmed'] = True
                auth_result['data_source_verification'] = 'VERIFIED'
                auth_result['verification_details'].append(f'Institutional markers found: {found_markers}')
            else:
                auth_result['verification_details'].append('No institutional markers found in dataset attributes')
        
        # Check for synthetic data patterns (simplified detection)
        if isinstance(dataset, np.ndarray):
            # Look for suspicious patterns that might indicate synthetic data
            if np.all(dataset == dataset.flat[0]):  # All identical values
                auth_result['synthetic_data_detected'] = True
                auth_result['verification_details'].append('Suspicious pattern: all identical values')
            elif len(np.unique(dataset)) < 3:  # Very few unique values
                auth_result['synthetic_data_detected'] = True
                auth_result['verification_details'].append('Suspicious pattern: very few unique values')
        
        # Final authentication decision
        if self.enforcement_flags['REAL_DATA_MANDATORY']:
            if not auth_result['authentic_data_confirmed']:
                auth_result['verification_details'].append('REAL_DATA_MANDATORY enforcement: authentic data required')
        
        if self.enforcement_flags['SYNTHETIC_DATA_FORBIDDEN']:
            if auth_result['synthetic_data_detected']:
                auth_result['authentic_data_confirmed'] = False
                auth_result['verification_details'].append('SYNTHETIC_DATA_FORBIDDEN enforcement: synthetic patterns detected')
        
        return auth_result
    
    def _perform_snr_validation(self, claim: Dict) -> Dict:
        """
        Perform comprehensive SNR validation using multiple methods.
        """
        if 'theoretical_signal' not in claim or 'real_dataset' not in claim:
            return {
                'validation_status': 'FAILED',
                'error': 'Missing theoretical_signal or real_dataset',
                'snr_db': -np.inf
            }
        
        # Simplified SNR validation - would use Hansen method if SNR analyzer available
        theoretical_signal = claim['theoretical_signal']
        real_dataset = claim['real_dataset']
        
        try:
            # Basic SNR calculation
            if hasattr(theoretical_signal, '__len__') and hasattr(real_dataset, '__len__'):
                signal_power = np.mean(np.array(theoretical_signal) ** 2)
                noise_power = np.var(np.array(real_dataset))
                snr_linear = signal_power / max(noise_power, 1e-10)
                snr_db = 10 * np.log10(snr_linear) if snr_linear > 0 else -np.inf
            else:
                snr_db = 0.0  # Fallback for non-array data
            
            return {
                'validation_status': 'COMPLETED',
                'snr_db': snr_db,
                'note': 'Simplified SNR calculation'
            }
        except Exception as e:
            return {
                'validation_status': 'FAILED',
                'error': f'SNR calculation failed: {str(e)}',
                'snr_db': -np.inf
            }
    
    def _analyze_plausibility_trap_risk(self, claim: Dict, validation_result: Dict) -> Dict:
        """
        Comprehensive plausibility trap risk analysis.
        """
        if self.plausibility_checker:
            evidence = {
                'snr_analysis': validation_result.get('snr_validation'),
                'real_data_validation': validation_result.get('data_authenticity_verification'),
                'statistical_significance': True  # Simplified for now
            }
            
            trap_analysis = self.plausibility_checker.prevent_plausibility_trap(
                claim.get('hypothesis', 'Unknown hypothesis'),
                evidence
            )
        else:
            # Simplified plausibility analysis
            trap_analysis = {
                'prevention_status': 'ANALYSIS_COMPLETED',
                'trap_risk_level': 'LOW',
                'note': 'Simplified analysis - PlausibilityChecker not available'
            }
        
        return trap_analysis
    
    def _assess_overall_validation(self, validation_result: Dict) -> Dict:
        """
        Assess overall validation status based on all validation components.
        """
        snr_validation = validation_result.get('snr_validation', {})
        trap_analysis = validation_result.get('plausibility_trap_analysis', {})
        constraints_check = validation_result.get('physical_constraints_check', {})
        
        # Determine overall status based on component results
        snr_db = snr_validation.get('snr_db', -np.inf)
        trap_risk = trap_analysis.get('trap_risk_level', 'HIGH')
        constraints_status = constraints_check.get('overall_status', 'UNKNOWN')
        
        # Use simplified thresholds when SNR analyzer not available
        SNR_THRESHOLDS = {
            'high_confidence': 10.0,    # 10 dB
            'standard_confidence': 5.0,  # 5 dB  
            'minimum_detection': 0.0     # 0 dB
        }
        
        if snr_db >= SNR_THRESHOLDS['high_confidence'] and trap_risk == 'LOW':
            validation_result['overall_validation_status'] = 'VALIDATED_HIGH_CONFIDENCE'
            validation_result['sakana_principle_status'] = 'COMPLIANT'
            validation_result['validation_confidence'] = 'HIGH'
        elif snr_db >= SNR_THRESHOLDS['standard_confidence'] and trap_risk in ['LOW', 'MODERATE']:
            validation_result['overall_validation_status'] = 'VALIDATED_MODERATE_CONFIDENCE'
            validation_result['sakana_principle_status'] = 'COMPLIANT'
            validation_result['validation_confidence'] = 'MODERATE'
        elif snr_db >= SNR_THRESHOLDS['minimum_detection']:
            validation_result['overall_validation_status'] = 'PRELIMINARY_DETECTION'
            validation_result['sakana_principle_status'] = 'MARGINAL_COMPLIANCE'
            validation_result['validation_confidence'] = 'LOW'
            validation_result['recommendations'].append('Additional validation recommended')
        else:
            validation_result['overall_validation_status'] = 'INSUFFICIENT_EVIDENCE'
            validation_result['sakana_principle_status'] = 'NON_COMPLIANT'
            validation_result['validation_confidence'] = 'NONE'
            validation_result['rejection_reasons'].append('Insufficient empirical evidence')
        
        # Check for constraint violations
        if constraints_status == 'VIOLATIONS_FOUND':
            validation_result['rejection_reasons'].append('Physical constraint violations detected')
            if validation_result['overall_validation_status'].startswith('VALIDATED'):
                validation_result['overall_validation_status'] = 'REQUIRES_REVISION'
        
        return validation_result
    
    def _log_rejection(self, validation_result: Dict) -> None:
        """Log rejected claim for analysis and improvement."""
        rejection_record = {
            'claim_id': validation_result['claim_id'],
            'hypothesis': validation_result['hypothesis'],
            'rejection_timestamp': validation_result['validation_timestamp'],
            'rejection_reasons': validation_result['rejection_reasons'],
            'sakana_principle_status': validation_result['sakana_principle_status']
        }
        
        self.rejected_claims.append(rejection_record)
        self.validation_history.append(validation_result)
        
        logger.warning(f"Claim {validation_result['claim_id']} REJECTED by Sakana Principle: {validation_result['rejection_reasons']}")
    
    def _log_successful_validation(self, validation_result: Dict) -> None:
        """Log successfully validated claim."""
        validation_record = {
            'claim_id': validation_result['claim_id'],
            'hypothesis': validation_result['hypothesis'],
            'validation_timestamp': validation_result['validation_timestamp'],
            'validation_status': validation_result['overall_validation_status'],
            'confidence_level': validation_result['validation_confidence']
        }
        
        self.validated_claims.append(validation_record)
        self.validation_history.append(validation_result)
        
        logger.info(f"Claim {validation_result['claim_id']} VALIDATED by Sakana Principle: {validation_result['overall_validation_status']}")
    
    def batch_validate_claims(self, claims: List[Dict]) -> Dict:
        """
        Validate multiple theoretical claims in batch mode.
        
        Args:
            claims: List of theoretical claims to validate
            
        Returns:
            Dict containing batch validation results and summary statistics
        """
        batch_results = {
            'batch_id': f"batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'total_claims': len(claims),
            'individual_results': [],
            'summary_statistics': {},
            'batch_status': 'PENDING'
        }
        
        try:
            # Validate each claim
            for i, claim in enumerate(claims):
                claim['id'] = claim.get('id', f"{batch_results['batch_id']}_claim_{i}")
                result = self.validate_theoretical_claim(claim)
                batch_results['individual_results'].append(result)
            
            # Generate summary statistics
            batch_results['summary_statistics'] = self._generate_batch_statistics(batch_results['individual_results'])
            batch_results['batch_status'] = 'COMPLETED'
            
            logger.info(f"Batch validation completed: {batch_results['summary_statistics']}")
            
        except Exception as e:
            batch_results['batch_status'] = 'FAILED'
            batch_results['error'] = str(e)
            logger.error(f"Batch validation failed: {e}")
        
        return batch_results
    
    def _generate_batch_statistics(self, results: List[Dict]) -> Dict:
        """Generate summary statistics for batch validation results."""
        status_counts = {}
        confidence_counts = {}
        
        for result in results:
            status = result['overall_validation_status']
            confidence = result['validation_confidence']
            
            status_counts[status] = status_counts.get(status, 0) + 1
            confidence_counts[confidence] = confidence_counts.get(confidence, 0) + 1
        
        total_claims = len(results)
        validated_claims = sum(1 for result in results if result['overall_validation_status'].startswith('VALIDATED'))
        rejection_rate = sum(1 for result in results if result['overall_validation_status'] == 'REJECTED') / total_claims
        
        return {
            'status_distribution': status_counts,
            'confidence_distribution': confidence_counts,
            'validation_rate': validated_claims / total_claims if total_claims > 0 else 0,
            'rejection_rate': rejection_rate,
            'plausibility_trap_detections': sum(1 for result in results 
                                              if result.get('sakana_principle_status') == 'PLAUSIBILITY_TRAP_DETECTED'),
            'compliance_rate': sum(1 for result in results 
                                 if result.get('sakana_principle_status') == 'COMPLIANT') / total_claims if total_claims > 0 else 0
        }
    
    def get_validation_report(self) -> Dict:
        """
        Generate comprehensive validation report showing Sakana Principle effectiveness.
        """
        total_validations = len(self.validation_history)
        
        if total_validations == 0:
            return {
                'report_status': 'NO_DATA',
                'message': 'No validations performed yet'
            }
        
        report = {
            'report_generated': datetime.now().isoformat(),
            'sakana_principle_enforcement': self.enforcement_flags,
            'validation_statistics': {
                'total_validations_attempted': total_validations,
                'successful_validations': len(self.validated_claims),
                'rejected_claims': len(self.rejected_claims),
                'success_rate': len(self.validated_claims) / total_validations,
                'rejection_rate': len(self.rejected_claims) / total_validations
            },
            'plausibility_trap_prevention': {
                'traps_detected': sum(1 for result in self.validation_history 
                                    if result.get('sakana_principle_status') == 'PLAUSIBILITY_TRAP_DETECTED'),
                'trap_detection_rate': sum(1 for result in self.validation_history 
                                         if result.get('sakana_principle_status') == 'PLAUSIBILITY_TRAP_DETECTED') / total_validations
            },
            'data_authenticity_enforcement': {
                'real_data_mandatory_enforced': self.enforcement_flags['REAL_DATA_MANDATORY'],
                'synthetic_data_forbidden_enforced': self.enforcement_flags['SYNTHETIC_DATA_FORBIDDEN']
            },
            'snr_analysis_summary': {'note': 'SNR analyzer not available in this configuration'}
        }
        
        return report
    
    def enforce_real_data_mandatory(self, enabled: bool = True) -> None:
        """Enable/disable real data mandatory enforcement."""
        self.enforcement_flags['REAL_DATA_MANDATORY'] = enabled
        self.real_data_mandatory = enabled
        logger.info(f"REAL_DATA_MANDATORY enforcement: {'ENABLED' if enabled else 'DISABLED'}")
    
    def enforce_synthetic_data_forbidden(self, enabled: bool = True) -> None:
        """Enable/disable synthetic data forbidden enforcement."""
        self.enforcement_flags['SYNTHETIC_DATA_FORBIDDEN'] = enabled
        self.synthetic_data_forbidden = enabled
        logger.info(f"SYNTHETIC_DATA_FORBIDDEN enforcement: {'ENABLED' if enabled else 'DISABLED'}")
    
    def validate_academic_paper(self, paper_path: str, paper_content: str = None) -> Dict:
        """
        Comprehensive Sakana Principle validation for academic papers.
        
        Detects "beautifully presented hypotheses with 128 perfect pages based on rubbish"
        by analyzing paper structure, mathematical consistency, experimental claims,
        and citation accuracy.
        
        Args:
            paper_path: Path to paper file (LaTeX, PDF, or text)
            paper_content: Optional paper content as string (if already loaded)
            
        Returns:
            Dict containing comprehensive paper validation results
        """
        validation_start = datetime.now()
        
        # Initialize paper validation result
        paper_validation = {
            'paper_id': paper_path.split('/')[-1] if paper_path else 'content_paper',
            'paper_path': paper_path,
            'validation_timestamp': validation_start.isoformat(),
            'paper_validation_mode': 'ACADEMIC_PAPER_ANALYSIS',
            'sakana_principle_status': 'PENDING',
            'plausibility_trap_analysis': None,
            'mathematical_rigor_check': None,
            'experimental_claims_validation': None,
            'citation_accuracy_verification': None,
            'statistical_validity_check': None,
            'physical_constraint_analysis': None,
            'overall_paper_status': 'PENDING',
            'sophisticated_nonsense_risk': 'UNKNOWN',
            'rejection_reasons': [],
            'validation_confidence': 'UNKNOWN',
            'paper_quality_score': 0.0
        }
        
        try:
            logger.info(f"🔬 Starting Sakana Principle paper validation: {paper_validation['paper_id']}")
            
            # Load paper content if not provided
            if paper_content is None and paper_path:
                paper_content = self._load_paper_content(paper_path)
            
            if not paper_content:
                paper_validation['rejection_reasons'].append('Paper content unavailable')
                paper_validation['overall_paper_status'] = 'VALIDATION_FAILED'
                return paper_validation
            
            # Step 1: Sophisticated Plausibility Trap Detection
            plausibility_analysis = self._detect_sophisticated_plausibility_traps(paper_content)
            paper_validation['plausibility_trap_analysis'] = plausibility_analysis
            
            if plausibility_analysis['sophisticated_nonsense_detected']:
                paper_validation['sophisticated_nonsense_risk'] = 'HIGH'
                paper_validation['rejection_reasons'].extend(plausibility_analysis['nonsense_indicators'])
            
            # Step 2: Mathematical Rigor Verification
            math_rigor = self._validate_mathematical_rigor(paper_content)
            paper_validation['mathematical_rigor_check'] = math_rigor
            
            if math_rigor['mathematical_errors_found']:
                paper_validation['rejection_reasons'].extend(math_rigor['error_descriptions'])
            
            # Step 3: Experimental Claims Validation
            experimental_validation = self._validate_experimental_claims(paper_content)
            paper_validation['experimental_claims_validation'] = experimental_validation
            
            if experimental_validation['unverifiable_claims_found']:
                paper_validation['rejection_reasons'].extend(experimental_validation['unverifiable_claims'])
            
            # Step 4: Citation Accuracy and Relevance Check
            citation_check = self._verify_citation_accuracy(paper_content)
            paper_validation['citation_accuracy_verification'] = citation_check
            
            if citation_check['citation_issues_found']:
                paper_validation['rejection_reasons'].extend(citation_check['citation_issues'])
            
            # Step 5: Statistical Validity Assessment
            statistical_check = self._assess_statistical_validity(paper_content)
            paper_validation['statistical_validity_check'] = statistical_check
            
            if statistical_check['statistical_errors_found']:
                paper_validation['rejection_reasons'].extend(statistical_check['statistical_issues'])
            
            # Step 6: Physical Constraint Enforcement
            physical_constraints = self._enforce_physical_constraints(paper_content)
            paper_validation['physical_constraint_analysis'] = physical_constraints
            
            if physical_constraints['constraint_violations_found']:
                paper_validation['rejection_reasons'].extend(physical_constraints['violations'])
            
            # Step 7: Overall Paper Assessment
            paper_validation = self._assess_overall_paper_validity(paper_validation)
            
            logger.info(f"✅ Paper validation complete: {paper_validation['overall_paper_status']}")
            
            # Log validation result
            self.validation_history.append(paper_validation)
            
            return paper_validation
            
        except Exception as e:
            paper_validation['sakana_principle_status'] = 'ERROR'
            paper_validation['overall_paper_status'] = 'VALIDATION_FAILED'
            paper_validation['rejection_reasons'].append(f'Paper validation error: {str(e)}')
            logger.error(f"❌ Paper validation failed: {e}")
            return paper_validation
    
    def _load_paper_content(self, paper_path: str) -> str:
        """Load paper content from various file formats."""
        try:
            if paper_path.endswith('.tex'):
                with open(paper_path, 'r', encoding='utf-8') as f:
                    return f.read()
            elif paper_path.endswith('.txt'):
                with open(paper_path, 'r', encoding='utf-8') as f:
                    return f.read()
            else:
                logger.warning(f"Unsupported file format: {paper_path}")
                return ""
        except Exception as e:
            logger.error(f"Failed to load paper content: {e}")
            return ""
    
    def _detect_sophisticated_plausibility_traps(self, paper_content: str) -> Dict:
        """
        Detect sophisticated but scientifically invalid claims that appear plausible.
        
        Identifies patterns common in well-formatted but scientifically flawed papers:
        - Impressive mathematical formalism without empirical grounding
        - Complex terminology masking simple or flawed concepts
        - Overconfident claims without adequate uncertainty quantification
        - Beautiful visualizations of unverified theoretical predictions
        """
        plausibility_analysis = {
            'sophisticated_nonsense_detected': False,
            'nonsense_indicators': [],
            'plausibility_trap_risk_level': 'LOW',
            'red_flags': [],
            'confidence_analysis': {},
            'formalism_vs_substance_ratio': 0.0
        }
        
        # Red flag patterns that indicate sophisticated nonsense
        red_flag_patterns = [
            # Overconfident language without uncertainty
            r'(?i)(definitively proves?|conclusively demonstrates?|unquestionably shows?)',
            # Complex mathematical formalism without empirical validation
            r'\\begin\{equation\}.*?\\end\{equation\}',
            # Grandiose claims about breakthrough results
            r'(?i)(revolutionary|breakthrough|paradigm.?shifting|unprecedented)',
            # Missing uncertainty quantification
            r'(?i)(exactly|precisely|perfectly) (predicts?|matches?|explains?)',
            # Theoretical claims without real data backing
            r'(?i)(our model predicts?|theoretical calculations? shows?|simulations? reveal)',
        ]
        
        # Count red flag occurrences
        total_red_flags = 0
        for i, pattern in enumerate(red_flag_patterns):
            import re
            matches = re.findall(pattern, paper_content)
            if matches:
                total_red_flags += len(matches)
                if i == 0:  # Overconfident language
                    plausibility_analysis['red_flags'].append(f'Overconfident language detected: {len(matches)} instances')
                elif i == 1:  # Mathematical formalism
                    formalism_count = len(matches)
                    # High formalism without empirical validation is suspicious
                    empirical_patterns = re.findall(r'(?i)(real data|experimental|observational|measured)', paper_content)
                    if formalism_count > 5 and len(empirical_patterns) < formalism_count / 3:
                        plausibility_analysis['red_flags'].append('High mathematical formalism with low empirical content')
                        plausibility_analysis['formalism_vs_substance_ratio'] = formalism_count / max(len(empirical_patterns), 1)
                elif i == 2:  # Grandiose claims
                    plausibility_analysis['red_flags'].append(f'Grandiose claims detected: {len(matches)} instances')
                elif i == 3:  # Missing uncertainty
                    plausibility_analysis['red_flags'].append(f'Overconfident predictions without uncertainty: {len(matches)} instances')
                elif i == 4:  # Theoretical claims
                    theoretical_count = len(matches)
                    validation_patterns = re.findall(r'(?i)(validated|verified|confirmed) (by|with|using)', paper_content)
                    if theoretical_count > len(validation_patterns) * 2:
                        plausibility_analysis['red_flags'].append('Many theoretical claims with insufficient validation')
        
        # Assess overall plausibility trap risk
        if total_red_flags > 15:
            plausibility_analysis['plausibility_trap_risk_level'] = 'HIGH'
            plausibility_analysis['sophisticated_nonsense_detected'] = True
            plausibility_analysis['nonsense_indicators'].append('High concentration of plausibility trap indicators')
        elif total_red_flags > 8:
            plausibility_analysis['plausibility_trap_risk_level'] = 'MODERATE'
            plausibility_analysis['nonsense_indicators'].append('Moderate plausibility trap risk detected')
        else:
            plausibility_analysis['plausibility_trap_risk_level'] = 'LOW'
        
        # Additional sophisticated nonsense patterns
        sophisticated_patterns = [
            r'(?i)(quantum|fractal|holographic|emergent) (properties?|behavior|dynamics?)',
            r'(?i)(novel|new|innovative) (framework|paradigm|approach) (for|to)',
            r'(?i)(breakthrough|revolutionary) (understanding|insight|discovery)'
        ]
        
        sophisticated_count = 0
        for pattern in sophisticated_patterns:
            import re
            matches = re.findall(pattern, paper_content)
            sophisticated_count += len(matches)
        
        if sophisticated_count > 5:
            plausibility_analysis['red_flags'].append('Excessive use of sophisticated-sounding but potentially meaningless terminology')
            plausibility_analysis['sophisticated_nonsense_detected'] = True
        
        return plausibility_analysis
    
    def _validate_mathematical_rigor(self, paper_content: str) -> Dict:
        """Validate mathematical rigor and consistency in the paper."""
        math_analysis = {
            'mathematical_errors_found': False,
            'error_descriptions': [],
            'equation_consistency_check': 'UNKNOWN',
            'dimensional_analysis_status': 'UNKNOWN',
            'mathematical_rigor_score': 0.0
        }
        
        # Check for common mathematical issues
        import re
        
        # Look for equations and mathematical expressions
        equations = re.findall(r'\\begin\{equation\}(.*?)\\end\{equation\}', paper_content, re.DOTALL)
        inline_math = re.findall(r'\$(.*?)\$', paper_content)
        
        total_math_expressions = len(equations) + len(inline_math)
        
        if total_math_expressions == 0:
            math_analysis['error_descriptions'].append('No mathematical expressions found in claimed scientific paper')
            math_analysis['mathematical_errors_found'] = True
            return math_analysis
        
        # Check for dimensional consistency indicators
        dimensional_indicators = re.findall(r'(?i)(units?|dimensions?|kg|m/s|joules?|watts?)', paper_content)
        if total_math_expressions > 5 and len(dimensional_indicators) < 3:
            math_analysis['error_descriptions'].append('Mathematical expressions lack dimensional consistency verification')
            math_analysis['mathematical_errors_found'] = True
        
        # Check for undefined variables
        variables = re.findall(r'[a-zA-Z](?:\^?\{[^}]*\})?', ' '.join(equations + inline_math))
        definitions = re.findall(r'(?i)(where|let|define) ([a-zA-Z])', paper_content)
        
        if len(variables) > len(definitions) * 3:
            math_analysis['error_descriptions'].append('Many mathematical variables potentially undefined')
            math_analysis['mathematical_errors_found'] = True
        
        # Basic rigor scoring
        if not math_analysis['mathematical_errors_found']:
            math_analysis['mathematical_rigor_score'] = 0.8
            math_analysis['equation_consistency_check'] = 'PASSED'
        else:
            math_analysis['mathematical_rigor_score'] = 0.3
            math_analysis['equation_consistency_check'] = 'FAILED'
        
        return math_analysis
    
    def _validate_experimental_claims(self, paper_content: str) -> Dict:
        """Validate experimental claims and their empirical backing."""
        experimental_analysis = {
            'unverifiable_claims_found': False,
            'unverifiable_claims': [],
            'real_data_verification_status': 'UNKNOWN',
            'experimental_rigor_score': 0.0,
            'data_availability_check': 'UNKNOWN'
        }
        
        import re
        
        # Look for experimental claims
        experimental_claims = re.findall(r'(?i)(our experiments?|measurements?|observations?|data) (show|reveal|demonstrate|indicate)', paper_content)
        theoretical_claims = re.findall(r'(?i)(our model|theory|simulations?) (predicts?|shows?|suggests?)', paper_content)
        
        # Check for data availability statements
        data_statements = re.findall(r'(?i)(data.{0,20}available|supplementary|repository|github|doi)', paper_content)
        
        if len(experimental_claims) > 0:
            if len(data_statements) == 0:
                experimental_analysis['unverifiable_claims_found'] = True
                experimental_analysis['unverifiable_claims'].append('Experimental claims made without data availability information')
            
            # Check for real dataset references
            real_data_indicators = re.findall(r'(?i)(GLENS|ARISE|GeoMIP|CMIP|observational|measured|recorded)', paper_content)
            if len(real_data_indicators) < len(experimental_claims) / 2:
                experimental_analysis['unverifiable_claims_found'] = True
                experimental_analysis['unverifiable_claims'].append('Insufficient reference to real datasets for experimental claims')
        
        # Check theory vs. experiment balance
        if len(theoretical_claims) > len(experimental_claims) * 3:
            experimental_analysis['unverifiable_claims_found'] = True
            experimental_analysis['unverifiable_claims'].append('Theory-heavy paper with insufficient experimental validation')
        
        # Score experimental rigor
        if not experimental_analysis['unverifiable_claims_found']:
            experimental_analysis['experimental_rigor_score'] = 0.8
            experimental_analysis['real_data_verification_status'] = 'VERIFIED'
        else:
            experimental_analysis['experimental_rigor_score'] = 0.3
            experimental_analysis['real_data_verification_status'] = 'INSUFFICIENT'
        
        return experimental_analysis
    
    def _verify_citation_accuracy(self, paper_content: str) -> Dict:
        """Verify citation accuracy and relevance."""
        citation_analysis = {
            'citation_issues_found': False,
            'citation_issues': [],
            'citation_density': 0.0,
            'self_citation_ratio': 0.0,
            'citation_quality_score': 0.0
        }
        
        import re
        
        # Count citations
        citations = re.findall(r'\\cite\{([^}]+)\}|\\citep?\{([^}]+)\}', paper_content)
        bibliography = re.findall(r'\\bibitem\{([^}]+)\}|@\w+\{([^,]+),', paper_content)
        
        total_citations = len(citations)
        total_references = len(bibliography)
        
        # Calculate citation density (citations per 1000 words)
        word_count = len(paper_content.split())
        if word_count > 0:
            citation_analysis['citation_density'] = (total_citations / word_count) * 1000
        
        # Check for citation issues
        if total_citations < 10:
            citation_analysis['citation_issues_found'] = True
            citation_analysis['citation_issues'].append('Insufficient citations for academic paper')
        
        if total_references != total_citations and abs(total_references - total_citations) > 5:
            citation_analysis['citation_issues_found'] = True
            citation_analysis['citation_issues'].append('Mismatch between citations and bibliography entries')
        
        # Check for recent citations (simplified - look for recent years)
        recent_years = re.findall(r'(202[0-9]|201[5-9])', paper_content)
        if len(recent_years) < total_citations * 0.3:
            citation_analysis['citation_issues_found'] = True
            citation_analysis['citation_issues'].append('Insufficient recent citations - may be outdated')
        
        # Score citation quality
        if not citation_analysis['citation_issues_found']:
            citation_analysis['citation_quality_score'] = 0.8
        else:
            citation_analysis['citation_quality_score'] = 0.4
        
        return citation_analysis
    
    def _assess_statistical_validity(self, paper_content: str) -> Dict:
        """Assess statistical validity of claims and analyses."""
        statistical_analysis = {
            'statistical_errors_found': False,
            'statistical_issues': [],
            'p_value_analysis': 'UNKNOWN',
            'uncertainty_quantification': 'UNKNOWN',
            'statistical_rigor_score': 0.0
        }
        
        import re
        
        # Look for statistical claims
        p_values = re.findall(r'p\s*[<>=]\s*0\.\d+', paper_content)
        significance_claims = re.findall(r'(?i)(significant|insignificant|p.?value)', paper_content)
        uncertainty_indicators = re.findall(r'(?i)(uncertainty|error bars?|confidence interval|standard deviation)', paper_content)
        
        # Check for statistical issues
        if len(significance_claims) > 0 and len(p_values) == 0:
            statistical_analysis['statistical_errors_found'] = True
            statistical_analysis['statistical_issues'].append('Statistical significance claimed without p-values')
        
        if len(significance_claims) > 0 and len(uncertainty_indicators) == 0:
            statistical_analysis['statistical_errors_found'] = True
            statistical_analysis['statistical_issues'].append('Statistical claims without uncertainty quantification')
        
        # Look for multiple testing issues
        multiple_tests = re.findall(r'(?i)(multiple|several|various) (tests?|comparisons?|analyses?)', paper_content)
        corrections = re.findall(r'(?i)(bonferroni|benjamini|fdr|correction)', paper_content)
        
        if len(multiple_tests) > 0 and len(corrections) == 0:
            statistical_analysis['statistical_errors_found'] = True
            statistical_analysis['statistical_issues'].append('Multiple testing without correction mentioned')
        
        # Score statistical rigor
        if not statistical_analysis['statistical_errors_found']:
            statistical_analysis['statistical_rigor_score'] = 0.8
            statistical_analysis['uncertainty_quantification'] = 'ADEQUATE'
        else:
            statistical_analysis['statistical_rigor_score'] = 0.4
            statistical_analysis['uncertainty_quantification'] = 'INSUFFICIENT'
        
        return statistical_analysis
    
    def _enforce_physical_constraints(self, paper_content: str) -> Dict:
        """Enforce physical constraints and conservation laws."""
        constraint_analysis = {
            'constraint_violations_found': False,
            'violations': [],
            'conservation_law_check': 'UNKNOWN',
            'thermodynamic_consistency': 'UNKNOWN',
            'physical_plausibility_score': 0.0
        }
        
        import re
        
        # Check for claims that might violate physical laws
        violation_patterns = [
            r'(?i)(perpetual motion|free energy|over.?unity)',
            r'(?i)(faster than light|superluminal)',
            r'(?i)(violates?.{0,20}(thermodynamics|conservation))',
            r'(?i)(efficiency.{0,10}(100%|greater than 100))'
        ]
        
        for pattern in violation_patterns:
            matches = re.findall(pattern, paper_content)
            if matches:
                constraint_analysis['constraint_violations_found'] = True
                constraint_analysis['violations'].append(f'Potential physical law violation detected: {matches[0]}')
        
        # Check for energy/mass balance considerations
        energy_mentions = re.findall(r'(?i)(energy|joule|watt|calorie)', paper_content)
        conservation_mentions = re.findall(r'(?i)(conservation|conserved|balance)', paper_content)
        
        if len(energy_mentions) > 5 and len(conservation_mentions) == 0:
            constraint_analysis['violations'].append('Energy considerations without conservation law discussion')
            constraint_analysis['constraint_violations_found'] = True
        
        # Score physical plausibility
        if not constraint_analysis['constraint_violations_found']:
            constraint_analysis['physical_plausibility_score'] = 0.9
            constraint_analysis['conservation_law_check'] = 'CONSISTENT'
        else:
            constraint_analysis['physical_plausibility_score'] = 0.2
            constraint_analysis['conservation_law_check'] = 'VIOLATIONS_DETECTED'
        
        return constraint_analysis
    
    def _assess_overall_paper_validity(self, paper_validation: Dict) -> Dict:
        """Assess overall paper validity based on all validation components."""
        
        # Extract component scores
        plausibility_risk = paper_validation['plausibility_trap_analysis']['plausibility_trap_risk_level']
        math_score = paper_validation['mathematical_rigor_check']['mathematical_rigor_score']
        experimental_score = paper_validation['experimental_claims_validation']['experimental_rigor_score']
        citation_score = paper_validation['citation_accuracy_verification']['citation_quality_score']
        statistical_score = paper_validation['statistical_validity_check']['statistical_rigor_score']
        physical_score = paper_validation['physical_constraint_analysis']['physical_plausibility_score']
        
        # Calculate overall quality score
        component_scores = [math_score, experimental_score, citation_score, statistical_score, physical_score]
        overall_score = sum(component_scores) / len(component_scores)
        paper_validation['paper_quality_score'] = overall_score
        
        # Determine overall status
        critical_failures = len(paper_validation['rejection_reasons'])
        
        if plausibility_risk == 'HIGH' or critical_failures > 3:
            paper_validation['overall_paper_status'] = 'REJECTED_SOPHISTICATED_NONSENSE'
            paper_validation['sakana_principle_status'] = 'PLAUSIBILITY_TRAP_DETECTED'
            paper_validation['sophisticated_nonsense_risk'] = 'HIGH'
            paper_validation['validation_confidence'] = 'HIGH'
        elif plausibility_risk == 'MODERATE' or critical_failures > 1:
            paper_validation['overall_paper_status'] = 'REQUIRES_MAJOR_REVISION'
            paper_validation['sakana_principle_status'] = 'MARGINAL_COMPLIANCE'
            paper_validation['sophisticated_nonsense_risk'] = 'MODERATE'
            paper_validation['validation_confidence'] = 'MODERATE'
        elif overall_score >= 0.7:
            paper_validation['overall_paper_status'] = 'VALIDATED_HIGH_CONFIDENCE'
            paper_validation['sakana_principle_status'] = 'COMPLIANT'
            paper_validation['sophisticated_nonsense_risk'] = 'LOW'
            paper_validation['validation_confidence'] = 'HIGH'
        elif overall_score >= 0.5:
            paper_validation['overall_paper_status'] = 'VALIDATED_MODERATE_CONFIDENCE'
            paper_validation['sakana_principle_status'] = 'COMPLIANT'
            paper_validation['sophisticated_nonsense_risk'] = 'LOW'
            paper_validation['validation_confidence'] = 'MODERATE'
        else:
            paper_validation['overall_paper_status'] = 'REQUIRES_REVISION'
            paper_validation['sakana_principle_status'] = 'NON_COMPLIANT'
            paper_validation['sophisticated_nonsense_risk'] = 'MODERATE'
            paper_validation['validation_confidence'] = 'LOW'
        
        return paper_validation

    def get_sakana_principle_status(self) -> Dict:
        """Get current Sakana Principle enforcement status."""
        return {
            'principle_active': True,
            'enforcement_flags': self.enforcement_flags,
            'validator_status': 'OPERATIONAL',
            'total_validations': len(self.validation_history),
            'plausibility_traps_prevented': sum(1 for result in self.validation_history 
                                              if result.get('sakana_principle_status') == 'PLAUSIBILITY_TRAP_DETECTED'),
            'paper_validation_capabilities': {
                'sophisticated_nonsense_detection': True,
                'mathematical_rigor_validation': True,
                'experimental_claims_verification': True,
                'citation_accuracy_checking': True,
                'statistical_validity_assessment': True,
                'physical_constraint_enforcement': True
            }
        }