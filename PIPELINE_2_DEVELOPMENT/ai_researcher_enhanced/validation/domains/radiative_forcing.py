"""
Radiative Forcing Domain Validator

Flexible validation for radiative forcing experiments including:
- Solar and longwave radiation studies
- Albedo and reflection analysis
- Cloud radiative effects
- Aerosol-radiation interactions
- Surface energy balance
- Atmospheric heating/cooling rates

This module adapts the Sakana Principle to radiative forcing research
with domain-appropriate validation criteria.
"""

import numpy as np
from typing import Dict, Union, Optional, Tuple, List, Any
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RadiativeForcingValidator:
    """
    Flexible validator for radiative forcing experiments.
    
    Adapts universal Sakana Principle requirements to radiation-specific
    validation criteria while maintaining physical realism.
    """
    
    def __init__(self):
        """Initialize radiative forcing validator with flexible ranges."""
        
        # Radiative forcing parameter ranges
        self.radiative_ranges = {
            # Fundamental radiation quantities
            'radiative_forcing_wm2': (-30.0, 30.0),        # Total RF range
            'solar_forcing_wm2': (-20.0, 20.0),            # Solar/shortwave forcing
            'longwave_forcing_wm2': (-15.0, 15.0),         # Longwave/thermal forcing
            'net_radiation_wm2': (-50.0, 400.0),           # Net radiation at surface
            
            # Optical properties
            'albedo': (0.0, 1.0),                          # Surface/cloud albedo
            'reflectance': (0.0, 1.0),                     # Spectral reflectance
            'transmittance': (0.0, 1.0),                   # Atmospheric transmittance
            'absorptance': (0.0, 1.0),                     # Absorption coefficient
            'optical_depth': (0.0, 10.0),                  # Optical depth
            'single_scattering_albedo': (0.0, 1.0),        # Scattering efficiency
            
            # Spectral properties
            'wavelength_um': (0.1, 100.0),                 # Wavelength range
            'frequency_hz': (1e12, 1e16),                  # Frequency range
            'wavenumber_cm1': (10, 10000),                 # Wavenumber range
            
            # Cloud radiative properties
            'cloud_radiative_effect_wm2': (-150.0, 50.0),  # CRE range
            'cloud_shortwave_effect_wm2': (-200.0, 0.0),   # SW cloud effect (cooling)
            'cloud_longwave_effect_wm2': (0.0, 100.0),     # LW cloud effect (warming)
            'cloud_optical_thickness': (0.0, 150.0),       # Cloud optical depth
            
            # Aerosol radiative properties
            'aerosol_optical_depth': (0.0, 5.0),           # AOD range
            'aerosol_forcing_wm2': (-3.0, 1.0),            # Aerosol direct forcing
            'ari_forcing_wm2': (-2.0, 0.5),                # Aerosol-radiation interaction
            'aci_forcing_wm2': (-2.0, 0.0),                # Aerosol-cloud interaction
            
            # Surface properties
            'surface_temperature_k': (200.0, 350.0),        # Surface temperature range
            'emissivity': (0.8, 1.0),                      # Surface emissivity
            'surface_albedo': (0.05, 0.95),                # Surface albedo range
            
            # Atmospheric profiles
            'solar_zenith_angle_deg': (0.0, 90.0),         # Solar geometry
            'pressure_mb': (0.1, 1100.0),                  # Atmospheric pressure
            'water_vapor_gkg': (0.001, 50.0),              # Water vapor mixing ratio
            'ozone_dobson': (200.0, 500.0),                # Ozone column
            
            # Energy balance
            'incoming_solar_wm2': (1300.0, 1400.0),        # Solar constant variation
            'outgoing_longwave_wm2': (200.0, 300.0),       # OLR range
            'planetary_albedo': (0.25, 0.35),              # Earth's planetary albedo
        }
        
        # Physical constants for validation
        self.physical_constants = {
            'solar_constant_wm2': 1361.0,                  # Solar constant
            'stefan_boltzmann': 5.67e-8,                   # Stefan-Boltzmann constant
            'earth_radius_m': 6.371e6,                     # Earth radius
            'solar_zenith_cosine_min': 0.0,                # cos(90°)
            'solar_zenith_cosine_max': 1.0,                # cos(0°)
        }
        
        # Expected datasets for radiative validation
        self.radiative_datasets = {
            'satellite_observations': ['CERES', 'MODIS', 'ERBE', 'ISCCP'],
            'surface_measurements': ['BSRN', 'SURFRAD', 'ARM'],
            'model_output': ['GLENS', 'CMIP6', 'radiative_kernels'],
            'reanalysis': ['ERA5', 'MERRA-2', 'JRA-55']
        }
        
        # Radiative phenomena detection
        self.phenomena_keywords = {
            'solar_radiation': ['solar', 'shortwave', 'visible', 'uv', 'near-infrared'],
            'thermal_radiation': ['longwave', 'thermal', 'infrared', 'blackbody'],
            'clouds': ['cloud', 'cre', 'lwp', 'iwp', 'optical depth'],
            'aerosols': ['aerosol', 'aod', 'scattering', 'absorption'],
            'surface': ['surface', 'albedo', 'emissivity', 'skin temperature'],
            'atmosphere': ['atmospheric', 'absorption', 'transmission', 'water vapor']
        }
        
        self.validation_history = []
        
        logger.info("Radiative Forcing Validator initialized with flexible validation criteria")
    
    def validate_radiative_experiment(self, experiment: Dict) -> Dict[str, Any]:
        """
        Comprehensive validation for radiative forcing experiments.
        
        Args:
            experiment: Radiative experiment description with parameters
            
        Returns:
            Dict containing detailed radiative validation results
        """
        validation_result = {
            'experiment_type': 'radiative_forcing',
            'validation_timestamp': datetime.now().isoformat(),
            'radiative_validation_passed': False,
            'phenomena_analysis': {},
            'parameter_validation': {},
            'energy_balance_validation': {},
            'optical_properties_validation': {},
            'spectral_validation': {},
            'violations': [],
            'recommendations': []
        }
        
        try:
            # Detect radiative phenomena
            phenomena_analysis = self._analyze_radiative_phenomena(experiment)
            validation_result['phenomena_analysis'] = phenomena_analysis
            
            # Validate radiative parameters
            parameter_validation = self._validate_radiative_parameters(experiment.get('parameters', {}))
            validation_result['parameter_validation'] = parameter_validation
            
            if not parameter_validation['parameters_valid']:
                validation_result['violations'].extend(parameter_validation['violations'])
            
            # Energy balance validation
            energy_balance = self._validate_energy_balance(experiment.get('parameters', {}))
            validation_result['energy_balance_validation'] = energy_balance
            
            if not energy_balance['energy_balanced']:
                validation_result['violations'].extend(energy_balance['violations'])
            
            # Optical properties validation
            optical_validation = self._validate_optical_properties(experiment.get('parameters', {}))
            validation_result['optical_properties_validation'] = optical_validation
            
            if not optical_validation['optically_consistent']:
                validation_result['violations'].extend(optical_validation['violations'])
            
            # Spectral validation
            spectral_validation = self._validate_spectral_properties(experiment.get('parameters', {}))
            validation_result['spectral_validation'] = spectral_validation
            
            if not spectral_validation['spectrally_valid']:
                validation_result['violations'].extend(spectral_validation['violations'])
            
            # Overall validation status
            validation_result['radiative_validation_passed'] = len(validation_result['violations']) == 0
            
            # Generate recommendations
            validation_result['recommendations'] = self._generate_radiative_recommendations(validation_result)
            
            self.validation_history.append(validation_result)
            
            logger.info(f"Radiative forcing validation: "
                       f"{'PASS' if validation_result['radiative_validation_passed'] else 'FAIL'}")
            
            return validation_result
            
        except Exception as e:
            logger.error(f"Radiative forcing validation failed: {e}")
            validation_result['violations'].append(f'RADIATIVE_VALIDATION_ERROR: {e}')
            return validation_result
    
    def _analyze_radiative_phenomena(self, experiment: Dict) -> Dict[str, Any]:
        """Analyze and identify radiative phenomena in experiment."""
        phenomena_result = {
            'detected_phenomena': [],
            'radiation_type': 'unknown',
            'spectral_region': 'broadband',
            'measurement_type': 'unknown'
        }
        
        experiment_text = str(experiment).lower()
        
        # Detect phenomena
        for phenomenon, keywords in self.phenomena_keywords.items():
            if any(keyword in experiment_text for keyword in keywords):
                phenomena_result['detected_phenomena'].append(phenomenon)
        
        # Determine radiation type
        if any(kw in experiment_text for kw in ['shortwave', 'solar', 'visible']):
            phenomena_result['radiation_type'] = 'shortwave'
        elif any(kw in experiment_text for kw in ['longwave', 'thermal', 'infrared']):
            phenomena_result['radiation_type'] = 'longwave'
        elif any(kw in experiment_text for kw in ['broadband', 'total', 'net']):
            phenomena_result['radiation_type'] = 'broadband'
        
        # Determine spectral region
        if any(kw in experiment_text for kw in ['spectral', 'wavelength', 'frequency']):
            phenomena_result['spectral_region'] = 'spectral'
        elif any(kw in experiment_text for kw in ['band', 'channel']):
            phenomena_result['spectral_region'] = 'multi-band'
        
        # Determine measurement type
        if any(kw in experiment_text for kw in ['satellite', 'remote sensing', 'toa']):
            phenomena_result['measurement_type'] = 'satellite'
        elif any(kw in experiment_text for kw in ['surface', 'ground', 'station']):
            phenomena_result['measurement_type'] = 'surface'
        elif any(kw in experiment_text for kw in ['model', 'simulation', 'calculation']):
            phenomena_result['measurement_type'] = 'model'
        
        return phenomena_result
    
    def _validate_radiative_parameters(self, parameters: Dict) -> Dict[str, Any]:
        """Validate radiative-specific parameters against physical ranges."""
        parameter_result = {
            'parameters_valid': True,
            'parameter_checks': [],
            'violations': []
        }
        
        for param_name, param_value in parameters.items():
            if isinstance(param_value, (int, float)):
                param_check = self._check_radiative_range(param_name, param_value)
                parameter_result['parameter_checks'].append(param_check)
                
                if not param_check['valid']:
                    parameter_result['violations'].append(
                        f'RADIATIVE_PARAMETER_OUT_OF_RANGE: {param_name}={param_value}'
                    )
                    parameter_result['parameters_valid'] = False
        
        return parameter_result
    
    def _check_radiative_range(self, param_name: str, param_value: float) -> Dict[str, Any]:
        """Check if radiative parameter is within physical range."""
        param_check = {
            'parameter': param_name,
            'value': param_value,
            'valid': True,
            'applicable_range': None,
            'range_type': 'unknown'
        }
        
        # Find applicable range with flexible matching
        param_lower = param_name.lower()
        for range_key, (min_val, max_val) in self.radiative_ranges.items():
            range_parts = range_key.split('_')
            
            # Check if parameter name contains range key components
            if any(part in param_lower for part in range_parts):
                param_check['applicable_range'] = (min_val, max_val)
                param_check['range_type'] = range_key
                param_check['valid'] = min_val <= param_value <= max_val
                break
        
        return param_check
    
    def _validate_energy_balance(self, parameters: Dict) -> Dict[str, Any]:
        """Validate energy balance and conservation principles."""
        balance_result = {
            'energy_balanced': True,
            'balance_checks': [],
            'violations': []
        }
        
        # Global energy balance check
        if ('incoming_solar_wm2' in parameters and 
            'outgoing_longwave_wm2' in parameters and 
            'planetary_albedo' in parameters):
            
            solar_in = parameters['incoming_solar_wm2']
            olr_out = parameters['outgoing_longwave_wm2']
            albedo = parameters['planetary_albedo']
            
            # Calculate absorbed solar radiation
            absorbed_solar = solar_in * (1 - albedo) / 4  # Divided by 4 for geometry
            
            balance_check = {
                'check_type': 'global_energy_balance',
                'solar_input_wm2': solar_in,
                'planetary_albedo': albedo,
                'absorbed_solar_wm2': absorbed_solar,
                'olr_output_wm2': olr_out,
                'imbalance_wm2': absorbed_solar - olr_out,
                'balanced': abs(absorbed_solar - olr_out) < 10.0  # 10 W/m² tolerance
            }
            
            balance_result['balance_checks'].append(balance_check)
            
            if not balance_check['balanced']:
                balance_result['violations'].append(
                    f'ENERGY_IMBALANCE: {balance_check["imbalance_wm2"]:.1f} W/m² imbalance exceeds tolerance'
                )
                balance_result['energy_balanced'] = False
        
        # Surface energy balance check
        if ('net_radiation_wm2' in parameters and 
            'surface_temperature_k' in parameters and 
            'emissivity' in parameters):
            
            net_rad = parameters['net_radiation_wm2']
            surf_temp = parameters['surface_temperature_k']
            emissivity = parameters['emissivity']
            
            # Calculate emitted longwave radiation
            emitted_lw = emissivity * self.physical_constants['stefan_boltzmann'] * surf_temp**4
            
            balance_check = {
                'check_type': 'surface_energy_balance',
                'net_radiation_wm2': net_rad,
                'surface_temperature_k': surf_temp,
                'emissivity': emissivity,
                'emitted_longwave_wm2': emitted_lw,
                'residual_wm2': net_rad - emitted_lw,
                'reasonable_residual': abs(net_rad - emitted_lw) < 100.0  # Allow for sensible/latent heat
            }
            
            balance_result['balance_checks'].append(balance_check)
            
            if not balance_check['reasonable_residual']:
                balance_result['violations'].append(
                    f'SURFACE_ENERGY_IMBALANCE: {balance_check["residual_wm2"]:.1f} W/m² residual too large'
                )
                balance_result['energy_balanced'] = False
        
        return balance_result
    
    def _validate_optical_properties(self, parameters: Dict) -> Dict[str, Any]:
        """Validate optical properties for physical consistency."""
        optical_result = {
            'optically_consistent': True,
            'optical_checks': [],
            'violations': []
        }
        
        # Albedo conservation check
        optical_properties = ['reflectance', 'transmittance', 'absorptance']
        present_properties = {prop: parameters.get(prop) for prop in optical_properties 
                             if parameters.get(prop) is not None}
        
        if len(present_properties) >= 2:
            total_fraction = sum(present_properties.values())
            
            optical_check = {
                'check_type': 'optical_property_conservation',
                'properties': present_properties,
                'total_fraction': total_fraction,
                'conserved': 0.95 <= total_fraction <= 1.05  # Allow 5% tolerance
            }
            
            optical_result['optical_checks'].append(optical_check)
            
            if not optical_check['conserved']:
                optical_result['violations'].append(
                    f'OPTICAL_PROPERTY_NON_CONSERVATION: Total fraction {total_fraction:.3f} ≠ 1.0'
                )
                optical_result['optically_consistent'] = False
        
        # Single scattering albedo check
        if 'single_scattering_albedo' in parameters and 'optical_depth' in parameters:
            ssa = parameters['single_scattering_albedo']
            tau = parameters['optical_depth']
            
            # Check for physical realism
            if ssa > 1.0 or ssa < 0.0:
                optical_result['violations'].append(
                    f'SINGLE_SCATTERING_ALBEDO_INVALID: SSA {ssa} outside [0,1]'
                )
                optical_result['optically_consistent'] = False
            
            if tau < 0.0:
                optical_result['violations'].append(
                    f'OPTICAL_DEPTH_NEGATIVE: Optical depth {tau} must be positive'
                )
                optical_result['optically_consistent'] = False
        
        return optical_result
    
    def _validate_spectral_properties(self, parameters: Dict) -> Dict[str, Any]:
        """Validate spectral properties and wavelength dependencies."""
        spectral_result = {
            'spectrally_valid': True,
            'spectral_checks': [],
            'violations': []
        }
        
        # Wavelength range check
        if 'wavelength_um' in parameters:
            wavelength = parameters['wavelength_um']
            
            spectral_check = {
                'check_type': 'wavelength_range',
                'wavelength_um': wavelength,
                'spectral_region': self._classify_spectral_region(wavelength)
            }
            
            if wavelength <= 0:
                spectral_result['violations'].append(
                    f'WAVELENGTH_NON_POSITIVE: Wavelength {wavelength} μm must be positive'
                )
                spectral_result['spectrally_valid'] = False
            
            spectral_result['spectral_checks'].append(spectral_check)
        
        # Frequency-wavelength consistency
        if 'frequency_hz' in parameters and 'wavelength_um' in parameters:
            freq = parameters['frequency_hz']
            wavelength = parameters['wavelength_um']
            
            # Calculate expected frequency (c = λν)
            c_light = 2.998e8  # m/s
            expected_freq = c_light / (wavelength * 1e-6)  # Convert μm to m
            
            spectral_check = {
                'check_type': 'frequency_wavelength_consistency',
                'frequency_hz': freq,
                'wavelength_um': wavelength,
                'expected_frequency_hz': expected_freq,
                'relative_error': abs(freq - expected_freq) / expected_freq,
                'consistent': abs(freq - expected_freq) / expected_freq < 0.01  # 1% tolerance
            }
            
            spectral_result['spectral_checks'].append(spectral_check)
            
            if not spectral_check['consistent']:
                spectral_result['violations'].append(
                    f'FREQUENCY_WAVELENGTH_INCONSISTENT: {spectral_check["relative_error"]:.1%} error'
                )
                spectral_result['spectrally_valid'] = False
        
        return spectral_result
    
    def _classify_spectral_region(self, wavelength_um: float) -> str:
        """Classify spectral region based on wavelength."""
        if wavelength_um < 0.4:
            return 'ultraviolet'
        elif wavelength_um < 0.7:
            return 'visible'
        elif wavelength_um < 4.0:
            return 'near_infrared'
        elif wavelength_um < 15.0:
            return 'thermal_infrared'
        else:
            return 'far_infrared'
    
    def _generate_radiative_recommendations(self, validation_result: Dict) -> List[str]:
        """Generate radiative-specific recommendations."""
        recommendations = []
        violations = validation_result['violations']
        
        if validation_result['radiative_validation_passed']:
            recommendations.append("✅ Radiative forcing experiment meets validation criteria")
        else:
            recommendations.append("❌ Radiative forcing validation failed - address issues below")
        
        # Phenomena-specific recommendations
        phenomena = validation_result['phenomena_analysis']['detected_phenomena']
        radiation_type = validation_result['phenomena_analysis']['radiation_type']
        
        if phenomena:
            recommendations.append(f"🌞 Detected radiative phenomena: {', '.join(phenomena)}")
            
            if 'solar_radiation' in phenomena:
                recommendations.append("☀️ Solar radiation studies: Consider diurnal and seasonal cycles")
            if 'thermal_radiation' in phenomena:
                recommendations.append("🌡️ Thermal radiation studies: Account for temperature gradients")
            if 'clouds' in phenomena:
                recommendations.append("☁️ Cloud studies: Include cloud fraction and vertical structure")
            if 'aerosols' in phenomena:
                recommendations.append("🌫️ Aerosol studies: Consider size distribution and composition")
        
        # Parameter recommendations
        if any('RADIATIVE_PARAMETER_OUT_OF_RANGE' in v for v in violations):
            recommendations.append("📊 Radiative parameters outside physical ranges")
            recommendations.append("• Check against observational constraints")
            recommendations.append("• Consider measurement uncertainties")
        
        # Energy balance recommendations
        if any('ENERGY_IMBALANCE' in v for v in violations):
            recommendations.append("⚖️ Energy balance violation detected")
            recommendations.append("• Verify global energy budget calculations")
            recommendations.append("• Check for missing energy terms")
        
        if any('SURFACE_ENERGY_IMBALANCE' in v for v in violations):
            recommendations.append("🌍 Surface energy balance issues")
            recommendations.append("• Include sensible and latent heat fluxes")
            recommendations.append("• Check surface temperature consistency")
        
        # Optical property recommendations
        if any('OPTICAL_PROPERTY_NON_CONSERVATION' in v for v in violations):
            recommendations.append("🔍 Optical property conservation violated")
            recommendations.append("• Ensure reflectance + transmittance + absorptance = 1")
            recommendations.append("• Check for measurement/calculation errors")
        
        # Spectral recommendations
        if any('FREQUENCY_WAVELENGTH_INCONSISTENT' in v for v in violations):
            recommendations.append("🌈 Spectral property inconsistency")
            recommendations.append("• Verify wavelength-frequency relationship (c = λν)")
            recommendations.append("• Check units and conversions")
        
        # Dataset recommendations
        recommendations.append("📚 Recommended datasets for radiative validation:")
        if radiation_type == 'shortwave':
            recommendations.append("• CERES for shortwave radiation budget")
            recommendations.append("• MODIS for cloud optical properties")
        elif radiation_type == 'longwave':
            recommendations.append("• AIRS/IASI for longwave spectral measurements")
            recommendations.append("• Surface radiation networks (BSRN, SURFRAD)")
        else:
            recommendations.append("• CERES for broadband radiation budget")
            recommendations.append("• ERA5 reanalysis for comprehensive fields")
        
        return recommendations
    
    def get_radiative_validation_summary(self) -> Dict[str, Any]:
        """Get summary of radiative forcing validation history."""
        if not self.validation_history:
            return {'total_validations': 0, 'summary': 'No radiative forcing validations performed'}
        
        total = len(self.validation_history)
        passed = sum(1 for v in self.validation_history if v['radiative_validation_passed'])
        
        # Analyze radiation types
        radiation_types = []
        for validation in self.validation_history:
            rad_type = validation.get('phenomena_analysis', {}).get('radiation_type', 'unknown')
            radiation_types.append(rad_type)
        
        from collections import Counter
        type_counts = Counter(radiation_types)
        
        return {
            'total_radiative_validations': total,
            'success_rate': passed / total,
            'radiation_type_distribution': dict(type_counts),
            'energy_balance_failure_rate': sum(1 for v in self.validation_history 
                                             if not v.get('energy_balance_validation', {}).get('energy_balanced', True)) / total,
            'optical_consistency_failure_rate': sum(1 for v in self.validation_history 
                                                   if not v.get('optical_properties_validation', {}).get('optically_consistent', True)) / total
        }