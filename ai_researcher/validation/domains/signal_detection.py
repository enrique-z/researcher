"""
Signal Detection Domain Validator

Specialized validation for signal detection experiments including:
- Spectroscopy (including Volterra kernel approaches)
- Remote sensing and satellite observations  
- Radar and lidar measurements
- Communications signal analysis
- Acoustic signal processing

This module contains the spectroscopy-specific thresholds and SNR analysis
that were identified in the Hangzhou case, but ONLY applies them when
the experiment is actually about signal detection.
"""

import numpy as np
import xarray as xr
import scipy.stats as stats
from typing import Dict, Union, Optional, Tuple, List
import warnings
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SignalDetectionValidator:
    """
    Specialized validator for signal detection experiments.
    
    Contains the spectroscopy-specific validation criteria including
    the critical -15.54 dB threshold from the Hangzhou case.
    """
    
    def __init__(self, ensemble_size_min: int = 10, temporal_persistence_years: int = 3):
        """
        Initialize signal detection validator.
        
        Args:
            ensemble_size_min: Minimum ensemble members for statistical validation
            temporal_persistence_years: Minimum persistence for signal detection
        """
        self.ensemble_size_min = ensemble_size_min
        self.temporal_persistence_years = temporal_persistence_years
        
        # Signal detection thresholds (from research and Hangzhou case)
        self.snr_thresholds = {
            'undetectable_limit_db': -15.54,   # Critical threshold from Hangzhou spectroscopy case
            'minimum_detectable_db': 0.0,      # Hansen methodology minimum
            'standard_confidence_db': 6.0,     # Standard detection threshold
            'high_confidence_db': 9.5,         # High-confidence detection
            'exceptional_db': 15.0             # Exceptional signal strength
        }
        
        # Spectroscopy-specific parameters
        self.spectroscopy_ranges = {
            'volterra_kernel_order': (1, 5),           # Kernel expansion order
            'eigenvalue_count': (1, 1000),             # Number of eigenvalues
            'frequency_resolution_hz': (0.001, 1000),  # Spectral resolution
            'integration_time_s': (0.1, 3600),         # Signal integration time
            'optical_depth': (0.001, 10.0),            # Atmospheric optical depth
        }
        
        # Signal detection history
        self.detection_history = []
        
        logger.info("Signal Detection Validator initialized with Hangzhou case thresholds")
    
    def validate_signal_experiment(self, experiment: Dict) -> Dict:
        """
        Comprehensive validation for signal detection experiments.
        
        Args:
            experiment: Signal detection experiment description
            
        Returns:
            Dict containing detailed signal detection validation results
        """
        validation_result = {
            'experiment_type': 'signal_detection',
            'validation_timestamp': datetime.now().isoformat(),
            'signal_validation_passed': False,
            'snr_analysis': {},
            'spectroscopy_validation': {},
            'detection_feasibility': {},
            'hangzhou_case_check': {},
            'violations': [],
            'recommendations': []
        }
        
        try:
            # Extract signal parameters
            parameters = experiment.get('parameters', {})
            
            # SNR Analysis (core of signal detection validation)
            snr_analysis = self._analyze_snr_requirements(parameters)
            validation_result['snr_analysis'] = snr_analysis
            
            if not snr_analysis['snr_adequate']:
                validation_result['violations'].extend(snr_analysis['violations'])
            
            # Spectroscopy-specific validation (if applicable)
            if self._is_spectroscopy_experiment(experiment):
                spectroscopy_validation = self._validate_spectroscopy_specifics(experiment)
                validation_result['spectroscopy_validation'] = spectroscopy_validation
                
                if not spectroscopy_validation['spectroscopy_valid']:
                    validation_result['violations'].extend(spectroscopy_validation['violations'])
            
            # Detection feasibility analysis
            feasibility = self._assess_detection_feasibility(experiment)
            validation_result['detection_feasibility'] = feasibility
            
            if not feasibility['detection_feasible']:
                validation_result['violations'].extend(feasibility['violations'])
            
            # Hangzhou case prevention check
            hangzhou_check = self._check_hangzhou_case_prevention(experiment)
            validation_result['hangzhou_case_check'] = hangzhou_check
            
            if hangzhou_check['hangzhou_risk_detected']:
                validation_result['violations'].extend(hangzhou_check['violations'])
            
            # Overall signal validation status
            validation_result['signal_validation_passed'] = len(validation_result['violations']) == 0
            
            # Generate recommendations
            validation_result['recommendations'] = self._generate_signal_recommendations(validation_result)
            
            # Record validation
            self.detection_history.append(validation_result)
            
            logger.info(f"Signal detection validation: "
                       f"{'PASS' if validation_result['signal_validation_passed'] else 'FAIL'}")
            
            return validation_result
            
        except Exception as e:
            logger.error(f"Signal detection validation failed: {e}")
            validation_result['violations'].append(f'SIGNAL_VALIDATION_ERROR: {e}')
            return validation_result
    
    def calculate_snr(self, 
                     theoretical_signal: Union[np.ndarray, xr.DataArray], 
                     real_dataset: Union[np.ndarray, xr.DataArray], 
                     method: str = 'hansen') -> Dict:
        """
        Calculate Signal-to-Noise Ratio using specified methodology.
        
        This is the core SNR calculation that was used to identify the
        -15.54 dB threshold in the Hangzhou spectroscopy case.
        
        Args:
            theoretical_signal: Predicted signal from theory
            real_dataset: Real observational data for noise characterization
            method: SNR calculation method ('hansen', 'welch', 'periodogram')
            
        Returns:
            Dict containing SNR analysis results
        """
        snr_result = {
            'snr_linear': 0.0,
            'snr_db': -np.inf,
            'method': method,
            'signal_power': 0.0,
            'noise_power': 0.0,
            'detectable': False,
            'confidence_level': 0.0,
            'analysis_timestamp': datetime.now().isoformat()
        }
        
        try:
            # Convert to numpy arrays if needed
            if hasattr(theoretical_signal, 'values'):
                signal = theoretical_signal.values.flatten()
            else:
                signal = np.asarray(theoretical_signal).flatten()
            
            if hasattr(real_dataset, 'values'):
                noise = real_dataset.values.flatten()
            else:
                noise = np.asarray(real_dataset).flatten()
            
            # Ensure same length
            min_length = min(len(signal), len(noise))
            signal = signal[:min_length]
            noise = noise[:min_length]
            
            if method == 'hansen':
                snr_result.update(self._calculate_snr_hansen(signal, noise))
            elif method == 'welch':
                snr_result.update(self._calculate_snr_welch(signal, noise))
            elif method == 'periodogram':
                snr_result.update(self._calculate_snr_periodogram(signal, noise))
            else:
                raise ValueError(f"Unknown SNR method: {method}")
            
            # Determine detectability based on thresholds
            snr_db = snr_result['snr_db']
            
            if snr_db <= self.snr_thresholds['undetectable_limit_db']:
                snr_result['detectable'] = False
                snr_result['detection_category'] = 'UNDETECTABLE'
                snr_result['hangzhou_case_risk'] = True
            elif snr_db < self.snr_thresholds['minimum_detectable_db']:
                snr_result['detectable'] = False
                snr_result['detection_category'] = 'BELOW_MINIMUM'
            elif snr_db < self.snr_thresholds['standard_confidence_db']:
                snr_result['detectable'] = True
                snr_result['detection_category'] = 'MARGINALLY_DETECTABLE'
            elif snr_db < self.snr_thresholds['high_confidence_db']:
                snr_result['detectable'] = True
                snr_result['detection_category'] = 'DETECTABLE'
            else:
                snr_result['detectable'] = True
                snr_result['detection_category'] = 'HIGH_CONFIDENCE'
            
            return snr_result
            
        except Exception as e:
            logger.error(f"SNR calculation failed: {e}")
            snr_result['error'] = str(e)
            return snr_result
    
    def _calculate_snr_hansen(self, signal: np.ndarray, noise: np.ndarray) -> Dict:
        """Hansen's classical SNR methodology."""
        signal_power = np.var(signal)
        noise_power = np.var(noise)
        
        if noise_power == 0:
            snr_linear = np.inf
            snr_db = np.inf
        else:
            snr_linear = signal_power / noise_power
            snr_db = 10 * np.log10(snr_linear) if snr_linear > 0 else -np.inf
        
        return {
            'snr_linear': snr_linear,
            'snr_db': snr_db,
            'signal_power': signal_power,
            'noise_power': noise_power,
            'method_details': 'Hansen classical variance-based SNR'
        }
    
    def _calculate_snr_welch(self, signal: np.ndarray, noise: np.ndarray) -> Dict:
        """Welch's method for spectral SNR analysis."""
        from scipy import signal as scipy_signal
        
        # Compute power spectral densities
        f_signal, psd_signal = scipy_signal.welch(signal)
        f_noise, psd_noise = scipy_signal.welch(noise)
        
        # Calculate SNR in frequency domain
        signal_power = np.mean(psd_signal)
        noise_power = np.mean(psd_noise)
        
        if noise_power == 0:
            snr_linear = np.inf
            snr_db = np.inf
        else:
            snr_linear = signal_power / noise_power
            snr_db = 10 * np.log10(snr_linear) if snr_linear > 0 else -np.inf
        
        return {
            'snr_linear': snr_linear,
            'snr_db': snr_db,
            'signal_power': signal_power,
            'noise_power': noise_power,
            'method_details': 'Welch spectral estimation',
            'frequency_analysis': {
                'peak_frequency': f_signal[np.argmax(psd_signal)],
                'bandwidth': f_signal[-1] - f_signal[0]
            }
        }
    
    def _calculate_snr_periodogram(self, signal: np.ndarray, noise: np.ndarray) -> Dict:
        """Periodogram-based SNR analysis."""
        from scipy import signal as scipy_signal
        
        # Compute periodograms
        f_signal, psd_signal = scipy_signal.periodogram(signal)
        f_noise, psd_noise = scipy_signal.periodogram(noise)
        
        # Calculate average power
        signal_power = np.mean(psd_signal)
        noise_power = np.mean(psd_noise)
        
        if noise_power == 0:
            snr_linear = np.inf
            snr_db = np.inf
        else:
            snr_linear = signal_power / noise_power
            snr_db = 10 * np.log10(snr_linear) if snr_linear > 0 else -np.inf
        
        return {
            'snr_linear': snr_linear,
            'snr_db': snr_db,
            'signal_power': signal_power,
            'noise_power': noise_power,
            'method_details': 'Periodogram power estimation'
        }
    
    def _analyze_snr_requirements(self, parameters: Dict) -> Dict:
        """Analyze SNR requirements from experiment parameters."""
        snr_analysis = {
            'snr_adequate': False,
            'snr_db': None,
            'threshold_comparison': {},
            'violations': []
        }
        
        # Extract SNR information from parameters
        snr_params = ['snr_db', 'signal_to_noise_ratio', 'snr_threshold', 'signal_strength']
        snr_value = None
        
        for param in snr_params:
            if param in parameters:
                snr_value = parameters[param]
                break
        
        if snr_value is None:
            snr_analysis['violations'].append('NO_SNR_SPECIFIED')
            return snr_analysis
        
        snr_analysis['snr_db'] = snr_value
        
        # Compare against thresholds
        thresholds = self.snr_thresholds
        snr_analysis['threshold_comparison'] = {
            'above_undetectable_limit': snr_value > thresholds['undetectable_limit_db'],
            'above_minimum_detectable': snr_value >= thresholds['minimum_detectable_db'],
            'above_standard_confidence': snr_value >= thresholds['standard_confidence_db'],
            'above_high_confidence': snr_value >= thresholds['high_confidence_db']
        }
        
        # Check for violations
        if snr_value <= thresholds['undetectable_limit_db']:
            snr_analysis['violations'].append(
                f'SNR_UNDETECTABLE: {snr_value} dB <= {thresholds["undetectable_limit_db"]} dB (Hangzhou limit)'
            )
        elif snr_value < thresholds['minimum_detectable_db']:
            snr_analysis['violations'].append(
                f'SNR_BELOW_MINIMUM: {snr_value} dB < {thresholds["minimum_detectable_db"]} dB'
            )
        else:
            snr_analysis['snr_adequate'] = True
        
        return snr_analysis
    
    def _is_spectroscopy_experiment(self, experiment: Dict) -> bool:
        """Determine if experiment involves spectroscopy."""
        content = str(experiment).lower()
        spectroscopy_indicators = [
            'spectroscopy', 'spectral', 'volterra', 'kernel', 'eigenvalue',
            'optical', 'infrared', 'lidar', 'radar', 'remote sensing'
        ]
        return any(indicator in content for indicator in spectroscopy_indicators)
    
    def _validate_spectroscopy_specifics(self, experiment: Dict) -> Dict:
        """Validate spectroscopy-specific parameters and methods."""
        spectroscopy_result = {
            'spectroscopy_valid': False,
            'volterra_validation': {},
            'optical_validation': {},
            'violations': []
        }
        
        parameters = experiment.get('parameters', {})
        
        # Volterra kernel validation (if applicable)
        if 'volterra' in str(experiment).lower():
            volterra_validation = self._validate_volterra_parameters(parameters)
            spectroscopy_result['volterra_validation'] = volterra_validation
            
            if not volterra_validation['valid']:
                spectroscopy_result['violations'].extend(volterra_validation['violations'])
        
        # Optical parameter validation
        optical_validation = self._validate_optical_parameters(parameters)
        spectroscopy_result['optical_validation'] = optical_validation
        
        if not optical_validation['valid']:
            spectroscopy_result['violations'].extend(optical_validation['violations'])
        
        spectroscopy_result['spectroscopy_valid'] = len(spectroscopy_result['violations']) == 0
        
        return spectroscopy_result
    
    def _validate_volterra_parameters(self, parameters: Dict) -> Dict:
        """Validate Volterra kernel-specific parameters."""
        volterra_result = {
            'valid': True,
            'violations': [],
            'parameter_checks': []
        }
        
        # Check Volterra-specific parameters
        volterra_params = {
            'kernel_order': 'volterra_kernel_order',
            'eigenvalue_count': 'eigenvalue_count'
        }
        
        for param_key, range_key in volterra_params.items():
            if param_key in parameters:
                value = parameters[param_key]
                if range_key in self.spectroscopy_ranges:
                    min_val, max_val = self.spectroscopy_ranges[range_key]
                    
                    param_check = {
                        'parameter': param_key,
                        'value': value,
                        'range': (min_val, max_val),
                        'valid': min_val <= value <= max_val
                    }
                    
                    volterra_result['parameter_checks'].append(param_check)
                    
                    if not param_check['valid']:
                        volterra_result['valid'] = False
                        volterra_result['violations'].append(
                            f'VOLTERRA_PARAM_OUT_OF_RANGE: {param_key}={value} outside [{min_val}, {max_val}]'
                        )
        
        return volterra_result
    
    def _validate_optical_parameters(self, parameters: Dict) -> Dict:
        """Validate optical measurement parameters."""
        optical_result = {
            'valid': True,
            'violations': [],
            'parameter_checks': []
        }
        
        # Check optical parameters
        optical_params = {
            'integration_time': 'integration_time_s',
            'optical_depth': 'optical_depth',
            'frequency_resolution': 'frequency_resolution_hz'
        }
        
        for param_key, range_key in optical_params.items():
            if param_key in parameters:
                value = parameters[param_key]
                if range_key in self.spectroscopy_ranges:
                    min_val, max_val = self.spectroscopy_ranges[range_key]
                    
                    param_check = {
                        'parameter': param_key,
                        'value': value,
                        'range': (min_val, max_val),
                        'valid': min_val <= value <= max_val
                    }
                    
                    optical_result['parameter_checks'].append(param_check)
                    
                    if not param_check['valid']:
                        optical_result['valid'] = False
                        optical_result['violations'].append(
                            f'OPTICAL_PARAM_OUT_OF_RANGE: {param_key}={value} outside [{min_val}, {max_val}]'
                        )
        
        return optical_result
    
    def _assess_detection_feasibility(self, experiment: Dict) -> Dict:
        """Assess overall detection feasibility."""
        feasibility_result = {
            'detection_feasible': False,
            'feasibility_score': 0.0,
            'limiting_factors': [],
            'violations': []
        }
        
        parameters = experiment.get('parameters', {})
        feasibility_score = 0.0
        
        # SNR contribution to feasibility
        snr_value = parameters.get('snr_db', parameters.get('signal_to_noise_ratio', -np.inf))
        if snr_value > self.snr_thresholds['high_confidence_db']:
            feasibility_score += 0.4
        elif snr_value > self.snr_thresholds['standard_confidence_db']:
            feasibility_score += 0.3
        elif snr_value > self.snr_thresholds['minimum_detectable_db']:
            feasibility_score += 0.2
        else:
            feasibility_result['limiting_factors'].append('Insufficient SNR')
        
        # Integration time contribution
        integration_time = parameters.get('integration_time', parameters.get('observation_time', 0))
        if integration_time > 3600:  # > 1 hour
            feasibility_score += 0.2
        elif integration_time > 600:  # > 10 minutes
            feasibility_score += 0.1
        else:
            feasibility_result['limiting_factors'].append('Short integration time')
        
        # Ensemble size contribution
        ensemble_size = parameters.get('ensemble_size', 1)
        if ensemble_size >= 20:
            feasibility_score += 0.2
        elif ensemble_size >= 10:
            feasibility_score += 0.1
        else:
            feasibility_result['limiting_factors'].append('Small ensemble size')
        
        # Temporal persistence contribution
        persistence = parameters.get('temporal_persistence_years', 0)
        if persistence >= self.temporal_persistence_years:
            feasibility_score += 0.2
        else:
            feasibility_result['limiting_factors'].append('Insufficient temporal persistence')
        
        feasibility_result['feasibility_score'] = feasibility_score
        feasibility_result['detection_feasible'] = feasibility_score >= 0.6
        
        if not feasibility_result['detection_feasible']:
            feasibility_result['violations'].append(
                f'DETECTION_NOT_FEASIBLE: Score {feasibility_score:.2f} < 0.6'
            )
        
        return feasibility_result
    
    def _check_hangzhou_case_prevention(self, experiment: Dict) -> Dict:
        """
        Check for patterns similar to the Hangzhou case that led to the Sakana Principle.
        
        The Hangzhou case involved elegant Volterra kernel spectroscopy theory
        that was empirically falsified by the -15.54 dB undetectable signal threshold.
        """
        hangzhou_check = {
            'hangzhou_risk_detected': False,
            'risk_factors': [],
            'violations': [],
            'prevention_measures': []
        }
        
        content = str(experiment).lower()
        parameters = experiment.get('parameters', {})
        
        # Check for Hangzhou-like patterns
        hangzhou_indicators = [
            'volterra', 'kernel', 'spectroscopy', 'eigenvalue', 'optimization',
            'sophisticated', 'elegant', 'advanced mathematical'
        ]
        
        sophisticated_count = sum(1 for indicator in hangzhou_indicators if indicator in content)
        
        # Check SNR value
        snr_value = parameters.get('snr_db', parameters.get('signal_to_noise_ratio', 0))
        
        # Risk factor analysis
        if sophisticated_count >= 2:
            hangzhou_check['risk_factors'].append('High theoretical sophistication')
        
        if snr_value <= self.snr_thresholds['undetectable_limit_db']:
            hangzhou_check['risk_factors'].append(f'SNR at/below Hangzhou threshold ({snr_value} dB)')
            hangzhou_check['hangzhou_risk_detected'] = True
            hangzhou_check['violations'].append(
                f'HANGZHOU_CASE_RISK: SNR {snr_value} dB matches undetectable threshold'
            )
        
        # Check for lack of empirical grounding
        empirical_indicators = ['measured', 'observed', 'glens', 'data', 'validation']
        empirical_count = sum(1 for indicator in empirical_indicators if indicator in content)
        
        if sophisticated_count >= 2 and empirical_count == 0:
            hangzhou_check['risk_factors'].append('Sophisticated theory without empirical grounding')
            hangzhou_check['hangzhou_risk_detected'] = True
            hangzhou_check['violations'].append('HANGZHOU_PATTERN: Elegant theory lacks empirical validation')
        
        # Prevention measures
        if hangzhou_check['hangzhou_risk_detected']:
            hangzhou_check['prevention_measures'] = [
                'Increase SNR above -15.54 dB threshold',
                'Include real GLENS data validation',
                'Provide quantitative empirical evidence',
                'Reduce theoretical complexity if not empirically supported'
            ]
        
        return hangzhou_check
    
    def _generate_signal_recommendations(self, validation_result: Dict) -> List[str]:
        """Generate recommendations specific to signal detection experiments."""
        recommendations = []
        violations = validation_result['violations']
        
        if validation_result['signal_validation_passed']:
            recommendations.append("✅ Signal detection experiment meets validation criteria")
        else:
            recommendations.append("❌ Signal detection validation failed - address issues below")
        
        # SNR-specific recommendations
        if any('SNR_UNDETECTABLE' in v for v in violations):
            recommendations.append("🚨 CRITICAL: Signal undetectable (Hangzhou case risk)")
            recommendations.append("• Increase signal strength or reduce noise")
            recommendations.append("• Consider alternative detection methods")
            recommendations.append("• Extend observation time or ensemble size")
        
        if any('SNR_BELOW_MINIMUM' in v for v in violations):
            recommendations.append("⚠️  SNR below minimum detection threshold")
            recommendations.append("• Improve signal processing techniques")
            recommendations.append("• Increase integration time")
        
        # Spectroscopy-specific recommendations
        if 'spectroscopy_validation' in validation_result:
            if any('VOLTERRA_PARAM_OUT_OF_RANGE' in v for v in violations):
                recommendations.append("• Review Volterra kernel parameters for physical realism")
            
            if any('OPTICAL_PARAM_OUT_OF_RANGE' in v for v in violations):
                recommendations.append("• Adjust optical parameters to realistic ranges")
        
        # Hangzhou case prevention
        if validation_result.get('hangzhou_case_check', {}).get('hangzhou_risk_detected', False):
            recommendations.append("🚨 HANGZHOU CASE RISK DETECTED")
            recommendations.append("• This pattern matches the original plausibility trap")
            recommendations.append("• Require empirical validation before proceeding")
            recommendations.append("• Consider fundamental experimental redesign")
        
        return recommendations
    
    def get_signal_detection_summary(self) -> Dict:
        """Get summary of signal detection validation history."""
        if not self.detection_history:
            return {'total_validations': 0, 'summary': 'No signal detection validations performed'}
        
        total = len(self.detection_history)
        passed = sum(1 for v in self.detection_history if v['signal_validation_passed'])
        hangzhou_risks = sum(1 for v in self.detection_history 
                           if v.get('hangzhou_case_check', {}).get('hangzhou_risk_detected', False))
        
        return {
            'total_signal_validations': total,
            'success_rate': passed / total,
            'hangzhou_risk_detection_rate': hangzhou_risks / total,
            'average_snr_db': np.mean([
                v.get('snr_analysis', {}).get('snr_db', 0) 
                for v in self.detection_history 
                if 'snr_analysis' in v and 'snr_db' in v['snr_analysis']
            ]) if total > 0 else 0,
            'undetectable_signal_rate': sum(1 for v in self.detection_history 
                                          if any('SNR_UNDETECTABLE' in viol 
                                                for viol in v.get('violations', []))) / total
        }