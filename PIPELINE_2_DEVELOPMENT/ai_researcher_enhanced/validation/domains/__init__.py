"""
Domain-Specific Validation Modules

This package contains specialized validation modules for different experimental domains:
- signal_detection: For spectroscopy, remote sensing, and signal analysis experiments
- chemical_composition: For SAI particle chemistry and atmospheric chemistry studies
- particle_dynamics: For aerosol transport, settling, and microphysics experiments
- climate_response: For temperature, precipitation, and climate feedback studies

Each module implements domain-specific validation criteria while adhering to
the universal Sakana Principle requirements.
"""

from .signal_detection import SignalDetectionValidator
from .chemical_composition import ChemicalCompositionValidator

__all__ = [
    'SignalDetectionValidator',
    'ChemicalCompositionValidator'
]