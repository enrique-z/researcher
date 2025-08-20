"""
Atmospheric Transport Domain Validator

Flexible validation for atmospheric transport experiments including:
- Wind patterns and circulation studies
- Tracer transport and mixing
- Diffusion and dispersion analysis
- Residence time calculations
- Mass transport and conservation
- Stratospheric-tropospheric exchange

This module adapts the Sakana Principle to atmospheric transport research
with domain-appropriate validation criteria.
"""

import numpy as np
from typing import Dict, Union, Optional, Tuple, List, Any
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AtmosphericTransportValidator:
    """
    Flexible validator for atmospheric transport experiments.
    
    Adapts universal Sakana Principle requirements to transport-specific
    validation criteria while maintaining fluid dynamical realism.
    """
    
    def __init__(self):
        """Initialize atmospheric transport validator with flexible ranges."""
        
        # Atmospheric transport parameter ranges
        self.transport_ranges = {
            # Wind and circulation
            'wind_speed_ms': (0.0, 150.0),                 # Wind speed range (hurricane max ~70 m/s)
            'zonal_wind_ms': (-100.0, 100.0),              # U-component wind
            'meridional_wind_ms': (-50.0, 50.0),           # V-component wind
            'vertical_velocity_pas': (-10.0, 10.0),        # Omega in Pa/s
            'vertical_velocity_ms': (-0.1, 0.1),           # W-component in m/s
            
            # Atmospheric dynamics
            'pressure_pa': (1.0, 110000.0),                # Pressure range (surface to stratosphere)
            'pressure_mb': (0.01, 1100.0),                 # Pressure in mb/hPa
            'altitude_km': (0.0, 100.0),                   # Altitude range
            'potential_temperature_k': (250.0, 2000.0),    # Potential temperature
            'geopotential_height_m': (-500.0, 50000.0),    # Geopotential height
            
            # Transport coefficients
            'diffusion_coefficient_m2s': (1e-6, 1e6),      # Turbulent diffusion
            'eddy_diffusivity_m2s': (1e-3, 1e6),           # Eddy diffusivity
            'mixing_coefficient_m2s': (1e-5, 1e5),         # Mixing coefficient
            'exchange_coefficient_m2s': (1e-4, 1e4),       # Exchange coefficient
            
            # Tracer properties
            'mixing_ratio_ppv': (1e-15, 1e-3),             # Mixing ratio (vol/vol)
            'mixing_ratio_ppm': (1e-9, 1e3),               # Mixing ratio (ppm)
            'concentration_molm3': (1e-12, 1e-3),          # Concentration
            'mass_concentration_kgm3': (1e-15, 1e-6),      # Mass concentration
            
            # Timescales
            'residence_time_days': (0.1, 10000.0),         # Atmospheric residence time
            'transport_time_days': (0.1, 1000.0),          # Transport timescale
            'mixing_time_days': (0.1, 365.0),              # Mixing timescale
            'lifetime_days': (0.1, 10000.0),               # Chemical/physical lifetime
            
            # Spatial scales
            'length_scale_km': (0.1, 20000.0),             # Horizontal length scale
            'vertical_scale_km': (0.001, 100.0),           # Vertical scale
            'correlation_length_km': (1.0, 5000.0),        # Correlation length
            
            # Fluxes and gradients
            'mass_flux_kgm2s': (1e-12, 1e-3),              # Mass flux
            'tracer_flux_molm2s': (1e-15, 1e-6),           # Tracer flux
            'gradient_concentration': (1e-15, 1e-6),        # Concentration gradient
            'gradient_temperature_km': (-20.0, 20.0),       # Temperature gradient K/km
            
            # Stability parameters
            'richardson_number': (-10.0, 10.0),             # Bulk Richardson number
            'brunt_vaisala_frequency_s': (0.0, 0.1),       # Buoyancy frequency
            'rossby_number': (0.001, 100.0),               # Rossby number
            'peclet_number': (1.0, 1e10),                  # Peclet number
        }
        
        # Physical constants for transport validation
        self.physical_constants = {
            'earth_rotation_rate_s': 7.29e-5,              # Earth's rotation rate
            'earth_radius_m': 6.371e6,                     # Earth radius
            'gravity_ms2': 9.81,                           # Gravitational acceleration
            'gas_constant_air': 287.0,                     # Specific gas constant for air
            'cp_air': 1004.0,                              # Specific heat at constant pressure
            'molecular_diffusivity_air_m2s': 2e-5,         # Molecular diffusivity in air
        }
        
        # Expected datasets for transport validation
        self.transport_datasets = {
            'meteorological_data': ['ERA5', 'NCEP', 'JRA-55', 'MERRA-2'],
            'tracer_observations': ['AGAGE', 'NOAA_ESRL', 'TCCON', 'satellite'],
            'model_output': ['GLENS', 'WACCM', 'transport_models'],
            'aircraft_data': ['HIPPO', 'ATom', 'CARIBIC', 'commercial_aircraft']
        }
        
        # Transport phenomena detection
        self.phenomena_keywords = {
            'advection': ['advection', 'transport', 'wind', 'circulation', 'flow'],
            'diffusion': ['diffusion', 'mixing', 'turbulence', 'eddy', 'dispersion'],
            'convection': ['convection', 'convective', 'updraft', 'downdraft'],
            'stratosphere': ['stratosphere', 'stratospheric', 'tropopause', 'ozone'],
            'troposphere': ['troposphere', 'tropospheric', 'boundary layer', 'surface'],
            'exchange': ['exchange', 'ste', 'cross-tropopause', 'vertical transport'],
            'tracer': ['tracer', 'passive', 'conservative', 'chemical species'],
            'jet_stream': ['jet', 'jet stream', 'westerlies', 'polar front']
        }
        
        self.validation_history = []
        
        logger.info("Atmospheric Transport Validator initialized with flexible validation criteria")
    
    def validate_transport_experiment(self, experiment: Dict) -> Dict[str, Any]:
        """
        Comprehensive validation for atmospheric transport experiments.
        
        Args:
            experiment: Transport experiment description with parameters
            
        Returns:
            Dict containing detailed transport validation results
        """
        validation_result = {
            'experiment_type': 'atmospheric_transport',
            'validation_timestamp': datetime.now().isoformat(),
            'transport_validation_passed': False,
            'phenomena_analysis': {},
            'parameter_validation': {},
            'fluid_dynamics_validation': {},
            'mass_conservation_validation': {},
            'timescale_validation': {},
            'violations': [],
            'recommendations': []
        }
        
        try:
            # Detect transport phenomena
            phenomena_analysis = self._analyze_transport_phenomena(experiment)
            validation_result['phenomena_analysis'] = phenomena_analysis
            
            # Validate transport parameters
            parameter_validation = self._validate_transport_parameters(experiment.get('parameters', {}))
            validation_result['parameter_validation'] = parameter_validation
            
            if not parameter_validation['parameters_valid']:
                validation_result['violations'].extend(parameter_validation['violations'])
            
            # Fluid dynamics validation
            fluid_dynamics = self._validate_fluid_dynamics(experiment.get('parameters', {}))
            validation_result['fluid_dynamics_validation'] = fluid_dynamics
            
            if not fluid_dynamics['dynamically_consistent']:
                validation_result['violations'].extend(fluid_dynamics['violations'])
            
            # Mass conservation validation
            mass_conservation = self._validate_mass_conservation(experiment.get('parameters', {}))
            validation_result['mass_conservation_validation'] = mass_conservation
            
            if not mass_conservation['mass_conserved']:
                validation_result['violations'].extend(mass_conservation['violations'])
            
            # Timescale validation
            timescale_validation = self._validate_timescales(experiment.get('parameters', {}))
            validation_result['timescale_validation'] = timescale_validation
            
            if not timescale_validation['timescales_consistent']:
                validation_result['violations'].extend(timescale_validation['violations'])
            
            # Overall validation status
            validation_result['transport_validation_passed'] = len(validation_result['violations']) == 0
            
            # Generate recommendations
            validation_result['recommendations'] = self._generate_transport_recommendations(validation_result)
            
            self.validation_history.append(validation_result)
            
            logger.info(f"Atmospheric transport validation: "
                       f"{'PASS' if validation_result['transport_validation_passed'] else 'FAIL'}")
            
            return validation_result
            
        except Exception as e:
            logger.error(f"Atmospheric transport validation failed: {e}")
            validation_result['violations'].append(f'TRANSPORT_VALIDATION_ERROR: {e}')
            return validation_result
    
    def _analyze_transport_phenomena(self, experiment: Dict) -> Dict[str, Any]:
        """Analyze and identify transport phenomena in experiment."""
        phenomena_result = {
            'detected_phenomena': [],
            'transport_type': 'unknown',
            'spatial_domain': 'unknown',
            'temporal_domain': 'unknown',
            'dominant_process': 'unknown'
        }
        
        experiment_text = str(experiment).lower()
        
        # Detect phenomena
        for phenomenon, keywords in self.phenomena_keywords.items():
            if any(keyword in experiment_text for keyword in keywords):
                phenomena_result['detected_phenomena'].append(phenomenon)
        
        # Determine transport type
        if any(kw in experiment_text for kw in ['advection', 'wind', 'circulation']):
            phenomena_result['transport_type'] = 'advective'
        elif any(kw in experiment_text for kw in ['diffusion', 'mixing', 'turbulence']):
            phenomena_result['transport_type'] = 'diffusive'
        elif any(kw in experiment_text for kw in ['convection', 'convective']):
            phenomena_result['transport_type'] = 'convective'
        
        # Determine spatial domain
        if any(kw in experiment_text for kw in ['global', 'hemispheric', 'planetary']):
            phenomena_result['spatial_domain'] = 'global'
        elif any(kw in experiment_text for kw in ['regional', 'continental', 'synoptic']):
            phenomena_result['spatial_domain'] = 'regional'
        elif any(kw in experiment_text for kw in ['local', 'mesoscale', 'urban']):
            phenomena_result['spatial_domain'] = 'local'
        
        # Determine temporal domain
        if any(kw in experiment_text for kw in ['climate', 'long-term', 'multiyear']):
            phenomena_result['temporal_domain'] = 'climate'
        elif any(kw in experiment_text for kw in ['seasonal', 'annual']):
            phenomena_result['temporal_domain'] = 'seasonal'
        elif any(kw in experiment_text for kw in ['synoptic', 'daily', 'weather']):
            phenomena_result['temporal_domain'] = 'synoptic'
        
        # Determine dominant process
        if len(phenomena_result['detected_phenomena']) > 0:
            phenomena_result['dominant_process'] = phenomena_result['detected_phenomena'][0]
        
        return phenomena_result
    
    def _validate_transport_parameters(self, parameters: Dict) -> Dict[str, Any]:
        """Validate transport-specific parameters against physical ranges."""
        parameter_result = {
            'parameters_valid': True,
            'parameter_checks': [],
            'violations': []
        }
        
        for param_name, param_value in parameters.items():
            if isinstance(param_value, (int, float)):
                param_check = self._check_transport_range(param_name, param_value)
                parameter_result['parameter_checks'].append(param_check)
                
                if not param_check['valid']:
                    parameter_result['violations'].append(
                        f'TRANSPORT_PARAMETER_OUT_OF_RANGE: {param_name}={param_value}'
                    )
                    parameter_result['parameters_valid'] = False
        
        return parameter_result
    
    def _check_transport_range(self, param_name: str, param_value: float) -> Dict[str, Any]:
        """Check if transport parameter is within physical range."""
        param_check = {
            'parameter': param_name,
            'value': param_value,
            'valid': True,
            'applicable_range': None,
            'range_type': 'unknown'
        }
        
        # Find applicable range with flexible matching
        param_lower = param_name.lower()
        for range_key, (min_val, max_val) in self.transport_ranges.items():
            range_parts = range_key.split('_')
            
            # Check if parameter name contains range key components
            if any(part in param_lower for part in range_parts):
                param_check['applicable_range'] = (min_val, max_val)
                param_check['range_type'] = range_key
                param_check['valid'] = min_val <= param_value <= max_val
                break
        
        return param_check
    
    def _validate_fluid_dynamics(self, parameters: Dict) -> Dict[str, Any]:
        """Validate fluid dynamics consistency."""
        dynamics_result = {
            'dynamically_consistent': True,
            'dynamics_checks': [],
            'violations': []
        }
        
        # Wind speed consistency check
        wind_components = ['zonal_wind_ms', 'meridional_wind_ms']
        if all(param in parameters for param in wind_components):
            u_wind = parameters['zonal_wind_ms']
            v_wind = parameters['meridional_wind_ms']
            calculated_speed = np.sqrt(u_wind**2 + v_wind**2)
            
            if 'wind_speed_ms' in parameters:
                given_speed = parameters['wind_speed_ms']
                speed_difference = abs(calculated_speed - given_speed)
                
                dynamics_check = {
                    'check_type': 'wind_speed_consistency',
                    'u_component': u_wind,
                    'v_component': v_wind,
                    'calculated_speed': calculated_speed,
                    'given_speed': given_speed,
                    'speed_difference': speed_difference,
                    'consistent': speed_difference < 0.1 * given_speed  # 10% tolerance
                }
                
                dynamics_result['dynamics_checks'].append(dynamics_check)
                
                if not dynamics_check['consistent']:
                    dynamics_result['violations'].append(
                        f'WIND_SPEED_INCONSISTENCY: Given speed {given_speed:.1f} vs calculated {calculated_speed:.1f} m/s'
                    )
                    dynamics_result['dynamically_consistent'] = False
        
        # Geostrophic balance check (if applicable)
        if all(param in parameters for param in ['zonal_wind_ms', 'meridional_wind_ms', 'pressure_gradient_pam']):
            # Simplified geostrophic balance check
            u_wind = parameters['zonal_wind_ms']
            v_wind = parameters['meridional_wind_ms']
            # Note: Full geostrophic balance would need pressure gradients and Coriolis parameter
            
            # Check if winds are reasonable for given pressure gradient
            wind_magnitude = np.sqrt(u_wind**2 + v_wind**2)
            if wind_magnitude > 100.0:  # Extreme wind speeds
                dynamics_result['violations'].append(
                    f'EXTREME_WIND_SPEED: Wind magnitude {wind_magnitude:.1f} m/s exceeds typical atmospheric values'
                )
                dynamics_result['dynamically_consistent'] = False
        
        # Vertical velocity consistency
        if 'vertical_velocity_ms' in parameters and 'vertical_velocity_pas' in parameters:
            w_ms = parameters['vertical_velocity_ms']
            omega_pas = parameters['vertical_velocity_pas']
            
            # Convert omega to w (approximate)
            # w ≈ -ω / (ρg), assuming ρ ≈ 1.2 kg/m³, g = 9.81 m/s²
            rho_g = 1.2 * self.physical_constants['gravity_ms2']
            w_from_omega = -omega_pas / rho_g
            
            dynamics_check = {
                'check_type': 'vertical_velocity_consistency',
                'w_ms': w_ms,
                'omega_pas': omega_pas,
                'w_from_omega': w_from_omega,
                'relative_difference': abs(w_ms - w_from_omega) / max(abs(w_ms), abs(w_from_omega), 1e-6),
                'consistent': abs(w_ms - w_from_omega) / max(abs(w_ms), abs(w_from_omega), 1e-6) < 0.5  # 50% tolerance
            }
            
            dynamics_result['dynamics_checks'].append(dynamics_check)
            
            if not dynamics_check['consistent']:
                dynamics_result['violations'].append(
                    f'VERTICAL_VELOCITY_INCONSISTENCY: w={w_ms:.4f} m/s vs ω-derived={w_from_omega:.4f} m/s'
                )
                dynamics_result['dynamically_consistent'] = False
        
        return dynamics_result
    
    def _validate_mass_conservation(self, parameters: Dict) -> Dict[str, Any]:
        """Validate mass conservation principles."""
        conservation_result = {
            'mass_conserved': True,
            'conservation_checks': [],
            'violations': []
        }
        
        # Continuity equation check (simplified)
        if 'mass_flux_kgm2s' in parameters and 'concentration_molm3' in parameters:
            mass_flux = parameters['mass_flux_kgm2s']
            concentration = parameters['concentration_molm3']
            
            # Check if fluxes are reasonable for given concentrations
            if concentration > 0:
                flux_concentration_ratio = abs(mass_flux) / concentration
                
                conservation_check = {
                    'check_type': 'flux_concentration_consistency',
                    'mass_flux': mass_flux,
                    'concentration': concentration,
                    'flux_concentration_ratio': flux_concentration_ratio,
                    'reasonable': flux_concentration_ratio < 1e10  # Reasonable transport velocity
                }
                
                conservation_result['conservation_checks'].append(conservation_check)
                
                if not conservation_check['reasonable']:
                    conservation_result['violations'].append(
                        f'UNREALISTIC_FLUX_CONCENTRATION_RATIO: {flux_concentration_ratio:.2e} suggests unrealistic transport'
                    )
                    conservation_result['mass_conserved'] = False
        
        # Mixing ratio conservation
        mixing_ratios = ['mixing_ratio_ppv', 'mixing_ratio_ppm']
        for ratio_param in mixing_ratios:
            if ratio_param in parameters:
                mixing_ratio = parameters[ratio_param]
                
                # Check for unphysical mixing ratios
                if mixing_ratio < 0:
                    conservation_result['violations'].append(
                        f'NEGATIVE_MIXING_RATIO: {ratio_param}={mixing_ratio} cannot be negative'
                    )
                    conservation_result['mass_conserved'] = False
                
                if ratio_param == 'mixing_ratio_ppv' and mixing_ratio > 1.0:
                    conservation_result['violations'].append(
                        f'MIXING_RATIO_EXCEEDS_UNITY: {mixing_ratio} > 1.0 (volume fraction cannot exceed 100%)'
                    )
                    conservation_result['mass_conserved'] = False
        
        return conservation_result
    
    def _validate_timescales(self, parameters: Dict) -> Dict[str, Any]:
        """Validate timescale consistency and physical realism."""
        timescale_result = {
            'timescales_consistent': True,
            'timescale_checks': [],
            'violations': []
        }
        
        # Collect timescale parameters
        timescale_params = ['residence_time_days', 'transport_time_days', 
                           'mixing_time_days', 'lifetime_days']
        
        detected_timescales = {}
        for param_name in timescale_params:
            if param_name in parameters:
                timescale_value = parameters[param_name]
                detected_timescales[param_name] = timescale_value
                
                # Check if timescale is positive
                if timescale_value <= 0:
                    timescale_result['violations'].append(
                        f'NON_POSITIVE_TIMESCALE: {param_name}={timescale_value} must be positive'
                    )
                    timescale_result['timescales_consistent'] = False
        
        # Timescale ordering check
        if ('transport_time_days' in detected_timescales and 
            'mixing_time_days' in detected_timescales):
            
            transport_time = detected_timescales['transport_time_days']
            mixing_time = detected_timescales['mixing_time_days']
            
            # Typically, mixing time should be comparable to or shorter than transport time
            timescale_check = {
                'check_type': 'transport_mixing_timescale_ordering',
                'transport_time_days': transport_time,
                'mixing_time_days': mixing_time,
                'ratio': mixing_time / transport_time,
                'reasonable_ordering': mixing_time <= 10 * transport_time  # Allow factor of 10
            }
            
            timescale_result['timescale_checks'].append(timescale_check)
            
            if not timescale_check['reasonable_ordering']:
                timescale_result['violations'].append(
                    f'UNREASONABLE_TIMESCALE_ORDERING: Mixing time {mixing_time:.1f} >> transport time {transport_time:.1f} days'
                )
                timescale_result['timescales_consistent'] = False
        
        # Residence time vs lifetime check
        if ('residence_time_days' in detected_timescales and 
            'lifetime_days' in detected_timescales):
            
            residence_time = detected_timescales['residence_time_days']
            lifetime = detected_timescales['lifetime_days']
            
            # Residence time should typically be shorter than chemical lifetime
            timescale_check = {
                'check_type': 'residence_lifetime_comparison',
                'residence_time_days': residence_time,
                'lifetime_days': lifetime,
                'ratio': residence_time / lifetime,
                'physical_relationship': residence_time <= lifetime  # Residence ≤ lifetime
            }
            
            timescale_result['timescale_checks'].append(timescale_check)
            
            if not timescale_check['physical_relationship'] and lifetime < 1000:  # Only flag for short lifetimes
                timescale_result['violations'].append(
                    f'RESIDENCE_LIFETIME_INCONSISTENCY: Residence time {residence_time:.1f} > lifetime {lifetime:.1f} days'
                )
                timescale_result['timescales_consistent'] = False
        
        return timescale_result
    
    def _generate_transport_recommendations(self, validation_result: Dict) -> List[str]:
        """Generate transport-specific recommendations."""
        recommendations = []
        violations = validation_result['violations']
        
        if validation_result['transport_validation_passed']:
            recommendations.append("✅ Atmospheric transport experiment meets validation criteria")
        else:
            recommendations.append("❌ Atmospheric transport validation failed - address issues below")
        
        # Phenomena-specific recommendations
        phenomena = validation_result['phenomena_analysis']['detected_phenomena']
        transport_type = validation_result['phenomena_analysis']['transport_type']
        
        if phenomena:
            recommendations.append(f"🌪️ Detected transport phenomena: {', '.join(phenomena)}")
            
            if 'advection' in phenomena:
                recommendations.append("💨 Advection studies: Consider wind shear and directional changes")
            if 'diffusion' in phenomena:
                recommendations.append("🌀 Diffusion studies: Include turbulence parameterization")
            if 'convection' in phenomena:
                recommendations.append("⬆️ Convection studies: Account for vertical mixing and entrainment")
            if 'stratosphere' in phenomena:
                recommendations.append("🌌 Stratospheric studies: Consider Brewer-Dobson circulation")
        
        # Parameter recommendations
        if any('TRANSPORT_PARAMETER_OUT_OF_RANGE' in v for v in violations):
            recommendations.append("📊 Transport parameters outside physical ranges")
            recommendations.append("• Check against meteorological observations")
            recommendations.append("• Consider atmospheric stability conditions")
        
        # Fluid dynamics recommendations
        if any('WIND_SPEED_INCONSISTENCY' in v for v in violations):
            recommendations.append("💨 Wind vector inconsistency detected")
            recommendations.append("• Verify wind component calculations")
            recommendations.append("• Check coordinate system conventions")
        
        if any('EXTREME_WIND_SPEED' in v for v in violations):
            recommendations.append("🌪️ Extreme wind speeds detected")
            recommendations.append("• Verify if hurricane/jet stream conditions intended")
            recommendations.append("• Check for data quality issues")
        
        # Mass conservation recommendations
        if any('NEGATIVE_MIXING_RATIO' in v for v in violations):
            recommendations.append("⚠️ Unphysical negative concentrations")
            recommendations.append("• Check calculation methods and units")
            recommendations.append("• Consider numerical precision issues")
        
        if any('UNREALISTIC_FLUX_CONCENTRATION_RATIO' in v for v in violations):
            recommendations.append("🔄 Mass flux inconsistency")
            recommendations.append("• Verify flux calculations and units")
            recommendations.append("• Check transport velocity assumptions")
        
        # Timescale recommendations
        if any('NON_POSITIVE_TIMESCALE' in v for v in violations):
            recommendations.append("⏰ Invalid timescale values")
            recommendations.append("• All timescales must be positive")
            recommendations.append("• Check calculation methods")
        
        if any('TIMESCALE_ORDERING' in v for v in violations):
            recommendations.append("⏱️ Unrealistic timescale relationships")
            recommendations.append("• Review physical processes and their timescales")
            recommendations.append("• Consider multi-scale interactions")
        
        # Dataset recommendations
        recommendations.append("📚 Recommended datasets for transport validation:")
        if transport_type == 'advective':
            recommendations.append("• ERA5/NCEP reanalysis for wind fields")
            recommendations.append("• Radiosonde data for vertical profiles")
        elif transport_type == 'diffusive':
            recommendations.append("• Aircraft data (HIPPO, ATom) for tracer gradients")
            recommendations.append("• Ground-based networks (AGAGE, NOAA) for background concentrations")
        else:
            recommendations.append("• GLENS model output for comprehensive transport fields")
            recommendations.append("• Satellite observations for global tracer distributions")
        
        return recommendations
    
    def get_transport_validation_summary(self) -> Dict[str, Any]:
        """Get summary of atmospheric transport validation history."""
        if not self.validation_history:
            return {'total_validations': 0, 'summary': 'No atmospheric transport validations performed'}
        
        total = len(self.validation_history)
        passed = sum(1 for v in self.validation_history if v['transport_validation_passed'])
        
        # Analyze transport types
        transport_types = []
        for validation in self.validation_history:
            transport_type = validation.get('phenomena_analysis', {}).get('transport_type', 'unknown')
            transport_types.append(transport_type)
        
        from collections import Counter
        type_counts = Counter(transport_types)
        
        return {
            'total_transport_validations': total,
            'success_rate': passed / total,
            'transport_type_distribution': dict(type_counts),
            'fluid_dynamics_failure_rate': sum(1 for v in self.validation_history 
                                             if not v.get('fluid_dynamics_validation', {}).get('dynamically_consistent', True)) / total,
            'mass_conservation_failure_rate': sum(1 for v in self.validation_history 
                                                 if not v.get('mass_conservation_validation', {}).get('mass_conserved', True)) / total,
            'timescale_failure_rate': sum(1 for v in self.validation_history 
                                        if not v.get('timescale_validation', {}).get('timescales_consistent', True)) / total
        }