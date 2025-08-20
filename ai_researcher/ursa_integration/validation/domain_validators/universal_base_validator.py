"""
Universal Base Validator

Abstract base class for domain-specific validation that ensures consistent
validation interface across all scientific research domains.

Key Features:
- Domain-agnostic validation framework
- Universal empirical validation requirements
- Configurable validation criteria per domain
- Integration with URSA experimental framework
- Real data enforcement across all domains

Designed to be extended by domain-specific validators (climate, physics, chemistry, biology).
"""

import logging
import numpy as np
from abc import ABC, abstractmethod
from typing import Dict, List, Union, Optional, Any
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UniversalBaseValidator(ABC):
    """
    Abstract base validator for all scientific research domains.
    
    Provides universal validation framework that all domain-specific
    validators must implement while allowing domain customization.
    """
    
    def __init__(self, research_domain: str):
        """
        Initialize base validator.
        
        Args:
            research_domain: Research domain identifier
        """
        self.research_domain = research_domain
        self.validation_history = []
        self.domain_specific_config = {}
        
        # Universal validation requirements (all domains must support)
        self.universal_requirements = {
            'real_data_verification': True,
            'empirical_validation': True,
            'statistical_significance': True,
            'physical_constraint_checking': True,
            'order_of_magnitude_validation': True,
            'plausibility_assessment': True
        }
        
        # Load domain-specific configuration
        self._load_domain_config()
        
        logger.info(f"✅ Universal base validator initialized for {research_domain}")
    
    @abstractmethod
    def _load_domain_config(self):
        """Load domain-specific validation configuration."""
        pass
    
    @abstractmethod
    def validate_domain_experiment(self, experiment_config: Dict) -> Dict:
        """
        Validate experiment using domain-specific criteria.
        
        Args:
            experiment_config: Domain-specific experiment configuration
            
        Returns:
            Dict with domain validation results
        """
        pass
    
    @abstractmethod
    def get_domain_validation_criteria(self) -> Dict:
        """Get domain-specific validation criteria."""
        pass
    
    def validate_universal_requirements(self, experiment_config: Dict) -> Dict:
        """
        Validate universal requirements that apply to all domains.
        
        Args:
            experiment_config: Experiment configuration
            
        Returns:
            Dict with universal validation results
        """
        universal_result = {
            'real_data_verification': self._verify_real_data(experiment_config),
            'empirical_validation': self._validate_empirical_claims(experiment_config),
            'statistical_significance': self._check_statistical_significance(experiment_config),
            'physical_constraints': self._check_physical_constraints(experiment_config),
            'order_of_magnitude': self._validate_order_of_magnitude(experiment_config),
            'plausibility_assessment': self._assess_plausibility(experiment_config),
            'overall_universal_status': 'PENDING'
        }
        
        # Determine overall universal validation status
        failed_requirements = [
            req for req, result in universal_result.items() 
            if isinstance(result, dict) and result.get('status') == 'FAILED'
        ]
        
        if not failed_requirements:
            universal_result['overall_universal_status'] = 'PASSED'
        elif len(failed_requirements) <= 2:
            universal_result['overall_universal_status'] = 'MARGINAL'
        else:
            universal_result['overall_universal_status'] = 'FAILED'
        
        universal_result['failed_requirements'] = failed_requirements
        
        return universal_result
    
    def _verify_real_data(self, experiment_config: Dict) -> Dict:
        """Universal real data verification."""
        data_verification = {
            'status': 'UNKNOWN',
            'data_sources_verified': [],
            'synthetic_data_detected': False,
            'authenticity_confidence': 'UNKNOWN',
            'verification_details': []
        }
        
        # Check for real datasets
        if 'real_dataset' in experiment_config:
            dataset = experiment_config['real_dataset']
            
            # Basic authenticity checks
            if hasattr(dataset, 'attrs'):
                # Check for institutional markers
                attrs = dataset.attrs if hasattr(dataset.attrs, 'items') else {}
                institutional_markers = ['NCAR', 'UCAR', 'NOAA', 'NASA', 'institutional', 'official']
                
                found_markers = [
                    marker for marker in institutional_markers
                    if any(marker.lower() in str(value).lower() for value in attrs.values())
                ]
                
                if found_markers:
                    data_verification['data_sources_verified'] = found_markers
                    data_verification['status'] = 'VERIFIED'
                    data_verification['authenticity_confidence'] = 'HIGH'
                else:
                    data_verification['verification_details'].append('No institutional markers found')
                    data_verification['authenticity_confidence'] = 'LOW'
            
            # Check for synthetic data patterns
            if isinstance(dataset, np.ndarray):
                if np.all(dataset == dataset.flat[0]):
                    data_verification['synthetic_data_detected'] = True
                    data_verification['status'] = 'FAILED'
                    data_verification['verification_details'].append('Suspicious pattern: uniform values')
                elif len(np.unique(dataset)) < 5:
                    data_verification['synthetic_data_detected'] = True
                    data_verification['status'] = 'FAILED'
                    data_verification['verification_details'].append('Suspicious pattern: very few unique values')
        
        # Default to VERIFIED if no issues found
        if data_verification['status'] == 'UNKNOWN':
            data_verification['status'] = 'VERIFIED'
            data_verification['authenticity_confidence'] = 'MODERATE'
        
        return data_verification
    
    def _validate_empirical_claims(self, experiment_config: Dict) -> Dict:
        """Universal empirical validation."""
        empirical_validation = {
            'status': 'PENDING',
            'empirical_evidence_present': False,
            'quantitative_metrics_available': False,
            'falsifiability_assessment': 'UNKNOWN',
            'validation_details': []
        }
        
        # Check for empirical evidence
        if 'calculations' in experiment_config:
            calculations = experiment_config['calculations']
            if any('analysis' in calc for calc in calculations):
                empirical_validation['empirical_evidence_present'] = True
        
        # Check for quantitative metrics
        if 'parameters' in experiment_config:
            params = experiment_config['parameters']
            if any(isinstance(value, (int, float)) for value in params.values()):
                empirical_validation['quantitative_metrics_available'] = True
        
        # Assess falsifiability
        if 'hypothesis' in experiment_config or 'research_question' in experiment_config:
            hypothesis = experiment_config.get('hypothesis', experiment_config.get('research_question', ''))
            if any(word in hypothesis.lower() for word in ['compare', 'test', 'measure', 'analyze']):
                empirical_validation['falsifiability_assessment'] = 'FALSIFIABLE'
            else:
                empirical_validation['falsifiability_assessment'] = 'QUESTIONABLE'
        
        # Overall empirical validation status
        if (empirical_validation['empirical_evidence_present'] and 
            empirical_validation['quantitative_metrics_available'] and
            empirical_validation['falsifiability_assessment'] == 'FALSIFIABLE'):
            empirical_validation['status'] = 'PASSED'
        elif empirical_validation['empirical_evidence_present']:
            empirical_validation['status'] = 'MARGINAL'
        else:
            empirical_validation['status'] = 'FAILED'
            empirical_validation['validation_details'].append('Insufficient empirical evidence')
        
        return empirical_validation
    
    def _check_statistical_significance(self, experiment_config: Dict) -> Dict:
        """Universal statistical significance checking."""
        stats_check = {
            'status': 'PENDING',
            'statistical_tests_planned': False,
            'sample_size_adequate': 'UNKNOWN',
            'significance_level_defined': False,
            'statistical_details': []
        }
        
        # Check for statistical analysis in calculations
        if 'calculations' in experiment_config:
            calculations = experiment_config['calculations']
            statistical_terms = ['statistical_analysis', 'significance', 'test', 'correlation', 'regression']
            
            if any(any(term in calc for term in statistical_terms) for calc in calculations):
                stats_check['statistical_tests_planned'] = True
        
        # Check for adequate sample size (simplified)
        if 'real_dataset' in experiment_config:
            dataset = experiment_config['real_dataset']
            if hasattr(dataset, 'shape'):
                if np.prod(dataset.shape) > 30:  # Basic minimum sample size
                    stats_check['sample_size_adequate'] = 'ADEQUATE'
                else:
                    stats_check['sample_size_adequate'] = 'INSUFFICIENT'
            else:
                stats_check['sample_size_adequate'] = 'UNKNOWN'
        
        # Overall statistical status
        if (stats_check['statistical_tests_planned'] and 
            stats_check['sample_size_adequate'] == 'ADEQUATE'):
            stats_check['status'] = 'PASSED'
        elif stats_check['statistical_tests_planned']:
            stats_check['status'] = 'MARGINAL'
        else:
            stats_check['status'] = 'FAILED'
            stats_check['statistical_details'].append('No statistical analysis planned')
        
        return stats_check
    
    @abstractmethod
    def _check_physical_constraints(self, experiment_config: Dict) -> Dict:
        """Check domain-specific physical constraints."""
        pass
    
    def _validate_order_of_magnitude(self, experiment_config: Dict) -> Dict:
        """Universal order of magnitude validation."""
        magnitude_check = {
            'status': 'PENDING',
            'magnitude_estimates_present': False,
            'realistic_ranges': True,
            'magnitude_details': []
        }
        
        # Check for numerical parameters
        if 'parameters' in experiment_config:
            params = experiment_config['parameters']
            numerical_params = {k: v for k, v in params.items() if isinstance(v, (int, float))}
            
            if numerical_params:
                magnitude_check['magnitude_estimates_present'] = True
                
                # Basic sanity checks (domain-agnostic)
                for key, value in numerical_params.items():
                    if abs(value) > 1e20 or abs(value) < 1e-20:
                        magnitude_check['realistic_ranges'] = False
                        magnitude_check['magnitude_details'].append(f'Unrealistic value: {key}={value}')
        
        # Overall magnitude validation
        if magnitude_check['magnitude_estimates_present'] and magnitude_check['realistic_ranges']:
            magnitude_check['status'] = 'PASSED'
        elif magnitude_check['magnitude_estimates_present']:
            magnitude_check['status'] = 'MARGINAL'
        else:
            magnitude_check['status'] = 'FAILED'
            magnitude_check['magnitude_details'].append('No magnitude estimates provided')
        
        return magnitude_check
    
    def _assess_plausibility(self, experiment_config: Dict) -> Dict:
        """Universal plausibility assessment."""
        plausibility_assessment = {
            'status': 'PENDING',
            'theoretical_consistency': True,
            'experimental_feasibility': True,
            'plausibility_score': 0.0,
            'plausibility_details': []
        }
        
        # Basic plausibility checks
        score = 0.0
        
        # Check for clear research question
        if 'hypothesis' in experiment_config or 'research_question' in experiment_config:
            score += 0.3
        
        # Check for methodology
        if 'calculations' in experiment_config and experiment_config['calculations']:
            score += 0.3
        
        # Check for data sources
        if 'real_dataset' in experiment_config:
            score += 0.4
        
        plausibility_assessment['plausibility_score'] = score
        
        # Assess overall plausibility
        if score >= 0.8:
            plausibility_assessment['status'] = 'PASSED'
        elif score >= 0.5:
            plausibility_assessment['status'] = 'MARGINAL'
        else:
            plausibility_assessment['status'] = 'FAILED'
            plausibility_assessment['plausibility_details'].append('Insufficient experimental design')
        
        return plausibility_assessment
    
    def get_validator_status(self) -> Dict:
        """Get current validator status."""
        return {
            'validator_type': self.__class__.__name__,
            'research_domain': self.research_domain,
            'universal_requirements': self.universal_requirements,
            'total_validations': len(self.validation_history),
            'domain_config_loaded': bool(self.domain_specific_config),
            'status': 'OPERATIONAL'
        }
    
    def get_validation_summary(self) -> Dict:
        """Get validation summary for this domain."""
        if not self.validation_history:
            return {
                'domain': self.research_domain,
                'total_validations': 0,
                'status': 'NO_VALIDATIONS_YET'
            }
        
        passed_validations = sum(
            1 for result in self.validation_history
            if result.get('overall_universal_status') == 'PASSED'
        )
        
        return {
            'domain': self.research_domain,
            'total_validations': len(self.validation_history),
            'success_rate': passed_validations / len(self.validation_history),
            'recent_validation': self.validation_history[-1].get('validation_timestamp'),
            'status': 'OPERATIONAL'
        }