"""
Plausibility Checker: Validates theoretical claims against known physics constraints
Part of the Sakana Principle framework for preventing "plausibility trap" scenarios
"""

import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)


class PlausibilityChecker:
    """
    Validates theoretical claims against physical constraints to prevent plausibility traps.
    
    The "plausibility trap" occurs when AI generates sophisticated-sounding claims that
    are physically impossible or violate known scientific constraints.
    """
    
    def __init__(self):
        """Initialize plausibility checker with constraint databases"""
        logger.info("Initializing PlausibilityChecker for constraint validation")
        
        # Physical constraint databases (expandable by domain)
        self.constraint_database = {
            'chemical_composition': {
                'h2so4_concentration_range': (10, 98),  # Percent, stratospheric conditions
                'temperature_range_k': (180, 280),      # Kelvin, stratospheric range
                'pressure_range_hpa': (1, 1000),       # hPa, atmospheric range
                'particle_size_range_nm': (10, 10000)   # Nanometers, aerosol range
            },
            'atmospheric_transport': {
                'wind_speed_range_ms': (0, 150),        # m/s, realistic atmospheric winds
                'altitude_range_km': (0, 50),           # km, atmospheric layers
                'diffusion_coefficient_range': (1e-6, 1e-2),  # m²/s, atmospheric diffusion
                'mixing_ratio_range': (1e-12, 1e-3)     # kg/kg, trace gas mixing ratios
            },
            'climate_response': {
                'temperature_change_range_k': (-10, 10), # K, realistic SAI temperature changes
                'precipitation_change_percent': (-50, 50), # Percent, precipitation changes
                'forcing_range_wm2': (-10, 10),         # W/m², radiative forcing range
                'response_timescale_years': (0.1, 100)   # Years, climate response timescales
            }
        }
        
    def check_theoretical_claim(self, claim: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check if a theoretical claim violates known physical constraints
        
        Args:
            claim: Theoretical claim with parameters and values
            
        Returns:
            Validation result with constraint checks
        """
        validation_result = {
            'plausible': True,
            'constraint_violations': [],
            'warnings': [],
            'domain': claim.get('domain', 'unknown')
        }
        
        # Extract domain and parameters
        domain = claim.get('domain', 'chemical_composition')
        parameters = claim.get('parameters', {})
        
        if domain in self.constraint_database:
            constraints = self.constraint_database[domain]
            
            # Check each parameter against constraints
            for param_name, param_value in parameters.items():
                constraint_key = f"{param_name}_range" if not param_name.endswith('_range') else param_name
                
                if constraint_key in constraints:
                    min_val, max_val = constraints[constraint_key]
                    
                    if isinstance(param_value, (int, float)):
                        if param_value < min_val or param_value > max_val:
                            validation_result['plausible'] = False
                            validation_result['constraint_violations'].append({
                                'parameter': param_name,
                                'value': param_value,
                                'valid_range': (min_val, max_val),
                                'severity': 'critical'
                            })
                        elif param_value < min_val * 1.2 or param_value > max_val * 0.8:
                            validation_result['warnings'].append({
                                'parameter': param_name,
                                'value': param_value,
                                'message': f'Parameter near constraint boundary: {param_value} vs range {(min_val, max_val)}'
                            })
        
        # Check for common plausibility trap patterns
        self._check_plausibility_patterns(claim, validation_result)
        
        return validation_result
    
    def _check_plausibility_patterns(self, claim: Dict[str, Any], validation_result: Dict[str, Any]):
        """Check for common plausibility trap patterns in claims"""
        
        claim_text = claim.get('hypothesis', '') + ' ' + claim.get('methodology', '')
        claim_lower = claim_text.lower()
        
        # Pattern 1: Unrealistic efficiency claims
        efficiency_keywords = ['100% efficient', 'perfect efficiency', 'zero loss', 'infinite']
        for keyword in efficiency_keywords:
            if keyword in claim_lower:
                validation_result['warnings'].append({
                    'pattern': 'unrealistic_efficiency',
                    'message': f'Detected potentially unrealistic efficiency claim: "{keyword}"'
                })
        
        # Pattern 2: Violating conservation laws
        conservation_violations = ['energy creation', 'mass creation', 'perpetual motion']
        for violation in conservation_violations:
            if violation in claim_lower:
                validation_result['plausible'] = False
                validation_result['constraint_violations'].append({
                    'pattern': 'conservation_law_violation',
                    'message': f'Possible conservation law violation: "{violation}"',
                    'severity': 'critical'
                })
        
        # Pattern 3: Scale mismatches
        if 'global' in claim_lower and 'instantaneous' in claim_lower:
            validation_result['warnings'].append({
                'pattern': 'scale_mismatch',
                'message': 'Global and instantaneous effects may be physically inconsistent'
            })
    
    def validate_domain_consistency(self, claim: Dict[str, Any]) -> bool:
        """
        Validate that claim parameters are consistent within their domain
        
        Args:
            claim: Theoretical claim to validate
            
        Returns:
            True if parameters are consistent, False otherwise
        """
        domain = claim.get('domain', 'unknown')
        parameters = claim.get('parameters', {})
        
        # Domain-specific consistency checks
        if domain == 'chemical_composition':
            return self._validate_chemical_consistency(parameters)
        elif domain == 'atmospheric_transport':
            return self._validate_transport_consistency(parameters)
        elif domain == 'climate_response':
            return self._validate_climate_consistency(parameters)
        
        return True  # Default to true for unknown domains
    
    def _validate_chemical_consistency(self, parameters: Dict[str, Any]) -> bool:
        """Validate chemical composition parameter consistency"""
        
        # Check H2SO4 concentration vs temperature consistency
        h2so4_conc = parameters.get('h2so4_concentration_percent')
        temperature = parameters.get('temperature_k')
        
        if h2so4_conc and temperature:
            # High concentrations should correspond to lower temperatures (stratospheric conditions)
            if h2so4_conc > 80 and temperature > 240:
                logger.warning(f"High H2SO4 concentration ({h2so4_conc}%) with high temperature ({temperature}K) may be inconsistent")
                return False
        
        return True
    
    def _validate_transport_consistency(self, parameters: Dict[str, Any]) -> bool:
        """Validate atmospheric transport parameter consistency"""
        
        # Check wind speed vs altitude consistency
        wind_speed = parameters.get('wind_speed_ms')
        altitude = parameters.get('altitude_km')
        
        if wind_speed and altitude:
            # Very high wind speeds at low altitudes are uncommon
            if wind_speed > 50 and altitude < 5:
                logger.warning(f"High wind speed ({wind_speed} m/s) at low altitude ({altitude} km) may be unusual")
                return False
        
        return True
    
    def _validate_climate_consistency(self, parameters: Dict[str, Any]) -> bool:
        """Validate climate response parameter consistency"""
        
        # Check temperature change vs forcing consistency
        temp_change = parameters.get('temperature_change_k')
        forcing = parameters.get('forcing_wm2')
        
        if temp_change and forcing:
            # Rough climate sensitivity check (typical: 0.8 K per W/m²)
            expected_temp_change = forcing * 0.8
            if abs(temp_change - expected_temp_change) > 2.0:
                logger.warning(f"Temperature change ({temp_change}K) may be inconsistent with forcing ({forcing} W/m²)")
                return False
        
        return True
    
    def get_constraint_summary(self, domain: str) -> Dict[str, Any]:
        """Get summary of constraints for a specific domain"""
        if domain in self.constraint_database:
            return {
                'domain': domain,
                'constraints': self.constraint_database[domain],
                'total_constraints': len(self.constraint_database[domain])
            }
        return {'domain': domain, 'constraints': {}, 'total_constraints': 0}