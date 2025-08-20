"""
Climate Domain Validator

Specialized validator for climate research experiments including SAI, GeoMIP,
and general climate modeling studies. Inherits from UniversalBaseValidator
and adds climate-specific validation criteria.

Key Features:
- Climate data validation (GLENS, GeoMIP, ARISE-SAI)
- SAI experiment validation (pulse vs continuous)
- Physical constraint checking for climate models
- Temperature, precipitation, and aerosol validation
- Climate-specific statistical validation
"""

import logging
import numpy as np
from typing import Dict, List, Union, Optional, Any
from datetime import datetime

from .universal_base_validator import UniversalBaseValidator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ClimateValidator(UniversalBaseValidator):
    """
    Climate research domain validator with specialized validation for
    climate modeling, SAI experiments, and atmospheric science studies.
    """
    
    def __init__(self):
        """Initialize climate validator."""
        super().__init__("climate")
        
        logger.info("🌡️ Climate domain validator initialized")
    
    def _load_domain_config(self):
        """Load climate-specific validation configuration."""
        self.domain_specific_config = {
            'temperature_ranges': {
                'global_mean': (-50, 50),  # Celsius
                'surface_temperature': (-100, 60),
                'stratosphere_temperature': (-100, 20)
            },
            'aerosol_ranges': {
                'optical_depth': (0.0, 2.0),
                'mass_concentration': (0.0, 1000.0),  # μg/m³
                'injection_rate': (0.0, 50.0)  # Mt SO2/year
            },
            'climate_sensitivity': {
                'co2_doubling': (1.5, 4.5),  # K per CO2 doubling
                'aerosol_forcing': (-3.0, 0.0)  # W/m²
            },
            'sai_specific': {
                'injection_altitudes': (15, 25),  # km
                'particle_sizes': (0.1, 2.0),  # μm
                'residence_time': (0.5, 5.0)  # years
            },
            'statistical_requirements': {
                'minimum_years': 10,
                'seasonal_cycles': 4,
                'spatial_coverage': 0.8  # fraction of globe
            }
        }
    
    def validate_domain_experiment(self, experiment_config: Dict) -> Dict:
        """
        Validate climate experiment using climate-specific criteria.
        
        Args:
            experiment_config: Climate experiment configuration
            
        Returns:
            Dict with climate validation results
        """
        validation_start = datetime.now()
        
        # Initialize climate validation result
        climate_result = {
            'validation_timestamp': validation_start.isoformat(),
            'experiment_type': experiment_config.get('experiment_type', 'general_climate'),
            'climate_data_validation': None,
            'physical_constraints_check': None,
            'climate_statistical_validation': None,
            'sai_specific_validation': None,
            'real_data_verified': False,
            'empirical_validation_status': 'PENDING',
            'domain_compliance_status': 'PENDING',
            'confidence_level': 'UNKNOWN',
            'climate_validation_details': []
        }
        
        try:
            logger.info("🌡️ Starting climate domain validation")
            
            # Step 1: Universal validation requirements
            universal_results = self.validate_universal_requirements(experiment_config)
            climate_result['universal_validation'] = universal_results
            
            # Step 2: Climate data validation
            climate_data_validation = self._validate_climate_data(experiment_config)
            climate_result['climate_data_validation'] = climate_data_validation
            
            # Step 3: Physical constraints checking
            constraints_check = self._check_physical_constraints(experiment_config)
            climate_result['physical_constraints_check'] = constraints_check
            
            # Step 4: Climate statistical validation
            stats_validation = self._validate_climate_statistics(experiment_config)
            climate_result['climate_statistical_validation'] = stats_validation
            
            # Step 5: SAI-specific validation if applicable
            if experiment_config.get('experiment_type') in ['sai_analysis', 'sai_experiment']:
                sai_validation = self.validate_sai_experiment(experiment_config)
                climate_result['sai_specific_validation'] = sai_validation
            
            # Step 6: Overall climate domain assessment
            climate_result = self._assess_climate_domain_compliance(climate_result)
            
            # Log validation
            self.validation_history.append(climate_result)
            
            logger.info(f"✅ Climate validation complete: {climate_result['domain_compliance_status']}")
            
            return climate_result
            
        except Exception as e:
            climate_result['domain_compliance_status'] = 'VALIDATION_ERROR'
            climate_result['climate_validation_details'].append(f'Climate validation error: {str(e)}')
            logger.error(f"❌ Climate validation failed: {e}")
            return climate_result
    
    def _validate_climate_data(self, experiment_config: Dict) -> Dict:
        """Validate climate data sources and formats."""
        data_validation = {
            'data_sources_validated': [],
            'glens_data_verified': False,
            'geomip_compatibility': False,
            'temporal_coverage_adequate': False,
            'spatial_coverage_adequate': False,
            'variable_completeness': 'UNKNOWN',
            'data_validation_status': 'PENDING',
            'validation_details': []
        }
        
        # Check for climate datasets
        if 'real_dataset' in experiment_config:
            dataset = experiment_config['real_dataset']
            
            # Check for GLENS/GeoMIP markers
            if hasattr(dataset, 'attrs'):
                attrs = dataset.attrs if hasattr(dataset.attrs, 'items') else {}
                climate_markers = ['GLENS', 'GeoMIP', 'CESM', 'ARISE-SAI', 'NCAR', 'climate']
                
                found_markers = [
                    marker for marker in climate_markers
                    if any(marker.lower() in str(value).lower() for value in attrs.values())
                ]
                
                if found_markers:
                    data_validation['data_sources_validated'] = found_markers
                    if 'GLENS' in found_markers:
                        data_validation['glens_data_verified'] = True
                    if 'GeoMIP' in found_markers:
                        data_validation['geomip_compatibility'] = True
            
            # Check temporal coverage
            if hasattr(dataset, 'time') or 'time' in experiment_config.get('parameters', {}):
                years_param = experiment_config.get('parameters', {}).get('analysis_years', 0)
                if years_param >= self.domain_specific_config['statistical_requirements']['minimum_years']:
                    data_validation['temporal_coverage_adequate'] = True
                else:
                    data_validation['validation_details'].append(f'Insufficient temporal coverage: {years_param} years')
            
            # Check required climate variables
            required_vars = ['temperature', 'TREFHT', 'aerosol_optical_depth', 'BURDEN1']
            if hasattr(dataset, 'keys'):
                available_vars = list(dataset.keys()) if hasattr(dataset, 'keys') else []
                if any(var in available_vars for var in required_vars):
                    data_validation['variable_completeness'] = 'ADEQUATE'
                else:
                    data_validation['variable_completeness'] = 'INSUFFICIENT'
                    data_validation['validation_details'].append('Missing required climate variables')
        
        # Overall climate data validation
        if (data_validation['data_sources_validated'] and 
            data_validation['temporal_coverage_adequate'] and
            data_validation['variable_completeness'] == 'ADEQUATE'):
            data_validation['data_validation_status'] = 'VALIDATED'
        elif data_validation['data_sources_validated']:
            data_validation['data_validation_status'] = 'MARGINAL'
        else:
            data_validation['data_validation_status'] = 'FAILED'
            data_validation['validation_details'].append('Climate data validation failed')
        
        return data_validation
    
    def _check_physical_constraints(self, experiment_config: Dict) -> Dict:
        """Check climate-specific physical constraints."""
        constraints_check = {
            'temperature_constraints': 'UNKNOWN',
            'aerosol_constraints': 'UNKNOWN',
            'climate_sensitivity_constraints': 'UNKNOWN',
            'sai_constraints': 'UNKNOWN',
            'overall_constraints_status': 'PENDING',
            'constraint_violations': [],
            'constraint_details': []
        }
        
        # Check temperature constraints
        if 'parameters' in experiment_config:
            params = experiment_config['parameters']
            
            # Temperature range checking
            for temp_param in ['temperature', 'temp_change', 'cooling_effect']:
                if temp_param in params:
                    temp_value = params[temp_param]
                    if isinstance(temp_value, (int, float)):
                        temp_range = self.domain_specific_config['temperature_ranges']['global_mean']
                        if temp_range[0] <= temp_value <= temp_range[1]:
                            constraints_check['temperature_constraints'] = 'VALID'
                        else:
                            constraints_check['temperature_constraints'] = 'VIOLATED'
                            constraints_check['constraint_violations'].append(f'Temperature out of range: {temp_value}°C')
            
            # Aerosol constraints for SAI experiments
            if experiment_config.get('experiment_type') in ['sai_analysis', 'sai_experiment']:
                for aerosol_param in ['injection_rate', 'aod', 'aerosol_optical_depth']:
                    if aerosol_param in params:
                        aerosol_value = params[aerosol_param]
                        if isinstance(aerosol_value, (int, float)):
                            if 'optical_depth' in aerosol_param:
                                aod_range = self.domain_specific_config['aerosol_ranges']['optical_depth']
                                if aod_range[0] <= aerosol_value <= aod_range[1]:
                                    constraints_check['aerosol_constraints'] = 'VALID'
                                else:
                                    constraints_check['aerosol_constraints'] = 'VIOLATED'
                                    constraints_check['constraint_violations'].append(f'AOD out of range: {aerosol_value}')
                            elif 'injection' in aerosol_param:
                                injection_range = self.domain_specific_config['aerosol_ranges']['injection_rate']
                                if injection_range[0] <= aerosol_value <= injection_range[1]:
                                    constraints_check['sai_constraints'] = 'VALID'
                                else:
                                    constraints_check['sai_constraints'] = 'VIOLATED'
                                    constraints_check['constraint_violations'].append(f'Injection rate out of range: {aerosol_value}')
        
        # Overall constraint assessment
        constraint_statuses = [
            constraints_check['temperature_constraints'],
            constraints_check['aerosol_constraints'],
            constraints_check['sai_constraints']
        ]
        
        if 'VIOLATED' in constraint_statuses:
            constraints_check['overall_constraints_status'] = 'VIOLATIONS_FOUND'
        elif all(status in ['VALID', 'UNKNOWN'] for status in constraint_statuses):
            constraints_check['overall_constraints_status'] = 'CONSTRAINTS_SATISFIED'
        else:
            constraints_check['overall_constraints_status'] = 'PARTIAL_COMPLIANCE'
        
        return constraints_check
    
    def _validate_climate_statistics(self, experiment_config: Dict) -> Dict:
        """Validate climate-specific statistical requirements."""
        stats_validation = {
            'temporal_analysis_adequate': False,
            'spatial_analysis_adequate': False,
            'climate_trend_analysis': 'UNKNOWN',
            'seasonal_cycle_analysis': 'UNKNOWN',
            'statistical_significance_planned': False,
            'climate_stats_status': 'PENDING',
            'statistical_details': []
        }
        
        # Check for climate-specific statistical analysis
        if 'calculations' in experiment_config:
            calculations = experiment_config['calculations']
            
            # Check for temporal analysis
            temporal_keywords = ['trend', 'time_series', 'temporal', 'annual', 'monthly']
            if any(any(keyword in calc for keyword in temporal_keywords) for calc in calculations):
                stats_validation['temporal_analysis_adequate'] = True
                stats_validation['climate_trend_analysis'] = 'PLANNED'
            
            # Check for spatial analysis
            spatial_keywords = ['spatial', 'global', 'regional', 'latitude', 'longitude']
            if any(any(keyword in calc for keyword in spatial_keywords) for calc in calculations):
                stats_validation['spatial_analysis_adequate'] = True
            
            # Check for seasonal analysis
            seasonal_keywords = ['seasonal', 'season', 'cycle', 'winter', 'summer']
            if any(any(keyword in calc for keyword in seasonal_keywords) for calc in calculations):
                stats_validation['seasonal_cycle_analysis'] = 'PLANNED'
            
            # Check for statistical significance
            significance_keywords = ['statistical_analysis', 'significance', 'p_value', 'confidence']
            if any(any(keyword in calc for keyword in significance_keywords) for calc in calculations):
                stats_validation['statistical_significance_planned'] = True
        
        # Overall climate statistics validation
        if (stats_validation['temporal_analysis_adequate'] and 
            stats_validation['spatial_analysis_adequate'] and
            stats_validation['statistical_significance_planned']):
            stats_validation['climate_stats_status'] = 'ADEQUATE'
        elif stats_validation['temporal_analysis_adequate'] or stats_validation['spatial_analysis_adequate']:
            stats_validation['climate_stats_status'] = 'MARGINAL'
        else:
            stats_validation['climate_stats_status'] = 'INSUFFICIENT'
            stats_validation['statistical_details'].append('Insufficient climate statistical analysis')
        
        return stats_validation
    
    def validate_sai_experiment(self, experiment_config: Dict) -> Dict:
        """
        Specialized validation for SAI (Stratospheric Aerosol Injection) experiments.
        
        Args:
            experiment_config: SAI experiment configuration
            
        Returns:
            Dict with SAI-specific validation results
        """
        sai_validation = {
            'injection_strategy_validation': 'PENDING',
            'aerosol_transport_validation': 'PENDING',
            'climate_response_validation': 'PENDING',
            'pulse_vs_continuous_analysis': 'UNKNOWN',
            'glens_data_integration': False,
            'sai_physical_constraints': 'PENDING',
            'overall_sai_status': 'PENDING',
            'sai_validation_details': []
        }
        
        try:
            logger.info("🌡️ Validating SAI experiment specifics")
            
            # Check injection strategy
            injection_type = experiment_config.get('parameters', {}).get('injection_type')
            if injection_type in ['pulse', 'continuous']:
                sai_validation['injection_strategy_validation'] = 'VALID'
                sai_validation['pulse_vs_continuous_analysis'] = injection_type.upper()
            else:
                sai_validation['injection_strategy_validation'] = 'INVALID'
                sai_validation['sai_validation_details'].append('Invalid injection strategy')
            
            # Check for GLENS data integration
            if 'real_dataset' in experiment_config:
                dataset = experiment_config['real_dataset']
                if hasattr(dataset, 'attrs'):
                    attrs = dataset.attrs if hasattr(dataset.attrs, 'items') else {}
                    if any('GLENS' in str(value) for value in attrs.values()):
                        sai_validation['glens_data_integration'] = True
            
            # Check aerosol transport calculations
            if 'calculations' in experiment_config:
                calculations = experiment_config['calculations']
                transport_keywords = ['transport', 'aerosol', 'diffusion', 'residence']
                if any(any(keyword in calc for keyword in transport_keywords) for calc in calculations):
                    sai_validation['aerosol_transport_validation'] = 'PLANNED'
                else:
                    sai_validation['aerosol_transport_validation'] = 'MISSING'
                
                # Check climate response analysis
                response_keywords = ['climate', 'temperature', 'cooling', 'response']
                if any(any(keyword in calc for keyword in response_keywords) for calc in calculations):
                    sai_validation['climate_response_validation'] = 'PLANNED'
                else:
                    sai_validation['climate_response_validation'] = 'MISSING'
            
            # Check SAI physical constraints
            if 'parameters' in experiment_config:
                params = experiment_config['parameters']
                sai_params = ['injection_rate', 'injection_altitude', 'particle_size']
                
                sai_constraints_valid = True
                for param in sai_params:
                    if param in params:
                        value = params[param]
                        if param == 'injection_altitude':
                            altitude_range = self.domain_specific_config['sai_specific']['injection_altitudes']
                            if not (altitude_range[0] <= value <= altitude_range[1]):
                                sai_constraints_valid = False
                                sai_validation['sai_validation_details'].append(f'Invalid injection altitude: {value} km')
                
                sai_validation['sai_physical_constraints'] = 'VALID' if sai_constraints_valid else 'VIOLATED'
            
            # Overall SAI validation assessment
            sai_components = [
                sai_validation['injection_strategy_validation'],
                sai_validation['aerosol_transport_validation'],
                sai_validation['climate_response_validation']
            ]
            
            if all(comp in ['VALID', 'PLANNED'] for comp in sai_components):
                sai_validation['overall_sai_status'] = 'SAI_EXPERIMENT_VALIDATED'
            elif any(comp in ['VALID', 'PLANNED'] for comp in sai_components):
                sai_validation['overall_sai_status'] = 'SAI_EXPERIMENT_MARGINAL'
            else:
                sai_validation['overall_sai_status'] = 'SAI_EXPERIMENT_FAILED'
                sai_validation['sai_validation_details'].append('SAI experiment validation failed')
            
            return sai_validation
            
        except Exception as e:
            sai_validation['overall_sai_status'] = 'SAI_VALIDATION_ERROR'
            sai_validation['sai_validation_details'].append(f'SAI validation error: {str(e)}')
            logger.error(f"❌ SAI validation failed: {e}")
            return sai_validation
    
    def _assess_climate_domain_compliance(self, climate_result: Dict) -> Dict:
        """Assess overall climate domain compliance."""
        # Extract component results
        universal_results = climate_result.get('universal_validation', {})
        data_validation = climate_result.get('climate_data_validation', {})
        constraints_check = climate_result.get('physical_constraints_check', {})
        stats_validation = climate_result.get('climate_statistical_validation', {})
        sai_validation = climate_result.get('sai_specific_validation', {})
        
        # Set real data verification status
        if data_validation.get('data_validation_status') == 'VALIDATED':
            climate_result['real_data_verified'] = True
        
        # Set empirical validation status
        empirical_components = [
            universal_results.get('empirical_validation', {}).get('status'),
            data_validation.get('data_validation_status'),
            stats_validation.get('climate_stats_status')
        ]
        
        if all(comp in ['PASSED', 'VALIDATED', 'ADEQUATE'] for comp in empirical_components):
            climate_result['empirical_validation_status'] = 'SUFFICIENT'
        elif any(comp in ['PASSED', 'VALIDATED', 'ADEQUATE'] for comp in empirical_components):
            climate_result['empirical_validation_status'] = 'MARGINAL'
        else:
            climate_result['empirical_validation_status'] = 'INSUFFICIENT'
        
        # Set overall domain compliance
        compliance_components = [
            universal_results.get('overall_universal_status'),
            data_validation.get('data_validation_status'),
            constraints_check.get('overall_constraints_status'),
            stats_validation.get('climate_stats_status')
        ]
        
        if sai_validation:
            compliance_components.append(sai_validation.get('overall_sai_status'))
        
        passed_components = sum(1 for comp in compliance_components 
                              if comp in ['PASSED', 'VALIDATED', 'ADEQUATE', 'CONSTRAINTS_SATISFIED', 'SAI_EXPERIMENT_VALIDATED'])
        
        if passed_components >= len(compliance_components) * 0.8:
            climate_result['domain_compliance_status'] = 'COMPLIANT'
            climate_result['confidence_level'] = 'HIGH'
        elif passed_components >= len(compliance_components) * 0.6:
            climate_result['domain_compliance_status'] = 'MARGINAL_COMPLIANCE'
            climate_result['confidence_level'] = 'MODERATE'
        else:
            climate_result['domain_compliance_status'] = 'NON_COMPLIANT'
            climate_result['confidence_level'] = 'LOW'
        
        return climate_result
    
    def get_domain_validation_criteria(self) -> Dict:
        """Get climate-specific validation criteria."""
        return {
            'domain': 'climate',
            'required_data_sources': ['GLENS', 'GeoMIP', 'ARISE-SAI', 'observational'],
            'physical_constraints': self.domain_specific_config,
            'statistical_requirements': self.domain_specific_config['statistical_requirements'],
            'sai_specific_criteria': self.domain_specific_config['sai_specific'],
            'validation_categories': [
                'climate_data_validation',
                'physical_constraints_check',
                'climate_statistical_validation',
                'sai_specific_validation'
            ]
        }