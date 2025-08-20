"""
GLENS Integration Module for Pipeline 2
Integrates AI-S-Plus GLENS loader with Pipeline 2 Development framework
"""

import os
import sys
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
import json

# Add AI-S-Plus path for imports
AI_S_PLUS_PATH = "/Users/apple/code/ai-s-plus"
sys.path.insert(0, str(Path(AI_S_PLUS_PATH) / "AI-Scientist-v2" / "core"))

try:
    from ai_scientist.utils.glens_loader import GLENSDataLoader, GLENSConfig
    GLENS_AVAILABLE = True
except ImportError as e:
    GLENS_AVAILABLE = False
    logging.warning(f"GLENS loader not available: {e}")

logger = logging.getLogger(__name__)

class Pipeline2GLENSIntegration:
    """
    Integration bridge between AI-S-Plus GLENS loader and Pipeline 2 framework
    """
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path
        self.glens_loader = None
        self.initialized = False
        
        if GLENS_AVAILABLE:
            try:
                self._initialize_glens_loader()
                self.initialized = True
                logger.info("✅ GLENS integration initialized successfully")
            except Exception as e:
                logger.error(f"❌ Failed to initialize GLENS loader: {e}")
        else:
            logger.warning("⚠️ GLENS loader not available - operating without real climate data")
    
    def _initialize_glens_loader(self):
        """Initialize GLENS loader with Pipeline 2 compatible configuration"""
        config = GLENSConfig(
            data_source_type="glens",
            prefer_data_source="glens",
            spatial_aggregation="global_mean",
            scenarios={
                "baseline": "GLENS_control",
                "continuous_sai": "GLENS_geoengineering", 
                "pulsed_sai": "GLENS_feedback",
                "control": "GLENS_control",
                "sai": "GLENS_geoengineering",
                "intervention": "GLENS_geoengineering"
            },
            variables={
                "temperature": "TREFHT",
                "precipitation": "PRECT", 
                "clouds": "CLDTOT",
                "aerosol_burden": "BURDEN1"
            }
        )
        
        self.glens_loader = GLENSDataLoader(config)
        logger.info("GLENS loader initialized with Pipeline 2 configuration")
    
    def load_scenarios_for_experiment(self, experiment_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Load GLENS scenarios based on experiment configuration
        
        Args:
            experiment_config: Experiment configuration from Pipeline 2
            
        Returns:
            Dict containing loaded GLENS data for the experiment
        """
        if not self.initialized:
            logger.warning("GLENS not initialized - returning mock data structure")
            return self._create_mock_data_structure(experiment_config)
        
        try:
            # Extract scenarios from experiment config
            scenarios = experiment_config.get("scenarios", ["baseline", "continuous_sai"])
            variables = experiment_config.get("variables", ["temperature"])
            
            logger.info(f"Loading GLENS data for scenarios: {scenarios}")
            
            # Load data using GLENS loader
            loaded_data = self.glens_loader.load_scenarios(scenarios, variables)
            
            # Format for Pipeline 2 compatibility
            pipeline2_data = self._format_for_pipeline2(loaded_data, scenarios, variables)
            
            return {
                "status": "success",
                "data_source": "GLENS",
                "scenarios": scenarios,
                "variables": variables,
                "data": pipeline2_data,
                "metadata": {
                    "ensemble_members": 20,  # Default GLENS ensemble size
                    "time_period": "2020-2069",  # Default GLENS time period
                    "spatial_resolution": "global_mean"
                }
            }
            
        except Exception as e:
            logger.error(f"Failed to load GLENS data: {e}")
            return {
                "status": "error",
                "error": str(e),
                "fallback_data": self._create_mock_data_structure(experiment_config)
            }
    
    def _format_for_pipeline2(self, glens_data: Any, scenarios: List[str], variables: List[str]) -> Dict[str, Any]:
        """Format GLENS data for Pipeline 2 consumption"""
        formatted_data = {}
        
        for scenario in scenarios:
            formatted_data[scenario] = {}
            
            for variable in variables:
                try:
                    # Get data for this scenario/variable combination
                    data_values = self._extract_data_values(glens_data, scenario, variable)
                    
                    formatted_data[scenario][variable] = {
                        "values": data_values.tolist() if hasattr(data_values, 'tolist') else data_values,
                        "units": self._get_variable_units(variable),
                        "description": self._get_variable_description(variable)
                    }
                    
                except Exception as e:
                    logger.warning(f"Failed to extract {variable} for {scenario}: {e}")
                    formatted_data[scenario][variable] = {
                        "values": [],
                        "units": "unknown",
                        "description": f"Failed to load {variable}",
                        "error": str(e)
                    }
        
        return formatted_data
    
    def _extract_data_values(self, glens_data: Any, scenario: str, variable: str):
        """Extract actual data values from GLENS dataset"""
        # This depends on the structure returned by GLENS loader
        if hasattr(glens_data, 'get_scenario_data'):
            scenario_data = glens_data.get_scenario_data(scenario)
            if hasattr(scenario_data, variable):
                return getattr(scenario_data, variable)
        
        # Fallback: try to access as dictionary
        if isinstance(glens_data, dict):
            return glens_data.get(scenario, {}).get(variable, [])
        
        # Return empty list if can't extract
        return []
    
    def _get_variable_units(self, variable: str) -> str:
        """Get units for climate variables"""
        units_map = {
            "temperature": "K",
            "precipitation": "mm/day",
            "clouds": "fraction",
            "aerosol_burden": "kg/m²"
        }
        return units_map.get(variable, "unknown")
    
    def _get_variable_description(self, variable: str) -> str:
        """Get description for climate variables"""
        descriptions = {
            "temperature": "Reference height temperature",
            "precipitation": "Total precipitation rate",
            "clouds": "Total cloud fraction",
            "aerosol_burden": "Aerosol burden"
        }
        return descriptions.get(variable, f"Climate variable: {variable}")
    
    def _create_mock_data_structure(self, experiment_config: Dict[str, Any]) -> Dict[str, Any]:
        """Create mock data structure when GLENS not available"""
        scenarios = experiment_config.get("scenarios", ["baseline", "continuous_sai"])
        variables = experiment_config.get("variables", ["temperature"])
        
        mock_data = {}
        for scenario in scenarios:
            mock_data[scenario] = {}
            for variable in variables:
                mock_data[scenario][variable] = {
                    "values": [],
                    "units": self._get_variable_units(variable),
                    "description": f"Mock {variable} data",
                    "note": "GLENS loader not available - using placeholder"
                }
        
        return mock_data
    
    def validate_climate_experiment(self, experiment_claims: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Validate experimental claims against GLENS data
        
        Args:
            experiment_claims: List of claims to validate
            
        Returns:
            Validation results with support evidence
        """
        if not self.initialized:
            return {
                "validation_status": "skipped",
                "reason": "GLENS loader not available",
                "supported_claims": 0,
                "total_claims": len(experiment_claims)
            }
        
        supported_claims = 0
        validation_details = []
        
        for claim in experiment_claims:
            try:
                # Extract claim parameters
                scenario = claim.get("scenario", "baseline")
                variable = claim.get("variable", "temperature")
                expected_value = claim.get("expected_value")
                tolerance = claim.get("tolerance", 0.1)
                
                # Load corresponding GLENS data
                glens_value = self._get_glens_value_for_claim(scenario, variable)
                
                # Validate claim
                is_supported = self._validate_single_claim(expected_value, glens_value, tolerance)
                
                if is_supported:
                    supported_claims += 1
                
                validation_details.append({
                    "claim": claim.get("description", "Unknown claim"),
                    "expected": expected_value,
                    "glens_value": glens_value,
                    "supported": is_supported,
                    "scenario": scenario,
                    "variable": variable
                })
                
            except Exception as e:
                logger.warning(f"Failed to validate claim: {e}")
                validation_details.append({
                    "claim": claim.get("description", "Unknown claim"),
                    "supported": False,
                    "error": str(e)
                })
        
        return {
            "validation_status": "completed",
            "supported_claims": supported_claims,
            "total_claims": len(experiment_claims),
            "support_rate": supported_claims / len(experiment_claims) if experiment_claims else 0,
            "details": validation_details
        }
    
    def _get_glens_value_for_claim(self, scenario: str, variable: str) -> Optional[float]:
        """Get GLENS value for a specific scenario/variable combination"""
        try:
            # This would use the GLENS loader to get actual values
            # For now, return None to indicate no data available
            return None
        except Exception as e:
            logger.warning(f"Failed to get GLENS value for {scenario}/{variable}: {e}")
            return None
    
    def _validate_single_claim(self, expected: float, actual: Optional[float], tolerance: float) -> bool:
        """Validate a single claim against GLENS data"""
        if actual is None or expected is None:
            return False
        
        return abs(expected - actual) <= tolerance
    
    def get_integration_status(self) -> Dict[str, Any]:
        """Get current integration status"""
        return {
            "glens_available": GLENS_AVAILABLE,
            "initialized": self.initialized,
            "loader_status": "operational" if self.initialized else "unavailable",
            "data_source": "GLENS" if self.initialized else "mock",
            "ai_s_plus_path": AI_S_PLUS_PATH
        }

def test_glens_integration():
    """Test function for GLENS integration"""
    logger.info("🧪 Testing GLENS integration...")
    
    integration = Pipeline2GLENSIntegration()
    status = integration.get_integration_status()
    
    logger.info(f"Integration status: {status}")
    
    # Test experiment configuration
    test_experiment = {
        "scenarios": ["baseline", "continuous_sai"],
        "variables": ["temperature", "precipitation"],
        "experiment_type": "sai_comparison"
    }
    
    # Test data loading
    result = integration.load_scenarios_for_experiment(test_experiment)
    logger.info(f"Load result status: {result.get('status', 'unknown')}")
    
    # Test claim validation
    test_claims = [
        {
            "description": "Temperature increase under SAI",
            "scenario": "continuous_sai",
            "variable": "temperature", 
            "expected_value": 285.0,
            "tolerance": 2.0
        }
    ]
    
    validation_result = integration.validate_climate_experiment(test_claims)
    logger.info(f"Validation result: {validation_result['validation_status']}")
    
    return status["initialized"]

if __name__ == "__main__":
    success = test_glens_integration()
    print(f"✅ GLENS integration test {'PASSED' if success else 'FAILED'}")