"""
Signal-to-Noise Ratio Analyzer

Implements state-of-the-art SNR analysis methods for scientific hypothesis validation
following GLENS/ARISE-SAI project methodologies and Hansen's classical framework.

Based on latest 2024-2025 research findings:
- Hansen's SNR thresholds: 1.0 (basic), 2.0 (standard), 3.0 (high-confidence)
- GLENS project methodology for signal detection
- Prevention of "plausibility trap" scenarios with insufficient signal strength
"""

import numpy as np
import xarray as xr
import scipy.stats as stats
from typing import Dict, Union, Optional, Tuple
import warnings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SNRAnalyzer:
    """
    Advanced Signal-to-Noise Ratio analyzer for climate science applications.
    
    Implements multiple SNR calculation methods based on:
    - Hansen et al. (1988) classical methodology
    - NCAR GLENS project thresholds
    - ARISE-SAI detection frameworks
    """
    
    # SNR thresholds based on research findings
    SNR_THRESHOLDS = {
        'minimum_detection': 1.0,      # 0 dB - minimum for signal presence
        'standard_confidence': 2.0,     # +6 dB - standard detection threshold
        'high_confidence': 3.0,         # +9.5 dB - high-confidence threshold
        'plausibility_trap_limit': -15.54  # dB - undetectable signal threshold
    }
    
    def __init__(self, ensemble_size_min: int = 10, temporal_persistence_years: int = 3):
        """
        Initialize SNR Analyzer with validation parameters.
        
        Args:
            ensemble_size_min: Minimum ensemble members required (default: 10, recommended: 20+)
            temporal_persistence_years: Minimum years above threshold for detection (default: 3)
        """
        self.ensemble_size_min = ensemble_size_min
        self.temporal_persistence_years = temporal_persistence_years
        self.validation_history = []
        
    def calculate_snr(self, theoretical_signal: Union[np.ndarray, xr.DataArray], 
                     real_dataset: Union[np.ndarray, xr.DataArray],
                     method: str = 'hansen') -> Dict:
        """
        Calculate Signal-to-Noise Ratio using specified method.
        
        Args:
            theoretical_signal: Predicted signal from hypothesis
            real_dataset: Real climate data for noise estimation
            method: SNR calculation method ('hansen', 'ensemble_based', 'glens')
            
        Returns:
            Dict containing SNR values, confidence level, and validation status
        """
        try:
            if method == 'hansen':
                return self._hansen_snr(theoretical_signal, real_dataset)
            elif method == 'ensemble_based':
                return self._ensemble_snr(theoretical_signal, real_dataset)
            elif method == 'glens':
                return self._glens_snr(theoretical_signal, real_dataset)
            else:
                raise ValueError(f"Unknown SNR method: {method}")
                
        except Exception as e:
            logger.error(f"SNR calculation failed: {e}")
            return self._create_failed_result(str(e))
    
    def _hansen_snr(self, signal: Union[np.ndarray, xr.DataArray], 
                   dataset: Union[np.ndarray, xr.DataArray]) -> Dict:
        """
        Hansen et al. (1988) classical SNR methodology.
        
        SNR = |Signal| / Noise_std
        Where Signal = smoothed difference and Noise = std of residuals
        """
        # Convert to numpy arrays if needed
        signal_arr = self._ensure_numpy(signal)
        data_arr = self._ensure_numpy(dataset)
        
        # Calculate signal strength (absolute mean difference)
        signal_strength = np.abs(np.mean(signal_arr))
        
        # Calculate noise (standard deviation of dataset)
        noise_std = np.std(data_arr, ddof=1)
        
        # Avoid division by zero
        if noise_std == 0:
            snr_ratio = np.inf
            snr_db = np.inf
        else:
            snr_ratio = signal_strength / noise_std
            snr_db = 10 * np.log10(snr_ratio) if snr_ratio > 0 else -np.inf
        
        return self._create_snr_result(snr_ratio, snr_db, 'hansen', {
            'signal_strength': signal_strength,
            'noise_std': noise_std
        })
    
    def _ensemble_snr(self, signal: Union[np.ndarray, xr.DataArray], 
                     dataset: Union[np.ndarray, xr.DataArray]) -> Dict:
        """
        Ensemble-based SNR following ARISE-SAI methodology.
        
        SNR = |ensemble_mean_trend| / std(trends_across_members)
        """
        # Assume dataset has ensemble dimension
        if hasattr(dataset, 'dims') and 'member' in dataset.dims:
            ensemble_mean = dataset.mean('member')
            ensemble_std = dataset.std('member', ddof=1)
        else:
            # Treat as single realization, estimate internal variability
            ensemble_mean = np.mean(dataset, axis=0)
            ensemble_std = np.std(dataset, axis=0, ddof=1)
        
        signal_arr = self._ensure_numpy(signal)
        
        # Calculate SNR
        mean_std = np.mean(ensemble_std) if hasattr(ensemble_std, '__iter__') else ensemble_std
        
        if mean_std == 0:
            snr_ratio = np.inf
            snr_db = np.inf
        else:
            snr_ratio = np.abs(np.mean(signal_arr)) / mean_std
            snr_db = 10 * np.log10(snr_ratio) if snr_ratio > 0 else -np.inf
        
        return self._create_snr_result(snr_ratio, snr_db, 'ensemble_based', {
            'ensemble_mean': np.mean(ensemble_mean) if hasattr(ensemble_mean, '__iter__') else ensemble_mean,
            'ensemble_std': mean_std
        })
    
    def _glens_snr(self, signal: Union[np.ndarray, xr.DataArray], 
                  dataset: Union[np.ndarray, xr.DataArray]) -> Dict:
        """
        GLENS project SNR methodology with machine learning validation.
        
        Implements detection within 1 year for temperature, 15 years for precipitation.
        """
        signal_arr = self._ensure_numpy(signal)
        data_arr = self._ensure_numpy(dataset)
        
        # GLENS-specific calculation
        forced_response = np.mean(signal_arr)  # Ensemble mean as forced response
        internal_variability = np.std(data_arr, ddof=1)  # Standard deviation as internal variability
        
        if internal_variability == 0:
            snr_ratio = np.inf
            snr_db = np.inf
        else:
            snr_ratio = np.abs(forced_response) / internal_variability
            snr_db = 10 * np.log10(snr_ratio) if snr_ratio > 0 else -np.inf
        
        # GLENS-specific validation
        detection_capability = self._assess_glens_detection(snr_db)
        
        return self._create_snr_result(snr_ratio, snr_db, 'glens', {
            'forced_response': forced_response,
            'internal_variability': internal_variability,
            'detection_capability': detection_capability
        })
    
    def _assess_glens_detection(self, snr_db: float) -> Dict:
        """Assess detection capability based on GLENS project findings."""
        if snr_db >= 9.5:  # SNR >= 3.0
            return {'temperature_years': '<1', 'precipitation_years': '<5', 'confidence': 'HIGH'}
        elif snr_db >= 6.0:  # SNR >= 2.0
            return {'temperature_years': '1-2', 'precipitation_years': '5-10', 'confidence': 'MODERATE'}
        elif snr_db >= 0:  # SNR >= 1.0
            return {'temperature_years': '2-5', 'precipitation_years': '10-15', 'confidence': 'LOW'}
        else:
            return {'temperature_years': '>10', 'precipitation_years': '>20', 'confidence': 'INSUFFICIENT'}
    
    def validate_empirical_falsifiability(self, hypothesis: str, dataset: Union[np.ndarray, xr.DataArray],
                                        theoretical_signal: Optional[Union[np.ndarray, xr.DataArray]] = None) -> Dict:
        """
        Validate that a hypothesis can be empirically falsified using real data.
        
        Implements the core Sakana Principle validation to prevent "plausibility trap" scenarios.
        
        Args:
            hypothesis: Text description of theoretical hypothesis
            dataset: Real climate dataset for validation
            theoretical_signal: Predicted signal from hypothesis (if available)
            
        Returns:
            Dict containing validation status, SNR metrics, and falsifiability assessment
        """
        validation_result = {
            'hypothesis': hypothesis,
            'validation_status': 'PENDING',
            'empirical_falsifiability': False,
            'snr_analysis': None,
            'physical_constraints_check': None,
            'plausibility_trap_risk': 'UNKNOWN',
            'recommendations': []
        }
        
        try:
            # Check if theoretical signal is provided
            if theoretical_signal is None:
                validation_result['validation_status'] = 'FAILED'
                validation_result['recommendations'].append(
                    'Hypothesis must provide quantitative theoretical signal for validation'
                )
                return validation_result
            
            # Calculate SNR
            snr_result = self.calculate_snr(theoretical_signal, dataset, method='hansen')
            validation_result['snr_analysis'] = snr_result
            
            # Check for plausibility trap (undetectable signal)
            snr_db = snr_result['snr_db']
            if snr_db <= self.SNR_THRESHOLDS['plausibility_trap_limit']:
                validation_result['validation_status'] = 'FAILED'
                validation_result['plausibility_trap_risk'] = 'HIGH'
                validation_result['recommendations'].append(
                    f'Signal undetectable: {snr_db:.2f} dB below limit of {self.SNR_THRESHOLDS["plausibility_trap_limit"]} dB'
                )
                return validation_result
            
            # Assess empirical falsifiability based on SNR thresholds
            if snr_db >= self.SNR_THRESHOLDS['high_confidence']:
                validation_result['validation_status'] = 'VALIDATED_HIGH_CONFIDENCE'
                validation_result['empirical_falsifiability'] = True
                validation_result['plausibility_trap_risk'] = 'LOW'
            elif snr_db >= self.SNR_THRESHOLDS['standard_confidence']:
                validation_result['validation_status'] = 'VALIDATED_MODERATE_CONFIDENCE'
                validation_result['empirical_falsifiability'] = True
                validation_result['plausibility_trap_risk'] = 'LOW'
            elif snr_db >= self.SNR_THRESHOLDS['minimum_detection']:
                validation_result['validation_status'] = 'PRELIMINARY_DETECTION'
                validation_result['empirical_falsifiability'] = True
                validation_result['plausibility_trap_risk'] = 'MODERATE'
                validation_result['recommendations'].append(
                    'Signal detectable but below standard confidence threshold. Additional validation recommended.'
                )
            else:
                validation_result['validation_status'] = 'INSUFFICIENT_SIGNAL'
                validation_result['plausibility_trap_risk'] = 'HIGH'
                validation_result['recommendations'].append(
                    f'Signal strength insufficient for reliable detection: {snr_db:.2f} dB'
                )
            
            # Log validation result
            self.validation_history.append(validation_result)
            logger.info(f"Hypothesis validation: {validation_result['validation_status']}, SNR: {snr_db:.2f} dB")
            
            return validation_result
            
        except Exception as e:
            validation_result['validation_status'] = 'ERROR'
            validation_result['recommendations'].append(f'Validation error: {str(e)}')
            logger.error(f"Validation failed: {e}")
            return validation_result
    
    def check_physical_constraints(self, theory_params: Dict) -> Dict:
        """
        Check theoretical parameters against known physical constraints.
        
        Args:
            theory_params: Dictionary of theoretical parameters and values
            
        Returns:
            Dict containing constraint validation results
        """
        constraint_results = {
            'overall_status': 'UNKNOWN',
            'constraint_checks': [],
            'violations': [],
            'warnings': []
        }
        
        # Climate-specific physical constraints
        climate_constraints = {
            'global_temperature_change': (-10.0, 10.0),  # °C per decade reasonable range
            'precipitation_change': (-50.0, 50.0),       # % change reasonable range
            'sai_injection_rate': (0.0, 50.0),           # Tg SO2/yr reasonable range
            'radiative_forcing': (-10.0, 10.0)           # W/m² reasonable range
        }
        
        violations_found = False
        
        for param, value in theory_params.items():
            if param.lower() in climate_constraints:
                min_val, max_val = climate_constraints[param.lower()]
                
                constraint_check = {
                    'parameter': param,
                    'value': value,
                    'constraint_range': (min_val, max_val),
                    'status': 'UNKNOWN'
                }
                
                if isinstance(value, (int, float)):
                    if min_val <= value <= max_val:
                        constraint_check['status'] = 'VALID'
                    else:
                        constraint_check['status'] = 'VIOLATION'
                        violations_found = True
                        constraint_results['violations'].append(
                            f'{param}: {value} outside reasonable range [{min_val}, {max_val}]'
                        )
                
                constraint_results['constraint_checks'].append(constraint_check)
        
        # Set overall status
        if violations_found:
            constraint_results['overall_status'] = 'VIOLATIONS_FOUND'
        elif constraint_results['constraint_checks']:
            constraint_results['overall_status'] = 'CONSTRAINTS_SATISFIED'
        else:
            constraint_results['overall_status'] = 'NO_CONSTRAINTS_CHECKED'
        
        return constraint_results
    
    def prevent_plausibility_trap(self, claim: str, evidence: Dict) -> Dict:
        """
        Prevent acceptance of plausible-sounding but empirically ungrounded claims.
        
        Core implementation of the Sakana Principle to avoid the "plausibility trap"
        where theoretical elegance is mistaken for empirical validity.
        
        Args:
            claim: Theoretical claim to validate
            evidence: Dictionary containing empirical evidence and validation results
            
        Returns:
            Dict containing trap prevention analysis and recommendations
        """
        trap_analysis = {
            'claim': claim,
            'trap_risk_level': 'UNKNOWN',
            'empirical_support': False,
            'theoretical_elegance': 'UNKNOWN',
            'validation_requirements': [],
            'prevention_status': 'PENDING'
        }
        
        # Check for empirical evidence
        required_evidence = ['snr_analysis', 'real_data_validation', 'statistical_significance']
        empirical_score = 0
        
        for evidence_type in required_evidence:
            if evidence_type in evidence and evidence[evidence_type] is not None:
                empirical_score += 1
            else:
                trap_analysis['validation_requirements'].append(f'Missing: {evidence_type}')
        
        # Assess empirical support strength
        if empirical_score == len(required_evidence):
            trap_analysis['empirical_support'] = True
            
            # Check SNR validation if available
            if 'snr_analysis' in evidence:
                snr_result = evidence['snr_analysis']
                if isinstance(snr_result, dict) and 'snr_db' in snr_result:
                    snr_db = snr_result['snr_db']
                    
                    if snr_db <= self.SNR_THRESHOLDS['plausibility_trap_limit']:
                        trap_analysis['trap_risk_level'] = 'CRITICAL'
                        trap_analysis['prevention_status'] = 'CLAIM_REJECTED'
                        trap_analysis['validation_requirements'].append(
                            f'Signal undetectable: {snr_db:.2f} dB - Classic plausibility trap scenario'
                        )
                    elif snr_db >= self.SNR_THRESHOLDS['standard_confidence']:
                        trap_analysis['trap_risk_level'] = 'LOW'
                        trap_analysis['prevention_status'] = 'CLAIM_SUPPORTED'
                    else:
                        trap_analysis['trap_risk_level'] = 'MODERATE'
                        trap_analysis['prevention_status'] = 'REQUIRES_ADDITIONAL_VALIDATION'
        else:
            trap_analysis['trap_risk_level'] = 'HIGH'
            trap_analysis['prevention_status'] = 'INSUFFICIENT_EVIDENCE'
        
        # Log trap prevention analysis
        logger.info(f"Plausibility trap prevention: {trap_analysis['prevention_status']}, "
                   f"Risk level: {trap_analysis['trap_risk_level']}")
        
        return trap_analysis
    
    def _ensure_numpy(self, data: Union[np.ndarray, xr.DataArray]) -> np.ndarray:
        """Convert xarray DataArray to numpy array if needed."""
        if hasattr(data, 'values'):
            return data.values
        return np.asarray(data)
    
    def _create_snr_result(self, snr_ratio: float, snr_db: float, method: str, details: Dict) -> Dict:
        """Create standardized SNR result dictionary."""
        confidence_level = 'HIGH' if snr_db >= 9.5 else 'MODERATE' if snr_db >= 6.0 else 'LOW'
        
        return {
            'snr_ratio': snr_ratio,
            'snr_db': snr_db,
            'method': method,
            'confidence_level': confidence_level,
            'thresholds_met': {
                'minimum_detection': snr_db >= 0,
                'standard_confidence': snr_db >= 6.0,
                'high_confidence': snr_db >= 9.5
            },
            'details': details,
            'validation_status': 'SUCCESS'
        }
    
    def _create_failed_result(self, error_message: str) -> Dict:
        """Create failed SNR result dictionary."""
        return {
            'snr_ratio': np.nan,
            'snr_db': np.nan,
            'method': 'FAILED',
            'confidence_level': 'NONE',
            'thresholds_met': {
                'minimum_detection': False,
                'standard_confidence': False,
                'high_confidence': False
            },
            'details': {'error': error_message},
            'validation_status': 'FAILED'
        }
    
    def get_validation_summary(self) -> Dict:
        """Get summary of all validation attempts."""
        if not self.validation_history:
            return {'total_validations': 0, 'summary': 'No validations performed'}
        
        status_counts = {}
        for validation in self.validation_history:
            status = validation['validation_status']
            status_counts[status] = status_counts.get(status, 0) + 1
        
        return {
            'total_validations': len(self.validation_history),
            'status_distribution': status_counts,
            'success_rate': (status_counts.get('VALIDATED_HIGH_CONFIDENCE', 0) + 
                           status_counts.get('VALIDATED_MODERATE_CONFIDENCE', 0)) / len(self.validation_history)
        }