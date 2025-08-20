"""
Empirical Validation Framework

Core implementation of the empirical validation principle that forms the foundation
of the Sakana Principle. This framework prevents "plausibility trap" scenarios by
enforcing strict empirical validation requirements for all theoretical claims.

Key Features:
- Comprehensive empirical validation tests for all theoretical claims
- Integration with real GLENS/ARISE-SAI/GeoMIP datasets 
- Order-of-magnitude calculation verification
- Signal-to-noise ratio validation against physical constraints
- Multi-stage validation pipeline with comprehensive testing

Based on the critical lesson from the Hangzhou vs Sakana comparison where
theoretical elegance (Volterra kernel spectroscopy) was validated against
real data analysis showing -15.54 dB undetectable signals.
"""

import numpy as np
import xarray as xr
from typing import Dict, List, Union, Optional, Tuple, Any
import logging
from datetime import datetime
import json
from pathlib import Path
import warnings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EmpiricalValidationFramework:
    """
    Core empirical validation framework implementing the Sakana Principle.
    
    This framework enforces that every theoretical claim must undergo rigorous
    empirical testing using real datasets before acceptance. It prevents the
    "plausibility trap" where theoretical sophistication masks empirical inadequacy.
    """
    
    def __init__(self, 
                 strict_mode: bool = True,
                 real_data_mandatory: bool = True,
                 synthetic_data_forbidden: bool = True):
        """
        Initialize empirical falsification framework.
        
        Args:
            strict_mode: Enable strict falsification requirements
            real_data_mandatory: Require real datasets for all validations
            synthetic_data_forbidden: Forbid synthetic data usage
        """
        self.strict_mode = strict_mode
        self.real_data_mandatory = real_data_mandatory
        self.synthetic_data_forbidden = synthetic_data_forbidden
        
        # Validation criteria based on Sakana Principle
        self.validation_criteria = {
            'minimum_snr_threshold_db': 0.0,        # Minimum detectable signal
            'undetectable_limit_db': -15.54,        # Critical threshold from Hangzhou case
            'required_statistical_power': 0.8,      # Minimum statistical power
            'minimum_sample_size': 20,              # Minimum ensemble size
            'required_confidence_level': 0.95,      # Statistical confidence
            'maximum_p_value': 0.05,               # Statistical significance
            'minimum_effect_size': 0.3              # Practical significance
        }
        
        # Approved real datasets for empirical validation
        self.approved_datasets = {
            'GLENS': {
                'full_name': 'Geoengineering Large Ensemble',
                'institution': 'NCAR',
                'model': 'CESM1(WACCM)',
                'ensemble_size': 20,
                'temporal_coverage': '2020-2099',
                'doi': '10.5065/D6JH3JXX',
                'variables': ['TREFHT', 'PRECT', 'CLDTOT', 'BURDEN1'],
                'validation_status': 'APPROVED'
            },
            'ARISE-SAI': {
                'full_name': 'ARISE Stratospheric Aerosol Intervention',
                'institution': 'Multiple',
                'ensemble_size': 10,
                'temporal_coverage': '2035-2069',
                'variables': ['tas', 'pr', 'clt'],
                'validation_status': 'APPROVED'
            },
            'GeoMIP': {
                'full_name': 'Geoengineering Model Intercomparison Project',
                'institution': 'Multiple',
                'models': ['CESM1', 'HadGEM2-ES', 'IPSL-CM5A-LR'],
                'variables': ['tas', 'pr', 'rsdt', 'rsut'],
                'validation_status': 'APPROVED'
            }
        }
        
        # Validation test history
        self.validation_history = []
        self.violation_reports = []
        
        logger.info(f"Empirical Validation Framework initialized")
        logger.info(f"Strict mode: {strict_mode}, Real data mandatory: {real_data_mandatory}")
    
    def validate_theoretical_claim(self, 
                                 claim: Dict,
                                 empirical_evidence: Dict,
                                 dataset_context: Optional[Dict] = None) -> Dict:
        """
        Perform comprehensive empirical validation of a theoretical claim.
        
        This is the core method that implements empirical validation principles
        applied to climate science research claims.
        
        Args:
            claim: Theoretical claim with parameters and predictions
            empirical_evidence: Real data evidence including SNR analysis
            dataset_context: Context about the datasets used for validation
            
        Returns:
            Dict containing validation results and validation status
        """
        validation_start_time = datetime.now()
        
        validation_result = {
            'claim_id': claim.get('id', f"claim_{int(validation_start_time.timestamp())}"),
            'validation_timestamp': validation_start_time.isoformat(),
            'validation_status': 'UNKNOWN',
            'empirical_validation_status': 'PENDING',
            'sakana_principle_compliance': False,
            'validation_tests': {},
            'violations': [],
            'supporting_evidence': {},
            'recommendations': []
        }
        
        try:
            logger.info(f"Starting empirical validation of claim: {claim.get('title', 'Unnamed claim')}")
            
            # Test 1: Real Data Validation
            real_data_test = self._test_real_data_requirement(empirical_evidence, dataset_context)
            validation_result['validation_tests']['real_data_validation'] = real_data_test
            
            if not real_data_test['passed']:
                validation_result['violations'].extend(real_data_test['violations'])
            
            # Test 2: Signal Detectability Test
            snr_test = self._test_signal_detectability(claim, empirical_evidence)
            validation_result['validation_tests']['signal_detectability'] = snr_test
            
            if not snr_test['passed']:
                validation_result['violations'].extend(snr_test['violations'])
            
            # Test 3: Statistical Significance Test
            stats_test = self._test_statistical_significance(empirical_evidence)
            validation_result['validation_tests']['statistical_significance'] = stats_test
            
            if not stats_test['passed']:
                validation_result['violations'].extend(stats_test['violations'])
            
            # Test 4: Order-of-Magnitude Validation
            magnitude_test = self._test_order_of_magnitude(claim)
            validation_result['validation_tests']['order_of_magnitude'] = magnitude_test
            
            if not magnitude_test['passed']:
                validation_result['violations'].extend(magnitude_test['violations'])
            
            # Test 5: Predictive Falsifiability Test
            falsifiability_test = self._test_predictive_falsifiability(claim)
            validation_result['validation_tests']['predictive_falsifiability'] = falsifiability_test
            
            if not falsifiability_test['passed']:
                validation_result['violations'].extend(falsifiability_test['violations'])
            
            # Determine overall validation status
            overall_status = self._determine_validation_status(validation_result)
            validation_result.update(overall_status)
            
            # Generate recommendations
            recommendations = self._generate_validation_recommendations(validation_result)
            validation_result['recommendations'] = recommendations
            
            # Record validation attempt
            self.validation_history.append(validation_result)
            
            # Log violations if any
            if falsification_result['violations']:
                self.violation_reports.append({
                    'claim_id': validation_result['claim_id'],
                    'timestamp': validation_start_time.isoformat(),
                    'violations': validation_result['violations'],
                    'severity': 'CRITICAL' if len(validation_result['violations']) > 2 else 'MODERATE'
                })
            
            logger.info(f"Validation completed: {validation_result['validation_status']}")
            
            return validation_result
            
        except Exception as e:
            logger.error(f"Empirical falsification failed: {e}")
            validation_result['validation_status'] = 'ERROR'
            validation_result['error_message'] = str(e)
            return validation_result
    
    def _test_real_data_requirement(self, 
                                   empirical_evidence: Dict, 
                                   dataset_context: Optional[Dict] = None) -> Dict:
        """
        Test that only approved real datasets are used for validation.
        
        This enforces REAL_DATA_MANDATORY=true and SYNTHETIC_DATA_FORBIDDEN=true.
        """
        test_result = {
            'test_name': 'Real Data Requirement',
            'passed': False,
            'violations': [],
            'evidence_quality': 'UNKNOWN',
            'approved_datasets_used': [],
            'dataset_verification': {}
        }
        
        try:
            # Check for real data verification in evidence
            if 'real_data_verification' not in empirical_evidence:
                test_result['violations'].append('MISSING_REAL_DATA_VERIFICATION')
                return test_result
            
            real_data_info = empirical_evidence['real_data_verification']
            
            # Test 1: Authentic data confirmation
            if not real_data_info.get('authentic_data_confirmed', False):
                test_result['violations'].append('AUTHENTIC_DATA_NOT_CONFIRMED')
            
            # Test 2: Synthetic data detection
            if real_data_info.get('synthetic_data_detected', False):
                test_result['violations'].append('SYNTHETIC_DATA_DETECTED')
            
            # Test 3: Institutional validation
            if not real_data_info.get('institutional_validation', False):
                test_result['violations'].append('INSTITUTIONAL_VALIDATION_FAILED')
            
            # Test 4: Dataset approval status
            dataset_name = real_data_info.get('dataset_name', '')
            if dataset_name in self.approved_datasets:
                test_result['approved_datasets_used'].append(dataset_name)
                test_result['dataset_verification'][dataset_name] = 'APPROVED'
            else:
                test_result['violations'].append(f'UNAPPROVED_DATASET: {dataset_name}')
            
            # Test 5: Provenance verification
            if not real_data_info.get('provenance_verified', False):
                test_result['violations'].append('PROVENANCE_NOT_VERIFIED')
            
            # Determine pass/fail
            test_result['passed'] = len(test_result['violations']) == 0
            
            if test_result['passed']:
                test_result['evidence_quality'] = 'AUTHENTIC'
            else:
                test_result['evidence_quality'] = 'INSUFFICIENT'
            
            return test_result
            
        except Exception as e:
            test_result['violations'].append(f'REAL_DATA_TEST_ERROR: {e}')
            return test_result
    
    def _test_signal_detectability(self, claim: Dict, empirical_evidence: Dict) -> Dict:
        """
        Test signal detectability using SNR analysis against GLENS thresholds.
        
        This implements the critical -15.54 dB threshold from the Hangzhou case.
        """
        test_result = {
            'test_name': 'Signal Detectability',
            'passed': False,
            'violations': [],
            'snr_analysis': {},
            'detectability_status': 'UNKNOWN',
            'threshold_comparison': {}
        }
        
        try:
            # Check for SNR analysis in evidence
            if 'snr_analysis' not in empirical_evidence:
                test_result['violations'].append('MISSING_SNR_ANALYSIS')
                return test_result
            
            snr_data = empirical_evidence['snr_analysis']
            test_result['snr_analysis'] = snr_data
            
            # Extract SNR value
            snr_db = snr_data.get('snr_db', -np.inf)
            
            if snr_db == -np.inf or snr_db is None:
                test_result['violations'].append('INVALID_SNR_VALUE')
                return test_result
            
            # Test against critical thresholds
            criteria = self.validation_criteria
            
            # Critical test: Undetectable limit (-15.54 dB)
            if snr_db <= criteria['undetectable_limit_db']:
                test_result['violations'].append(f'SIGNAL_UNDETECTABLE: {snr_db} dB <= {criteria["undetectable_limit_db"]} dB')
                test_result['detectability_status'] = 'UNDETECTABLE'
            
            # Minimum detectability test (0 dB)
            elif snr_db < criteria['minimum_snr_threshold_db']:
                test_result['violations'].append(f'SIGNAL_BELOW_MINIMUM: {snr_db} dB < {criteria["minimum_snr_threshold_db"]} dB')
                test_result['detectability_status'] = 'BELOW_MINIMUM'
            
            else:
                test_result['detectability_status'] = 'DETECTABLE'
            
            # Record threshold comparisons
            test_result['threshold_comparison'] = {
                'snr_db': snr_db,
                'undetectable_limit': criteria['undetectable_limit_db'],
                'minimum_threshold': criteria['minimum_snr_threshold_db'],
                'above_undetectable': snr_db > criteria['undetectable_limit_db'],
                'above_minimum': snr_db >= criteria['minimum_snr_threshold_db']
            }
            
            # Check detectability claim consistency
            claimed_detectable = snr_data.get('detectable', False)
            if claimed_detectable and test_result['detectability_status'] in ['UNDETECTABLE', 'BELOW_MINIMUM']:
                test_result['violations'].append('DETECTABILITY_CLAIM_INCONSISTENT')
            
            # Determine pass/fail
            test_result['passed'] = len(test_result['violations']) == 0
            
            return test_result
            
        except Exception as e:
            test_result['violations'].append(f'SNR_TEST_ERROR: {e}')
            return test_result
    
    def _test_statistical_significance(self, empirical_evidence: Dict) -> Dict:
        """
        Test statistical significance requirements for empirical validation.
        """
        test_result = {
            'test_name': 'Statistical Significance',
            'passed': False,
            'violations': [],
            'statistical_metrics': {},
            'significance_status': 'UNKNOWN'
        }
        
        try:
            # Check for statistical validation in evidence
            if 'statistical_validation' not in empirical_evidence:
                test_result['violations'].append('MISSING_STATISTICAL_VALIDATION')
                return test_result
            
            stats_data = empirical_evidence['statistical_validation']
            test_result['statistical_metrics'] = stats_data
            
            criteria = self.validation_criteria
            
            # Test p-value
            p_value = stats_data.get('p_value', 1.0)
            if p_value > criteria['maximum_p_value']:
                test_result['violations'].append(f'P_VALUE_TOO_HIGH: {p_value} > {criteria["maximum_p_value"]}')
            
            # Test confidence level
            confidence_level = stats_data.get('confidence_level', 0.0)
            if confidence_level < criteria['required_confidence_level']:
                test_result['violations'].append(f'CONFIDENCE_TOO_LOW: {confidence_level} < {criteria["required_confidence_level"]}')
            
            # Test sample size
            sample_size = stats_data.get('sample_size', 0)
            if sample_size < criteria['minimum_sample_size']:
                test_result['violations'].append(f'SAMPLE_SIZE_TOO_SMALL: {sample_size} < {criteria["minimum_sample_size"]}')
            
            # Test effect size if available
            effect_size = stats_data.get('effect_size', None)
            if effect_size is not None and effect_size < criteria['minimum_effect_size']:
                test_result['violations'].append(f'EFFECT_SIZE_TOO_SMALL: {effect_size} < {criteria["minimum_effect_size"]}')
            
            # Test statistical power if available
            power = stats_data.get('power', None)
            if power is not None and power < criteria['required_statistical_power']:
                test_result['violations'].append(f'STATISTICAL_POWER_TOO_LOW: {power} < {criteria["required_statistical_power"]}')
            
            # Determine significance status
            if len(test_result['violations']) == 0:
                test_result['significance_status'] = 'STATISTICALLY_SIGNIFICANT'
                test_result['passed'] = True
            else:
                test_result['significance_status'] = 'NOT_SIGNIFICANT'
            
            return test_result
            
        except Exception as e:
            test_result['violations'].append(f'STATS_TEST_ERROR: {e}')
            return test_result
    
    def _test_order_of_magnitude(self, claim: Dict) -> Dict:
        """
        Test that claimed parameters are within reasonable order-of-magnitude ranges.
        
        Prevents physically impossible parameter values that could indicate
        theoretical claims not grounded in physical reality.
        """
        test_result = {
            'test_name': 'Order of Magnitude Validation',
            'passed': False,
            'violations': [],
            'parameter_checks': [],
            'magnitude_status': 'UNKNOWN'
        }
        
        try:
            # Define reasonable physical ranges for climate parameters
            parameter_ranges = {
                'temperature_change': (-20.0, 20.0),        # °C
                'precipitation_change': (-80.0, 100.0),     # %
                'radiative_forcing': (-15.0, 15.0),         # W/m²
                'sai_injection_rate': (0.0, 100.0),         # Tg/yr
                'aerosol_burden': (0.0, 10.0),              # kg/m²
                'cloud_fraction_change': (-0.5, 0.5),       # Fractional change
                'signal_strength': (0.0, 100.0),            # Normalized units
                'noise_level': (0.0, 100.0),                # Normalized units
                'ensemble_size': (1, 100),                  # Number of members
                'time_horizon': (1, 100)                    # Years
            }
            
            # Extract parameters from claim
            parameters = claim.get('parameters', {})
            
            violations_found = False
            
            for param_name, param_value in parameters.items():
                param_check = {
                    'parameter': param_name,
                    'value': param_value,
                    'status': 'UNKNOWN',
                    'range_check': 'NOT_APPLICABLE'
                }
                
                # Find applicable range
                applicable_range = None
                for range_key, range_values in parameter_ranges.items():
                    if range_key.lower() in param_name.lower():
                        applicable_range = range_values
                        break
                
                if applicable_range and isinstance(param_value, (int, float)):
                    min_val, max_val = applicable_range
                    
                    if min_val <= param_value <= max_val:
                        param_check['status'] = 'VALID'
                        param_check['range_check'] = 'PASSED'
                    else:
                        param_check['status'] = 'VIOLATION'
                        param_check['range_check'] = 'FAILED'
                        violations_found = True
                        test_result['violations'].append(
                            f'PARAMETER_OUT_OF_RANGE: {param_name}={param_value} outside [{min_val}, {max_val}]'
                        )
                    
                    # Check for extreme order-of-magnitude issues
                    if abs(param_value) > 100 * max_val:
                        test_result['violations'].append(
                            f'ORDER_OF_MAGNITUDE_ERROR: {param_name}={param_value} (possible units error)'
                        )
                        violations_found = True
                
                test_result['parameter_checks'].append(param_check)
            
            # Determine overall status
            if not violations_found and test_result['parameter_checks']:
                test_result['magnitude_status'] = 'PHYSICALLY_REASONABLE'
                test_result['passed'] = True
            elif not test_result['parameter_checks']:
                test_result['magnitude_status'] = 'NO_PARAMETERS_TO_CHECK'
                test_result['passed'] = True  # No parameters is not a violation
            else:
                test_result['magnitude_status'] = 'PHYSICALLY_UNREASONABLE'
            
            return test_result
            
        except Exception as e:
            test_result['violations'].append(f'MAGNITUDE_TEST_ERROR: {e}')
            return test_result
    
    def _test_predictive_falsifiability(self, claim: Dict) -> Dict:
        """
        Test that the claim makes specific, falsifiable predictions.
        
        Implements Popper's criterion that scientific theories must be
        capable of being proven false through empirical observation.
        """
        test_result = {
            'test_name': 'Predictive Falsifiability',
            'passed': False,
            'violations': [],
            'falsifiability_analysis': {},
            'prediction_specificity': 'UNKNOWN'
        }
        
        try:
            claim_text = claim.get('claim_text', '') + ' ' + claim.get('methodology', '')
            
            # Check for specific, quantitative predictions
            quantitative_indicators = [
                r'\\d+\\s*(degree|°C|°F)',           # Temperature predictions
                r'\\d+\\s*(percent|%)',             # Percentage predictions  
                r'\\d+\\s*(year|month|day)',        # Time predictions
                r'\\d+\\s*(W/m²|Wm-2)',           # Radiative forcing
                r'\\d+\\s*(Tg|Mt|Gt)',            # Mass predictions
                r'p\\s*<\\s*0\\.\\d+',              # Statistical significance
                r'confidence\\s*interval',          # Confidence intervals
                r'\\d+.*ensemble',                  # Ensemble size
                r'SNR.*\\d+.*dB'                   # SNR specifications
            ]
            
            # Check for vague, unfalsifiable language
            vague_indicators = [
                'potentially', 'possibly', 'might', 'could',
                'may improve', 'suggests', 'indicates',
                'advanced techniques', 'sophisticated methods',
                'elegant approach', 'novel framework',
                'breakthrough', 'revolutionary'
            ]
            
            # Count quantitative vs vague indicators
            import re
            quantitative_matches = 0
            for pattern in quantitative_indicators:
                matches = len(re.findall(pattern, claim_text, re.IGNORECASE))
                quantitative_matches += matches
            
            vague_matches = 0
            for phrase in vague_indicators:
                if phrase.lower() in claim_text.lower():
                    vague_matches += 1
            
            test_result['falsifiability_analysis'] = {
                'quantitative_predictions': quantitative_matches,
                'vague_language_count': vague_matches,
                'specificity_ratio': quantitative_matches / max(vague_matches, 1)
            }
            
            # Test for testable hypotheses
            if 'hypothesis' not in claim and 'prediction' not in claim:
                test_result['violations'].append('NO_TESTABLE_HYPOTHESIS')
            
            # Test for quantitative predictions
            if quantitative_matches == 0:
                test_result['violations'].append('NO_QUANTITATIVE_PREDICTIONS')
            
            # Test for excessive vagueness
            if vague_matches > quantitative_matches * 2:
                test_result['violations'].append('EXCESSIVE_VAGUE_LANGUAGE')
            
            # Test for specific success/failure criteria
            success_criteria = claim.get('success_criteria', {})
            if not success_criteria:
                test_result['violations'].append('NO_SUCCESS_CRITERIA_DEFINED')
            
            # Determine falsifiability status
            if len(test_result['violations']) == 0:
                test_result['prediction_specificity'] = 'FALSIFIABLE'
                test_result['passed'] = True
            elif quantitative_matches > 0:
                test_result['prediction_specificity'] = 'PARTIALLY_FALSIFIABLE'
                # Allow partial pass for partially falsifiable claims
                if len(test_result['violations']) <= 1:
                    test_result['passed'] = True
            else:
                test_result['prediction_specificity'] = 'NON_FALSIFIABLE'
            
            return test_result
            
        except Exception as e:
            test_result['violations'].append(f'FALSIFIABILITY_TEST_ERROR: {e}')
            return test_result
    
    def _determine_validation_status(self, falsification_result: Dict) -> Dict:
        """
        Determine overall falsification status based on all test results.
        """
        status_result = {
            'falsification_status': 'UNKNOWN',
            'empirical_validation_status': 'UNKNOWN',
            'sakana_principle_compliance': False,
            'overall_assessment': 'UNKNOWN'
        }
        
        try:
            tests = falsification_result['falsification_tests']
            total_violations = len(falsification_result['violations'])
            
            # Count passed tests
            passed_tests = sum(1 for test in tests.values() if test.get('passed', False))
            total_tests = len(tests)
            
            # Critical failures that immediately fail falsification
            critical_violations = [
                'SIGNAL_UNDETECTABLE', 'SYNTHETIC_DATA_DETECTED', 
                'AUTHENTIC_DATA_NOT_CONFIRMED', 'INSTITUTIONAL_VALIDATION_FAILED'
            ]
            
            has_critical_violation = any(
                any(cv in violation for cv in critical_violations)
                for violation in falsification_result['violations']
            )
            
            # Determine falsification status
            if has_critical_violation:
                status_result['falsification_status'] = 'FALSIFIED'
                status_result['empirical_validation_status'] = 'CRITICAL_FAILURE'
                status_result['sakana_principle_compliance'] = False
                status_result['overall_assessment'] = 'CLAIM_REJECTED'
                
            elif total_violations == 0:
                status_result['falsification_status'] = 'NOT_FALSIFIED'
                status_result['empirical_validation_status'] = 'VALIDATED'
                status_result['sakana_principle_compliance'] = True
                status_result['overall_assessment'] = 'CLAIM_SUPPORTED'
                
            elif passed_tests >= total_tests * 0.8:  # 80% pass rate
                status_result['falsification_status'] = 'PARTIALLY_FALSIFIED'
                status_result['empirical_validation_status'] = 'REQUIRES_STRENGTHENING'
                status_result['sakana_principle_compliance'] = False
                status_result['overall_assessment'] = 'CLAIM_NEEDS_IMPROVEMENT'
                
            else:
                status_result['falsification_status'] = 'FALSIFIED'
                status_result['empirical_validation_status'] = 'INSUFFICIENT_EVIDENCE'
                status_result['sakana_principle_compliance'] = False
                status_result['overall_assessment'] = 'CLAIM_REJECTED'
            
            return status_result
            
        except Exception as e:
            logger.error(f"Status determination failed: {e}")
            status_result['falsification_status'] = 'ERROR'
            return status_result
    
    def _generate_validation_recommendations(self, falsification_result: Dict) -> List[str]:
        """
        Generate specific recommendations based on falsification results.
        """
        recommendations = []
        
        try:
            status = falsification_result['falsification_status']
            violations = falsification_result['violations']
            
            if status == 'FALSIFIED':
                recommendations.append("REJECT CLAIM: Failed empirical falsification tests")
                
                # Specific recommendations based on violations
                if any('UNDETECTABLE' in v for v in violations):
                    recommendations.append("Signal strength insufficient for detection - consider alternative approaches")
                    recommendations.append("Review experimental design to improve signal-to-noise ratio")
                
                if any('SYNTHETIC_DATA' in v for v in violations):
                    recommendations.append("Replace synthetic data with authentic observational datasets")
                    recommendations.append("Implement institutional data verification protocols")
                
                if any('STATISTICAL' in v for v in violations):
                    recommendations.append("Strengthen statistical analysis with larger sample sizes")
                    recommendations.append("Improve experimental design to meet significance thresholds")
                
            elif status == 'PARTIALLY_FALSIFIED':
                recommendations.append("CONDITIONAL ACCEPTANCE: Address identified weaknesses")
                recommendations.append("Strengthen empirical evidence before final acceptance")
                
                # Specific improvements needed
                if any('SNR' in v for v in violations):
                    recommendations.append("Improve signal detection methods or increase observation period")
                
                if any('SAMPLE_SIZE' in v for v in violations):
                    recommendations.append("Increase ensemble size or extend temporal coverage")
                
            elif status == 'NOT_FALSIFIED':
                recommendations.append("ACCEPT CLAIM: Passed all empirical falsification tests")
                recommendations.append("Claim demonstrates strong empirical support")
                recommendations.append("Meets Sakana Principle requirements for empirical validation")
                
            else:  # ERROR or UNKNOWN
                recommendations.append("DEFER DECISION: Address technical issues and resubmit")
                recommendations.append("Ensure all required evidence components are provided")
            
            # General recommendations for improvement
            if len(violations) > 0:
                recommendations.append("Implement systematic peer review before resubmission")
                recommendations.append("Consider collaboration with observational data specialists")
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Recommendation generation failed: {e}")
            return ["Error generating recommendations - manual review required"]
    
    def get_validation_summary(self) -> Dict:
        """
        Get summary statistics of all falsification attempts.
        """
        if not self.validation_history:
            return {'total_validations': 0, 'summary': 'No validations performed'}
        
        total_falsifications = len(self.falsification_history)
        
        # Count by status
        status_counts = {}
        for result in self.falsification_history:
            status = result['falsification_status']
            status_counts[status] = status_counts.get(status, 0) + 1
        
        # Count violations
        total_violations = len(self.violation_reports)
        
        # Calculate rates
        falsified_count = status_counts.get('FALSIFIED', 0) + status_counts.get('PARTIALLY_FALSIFIED', 0)
        not_falsified_count = status_counts.get('NOT_FALSIFIED', 0)
        
        falsification_rate = falsified_count / total_falsifications
        validation_rate = not_falsified_count / total_falsifications
        
        return {
            'total_falsifications': total_falsifications,
            'status_distribution': status_counts,
            'falsification_rate': falsification_rate,
            'validation_rate': validation_rate,
            'total_violations': total_violations,
            'violation_rate': total_violations / total_falsifications,
            'sakana_compliance_rate': validation_rate,
            'framework_effectiveness': 1 - falsification_rate  # Higher is better
        }
    
    def export_violation_report(self, output_path: str) -> None:
        """
        Export detailed violation report for analysis and improvement.
        """
        report = {
            'framework_info': {
                'version': '1.0.0',
                'strict_mode': self.strict_mode,
                'real_data_mandatory': self.real_data_mandatory,
                'generation_timestamp': datetime.now().isoformat()
            },
            'falsification_criteria': self.falsification_criteria,
            'approved_datasets': self.approved_datasets,
            'violation_reports': self.violation_reports,
            'summary_statistics': self.get_falsification_summary()
        }
        
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        logger.info(f"Violation report exported to: {output_path}")


