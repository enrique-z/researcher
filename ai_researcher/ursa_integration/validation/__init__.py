"""
Universal Validation Framework

Enhanced validation system that extends the Sakana Principle to work with any scientific domain.
Built on Pipeline 2 foundation but made domain-agnostic for universal research applications.

Key Components:
- UniversalSakanaValidator: Main universal validation engine
- Domain-specific validators for climate, physics, chemistry, biology
- Real data enforcement across all research domains
- Empirical validation requirements for any scientific claim
"""

from .universal_sakana_validator import UniversalSakanaValidator, create_universal_sakana_validator
from .domain_validators.universal_base_validator import UniversalBaseValidator
from .domain_validators.climate_validator import ClimateValidator

__all__ = [
    'UniversalSakanaValidator',
    'create_universal_sakana_validator', 
    'UniversalBaseValidator',
    'ClimateValidator'
]