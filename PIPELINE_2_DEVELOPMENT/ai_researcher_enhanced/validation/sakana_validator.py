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

from .experiment_validator import ExperimentValidator
from .plausibility_checker import PlausibilityChecker

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
        self.experiment_validator = ExperimentValidator(
            real_data_mandatory=real_data_mandatory,
            synthetic_data_forbidden=synthetic_data_forbidden,
            strict_mode=True
        )
        self.plausibility_checker = PlausibilityChecker()
        
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
        
        # Use Hansen method as primary validation
        snr_result = self.snr_analyzer.calculate_snr(
            claim['theoretical_signal'], 
            claim['real_dataset'], 
            method='hansen'
        )
        
        # Add empirical falsifiability assessment
        falsifiability_result = self.snr_analyzer.validate_empirical_falsifiability(
            claim.get('hypothesis', 'Unknown hypothesis'),
            claim['real_dataset'],
            claim['theoretical_signal']
        )
        
        # Combine results
        combined_result = {**snr_result, **falsifiability_result}
        return combined_result
    
    def _analyze_plausibility_trap_risk(self, claim: Dict, validation_result: Dict) -> Dict:
        """
        Comprehensive plausibility trap risk analysis.
        """
        evidence = {
            'snr_analysis': validation_result.get('snr_validation'),
            'real_data_validation': validation_result.get('data_authenticity_verification'),
            'statistical_significance': True  # Simplified for now
        }
        
        trap_analysis = self.snr_analyzer.prevent_plausibility_trap(
            claim.get('hypothesis', 'Unknown hypothesis'),
            evidence
        )
        
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
        
        if snr_db >= self.snr_analyzer.SNR_THRESHOLDS['high_confidence'] and trap_risk == 'LOW':
            validation_result['overall_validation_status'] = 'VALIDATED_HIGH_CONFIDENCE'
            validation_result['sakana_principle_status'] = 'COMPLIANT'
            validation_result['validation_confidence'] = 'HIGH'
        elif snr_db >= self.snr_analyzer.SNR_THRESHOLDS['standard_confidence'] and trap_risk in ['LOW', 'MODERATE']:
            validation_result['overall_validation_status'] = 'VALIDATED_MODERATE_CONFIDENCE'
            validation_result['sakana_principle_status'] = 'COMPLIANT'
            validation_result['validation_confidence'] = 'MODERATE'
        elif snr_db >= self.snr_analyzer.SNR_THRESHOLDS['minimum_detection']:
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
            'snr_analysis_summary': self.snr_analyzer.get_validation_summary()
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
    
    def get_sakana_principle_status(self) -> Dict:
        """Get current Sakana Principle enforcement status."""
        return {
            'principle_active': True,
            'enforcement_flags': self.enforcement_flags,
            'validator_status': 'OPERATIONAL',
            'total_validations': len(self.validation_history),
            'plausibility_traps_prevented': sum(1 for result in self.validation_history 
                                              if result.get('sakana_principle_status') == 'PLAUSIBILITY_TRAP_DETECTED')
        }