# Historical case analysis - The Hangzhou incident that led to Sakana Principle
def analyze_hangzhou_case() -> Dict:
    """
    Analyze the historical Hangzhou case that led to the development
    of the Sakana Principle and empirical falsification framework.
    
    This case study demonstrates how theoretical elegance can mask
    empirical inadequacy, leading to the "plausibility trap."
    """
    hangzhou_case = {
        'case_name': 'Hangzhou Volterra Kernel Spectroscopy Incident',
        'date': '2025-08-13',
        'description': 'Theoretical proposal for climate signal detection using advanced mathematical frameworks',
        'theoretical_claim': {
            'title': 'Volterra Kernel Spectroscopy for Climate Intervention Detection',
            'claim_text': 'Advanced Volterra kernel eigenvalue decomposition with stochastic optimization enables precise climate signal detection',
            'sophistication_level': 'VERY_HIGH',
            'mathematical_complexity': 'ADVANCED',
            'parameters': {
                'detection_confidence': 0.95,
                'signal_processing_method': 'Volterra kernels',
                'optimization_algorithm': 'stochastic eigenvalue'
            }
        },
        'empirical_evidence': {
            'snr_analysis': {
                'snr_db': -15.54,  # The critical undetectable threshold
                'method': 'standard Python scientific computing',
                'detectable': False,
                'analysis_framework': 'SciPy, NumPy, xarray with real NCAR GLENS data'
            },
            'real_data_verification': {
                'dataset_used': 'NCAR GLENS',
                'authentic_data_confirmed': True,
                'analysis_method': 'Standard scientific computing stack'
            }
        },
        'falsification_result': {
            'falsification_status': 'FALSIFIED',
            'critical_finding': 'Signal undetectable against natural climate variability',
            'snr_threshold_violation': True,
            'lesson_learned': 'Theoretical sophistication without empirical validation leads to plausibility trap'
        },
        'sakana_principle_development': {
            'key_insight': 'Empirical falsification using real data reveals physically impossible claims',
            'prevention_mechanism': 'Mandatory SNR threshold validation with approved datasets',
            'implementation': 'REAL_DATA_MANDATORY=true, SYNTHETIC_DATA_FORBIDDEN=true'
        }
    }
    
    return hangzhou_case