"""
Domain-Agnostic Experiment Validator

Core validation framework that works across all scientific domains:
- Chemical composition studies (SAI particle chemistry)
- Physical dynamics (aerosol transport, settling)
- Signal detection (spectroscopy, remote sensing)
- Climate modeling (temperature, precipitation responses)
- Policy analysis (governance, implementation studies)

This replaces domain-specific validators with a flexible, multi-domain approach
that implements the Sakana Principle universally while adapting validation
criteria to the specific experimental domain.
"""

import numpy as np
import xarray as xr
from typing import Dict, List, Union, Optional, Any
from enum import Enum
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ExperimentDomain(Enum):
    """Scientific domains for SAI research experiments."""
    CHEMICAL_COMPOSITION = "chemical_composition"
    PARTICLE_DYNAMICS = "particle_dynamics"
    SIGNAL_DETECTION = "signal_detection"
    CLIMATE_RESPONSE = "climate_response"
    ATMOSPHERIC_TRANSPORT = "atmospheric_transport"
    POLICY_GOVERNANCE = "policy_governance"
    RADIATIVE_FORCING = "radiative_forcing"
    UNKNOWN = "unknown"


class ExperimentValidator:
    """
    Universal experiment validator implementing the Sakana Principle
    across all scientific domains relevant to SAI research.
    
    The Sakana Principle (empirical validation mandatory) applies universally,
    but validation criteria adapt to the specific experimental domain.
    """
    
    def __init__(self, 
                 real_data_mandatory: bool = True,
                 synthetic_data_forbidden: bool = True,
                 strict_mode: bool = True):
        """
        Initialize domain-agnostic experiment validator.
        
        Args:
            real_data_mandatory: Require real datasets for validation
            synthetic_data_forbidden: Forbid synthetic data usage
            strict_mode: Enable strict validation criteria
        """
        self.real_data_mandatory = real_data_mandatory
        self.synthetic_data_forbidden = synthetic_data_forbidden
        self.strict_mode = strict_mode
        
        # Universal Sakana Principle requirements
        self.universal_requirements = {
            'empirical_evidence_mandatory': True,
            'quantitative_validation_required': True,
            'real_data_verification': real_data_mandatory,
            'plausibility_trap_prevention': True,
            'order_of_magnitude_checking': True
        }
        
        # Domain-specific validation criteria
        self.domain_criteria = self._initialize_domain_criteria()
        
        # Validation history
        self.validation_history = []
        
        logger.info("Domain-agnostic Experiment Validator initialized")
    
    def _initialize_domain_criteria(self) -> Dict[ExperimentDomain, Dict]:
        """Initialize validation criteria for each experimental domain."""
        return {
            ExperimentDomain.CHEMICAL_COMPOSITION: {
                'parameter_ranges': {
                    'concentration_ppm': (0.1, 10000),
                    'ph_value': (0.0, 14.0),
                    'temperature_k': (150, 350),
                    'pressure_pa': (1000, 100000),
                    'molecular_weight': (10, 1000)
                },
                'required_evidence': ['chemical_analysis', 'thermodynamic_data'],
                'datasets': ['GLENS', 'ARISE-SAI'],
                'validation_methods': ['chemical_feasibility', 'thermodynamic_stability'],
                'physical_constraints': ['mass_conservation', 'charge_balance']
            },
            
            ExperimentDomain.PARTICLE_DYNAMICS: {
                'parameter_ranges': {
                    'particle_size_um': (0.01, 10.0),
                    'settling_velocity_ms': (0.001, 1.0),
                    'reynolds_number': (0.001, 1000),
                    'drag_coefficient': (0.1, 2.0),
                    'density_kgm3': (500, 3000)
                },
                'required_evidence': ['particle_measurements', 'atmospheric_data'],
                'datasets': ['GLENS', 'GeoMIP'],
                'validation_methods': ['fluid_dynamics', 'particle_transport'],
                'physical_constraints': ['stokes_law', 'terminal_velocity']
            },
            
            ExperimentDomain.SIGNAL_DETECTION: {
                'parameter_ranges': {
                    'snr_db': (-30.0, 30.0),
                    'frequency_hz': (0.001, 1000),
                    'signal_amplitude': (0.001, 100),
                    'noise_floor': (0.001, 10),
                    'detection_threshold': (0.01, 0.99)
                },
                'required_evidence': ['signal_analysis', 'noise_characterization'],
                'datasets': ['GLENS', 'observational_data'],
                'validation_methods': ['snr_analysis', 'spectral_analysis'],
                'physical_constraints': ['nyquist_criterion', 'detection_limits'],
                'critical_thresholds': {
                    'undetectable_limit_db': -15.54,  # From Hangzhou case
                    'minimum_detectable_db': 0.0
                }
            },
            
            ExperimentDomain.CLIMATE_RESPONSE: {
                'parameter_ranges': {
                    'temperature_change_k': (-10.0, 10.0),
                    'precipitation_change_percent': (-50.0, 50.0),
                    'radiative_forcing_wm2': (-15.0, 15.0),
                    'response_time_years': (0.1, 100),
                    'spatial_scale_km': (10, 10000)
                },
                'required_evidence': ['climate_model_output', 'observational_data'],
                'datasets': ['GLENS', 'ARISE-SAI', 'GeoMIP'],
                'validation_methods': ['statistical_analysis', 'trend_analysis'],
                'physical_constraints': ['energy_balance', 'water_cycle']
            },
            
            ExperimentDomain.ATMOSPHERIC_TRANSPORT: {
                'parameter_ranges': {
                    'wind_speed_ms': (0.1, 100),
                    'diffusion_coefficient': (1e-6, 1e3),
                    'residence_time_days': (1, 1000),
                    'mixing_ratio': (1e-12, 1e-3),
                    'altitude_km': (0, 50)
                },
                'required_evidence': ['transport_modeling', 'atmospheric_measurements'],
                'datasets': ['GLENS', 'reanalysis_data'],
                'validation_methods': ['transport_modeling', 'tracer_analysis'],
                'physical_constraints': ['mass_conservation', 'atmospheric_dynamics']
            },
            
            ExperimentDomain.POLICY_GOVERNANCE: {
                'parameter_ranges': {
                    'implementation_cost_usd': (1e6, 1e12),
                    'timeline_years': (1, 50),
                    'stakeholder_count': (2, 200),
                    'governance_complexity': (1, 10),
                    'risk_assessment_score': (0.0, 1.0)
                },
                'required_evidence': ['stakeholder_analysis', 'cost_benefit_analysis'],
                'datasets': ['policy_documents', 'expert_assessments'],
                'validation_methods': ['stakeholder_validation', 'expert_review'],
                'physical_constraints': ['resource_availability', 'institutional_capacity']
            }
        }
    
    def detect_experiment_domain(self, experiment: Dict) -> ExperimentDomain:
        """
        Automatically detect the experimental domain based on content analysis.
        
        Args:
            experiment: Experiment description and parameters
            
        Returns:
            Detected experimental domain
        """
        content = str(experiment).lower()
        
        # Domain detection keywords
        domain_keywords = {
            ExperimentDomain.CHEMICAL_COMPOSITION: [
                'chemical', 'composition', 'molecular', 'ph', 'concentration',
                'sulfuric', 'acid', 'chemistry', 'reaction', 'catalytic'
            ],
            ExperimentDomain.PARTICLE_DYNAMICS: [
                'particle', 'aerosol', 'settling', 'dynamics', 'transport',
                'size distribution', 'microphysics', 'coagulation'
            ],
            ExperimentDomain.SIGNAL_DETECTION: [
                'signal', 'spectroscopy', 'detection', 'snr', 'noise',
                'volterra', 'kernel', 'frequency', 'amplitude'
            ],
            ExperimentDomain.CLIMATE_RESPONSE: [
                'climate', 'temperature', 'precipitation', 'response',
                'feedback', 'sensitivity', 'forcing'
            ],
            ExperimentDomain.ATMOSPHERIC_TRANSPORT: [
                'transport', 'atmospheric', 'circulation', 'mixing',
                'diffusion', 'residence time', 'tracer'
            ],
            ExperimentDomain.POLICY_GOVERNANCE: [
                'policy', 'governance', 'stakeholder', 'implementation',
                'regulation', 'international', 'agreement'
            ]
        }
        
        # Score each domain based on keyword matches
        domain_scores = {}
        for domain, keywords in domain_keywords.items():
            score = sum(1 for keyword in keywords if keyword in content)
            domain_scores[domain] = score
        
        # Return domain with highest score
        if max(domain_scores.values()) > 0:
            return max(domain_scores, key=domain_scores.get)
        else:
            return ExperimentDomain.UNKNOWN
    
    def validate_experiment(self, experiment: Dict) -> Dict:
        """
        Perform comprehensive validation adapted to the experimental domain.
        
        Args:
            experiment: Experiment description with parameters and context
            
        Returns:
            Dict containing validation results and recommendations
        """
        validation_start = datetime.now()
        
        # Detect experimental domain
        domain = self.detect_experiment_domain(experiment)
        
        validation_result = {
            'experiment_id': experiment.get('id', f"exp_{int(validation_start.timestamp())}"),
            'detected_domain': domain.value,
            'validation_timestamp': validation_start.isoformat(),
            'sakana_principle_compliance': False,
            'validation_tests': {},
            'violations': [],
            'recommendations': [],
            'domain_specific_results': {}
        }
        
        try:
            # Universal Sakana Principle tests (apply to all domains)
            universal_tests = self._perform_universal_validation(experiment)
            validation_result['validation_tests']['universal'] = universal_tests
            
            if not universal_tests['passed']:
                validation_result['violations'].extend(universal_tests['violations'])
            
            # Domain-specific validation
            if domain != ExperimentDomain.UNKNOWN:
                domain_tests = self._perform_domain_validation(experiment, domain)
                validation_result['validation_tests']['domain_specific'] = domain_tests
                validation_result['domain_specific_results'] = domain_tests
                
                if not domain_tests['passed']:
                    validation_result['violations'].extend(domain_tests['violations'])
            else:
                validation_result['violations'].append('UNKNOWN_DOMAIN: Cannot determine experimental domain')
            
            # Determine overall compliance
            validation_result['sakana_principle_compliance'] = (
                len(validation_result['violations']) == 0 and
                universal_tests['passed'] and
                (domain == ExperimentDomain.UNKNOWN or domain_tests['passed'])
            )
            
            # Generate recommendations
            validation_result['recommendations'] = self._generate_recommendations(
                validation_result, domain
            )
            
            # Record validation
            self.validation_history.append(validation_result)
            
            logger.info(f"Validation completed for {domain.value}: "
                       f"{'PASS' if validation_result['sakana_principle_compliance'] else 'FAIL'}")
            
            return validation_result
            
        except Exception as e:
            logger.error(f"Validation failed: {e}")
            validation_result['violations'].append(f'VALIDATION_ERROR: {e}')
            return validation_result
    
    def _perform_universal_validation(self, experiment: Dict) -> Dict:
        """
        Perform universal Sakana Principle validation (applies to all domains).
        """
        universal_result = {
            'test_name': 'Universal Sakana Principle Validation',
            'passed': False,
            'violations': [],
            'checks_performed': []
        }
        
        # Check 1: Empirical evidence requirement
        if not self._has_empirical_evidence(experiment):
            universal_result['violations'].append('MISSING_EMPIRICAL_EVIDENCE')
        universal_result['checks_performed'].append('empirical_evidence_check')
        
        # Check 2: Quantitative validation
        if not self._has_quantitative_parameters(experiment):
            universal_result['violations'].append('MISSING_QUANTITATIVE_PARAMETERS')
        universal_result['checks_performed'].append('quantitative_validation')
        
        # Check 3: Real data verification (if required)
        if self.real_data_mandatory and not self._has_real_data_reference(experiment):
            universal_result['violations'].append('REAL_DATA_REQUIRED')
        universal_result['checks_performed'].append('real_data_verification')
        
        # Check 4: Order-of-magnitude validation
        magnitude_violations = self._check_order_of_magnitude(experiment)
        universal_result['violations'].extend(magnitude_violations)
        universal_result['checks_performed'].append('order_of_magnitude_validation')
        
        # Check 5: Plausibility trap prevention
        plausibility_violations = self._check_plausibility_indicators(experiment)
        universal_result['violations'].extend(plausibility_violations)
        universal_result['checks_performed'].append('plausibility_trap_prevention')
        
        universal_result['passed'] = len(universal_result['violations']) == 0
        
        return universal_result
    
    def _perform_domain_validation(self, experiment: Dict, domain: ExperimentDomain) -> Dict:
        """
        Perform domain-specific validation based on experimental type.
        """
        domain_result = {
            'domain': domain.value,
            'test_name': f'{domain.value} Domain Validation',
            'passed': False,
            'violations': [],
            'parameter_checks': [],
            'validation_methods_applied': []
        }
        
        if domain not in self.domain_criteria:
            domain_result['violations'].append(f'UNSUPPORTED_DOMAIN: {domain.value}')
            return domain_result
        
        criteria = self.domain_criteria[domain]
        parameters = experiment.get('parameters', {})
        
        # Parameter range validation
        for param_name, param_value in parameters.items():
            if isinstance(param_value, (int, float)):
                param_check = self._validate_parameter_range(
                    param_name, param_value, criteria['parameter_ranges']
                )
                domain_result['parameter_checks'].append(param_check)
                
                if not param_check['valid']:
                    domain_result['violations'].append(
                        f'PARAMETER_OUT_OF_RANGE: {param_name}={param_value}'
                    )
        
        # Domain-specific physical constraints
        constraint_violations = self._check_physical_constraints(
            experiment, criteria.get('physical_constraints', [])
        )
        domain_result['violations'].extend(constraint_violations)
        
        # Required evidence validation
        evidence_violations = self._check_required_evidence(
            experiment, criteria.get('required_evidence', [])
        )
        domain_result['violations'].extend(evidence_violations)
        
        # Special handling for signal detection domain (includes spectroscopy thresholds)
        if domain == ExperimentDomain.SIGNAL_DETECTION:
            signal_violations = self._validate_signal_detection_specifics(experiment, criteria)
            domain_result['violations'].extend(signal_violations)
            domain_result['validation_methods_applied'].append('signal_detection_thresholds')
        
        domain_result['passed'] = len(domain_result['violations']) == 0
        
        return domain_result
    
    def _validate_signal_detection_specifics(self, experiment: Dict, criteria: Dict) -> List[str]:
        """
        Special validation for signal detection experiments (includes spectroscopy).
        
        This handles the -15.54 dB threshold and other signal-specific requirements
        ONLY when the experiment is actually about signal detection.
        """
        violations = []
        parameters = experiment.get('parameters', {})
        
        # Check for SNR-related parameters
        snr_params = ['snr_db', 'signal_to_noise', 'snr_threshold']
        snr_value = None
        
        for param in snr_params:
            if param in parameters:
                snr_value = parameters[param]
                break
        
        if snr_value is not None:
            # Apply spectroscopy-specific threshold (from Hangzhou case)
            critical_thresholds = criteria.get('critical_thresholds', {})
            undetectable_limit = critical_thresholds.get('undetectable_limit_db', -15.54)
            minimum_detectable = critical_thresholds.get('minimum_detectable_db', 0.0)
            
            if snr_value <= undetectable_limit:
                violations.append(f'SIGNAL_UNDETECTABLE: {snr_value} dB <= {undetectable_limit} dB (Hangzhou threshold)')
            elif snr_value < minimum_detectable:
                violations.append(f'SIGNAL_BELOW_MINIMUM: {snr_value} dB < {minimum_detectable} dB')
        
        return violations
    
    def _has_empirical_evidence(self, experiment: Dict) -> bool:
        """Check if experiment includes empirical evidence."""
        content = str(experiment).lower()
        evidence_indicators = [
            'data', 'measurement', 'observation', 'experiment',
            'glens', 'arise-sai', 'geomip', 'ncar', 'dataset'
        ]
        return any(indicator in content for indicator in evidence_indicators)
    
    def _has_quantitative_parameters(self, experiment: Dict) -> bool:
        """Check if experiment includes quantitative parameters."""
        parameters = experiment.get('parameters', {})
        return any(isinstance(v, (int, float)) for v in parameters.values())
    
    def _has_real_data_reference(self, experiment: Dict) -> bool:
        """Check if experiment references real datasets."""
        content = str(experiment).lower()
        real_data_indicators = [
            'glens', 'arise-sai', 'geomip', 'ncar', 'ucar',
            'observational', 'measured', 'experimental data'
        ]
        return any(indicator in content for indicator in real_data_indicators)
    
    def _check_order_of_magnitude(self, experiment: Dict) -> List[str]:
        """Check for order-of-magnitude violations in parameters."""
        violations = []
        parameters = experiment.get('parameters', {})
        
        for param_name, param_value in parameters.items():
            if isinstance(param_value, (int, float)):
                # Check for extreme values that suggest unrealistic parameters
                if abs(param_value) > 1e10:
                    violations.append(f'EXTREME_VALUE: {param_name}={param_value} (possible units error)')
                elif param_value == 0 and 'threshold' not in param_name.lower():
                    violations.append(f'ZERO_VALUE: {param_name}=0 (suspicious for physical parameter)')
        
        return violations
    
    def _check_plausibility_indicators(self, experiment: Dict) -> List[str]:
        """Check for plausibility trap indicators."""
        violations = []
        content = str(experiment).lower()
        
        # Check for excessive sophistication without empirical grounding
        sophistication_terms = ['elegant', 'sophisticated', 'advanced', 'novel', 'breakthrough']
        empirical_terms = ['measured', 'observed', 'validated', 'verified', 'tested']
        
        sophistication_count = sum(1 for term in sophistication_terms if term in content)
        empirical_count = sum(1 for term in empirical_terms if term in content)
        
        if sophistication_count > 2 and empirical_count == 0:
            violations.append('PLAUSIBILITY_TRAP_RISK: High sophistication, no empirical grounding')
        
        return violations
    
    def _validate_parameter_range(self, param_name: str, param_value: float, ranges: Dict) -> Dict:
        """Validate parameter against domain-specific ranges."""
        param_check = {
            'parameter': param_name,
            'value': param_value,
            'valid': True,
            'applicable_range': None,
            'range_check': 'NOT_APPLICABLE'
        }
        
        # Find applicable range
        for range_key, (min_val, max_val) in ranges.items():
            if any(key_part in param_name.lower() for key_part in range_key.split('_')):
                param_check['applicable_range'] = (min_val, max_val)
                param_check['range_check'] = 'APPLIED'
                
                if not (min_val <= param_value <= max_val):
                    param_check['valid'] = False
                    param_check['range_check'] = 'FAILED'
                break
        
        return param_check
    
    def _check_physical_constraints(self, experiment: Dict, constraints: List[str]) -> List[str]:
        """Check domain-specific physical constraints."""
        violations = []
        
        # This would be expanded with actual physical constraint checking
        # For now, placeholder implementation
        for constraint in constraints:
            # Would implement specific constraint checking here
            pass
        
        return violations
    
    def _check_required_evidence(self, experiment: Dict, required: List[str]) -> List[str]:
        """Check for required evidence types."""
        violations = []
        content = str(experiment).lower()
        
        for evidence_type in required:
            if evidence_type.lower() not in content:
                violations.append(f'MISSING_EVIDENCE: {evidence_type}')
        
        return violations
    
    def _generate_recommendations(self, validation_result: Dict, domain: ExperimentDomain) -> List[str]:
        """Generate domain-appropriate recommendations."""
        recommendations = []
        violations = validation_result['violations']
        
        if validation_result['sakana_principle_compliance']:
            recommendations.append("✅ APPROVED: Experiment meets Sakana Principle requirements")
        else:
            recommendations.append("❌ REQUIRES REVISION: Address violations before proceeding")
        
        # Domain-specific recommendations
        if domain == ExperimentDomain.CHEMICAL_COMPOSITION:
            if any('PARAMETER_OUT_OF_RANGE' in v for v in violations):
                recommendations.append("Review chemical parameter ranges for physical realism")
            if any('MISSING_EVIDENCE' in v for v in violations):
                recommendations.append("Include chemical analysis data or thermodynamic calculations")
        
        elif domain == ExperimentDomain.SIGNAL_DETECTION:
            if any('SIGNAL_UNDETECTABLE' in v for v in violations):
                recommendations.append("Signal strength insufficient - consider experimental redesign")
            if any('SIGNAL_BELOW_MINIMUM' in v for v in violations):
                recommendations.append("Increase signal strength or improve noise reduction")
        
        # Universal recommendations
        if any('MISSING_EMPIRICAL_EVIDENCE' in v for v in violations):
            recommendations.append("Include reference to real datasets (GLENS, ARISE-SAI, GeoMIP)")
        
        if any('PLAUSIBILITY_TRAP_RISK' in v for v in violations):
            recommendations.append("Balance theoretical sophistication with empirical evidence")
        
        return recommendations
    
    def get_validation_summary(self) -> Dict:
        """Get summary statistics of validation history."""
        if not self.validation_history:
            return {'total_validations': 0, 'summary': 'No validations performed'}
        
        total = len(self.validation_history)
        successful = sum(1 for v in self.validation_history if v['sakana_principle_compliance'])
        
        # Domain distribution
        domain_counts = {}
        for validation in self.validation_history:
            domain = validation['detected_domain']
            domain_counts[domain] = domain_counts.get(domain, 0) + 1
        
        return {
            'total_validations': total,
            'success_rate': successful / total,
            'domain_distribution': domain_counts,
            'sakana_compliance_rate': successful / total,
            'average_violations_per_experiment': sum(len(v['violations']) for v in self.validation_history) / total
        }