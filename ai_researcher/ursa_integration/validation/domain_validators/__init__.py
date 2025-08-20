"""
Domain-Specific Validators

Collection of validators specialized for different scientific research domains.
All inherit from UniversalBaseValidator to ensure consistent validation interface.

Available Domains:
- ClimateValidator: Climate research, SAI experiments, atmospheric science
- Future: PhysicsValidator, ChemistryValidator, BiologyValidator
"""

from .universal_base_validator import UniversalBaseValidator
from .climate_validator import ClimateValidator

__all__ = [
    'UniversalBaseValidator',
    'ClimateValidator'
]