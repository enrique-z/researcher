"""
Chemical Composition Domain Validator

Specialized validation for SAI particle chemistry experiments including:
- Sulfuric acid aerosol composition studies
- Chemical reaction kinetics in stratosphere  
- Atmospheric chemistry modeling
- Particle pH and acidity measurements
- Chemical equilibrium analysis
- Thermodynamic stability assessments

This module provides chemistry-specific validation criteria that adapt
the Sakana Principle to chemical composition research.
"""

import numpy as np
import xarray as xr
from typing import Dict, Union, Optional, Tuple, List
import logging
from datetime import datetime
import warnings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ChemicalCompositionValidator:
    """
    Specialized validator for chemical composition experiments.
    
    Implements chemistry-specific validation criteria while maintaining
    universal Sakana Principle requirements for empirical validation.
    """
    
    def __init__(self, temperature_range_k: Tuple[float, float] = (150, 350)):
        """
        Initialize chemical composition validator.
        
        Args:
            temperature_range_k: Valid temperature range in Kelvin for stratospheric conditions
        """
        self.temperature_range_k = temperature_range_k
        
        # Chemical parameter ranges for stratospheric SAI conditions
        self.chemical_ranges = {
            # Concentrations (various units)
            'h2so4_concentration_percent': (10.0, 98.0),      # Sulfuric acid weight %
            'h2so4_molarity': (0.1, 18.0),                    # Molarity of H2SO4
            'so2_ppm': (0.1, 1000.0),                         # SO2 concentration
            'h2o_percent': (2.0, 90.0),                       # Water content
            
            # Physical-chemical properties
            'ph_value': (0.0, 2.0),                           # Highly acidic for H2SO4
            'density_gcm3': (1.0, 2.0),                       # Liquid density
            'viscosity_cp': (0.5, 100.0),                     # Dynamic viscosity
            'surface_tension_nm': (50.0, 100.0),              # Surface tension
            
            # Thermodynamic properties
            'temperature_k': temperature_range_k,              # Stratospheric temperatures
            'pressure_pa': (1000, 10000),                     # Stratospheric pressures  
            'vapor_pressure_pa': (0.01, 1000.0),              # Vapor pressure
            'enthalpy_formation_kjmol': (-1000.0, 0.0),       # Formation enthalpy
            'gibbs_energy_kjmol': (-1000.0, 100.0),           # Gibbs free energy
            
            # Kinetic properties
            'reaction_rate_constant': (1e-20, 1e-5),          # Rate constants
            'activation_energy_kjmol': (0.0, 200.0),          # Activation energies
            'diffusion_coefficient_m2s': (1e-12, 1e-8),       # Molecular diffusion
            
            # Particle properties
            'particle_size_nm': (10.0, 1000.0),               # Particle diameter
            'number_concentration_cm3': (0.1, 1000.0),        # Number density
            'mass_concentration_ugm3': (0.1, 1000.0),         # Mass concentration
        }
        
        # Chemical species validation data
        self.chemical_species = {
            'H2SO4': {
                'molecular_weight': 98.079,
                'density_pure': 1.84,  # g/cm³ at 25°C
                'boiling_point_k': 610.0,
                'melting_point_k': 283.46,
                'valid_concentrations': (10.0, 100.0)  # Weight percent
            },
            'SO2': {
                'molecular_weight': 64.066,
                'boiling_point_k': 263.13,
                'melting_point_k': 200.25,
                'henry_constant': 1.23,  # M/atm at 25°C
                'valid_concentrations': (0.1, 10000.0)  # ppm
            },
            'H2O': {
                'molecular_weight': 18.015,
                'density_pure': 1.0,
                'boiling_point_k': 373.15,
                'melting_point_k': 273.15,
                'valid_concentrations': (0.0, 100.0)  # Weight percent
            },
            'H2SO4*H2O': {
                'molecular_weight': 116.094,
                'description': 'Hydrated sulfuric acid',
                'stability_range_k': (150, 300)
            }
        }
        
        # Required datasets for chemical validation
        self.chemical_datasets = {
            'GLENS': ['BURDEN1', 'BURDEN2', 'BURDEN3'],  # Aerosol burdens
            'ARISE-SAI': ['SO2', 'SO4', 'DMS'],           # Chemical species
            'laboratory_data': ['viscosity', 'density', 'ph'],
            'thermodynamic_databases': ['NIST', 'JANAF', 'HSC']
        }
        
        # Chemical validation history
        self.validation_history = []
        
        logger.info("Chemical Composition Validator initialized for stratospheric SAI conditions")
    
    def validate_chemical_experiment(self, experiment: Dict) -> Dict:
        """
        Comprehensive validation for chemical composition experiments.
        
        Args:
            experiment: Chemical experiment description with parameters
            
        Returns:
            Dict containing detailed chemical validation results
        """
        validation_result = {
            'experiment_type': 'chemical_composition',
            'validation_timestamp': datetime.now().isoformat(),
            'chemical_validation_passed': False,
            'composition_analysis': {},
            'thermodynamic_validation': {},
            'kinetic_validation': {},
            'species_validation': {},
            'physical_property_validation': {},
            'violations': [],
            'recommendations': []
        }
        
        try:
            parameters = experiment.get('parameters', {})
            
            # Chemical composition analysis
            composition_analysis = self._analyze_chemical_composition(parameters)
            validation_result['composition_analysis'] = composition_analysis
            
            if not composition_analysis['composition_valid']:
                validation_result['violations'].extend(composition_analysis['violations'])
            
            # Thermodynamic validation
            thermodynamic_validation = self._validate_thermodynamics(parameters)
            validation_result['thermodynamic_validation'] = thermodynamic_validation
            
            if not thermodynamic_validation['thermodynamically_feasible']:
                validation_result['violations'].extend(thermodynamic_validation['violations'])
            
            # Chemical kinetics validation
            kinetic_validation = self._validate_kinetics(parameters)
            validation_result['kinetic_validation'] = kinetic_validation
            
            if not kinetic_validation['kinetically_feasible']:
                validation_result['violations'].extend(kinetic_validation['violations'])
            
            # Species-specific validation
            species_validation = self._validate_chemical_species(experiment)
            validation_result['species_validation'] = species_validation
            
            if not species_validation['species_valid']:
                validation_result['violations'].extend(species_validation['violations'])
            
            # Physical properties validation
            physical_validation = self._validate_physical_properties(parameters)
            validation_result['physical_property_validation'] = physical_validation
            
            if not physical_validation['properties_valid']:
                validation_result['violations'].extend(physical_validation['violations'])
            
            # Overall chemical validation status
            validation_result['chemical_validation_passed'] = len(validation_result['violations']) == 0
            
            # Generate chemistry-specific recommendations
            validation_result['recommendations'] = self._generate_chemical_recommendations(validation_result)
            
            # Record validation
            self.validation_history.append(validation_result)
            
            logger.info(f"Chemical composition validation: "
                       f"{'PASS' if validation_result['chemical_validation_passed'] else 'FAIL'}")
            
            return validation_result
            
        except Exception as e:
            logger.error(f"Chemical composition validation failed: {e}")
            validation_result['violations'].append(f'CHEMICAL_VALIDATION_ERROR: {e}')
            return validation_result
    
    def _analyze_chemical_composition(self, parameters: Dict) -> Dict:
        """Analyze chemical composition for physical realism."""
        composition_result = {
            'composition_valid': False,
            'mass_balance': {},
            'concentration_checks': [],
            'violations': []
        }
        
        # Extract chemical concentrations
        concentrations = {}
        for param_name, param_value in parameters.items():
            if 'concentration' in param_name.lower() or 'percent' in param_name.lower():
                concentrations[param_name] = param_value
        
        # Mass balance check
        if 'h2so4_concentration_percent' in parameters and 'h2o_percent' in parameters:
            h2so4_percent = parameters['h2so4_concentration_percent']
            h2o_percent = parameters['h2o_percent']
            total_percent = h2so4_percent + h2o_percent
            
            composition_result['mass_balance'] = {
                'h2so4_percent': h2so4_percent,
                'h2o_percent': h2o_percent,
                'total_percent': total_percent,
                'mass_balance_valid': 90.0 <= total_percent <= 110.0  # Allow some tolerance
            }
            
            if not composition_result['mass_balance']['mass_balance_valid']:
                composition_result['violations'].append(
                    f'MASS_BALANCE_VIOLATION: Total composition {total_percent:.1f}% not ~100%'
                )
        
        # Individual concentration validation
        for param_name, param_value in concentrations.items():
            if isinstance(param_value, (int, float)):
                concentration_check = self._validate_concentration_range(param_name, param_value)
                composition_result['concentration_checks'].append(concentration_check)
                
                if not concentration_check['valid']:
                    composition_result['violations'].append(
                        f'CONCENTRATION_OUT_OF_RANGE: {param_name}={param_value}'
                    )
        
        composition_result['composition_valid'] = len(composition_result['violations']) == 0
        
        return composition_result
    
    def _validate_thermodynamics(self, parameters: Dict) -> Dict:
        """Validate thermodynamic feasibility of chemical system."""
        thermo_result = {
            'thermodynamically_feasible': False,
            'temperature_validation': {},
            'pressure_validation': {},
            'phase_stability': {},
            'violations': []
        }
        
        # Temperature validation
        temp_k = parameters.get('temperature_k', parameters.get('temperature', None))
        if temp_k is not None:
            temp_valid = self.temperature_range_k[0] <= temp_k <= self.temperature_range_k[1]
            thermo_result['temperature_validation'] = {
                'temperature_k': temp_k,
                'valid_range': self.temperature_range_k,
                'valid': temp_valid
            }
            
            if not temp_valid:
                thermo_result['violations'].append(
                    f'TEMPERATURE_OUT_OF_RANGE: {temp_k} K outside stratospheric range {self.temperature_range_k}'
                )
        
        # Pressure validation
        pressure_pa = parameters.get('pressure_pa', parameters.get('pressure', None))
        if pressure_pa is not None:
            pressure_range = self.chemical_ranges['pressure_pa']
            pressure_valid = pressure_range[0] <= pressure_pa <= pressure_range[1]
            thermo_result['pressure_validation'] = {
                'pressure_pa': pressure_pa,
                'valid_range': pressure_range,
                'valid': pressure_valid
            }
            
            if not pressure_valid:
                thermo_result['violations'].append(
                    f'PRESSURE_OUT_OF_RANGE: {pressure_pa} Pa outside stratospheric range {pressure_range}'
                )
        
        # Phase stability check
        if temp_k is not None and pressure_pa is not None:
            phase_stability = self._check_phase_stability(temp_k, pressure_pa, parameters)
            thermo_result['phase_stability'] = phase_stability
            
            if not phase_stability['stable']:
                thermo_result['violations'].extend(phase_stability['violations'])
        
        # Gibbs energy check (if provided)
        gibbs_energy = parameters.get('gibbs_energy_kjmol', None)
        if gibbs_energy is not None:
            if gibbs_energy > 0:
                thermo_result['violations'].append(
                    f'THERMODYNAMICALLY_UNFAVORABLE: ΔG = {gibbs_energy} kJ/mol > 0'
                )
        
        thermo_result['thermodynamically_feasible'] = len(thermo_result['violations']) == 0
        
        return thermo_result
    
    def _validate_kinetics(self, parameters: Dict) -> Dict:
        """Validate chemical kinetics parameters."""
        kinetic_result = {
            'kinetically_feasible': False,
            'rate_constant_validation': {},
            'activation_energy_validation': {},
            'violations': []
        }
        
        # Rate constant validation
        rate_constant = parameters.get('reaction_rate_constant', None)
        if rate_constant is not None:
            rate_range = self.chemical_ranges['reaction_rate_constant']
            rate_valid = rate_range[0] <= rate_constant <= rate_range[1]
            kinetic_result['rate_constant_validation'] = {
                'rate_constant': rate_constant,
                'valid_range': rate_range,
                'valid': rate_valid,
                'time_scale_s': 1 / rate_constant if rate_constant > 0 else np.inf
            }
            
            if not rate_valid:
                kinetic_result['violations'].append(
                    f'RATE_CONSTANT_OUT_OF_RANGE: {rate_constant} outside {rate_range}'
                )
        
        # Activation energy validation
        activation_energy = parameters.get('activation_energy_kjmol', None)
        if activation_energy is not None:
            ea_range = self.chemical_ranges['activation_energy_kjmol']
            ea_valid = ea_range[0] <= activation_energy <= ea_range[1]
            kinetic_result['activation_energy_validation'] = {
                'activation_energy_kjmol': activation_energy,
                'valid_range': ea_range,
                'valid': ea_valid
            }
            
            if not ea_valid:
                kinetic_result['violations'].append(
                    f'ACTIVATION_ENERGY_OUT_OF_RANGE: {activation_energy} kJ/mol outside {ea_range}'
                )
            
            # Check for unrealistically high activation energy
            if activation_energy > 150.0:
                kinetic_result['violations'].append(
                    f'ACTIVATION_ENERGY_TOO_HIGH: {activation_energy} kJ/mol (reaction too slow)'
                )
        
        kinetic_result['kinetically_feasible'] = len(kinetic_result['violations']) == 0
        
        return kinetic_result
    
    def _validate_chemical_species(self, experiment: Dict) -> Dict:
        """Validate chemical species mentioned in experiment."""
        species_result = {
            'species_valid': True,
            'detected_species': [],
            'species_checks': [],
            'violations': []
        }
        
        content = str(experiment).lower()
        
        # Detect chemical species in experiment description
        for species_name, species_data in self.chemical_species.items():
            if species_name.lower() in content:
                species_result['detected_species'].append(species_name)
                
                # Validate species-specific parameters
                species_check = self._validate_species_parameters(species_name, experiment.get('parameters', {}))
                species_result['species_checks'].append(species_check)
                
                if not species_check['valid']:
                    species_result['violations'].extend(species_check['violations'])
        
        # Check for required species in SAI experiments
        required_species = ['H2SO4', 'SO2']  # Typical for SAI
        missing_species = [species for species in required_species 
                          if species not in species_result['detected_species']]
        
        if missing_species:
            species_result['violations'].append(
                f'MISSING_REQUIRED_SPECIES: {missing_species} not mentioned for SAI experiment'
            )
        
        species_result['species_valid'] = len(species_result['violations']) == 0
        
        return species_result
    
    def _validate_species_parameters(self, species_name: str, parameters: Dict) -> Dict:
        """Validate parameters specific to a chemical species."""
        species_check = {
            'species': species_name,
            'valid': True,
            'parameter_checks': [],
            'violations': []
        }
        
        if species_name not in self.chemical_species:
            return species_check
        
        species_data = self.chemical_species[species_name]
        
        # Check molecular weight consistency
        if 'molecular_weight' in parameters:
            expected_mw = species_data['molecular_weight']
            actual_mw = parameters['molecular_weight']
            mw_tolerance = 0.1  # g/mol
            
            if abs(actual_mw - expected_mw) > mw_tolerance:
                species_check['violations'].append(
                    f'MOLECULAR_WEIGHT_MISMATCH: {species_name} MW {actual_mw} ≠ {expected_mw} g/mol'
                )
                species_check['valid'] = False
        
        # Check concentration ranges
        if 'valid_concentrations' in species_data:
            conc_range = species_data['valid_concentrations']
            
            # Look for concentration parameters
            conc_params = [p for p in parameters.keys() 
                          if species_name.lower() in p.lower() and 'concentration' in p.lower()]
            
            for param_name in conc_params:
                conc_value = parameters[param_name]
                if not (conc_range[0] <= conc_value <= conc_range[1]):
                    species_check['violations'].append(
                        f'SPECIES_CONCENTRATION_OUT_OF_RANGE: {param_name}={conc_value} outside {conc_range}'
                    )
                    species_check['valid'] = False
        
        species_check['parameter_checks'] = [
            {'parameter': 'molecular_weight', 'expected': species_data.get('molecular_weight', 'N/A')},
            {'parameter': 'concentration_range', 'expected': species_data.get('valid_concentrations', 'N/A')}
        ]
        
        return species_check
    
    def _validate_physical_properties(self, parameters: Dict) -> Dict:
        """Validate physical properties like density, viscosity, pH."""
        properties_result = {
            'properties_valid': True,
            'property_checks': [],
            'violations': []
        }
        
        # pH validation (critical for acidic aerosols)
        ph_value = parameters.get('ph_value', parameters.get('ph', None))
        if ph_value is not None:
            ph_range = self.chemical_ranges['ph_value']
            ph_valid = ph_range[0] <= ph_value <= ph_range[1]
            
            property_check = {
                'property': 'pH',
                'value': ph_value,
                'valid_range': ph_range,
                'valid': ph_valid,
                'acidity_level': 'Highly acidic' if ph_value < 1 else 'Acidic' if ph_value < 2 else 'Moderate'
            }
            
            properties_result['property_checks'].append(property_check)
            
            if not ph_valid:
                properties_result['violations'].append(
                    f'PH_OUT_OF_RANGE: pH {ph_value} outside acidic range {ph_range}'
                )
                properties_result['properties_valid'] = False
        
        # Density validation
        density = parameters.get('density_gcm3', parameters.get('density', None))
        if density is not None:
            density_range = self.chemical_ranges['density_gcm3']
            density_valid = density_range[0] <= density <= density_range[1]
            
            property_check = {
                'property': 'density',
                'value': density,
                'valid_range': density_range,
                'valid': density_valid
            }
            
            properties_result['property_checks'].append(property_check)
            
            if not density_valid:
                properties_result['violations'].append(
                    f'DENSITY_OUT_OF_RANGE: {density} g/cm³ outside {density_range}'
                )
                properties_result['properties_valid'] = False
        
        # Viscosity validation
        viscosity = parameters.get('viscosity_cp', parameters.get('viscosity', None))
        if viscosity is not None:
            viscosity_range = self.chemical_ranges['viscosity_cp']
            viscosity_valid = viscosity_range[0] <= viscosity <= viscosity_range[1]
            
            property_check = {
                'property': 'viscosity',
                'value': viscosity,
                'valid_range': viscosity_range,
                'valid': viscosity_valid
            }
            
            properties_result['property_checks'].append(property_check)
            
            if not viscosity_valid:
                properties_result['violations'].append(
                    f'VISCOSITY_OUT_OF_RANGE: {viscosity} cP outside {viscosity_range}'
                )
                properties_result['properties_valid'] = False
        
        return properties_result
    
    def _validate_concentration_range(self, param_name: str, param_value: float) -> Dict:
        """Validate concentration parameter against appropriate range."""
        concentration_check = {
            'parameter': param_name,
            'value': param_value,
            'valid': True,
            'applicable_range': None
        }
        
        # Find applicable range based on parameter name
        for range_key, (min_val, max_val) in self.chemical_ranges.items():
            if any(key_part in param_name.lower() for key_part in range_key.split('_')):
                concentration_check['applicable_range'] = (min_val, max_val)
                concentration_check['valid'] = min_val <= param_value <= max_val
                break
        
        return concentration_check
    
    def _check_phase_stability(self, temperature_k: float, pressure_pa: float, parameters: Dict) -> Dict:
        """Check phase stability under given conditions."""
        stability_result = {
            'stable': True,
            'phase': 'liquid',
            'violations': []
        }
        
        # For H2SO4-H2O system, check if conditions maintain liquid phase
        h2so4_percent = parameters.get('h2so4_concentration_percent', 75.0)
        
        # Simplified phase stability check
        # (In real implementation, would use detailed phase diagrams)
        if temperature_k < 200:
            stability_result['stable'] = False
            stability_result['phase'] = 'solid'
            stability_result['violations'].append(
                f'PHASE_INSTABILITY: Temperature {temperature_k} K too low for liquid phase'
            )
        
        if temperature_k > 320 and h2so4_percent > 90:
            stability_result['stable'] = False
            stability_result['violations'].append(
                f'PHASE_INSTABILITY: High T ({temperature_k} K) and concentration may cause vaporization'
            )
        
        return stability_result
    
    def _generate_chemical_recommendations(self, validation_result: Dict) -> List[str]:
        """Generate chemistry-specific recommendations."""
        recommendations = []
        violations = validation_result['violations']
        
        if validation_result['chemical_validation_passed']:
            recommendations.append("✅ Chemical composition experiment meets validation criteria")
        else:
            recommendations.append("❌ Chemical composition validation failed - address issues below")
        
        # Composition-specific recommendations
        if any('MASS_BALANCE_VIOLATION' in v for v in violations):
            recommendations.append("⚠️  Mass balance issue detected")
            recommendations.append("• Ensure H2SO4 + H2O percentages sum to ~100%")
            recommendations.append("• Account for trace species if present")
        
        if any('CONCENTRATION_OUT_OF_RANGE' in v for v in violations):
            recommendations.append("⚠️  Concentration parameters outside realistic ranges")
            recommendations.append("• Review literature values for stratospheric SAI conditions")
            recommendations.append("• Consider measurement uncertainties")
        
        # Thermodynamic recommendations
        if any('TEMPERATURE_OUT_OF_RANGE' in v for v in violations):
            recommendations.append("🌡️  Temperature outside stratospheric range (150-350 K)")
            recommendations.append("• Adjust to realistic stratospheric conditions")
        
        if any('THERMODYNAMICALLY_UNFAVORABLE' in v for v in violations):
            recommendations.append("⚛️  Thermodynamically unfavorable conditions")
            recommendations.append("• Check Gibbs free energy calculations")
            recommendations.append("• Consider kinetic vs. thermodynamic control")
        
        # Species-specific recommendations
        if any('MISSING_REQUIRED_SPECIES' in v for v in violations):
            recommendations.append("🧪 Required chemical species missing")
            recommendations.append("• Include H2SO4 and SO2 for SAI experiments")
            recommendations.append("• Specify chemical composition clearly")
        
        # Physical property recommendations
        if any('PH_OUT_OF_RANGE' in v for v in violations):
            recommendations.append("🧪 pH value inconsistent with acidic aerosols")
            recommendations.append("• SAI aerosols are highly acidic (pH 0-2)")
            recommendations.append("• Verify pH measurement conditions")
        
        # Data source recommendations
        recommendations.append("📊 Recommended datasets for chemical validation:")
        recommendations.append("• GLENS: BURDEN1, BURDEN2, BURDEN3 for aerosol composition")
        recommendations.append("• Laboratory studies: NIST, JANAF thermodynamic data")
        recommendations.append("• Atmospheric measurements: Field campaign data")
        
        return recommendations
    
    def get_chemical_validation_summary(self) -> Dict:
        """Get summary of chemical composition validation history."""
        if not self.validation_history:
            return {'total_validations': 0, 'summary': 'No chemical composition validations performed'}
        
        total = len(self.validation_history)
        passed = sum(1 for v in self.validation_history if v['chemical_validation_passed'])
        
        # Calculate average pH of validated experiments
        ph_values = []
        for validation in self.validation_history:
            for prop_check in validation.get('physical_property_validation', {}).get('property_checks', []):
                if prop_check.get('property') == 'pH':
                    ph_values.append(prop_check['value'])
        
        return {
            'total_chemical_validations': total,
            'success_rate': passed / total,
            'average_ph': np.mean(ph_values) if ph_values else None,
            'ph_range': (min(ph_values), max(ph_values)) if ph_values else None,
            'thermodynamic_failure_rate': sum(1 for v in self.validation_history 
                                            if not v.get('thermodynamic_validation', {}).get('thermodynamically_feasible', True)) / total,
            'mass_balance_failure_rate': sum(1 for v in self.validation_history 
                                           if not v.get('composition_analysis', {}).get('composition_valid', True)) / total
        }