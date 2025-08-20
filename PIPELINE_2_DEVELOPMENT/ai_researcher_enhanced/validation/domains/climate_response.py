"""
Climate Response Domain Validator

Flexible validation for climate response experiments including:
- Temperature and precipitation studies
- Climate sensitivity analysis  
- Feedback mechanism studies
- Regional climate impacts
- Long-term trend analysis
- Climate model validation

This module adapts the Sakana Principle to climate response research
with domain-appropriate validation criteria.
"""

import numpy as np
from typing import Dict, Union, Optional, Tuple, List, Any
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ClimateResponseValidator:
    """
    Flexible validator for climate response experiments.
    
    Adapts universal Sakana Principle requirements to climate-specific
    validation criteria while maintaining scientific rigor.
    """
    
    def __init__(self):
        """Initialize climate response validator with flexible ranges."""
        
        # Climate parameter ranges (flexible for different contexts)
        self.climate_ranges = {
            # Temperature responses
            'temperature_change_k': (-15.0, 15.0),        # Global/regional temperature changes
            'temperature_anomaly_k': (-10.0, 10.0),       # Temperature anomalies
            'warming_rate_k_decade': (-2.0, 2.0),         # Warming/cooling rates
            
            # Precipitation responses
            'precipitation_change_percent': (-80.0, 80.0), # Precipitation changes
            'precipitation_anomaly_mm': (-1000, 1000),     # Precipitation anomalies
            'drought_index': (-5.0, 5.0),                  # Drought severity indices
            
            # Climate sensitivity
            'climate_sensitivity_k': (1.5, 6.0),           # Climate sensitivity range
            'feedback_parameter': (-5.0, 0.0),             # Climate feedback parameter
            'equilibrium_time_years': (10, 200),           # Equilibration timescales
            
            # Radiative forcing
            'radiative_forcing_wm2': (-20.0, 20.0),        # RF range for various agents
            'albedo_change': (-0.5, 0.5),                  # Albedo changes
            'cloud_radiative_effect_wm2': (-100, 50),      # Cloud radiative effects
            
            # Spatial and temporal scales
            'spatial_scale_km': (1, 20000),                # From local to global
            'temporal_scale_years': (0.1, 1000),           # From seasonal to millennial
            'correlation_coefficient': (-1.0, 1.0),        # Statistical correlations
            
            # Physical constraints
            'heat_capacity_jkg_k': (500, 5000),            # Specific heat capacity
            'thermal_diffusivity_m2s': (1e-8, 1e-4),       # Thermal diffusivity
        }
        
        # Expected datasets for climate validation
        self.climate_datasets = {
            'model_output': ['GLENS', 'ARISE-SAI', 'GeoMIP', 'CMIP6'],
            'observations': ['HadCRUT', 'GISTEMP', 'ERA5', 'GPCP'],
            'reanalysis': ['NCEP', 'ERA-Interim', 'JRA-55'],
            'paleoclimate': ['LGM', 'mid-Holocene', 'PETM']
        }
        
        # Climate phenomena detection keywords
        self.phenomena_keywords = {
            'temperature': ['temperature', 'warming', 'cooling', 'thermal', 'heat'],
            'precipitation': ['precipitation', 'rainfall', 'drought', 'flood', 'humidity'],
            'circulation': ['circulation', 'wind', 'jet stream', 'monsoon', 'enso'],
            'ice': ['ice', 'glacier', 'snow', 'cryosphere', 'albedo'],
            'ocean': ['ocean', 'sea level', 'circulation', 'thermal expansion'],
            'clouds': ['cloud', 'albedo', 'feedback', 'radiative']
        }
        
        self.validation_history = []
        
        logger.info("Climate Response Validator initialized with flexible validation criteria")
    
    def validate_climate_experiment(self, experiment: Dict) -> Dict[str, Any]:
        """
        Comprehensive validation for climate response experiments.
        
        Args:
            experiment: Climate experiment description with parameters
            
        Returns:
            Dict containing detailed climate validation results
        """
        validation_result = {
            'experiment_type': 'climate_response',
            'validation_timestamp': datetime.now().isoformat(),
            'climate_validation_passed': False,
            'phenomena_analysis': {},
            'parameter_validation': {},
            'physical_consistency': {},
            'statistical_validation': {},
            'temporal_validation': {},
            'violations': [],
            'recommendations': []
        }
        
        try:
            # Detect climate phenomena
            phenomena_analysis = self._analyze_climate_phenomena(experiment)
            validation_result['phenomena_analysis'] = phenomena_analysis
            
            # Validate climate parameters
            parameter_validation = self._validate_climate_parameters(experiment.get('parameters', {}))
            validation_result['parameter_validation'] = parameter_validation
            
            if not parameter_validation['parameters_valid']:
                validation_result['violations'].extend(parameter_validation['violations'])
            
            # Check physical consistency
            physical_consistency = self._check_physical_consistency(experiment.get('parameters', {}))
            validation_result['physical_consistency'] = physical_consistency
            
            if not physical_consistency['physically_consistent']:
                validation_result['violations'].extend(physical_consistency['violations'])
            
            # Statistical validation
            statistical_validation = self._validate_statistical_methods(experiment)
            validation_result['statistical_validation'] = statistical_validation
            
            if not statistical_validation['statistically_valid']:
                validation_result['violations'].extend(statistical_validation['violations'])
            
            # Temporal validation
            temporal_validation = self._validate_temporal_scales(experiment.get('parameters', {}))
            validation_result['temporal_validation'] = temporal_validation
            
            if not temporal_validation['temporally_valid']:
                validation_result['violations'].extend(temporal_validation['violations'])
            
            # Overall validation status
            validation_result['climate_validation_passed'] = len(validation_result['violations']) == 0
            
            # Generate recommendations
            validation_result['recommendations'] = self._generate_climate_recommendations(validation_result)
            
            self.validation_history.append(validation_result)
            
            logger.info(f"Climate response validation: "
                       f"{'PASS' if validation_result['climate_validation_passed'] else 'FAIL'}")
            
            return validation_result
            
        except Exception as e:
            logger.error(f"Climate response validation failed: {e}")
            validation_result['violations'].append(f'CLIMATE_VALIDATION_ERROR: {e}')
            return validation_result
    
    def _analyze_climate_phenomena(self, experiment: Dict) -> Dict[str, Any]:
        """Analyze and identify climate phenomena in experiment."""
        phenomena_result = {
            'detected_phenomena': [],
            'primary_focus': None,
            'complexity_level': 'single',
            'spatial_scope': 'unknown',
            'temporal_scope': 'unknown'
        }
        
        experiment_text = str(experiment).lower()
        
        # Detect phenomena
        for phenomenon, keywords in self.phenomena_keywords.items():
            if any(keyword in experiment_text for keyword in keywords):
                phenomena_result['detected_phenomena'].append(phenomenon)
        
        # Determine primary focus
        if phenomena_result['detected_phenomena']:
            phenomena_result['primary_focus'] = phenomena_result['detected_phenomena'][0]
        
        # Assess complexity
        if len(phenomena_result['detected_phenomena']) > 2:
            phenomena_result['complexity_level'] = 'multi-phenomena'
        elif len(phenomena_result['detected_phenomena']) == 2:
            phenomena_result['complexity_level'] = 'coupled'
        
        # Determine spatial scope
        if any(term in experiment_text for term in ['global', 'worldwide', 'planetary']):
            phenomena_result['spatial_scope'] = 'global'
        elif any(term in experiment_text for term in ['regional', 'continental', 'basin']):
            phenomena_result['spatial_scope'] = 'regional'
        elif any(term in experiment_text for term in ['local', 'site', 'station']):
            phenomena_result['spatial_scope'] = 'local'
        
        # Determine temporal scope
        if any(term in experiment_text for term in ['century', 'centennial', 'long-term']):
            phenomena_result['temporal_scope'] = 'long-term'
        elif any(term in experiment_text for term in ['decade', 'decadal']):
            phenomena_result['temporal_scope'] = 'decadal'
        elif any(term in experiment_text for term in ['annual', 'yearly', 'seasonal']):
            phenomena_result['temporal_scope'] = 'interannual'
        
        return phenomena_result
    
    def _validate_climate_parameters(self, parameters: Dict) -> Dict[str, Any]:
        """Validate climate-specific parameters against realistic ranges."""
        parameter_result = {
            'parameters_valid': True,
            'parameter_checks': [],
            'violations': []
        }
        
        for param_name, param_value in parameters.items():
            if isinstance(param_value, (int, float)):
                param_check = self._check_parameter_range(param_name, param_value)
                parameter_result['parameter_checks'].append(param_check)
                
                if not param_check['valid']:
                    parameter_result['violations'].append(
                        f'CLIMATE_PARAMETER_OUT_OF_RANGE: {param_name}={param_value}'
                    )
                    parameter_result['parameters_valid'] = False
        
        return parameter_result
    
    def _check_parameter_range(self, param_name: str, param_value: float) -> Dict[str, Any]:
        """Check if parameter value is within realistic climate range."""
        param_check = {
            'parameter': param_name,
            'value': param_value,
            'valid': True,
            'applicable_range': None,
            'range_type': 'unknown'
        }
        
        # Find applicable range
        for range_key, (min_val, max_val) in self.climate_ranges.items():
            # Flexible matching: check if any part of range_key matches parameter name
            range_parts = range_key.split('_')
            param_parts = param_name.lower().split('_')
            
            if any(part in param_parts for part in range_parts):
                param_check['applicable_range'] = (min_val, max_val)
                param_check['range_type'] = range_key
                param_check['valid'] = min_val <= param_value <= max_val
                break
        
        return param_check
    
    def _check_physical_consistency(self, parameters: Dict) -> Dict[str, Any]:
        """Check physical consistency of climate parameters."""
        consistency_result = {
            'physically_consistent': True,
            'consistency_checks': [],
            'violations': []
        }
        
        # Energy balance check
        if 'radiative_forcing_wm2' in parameters and 'temperature_change_k' in parameters:
            rf = parameters['radiative_forcing_wm2']
            dt = parameters['temperature_change_k']
            
            # Rough climate sensitivity check (1.5-6 K per doubling CO2 ~ 3.7 W/m²)
            expected_sensitivity_range = (0.4, 1.6)  # K per W/m²
            actual_sensitivity = abs(dt / rf) if rf != 0 else 0
            
            consistency_check = {
                'check_type': 'energy_balance',
                'radiative_forcing': rf,
                'temperature_change': dt,
                'implied_sensitivity': actual_sensitivity,
                'expected_range': expected_sensitivity_range,
                'consistent': expected_sensitivity_range[0] <= actual_sensitivity <= expected_sensitivity_range[1]
            }
            
            consistency_result['consistency_checks'].append(consistency_check)
            
            if not consistency_check['consistent']:
                consistency_result['violations'].append(
                    f'ENERGY_BALANCE_INCONSISTENT: Implied sensitivity {actual_sensitivity:.2f} K/(W/m²) outside expected range'
                )
                consistency_result['physically_consistent'] = False
        
        # Precipitation-temperature relationship check
        if 'precipitation_change_percent' in parameters and 'temperature_change_k' in parameters:
            precip_change = parameters['precipitation_change_percent']
            temp_change = parameters['temperature_change_k']
            
            # Clausius-Clapeyron relation suggests ~7% per K for water vapor
            if temp_change != 0:
                precip_sensitivity = precip_change / temp_change
                expected_range = (-15, 15)  # %/K, allowing for dynamic effects
                
                consistency_check = {
                    'check_type': 'precipitation_temperature_scaling',
                    'precipitation_change_percent': precip_change,
                    'temperature_change_k': temp_change,
                    'precipitation_sensitivity': precip_sensitivity,
                    'expected_range': expected_range,
                    'consistent': expected_range[0] <= precip_sensitivity <= expected_range[1]
                }
                
                consistency_result['consistency_checks'].append(consistency_check)
                
                if not consistency_check['consistent']:
                    consistency_result['violations'].append(
                        f'PRECIPITATION_SCALING_INCONSISTENT: {precip_sensitivity:.1f} %/K outside expected range'
                    )
                    consistency_result['physically_consistent'] = False
        
        return consistency_result
    
    def _validate_statistical_methods(self, experiment: Dict) -> Dict[str, Any]:
        """Validate statistical methods and significance testing."""
        statistical_result = {
            'statistically_valid': True,
            'methods_detected': [],
            'significance_checks': [],
            'violations': []
        }
        
        experiment_text = str(experiment).lower()
        
        # Detect statistical methods
        statistical_methods = {
            'correlation': ['correlation', 'pearson', 'spearman'],
            'regression': ['regression', 'linear', 'trend'],
            'significance': ['significance', 'p-value', 'confidence'],
            'time_series': ['time series', 'autocorrelation', 'spectral'],
            'spatial': ['spatial', 'gridded', 'interpolation']
        }
        
        for method_type, keywords in statistical_methods.items():
            if any(keyword in experiment_text for keyword in keywords):
                statistical_result['methods_detected'].append(method_type)
        
        # Check for statistical significance considerations
        parameters = experiment.get('parameters', {})
        
        if 'p_value' in parameters:
            p_value = parameters['p_value']
            significance_check = {
                'test_type': 'p_value_check',
                'p_value': p_value,
                'significant': p_value < 0.05,
                'highly_significant': p_value < 0.01
            }
            statistical_result['significance_checks'].append(significance_check)
            
            if p_value > 0.1:
                statistical_result['violations'].append(
                    f'STATISTICAL_SIGNIFICANCE_LOW: p-value {p_value} > 0.1 (not significant)'
                )
                statistical_result['statistically_valid'] = False
        
        if 'correlation_coefficient' in parameters:
            corr_coef = parameters['correlation_coefficient']
            if not (-1.0 <= corr_coef <= 1.0):
                statistical_result['violations'].append(
                    f'CORRELATION_OUT_OF_BOUNDS: Correlation {corr_coef} outside [-1, 1]'
                )
                statistical_result['statistically_valid'] = False
        
        return statistical_result
    
    def _validate_temporal_scales(self, parameters: Dict) -> Dict[str, Any]:
        """Validate temporal scales and consistency."""
        temporal_result = {
            'temporally_valid': True,
            'scale_analysis': {},
            'violations': []
        }
        
        # Check temporal scale parameters
        temporal_params = ['temporal_scale_years', 'equilibrium_time_years', 
                          'response_time_years', 'timescale_years']
        
        detected_scales = {}
        for param_name in temporal_params:
            if param_name in parameters:
                scale_value = parameters[param_name]
                detected_scales[param_name] = scale_value
                
                # Check if scale is reasonable
                if scale_value <= 0:
                    temporal_result['violations'].append(
                        f'TEMPORAL_SCALE_INVALID: {param_name}={scale_value} must be positive'
                    )
                    temporal_result['temporally_valid'] = False
                
                elif scale_value > 10000:  # Beyond reasonable climate scales
                    temporal_result['violations'].append(
                        f'TEMPORAL_SCALE_TOO_LONG: {param_name}={scale_value} years exceeds realistic climate timescales'
                    )
                    temporal_result['temporally_valid'] = False
        
        temporal_result['scale_analysis'] = {
            'detected_scales': detected_scales,
            'shortest_scale': min(detected_scales.values()) if detected_scales else None,
            'longest_scale': max(detected_scales.values()) if detected_scales else None,
            'scale_separation': max(detected_scales.values()) / min(detected_scales.values()) if len(detected_scales) > 1 else 1.0
        }
        
        return temporal_result
    
    def _generate_climate_recommendations(self, validation_result: Dict) -> List[str]:
        """Generate climate-specific recommendations."""
        recommendations = []
        violations = validation_result['violations']
        
        if validation_result['climate_validation_passed']:
            recommendations.append("✅ Climate response experiment meets validation criteria")
        else:
            recommendations.append("❌ Climate response validation failed - address issues below")
        
        # Phenomena-specific recommendations
        phenomena = validation_result['phenomena_analysis']['detected_phenomena']
        if phenomena:
            recommendations.append(f"🌍 Detected climate phenomena: {', '.join(phenomena)}")
            
            if 'temperature' in phenomena:
                recommendations.append("🌡️ For temperature studies: Consider regional variations and seasonal cycles")
            if 'precipitation' in phenomena:
                recommendations.append("🌧️ For precipitation studies: Account for spatial heterogeneity and extreme events")
            if 'circulation' in phenomena:
                recommendations.append("💨 For circulation studies: Include multiple pressure levels and dynamics")
        
        # Parameter recommendations
        if any('CLIMATE_PARAMETER_OUT_OF_RANGE' in v for v in violations):
            recommendations.append("📊 Parameter values outside realistic climate ranges")
            recommendations.append("• Review observational constraints and model ranges")
            recommendations.append("• Consider uncertainties and ensemble approaches")
        
        # Physical consistency recommendations
        if any('ENERGY_BALANCE_INCONSISTENT' in v for v in violations):
            recommendations.append("⚖️ Energy balance inconsistency detected")
            recommendations.append("• Check climate sensitivity assumptions")
            recommendations.append("• Verify radiative forcing calculations")
        
        # Statistical recommendations
        if any('STATISTICAL_SIGNIFICANCE_LOW' in v for v in violations):
            recommendations.append("📈 Statistical significance concerns")
            recommendations.append("• Increase sample size or analysis period")
            recommendations.append("• Consider multiple testing corrections")
        
        # Dataset recommendations
        recommendations.append("📚 Recommended datasets for climate validation:")
        recommendations.append("• GLENS/ARISE-SAI for geoengineering experiments")
        recommendations.append("• CMIP6 models for climate change studies")
        recommendations.append("• ERA5/NCEP reanalysis for observational constraints")
        recommendations.append("• HadCRUT/GISTEMP for temperature validation")
        
        return recommendations
    
    def get_climate_validation_summary(self) -> Dict[str, Any]:
        """Get summary of climate response validation history."""
        if not self.validation_history:
            return {'total_validations': 0, 'summary': 'No climate response validations performed'}
        
        total = len(self.validation_history)
        passed = sum(1 for v in self.validation_history if v['climate_validation_passed'])
        
        # Analyze common phenomena
        all_phenomena = []
        for validation in self.validation_history:
            phenomena = validation.get('phenomena_analysis', {}).get('detected_phenomena', [])
            all_phenomena.extend(phenomena)
        
        from collections import Counter
        phenomena_counts = Counter(all_phenomena)
        
        return {
            'total_climate_validations': total,
            'success_rate': passed / total,
            'most_common_phenomena': phenomena_counts.most_common(3),
            'physical_consistency_failure_rate': sum(1 for v in self.validation_history 
                                                   if not v.get('physical_consistency', {}).get('physically_consistent', True)) / total,
            'statistical_failure_rate': sum(1 for v in self.validation_history 
                                          if not v.get('statistical_validation', {}).get('statistically_valid', True)) / total
        }