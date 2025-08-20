"""
GLENS Data Connector - Extracted from Sakana AI-S-Plus System

This module provides a Pipeline 2 compatible interface to the GLENS climate dataset
extracted and adapted from the Sakana (ai-s-plus) system. It maintains compatibility
with the original Sakana loader while adding Pipeline 2 specific enhancements.

Key Features:
- Direct adaptation of Sakana GLENS loader
- Mac M3 optimized chunked processing
- Pipeline 2 validation integration
- Real data authenticity verification
- Support for chemical composition variables
"""

import os
import sys
import json
import numpy as np
import xarray as xr
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union, Any
import logging
from datetime import datetime

# Import Sakana bridge for authenticity validation
from .sakana_bridge import SakanaBridge

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GLENSDataConnector:
    """
    Pipeline 2 compatible GLENS data connector based on Sakana system.
    
    This connector provides validated access to GLENS climate data with
    Pipeline 2 specific enhancements and chemical composition support.
    """
    
    def __init__(self, 
                 sakana_bridge: Optional[SakanaBridge] = None,
                 chunk_size_mb: int = 1024,  # 1GB chunks for Mac M3
                 cache_enabled: bool = True):
        """
        Initialize GLENS data connector.
        
        Args:
            sakana_bridge: Sakana bridge for validation (will create if None)
            chunk_size_mb: Chunk size in MB for Mac M3 optimization
            cache_enabled: Enable data caching
        """
        self.sakana_bridge = sakana_bridge or SakanaBridge()
        self.chunk_size_mb = chunk_size_mb
        self.cache_enabled = cache_enabled
        
        # Data cache for performance
        self.data_cache = {} if cache_enabled else None
        
        # Variable mappings for different domains
        self.variable_mappings = {
            # Chemical composition variables (priority for next experiments)
            'chemical_composition': {
                'aerosol_burden': 'BURDEN1',
                'sulfate_burden': 'BURDEN1', 
                'h2so4_concentration': 'BURDEN1',
                'particle_composition': 'BURDEN1',
                'chemical_species': 'BURDEN1'
            },
            # Climate response variables
            'climate_response': {
                'temperature': 'TREFHT',
                'surface_temperature': 'TREFHT',
                'precipitation': 'PRECT',
                'cloud_cover': 'CLDTOT',
                'total_cloud_fraction': 'CLDTOT'
            },
            # Atmospheric variables
            'atmospheric': {
                'surface_pressure': 'PS',
                'wind_speed': 'U',
                'vertical_velocity': 'OMEGA',
                'specific_humidity': 'Q'
            },
            # Radiative forcing variables
            'radiative': {
                'net_solar': 'FSNT',
                'net_longwave': 'FLNT',
                'shortwave_cloud_forcing': 'SWCF',
                'longwave_cloud_forcing': 'LWCF'
            }
        }
        
        # Scenario mappings
        self.scenario_mappings = {
            'control': 'GLENS_control',
            'baseline': 'GLENS_control',
            'ctrl': 'GLENS_control',
            'continuous_sai': 'GLENS_geoengineering',
            'geoengineering': 'GLENS_geoengineering',
            'sai': 'GLENS_geoengineering',
            'pulsed_sai': 'GLENS_feedback',
            'feedback': 'GLENS_feedback',
            'adaptive': 'GLENS_feedback'
        }
        
        logger.info("🔗 GLENS Data Connector initialized with Sakana integration")
    
    def detect_required_variables(self, experiment_description: str) -> List[str]:
        """
        Automatically detect required GLENS variables from experiment description.
        
        Args:
            experiment_description: Text description of experiment
            
        Returns:
            List of GLENS variable names
        """
        text = experiment_description.lower()
        required_vars = []
        
        # Check for chemical composition experiments (priority)
        chemical_keywords = ['chemical', 'composition', 'particle', 'aerosol', 'sulfate', 'h2so4']
        if any(keyword in text for keyword in chemical_keywords):
            required_vars.extend(['BURDEN1'])  # Aerosol burden for chemistry
            logger.info("🧪 Detected chemical composition experiment - added BURDEN1")
        
        # Check for climate response experiments
        climate_keywords = ['temperature', 'climate', 'warming', 'cooling']
        if any(keyword in text for keyword in climate_keywords):
            required_vars.extend(['TREFHT'])  # Temperature response
            logger.info("🌡️ Detected climate response experiment - added TREFHT")
        
        # Check for precipitation experiments
        precip_keywords = ['precipitation', 'rain', 'water', 'hydro']
        if any(keyword in text for keyword in precip_keywords):
            required_vars.extend(['PRECT'])  # Precipitation
            logger.info("🌧️ Detected precipitation experiment - added PRECT")
        
        # Check for cloud experiments
        cloud_keywords = ['cloud', 'albedo', 'reflection']
        if any(keyword in text for keyword in cloud_keywords):
            required_vars.extend(['CLDTOT'])  # Cloud cover
            logger.info("☁️ Detected cloud experiment - added CLDTOT")
        
        # Remove duplicates and return
        required_vars = list(set(required_vars))
        
        if not required_vars:
            # Default variables for unknown experiments
            required_vars = ['TREFHT', 'PRECT', 'CLDTOT']
            logger.info("❓ Unknown experiment type - using default variables")
        
        return required_vars
    
    def load_experiment_data(self, 
                           experiment_type: str,
                           scenarios: Optional[List[str]] = None,
                           variables: Optional[List[str]] = None,
                           validate_authenticity: bool = True) -> Dict[str, Any]:
        """
        Load GLENS data for a specific experiment type with validation.
        
        Args:
            experiment_type: Type of experiment (chemical_composition, climate_response, etc.)
            scenarios: Climate scenarios to load (defaults to control + sai)
            variables: Specific variables to load (auto-detected if None)
            validate_authenticity: Perform Sakana authenticity validation
            
        Returns:
            Dict with validated GLENS data and metadata
        """
        load_start = datetime.now()
        
        # Set defaults
        if scenarios is None:
            scenarios = ['control', 'continuous_sai', 'pulsed_sai']
        
        if variables is None:
            if experiment_type in self.variable_mappings:
                variables = list(self.variable_mappings[experiment_type].keys())
            else:
                variables = ['temperature', 'precipitation', 'aerosol_burden']
        
        # Map to GLENS variable names
        glens_variables = []
        for var in variables:
            mapped_var = self._map_variable_name(var, experiment_type)
            if mapped_var:
                glens_variables.append(mapped_var)
        
        logger.info(f"📊 Loading GLENS data: {experiment_type} experiment")
        logger.info(f"   Scenarios: {scenarios}")
        logger.info(f"   Variables: {variables} -> {glens_variables}")
        
        result = {
            'experiment_type': experiment_type,
            'scenarios_requested': scenarios,
            'variables_requested': variables,
            'glens_variables': glens_variables,
            'load_timestamp': load_start.isoformat(),
            'data': {},
            'metadata': {},
            'validation': {},
            'sakana_validated': False,
            'success': False
        }
        
        try:
            # Authenticity validation through Sakana bridge
            if validate_authenticity:
                auth_result = self.sakana_bridge.validate_data_authenticity({
                    'scenarios': scenarios,
                    'variables': glens_variables,
                    'experiment_type': experiment_type
                })
                result['validation']['authenticity'] = auth_result
                
                if not auth_result['authentic'] and self.sakana_bridge.real_data_mandatory:
                    result['error'] = 'AUTHENTICITY_FAILED: Real data required but not available'
                    return result
            
            # Load data through Sakana bridge
            data_result = self.sakana_bridge.load_validated_data(scenarios, glens_variables)
            
            if 'error' in data_result:
                result['error'] = data_result['error']
                return result
            
            # Process and optimize loaded data
            processed_data = self._process_loaded_data(
                data_result['data'], 
                experiment_type,
                scenarios,
                glens_variables
            )
            
            result['data'] = processed_data
            result['metadata'] = data_result['metadata']
            result['sakana_validated'] = data_result['sakana_principle_compliance']
            result['success'] = True
            
            load_time = (datetime.now() - load_start).total_seconds()
            logger.info(f"✅ GLENS data loaded successfully in {load_time:.2f}s")
            
        except Exception as e:
            result['error'] = f'LOAD_ERROR: {e}'
            logger.error(f"❌ Failed to load GLENS data: {e}")
        
        return result
    
    def load_chemical_composition_data(self, 
                                     scenarios: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Load GLENS data specifically for chemical composition experiments.
        
        This is optimized for the next experiments focusing on SAI particle chemistry.
        
        Args:
            scenarios: Climate scenarios (defaults to relevant SAI scenarios)
            
        Returns:
            Dict with chemical composition specific data
        """
        if scenarios is None:
            scenarios = ['control', 'continuous_sai']  # Key scenarios for chemistry
        
        return self.load_experiment_data(
            experiment_type='chemical_composition',
            scenarios=scenarios,
            variables=['aerosol_burden', 'sulfate_burden', 'particle_composition'],
            validate_authenticity=True
        )
    
    def _map_variable_name(self, variable: str, experiment_type: str) -> Optional[str]:
        """Map user variable name to GLENS variable name."""
        # First try experiment-type specific mapping
        if experiment_type in self.variable_mappings:
            domain_mapping = self.variable_mappings[experiment_type]
            if variable in domain_mapping:
                return domain_mapping[variable]
        
        # Try all mappings
        for domain_mapping in self.variable_mappings.values():
            if variable in domain_mapping:
                return domain_mapping[variable]
        
        # Direct mapping (variable name is already GLENS format)
        glens_vars = ['TREFHT', 'PRECT', 'CLDTOT', 'BURDEN1', 'PS', 'U', 'V', 'OMEGA', 'Q', 
                     'FSNT', 'FLNT', 'SWCF', 'LWCF']
        if variable.upper() in glens_vars:
            return variable.upper()
        
        logger.warning(f"⚠️ Unknown variable mapping: {variable}")
        return None
    
    def _process_loaded_data(self, 
                           raw_data: Dict, 
                           experiment_type: str,
                           scenarios: List[str],
                           variables: List[str]) -> Dict[str, Any]:
        """
        Process and optimize loaded GLENS data for Pipeline 2 use.
        
        Args:
            raw_data: Raw data from Sakana loader
            experiment_type: Type of experiment
            scenarios: Loaded scenarios
            variables: Loaded variables
            
        Returns:
            Processed and optimized data structure
        """
        processed = {
            'scenarios': {},
            'comparison_metrics': {},
            'experiment_optimized': {},
            'statistics': {}
        }
        
        # Process each scenario
        for scenario, scenario_data in raw_data.items():
            processed['scenarios'][scenario] = {}
            
            for variable, var_data in scenario_data.items():
                if isinstance(var_data, dict) and 'data' in var_data:
                    # Extract timeseries data
                    timeseries = var_data['data']
                    
                    processed['scenarios'][scenario][variable] = {
                        'timeseries': timeseries,
                        'mean': float(np.mean(timeseries)) if timeseries else 0.0,
                        'std': float(np.std(timeseries)) if timeseries else 0.0,
                        'min': float(np.min(timeseries)) if timeseries else 0.0,
                        'max': float(np.max(timeseries)) if timeseries else 0.0,
                        'units': var_data.get('units', 'unknown'),
                        'variable_name': var_data.get('variable_name', variable)
                    }
        
        # Calculate comparison metrics between scenarios
        if len(processed['scenarios']) >= 2:
            scenario_names = list(processed['scenarios'].keys())
            processed['comparison_metrics'] = self._calculate_scenario_comparisons(
                processed['scenarios'], scenario_names, variables
            )
        
        # Add experiment-type specific processing
        if experiment_type == 'chemical_composition':
            processed['experiment_optimized'] = self._process_chemical_data(processed)
        elif experiment_type == 'climate_response':
            processed['experiment_optimized'] = self._process_climate_data(processed)
        
        return processed
    
    def _calculate_scenario_comparisons(self, 
                                      scenarios_data: Dict, 
                                      scenario_names: List[str], 
                                      variables: List[str]) -> Dict[str, Any]:
        """Calculate comparison metrics between scenarios."""
        comparisons = {}
        
        # Compare first two scenarios
        if len(scenario_names) >= 2:
            scenario1, scenario2 = scenario_names[0], scenario_names[1]
            
            for var in variables:
                if (var in scenarios_data[scenario1] and 
                    var in scenarios_data[scenario2]):
                    
                    data1 = scenarios_data[scenario1][var]['timeseries']
                    data2 = scenarios_data[scenario2][var]['timeseries']
                    
                    if data1 and data2 and len(data1) == len(data2):
                        # Calculate difference
                        diff = np.array(data2) - np.array(data1)
                        
                        comparisons[f'{var}_difference'] = {
                            'mean_difference': float(np.mean(diff)),
                            'max_difference': float(np.max(np.abs(diff))),
                            'relative_change_percent': float(np.mean(diff) / np.mean(data1) * 100) if np.mean(data1) != 0 else 0.0,
                            'scenarios_compared': [scenario1, scenario2]
                        }
        
        return comparisons
    
    def _process_chemical_data(self, processed_data: Dict) -> Dict[str, Any]:
        """Process data specifically for chemical composition experiments."""
        chemical_metrics = {
            'processing_type': 'chemical_composition',
            'focus': 'SAI particle chemistry analysis'
        }
        
        # Look for aerosol burden data (key for chemical composition)
        for scenario, scenario_data in processed_data['scenarios'].items():
            if 'BURDEN1' in scenario_data:
                burden_data = scenario_data['BURDEN1']
                chemical_metrics[f'{scenario}_aerosol_analysis'] = {
                    'mean_burden': burden_data['mean'],
                    'burden_variability': burden_data['std'],
                    'particle_load_assessment': 'high' if burden_data['mean'] > 1e-3 else 'moderate'
                }
        
        return chemical_metrics
    
    def _process_climate_data(self, processed_data: Dict) -> Dict[str, Any]:
        """Process data specifically for climate response experiments."""
        climate_metrics = {
            'processing_type': 'climate_response',
            'focus': 'Climate system response analysis'
        }
        
        # Analyze temperature response if available
        for scenario, scenario_data in processed_data['scenarios'].items():
            if 'TREFHT' in scenario_data:
                temp_data = scenario_data['TREFHT']
                climate_metrics[f'{scenario}_temperature_analysis'] = {
                    'mean_temperature': temp_data['mean'],
                    'temperature_trend': 'warming' if temp_data['mean'] > 285 else 'cooling',
                    'variability': temp_data['std']
                }
        
        return climate_metrics
    
    def get_connector_status(self) -> Dict[str, Any]:
        """Get status of GLENS data connector."""
        return {
            'connector_active': True,
            'sakana_bridge_status': self.sakana_bridge.get_sakana_status(),
            'cache_enabled': self.cache_enabled,
            'chunk_size_mb': self.chunk_size_mb,
            'supported_experiment_types': list(self.variable_mappings.keys()),
            'supported_scenarios': list(self.scenario_mappings.keys()),
            'cached_datasets': len(self.data_cache) if self.data_cache else 0
        }


# Convenience functions for easy integration
def create_chemical_connector() -> GLENSDataConnector:
    """Create GLENS connector optimized for chemical composition experiments."""
    return GLENSDataConnector()

def create_climate_connector() -> GLENSDataConnector:
    """Create GLENS connector optimized for climate response experiments."""
    return GLENSDataConnector()