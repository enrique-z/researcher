"""
Climate Research Domain Configuration

This module provides specialized configuration for climate research domain.
Focused on climate science calculations, data handling, and validation.

Key Features:
- SAI injection analysis (pulse vs continuous)
- Climate data processing (GLENS, ARISE-SAI)
- Aerosol transport modeling
- Radiative forcing calculations
- Climate validation criteria
"""

import os
import json
import logging
from typing import Dict, List, Optional, Union, Any, Tuple
from datetime import datetime

from .universal_base_config import UniversalBaseConfig

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ClimateResearchConfig(UniversalBaseConfig):
    """
    Climate research specialized configuration.
    
    Provides climate-specific templates, validation criteria,
    and calculation methods for climate science research.
    """
    
    def __init__(self):
        """Initialize climate research configuration."""
        super().__init__("climate")
        logger.info("✅ Climate research configuration loaded")
    
    def _load_domain_specific_templates(self):
        """Load climate research specific templates."""
        self._load_climate_templates()
        self._load_climate_validation()
    
    def _load_climate_validation(self):
        """Load climate-specific validation criteria."""
        self.validation_criteria_templates['climate'] = {
            'temperature_range_check': {
                'description': 'Temperature values within realistic range',
                'min_value': -100,  # Celsius
                'max_value': 60,
                'required': True
            },
            'physical_consistency': {
                'description': 'Results consistent with physical laws',
                'required': True
            },
            'data_completeness': {
                'description': 'All required climate variables present',
                'required': True
            },
            'sai_effectiveness_bounds': {
                'description': 'SAI cooling effects within realistic bounds',
                'min_cooling': 0.0,  # K
                'max_cooling': 5.0,  # K
                'required': True
            }
        }
    
    def configure_sai_experiment(self, injection_type: str = "pulse") -> Dict[str, Any]:
        """
        Configure SAI injection experiment.
        
        Args:
            injection_type: "pulse" or "continuous"
            
        Returns:
            Dict with SAI experiment configuration
        """
        sai_config = {
            'experiment_type': 'sai_injection_analysis',
            'research_question': f'SAI {injection_type} injection strategy analysis',
            'calculations': ['sai_analysis', 'statistical_analysis', 'data_visualization'],
            'parameters': {
                'injection_type': injection_type,
                'analysis_years': 10,
                'monthly_resolution': True
            },
            'data_requirements': [
                {
                    'name': 'glens_data',
                    'source': 'GLENS',
                    'variables': ['temperature', 'aerosol_concentration'],
                    'required': True
                }
            ],
            'validation_criteria': self.get_validation_criteria({
                'calculations': ['sai_analysis']
            })
        }
        
        return sai_config
    
    def get_cambridge_sai_config(self) -> Tuple[Dict, Dict]:
        """
        Get complete configuration for Cambridge SAI analysis.
        
        Returns:
            Tuple of (pulse_config, continuous_config)
        """
        pulse_config = self.configure_sai_experiment("pulse")
        continuous_config = self.configure_sai_experiment("continuous")
        
        return pulse_config, continuous_config


# Convenience function for universal pipeline integration
def create_climate_config() -> ClimateResearchConfig:
    """Create climate research configuration."""
    return ClimateResearchConfig()

def get_cambridge_analysis_configs() -> Tuple[Dict, Dict]:
    """Get Cambridge SAI analysis configurations."""
    config = create_climate_config()
    return config.get_cambridge_sai_config()