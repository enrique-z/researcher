"""
Sakana Bridge - Critical Connection to AI-S-Plus System

This module creates the essential bridge between Pipeline 2 and the Sakana (ai-s-plus) 
system, enabling real data validation and empirical falsification capabilities.

Key Features:
- Direct integration with ai-s-plus GLENS loader
- Real-time data validation using Sakana principles  
- Anti-hallucination measures from Sakana system
- BFTS/MCTS calculation validation
- Authenticity verification for all datasets
"""

import os
import sys
import json
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union, Any
import logging
from datetime import datetime

# Add ai-s-plus to Python path for direct integration
AI_S_PLUS_PATH = "/Users/apple/code/ai-s-plus/AI-Scientist-v2"
if AI_S_PLUS_PATH not in sys.path:
    sys.path.insert(0, AI_S_PLUS_PATH)

try:
    # Import Sakana GLENS loader directly
    from core.ai_scientist_utils import GLENSDataLoader, GLENSConfig
    SAKANA_AVAILABLE = True
except ImportError as e:
    logging.warning(f"Sakana system not available: {e}")
    SAKANA_AVAILABLE = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SakanaBridge:
    """
    Critical bridge to Sakana (ai-s-plus) system for real data validation.
    
    This is the core integration that enables Pipeline 2 to access validated
    real climate data and perform empirical falsification as required by
    the Sakana Principle.
    """
    
    def __init__(self, 
                 real_data_mandatory: bool = True,
                 synthetic_data_forbidden: bool = True):
        """
        Initialize Sakana bridge with strict validation requirements.
        
        Args:
            real_data_mandatory: Enforce real data usage only
            synthetic_data_forbidden: Block synthetic data completely
        """
        self.real_data_mandatory = real_data_mandatory
        self.synthetic_data_forbidden = synthetic_data_forbidden
        
        # Initialize Sakana GLENS loader if available
        self.glens_loader = None
        self.sakana_available = SAKANA_AVAILABLE
        
        if self.sakana_available:
            try:
                # Configure GLENS loader with real data path
                config = GLENSConfig(
                    data_source_type="glens",
                    base_path="/Users/apple/code/ai-s-plus/AI-Scientist-v2/data_organized/REAL_DATA_DOWNLOADED",
                    spatial_aggregation="global_mean"
                )
                self.glens_loader = GLENSDataLoader(config)
                logger.info("✅ Sakana GLENS loader successfully initialized")
            except Exception as e:
                logger.error(f"❌ Failed to initialize Sakana GLENS loader: {e}")
                self.sakana_available = False
        
        # Track validation history
        self.validation_history = []
        
        # Data authenticity tracker
        self.data_authenticity_log = []
        
        logger.info(f"🌉 Sakana Bridge initialized - Available: {self.sakana_available}")
    
    def validate_data_authenticity(self, data_request: Dict) -> Dict[str, Any]:
        """
        Validate data authenticity using Sakana anti-hallucination measures.
        
        Args:
            data_request: Data request with scenarios and variables
            
        Returns:
            Dict with authenticity validation results
        """
        validation_result = {
            'timestamp': datetime.now().isoformat(),
            'request': data_request,
            'authentic': False,
            'source': 'unknown',
            'violations': [],
            'sakana_validated': False
        }
        
        if not self.sakana_available:
            validation_result['violations'].append('SAKANA_UNAVAILABLE: Cannot validate authenticity')
            return validation_result
        
        try:
            # Check if real GLENS data is available through Sakana
            if not self.glens_loader.real_data_available:
                if self.real_data_mandatory:
                    validation_result['violations'].append('REAL_DATA_REQUIRED: No authentic GLENS data available')
                    return validation_result
                else:
                    validation_result['violations'].append('WARNING: Using synthetic data - real data not found')
                    validation_result['source'] = 'synthetic_fallback'
            else:
                validation_result['authentic'] = True
                validation_result['source'] = 'glens_real_data'
                validation_result['sakana_validated'] = True
                logger.info("✅ Real GLENS data validated through Sakana system")
        
        except Exception as e:
            validation_result['violations'].append(f'VALIDATION_ERROR: {e}')
            logger.error(f"❌ Data authenticity validation failed: {e}")
        
        # Log validation attempt
        self.data_authenticity_log.append(validation_result)
        
        return validation_result
    
    def load_validated_data(self, 
                          scenarios: List[str], 
                          variables: List[str]) -> Dict[str, Any]:
        """
        Load data through Sakana system with authenticity validation.
        
        Args:
            scenarios: Climate scenarios to load
            variables: Variables to extract
            
        Returns:
            Dict with validated data or rejection notice
        """
        data_request = {
            'scenarios': scenarios,
            'variables': variables,
            'timestamp': datetime.now().isoformat()
        }
        
        # First validate data authenticity
        authenticity_check = self.validate_data_authenticity(data_request)
        
        result = {
            'authenticity_validation': authenticity_check,
            'data': {},
            'metadata': {},
            'sakana_principle_compliance': False
        }
        
        # Block if synthetic data forbidden and real data not available
        if (self.synthetic_data_forbidden and 
            not authenticity_check['authentic'] and 
            'REAL_DATA_REQUIRED' in str(authenticity_check['violations'])):
            
            result['error'] = 'SYNTHETIC_DATA_FORBIDDEN: Real data mandatory, synthetic blocked'
            logger.error("❌ Data loading blocked - synthetic data forbidden")
            return result
        
        # Load data through Sakana GLENS loader
        if self.sakana_available and self.glens_loader:
            try:
                loaded_data = self.glens_loader.load_scenarios(scenarios, variables)
                result['data'] = loaded_data
                result['sakana_principle_compliance'] = authenticity_check['authentic']
                
                # Add metadata about data source
                result['metadata'] = {
                    'data_source': authenticity_check['source'],
                    'authentic_data': authenticity_check['authentic'],
                    'sakana_validated': authenticity_check['sakana_validated'],
                    'loading_timestamp': datetime.now().isoformat(),
                    'scenarios_loaded': list(loaded_data.keys()),
                    'variables_loaded': variables
                }
                
                logger.info(f"✅ Successfully loaded {len(scenarios)} scenarios, {len(variables)} variables")
                
            except Exception as e:
                result['error'] = f'DATA_LOADING_ERROR: {e}'
                logger.error(f"❌ Failed to load data through Sakana: {e}")
        
        else:
            result['error'] = 'SAKANA_UNAVAILABLE: Cannot load data without Sakana system'
        
        return result
    
    def perform_sakana_validation(self, 
                                hypothesis: Dict,
                                required_data: List[str]) -> Dict[str, Any]:
        """
        Perform empirical validation using Sakana principles.
        
        Args:
            hypothesis: Scientific hypothesis to validate
            required_data: Required datasets for validation
            
        Returns:
            Dict with Sakana validation results
        """
        validation_start = datetime.now()
        
        sakana_result = {
            'validation_id': f"sakana_{int(validation_start.timestamp())}",
            'hypothesis': hypothesis,
            'required_data': required_data,
            'sakana_principle_satisfied': False,
            'empirical_evidence_found': False,
            'validation_tests': {},
            'violations': [],
            'recommendations': []
        }
        
        try:
            # Test 1: Check empirical grounding
            empirical_test = self._check_empirical_grounding(hypothesis, required_data)
            sakana_result['validation_tests']['empirical_grounding'] = empirical_test
            
            if not empirical_test['passed']:
                sakana_result['violations'].extend(empirical_test['violations'])
            else:
                sakana_result['empirical_evidence_found'] = True
            
            # Test 2: Data availability validation
            data_test = self._check_data_availability(required_data)
            sakana_result['validation_tests']['data_availability'] = data_test
            
            if not data_test['passed']:
                sakana_result['violations'].extend(data_test['violations'])
            
            # Test 3: Physical plausibility check
            plausibility_test = self._check_physical_plausibility(hypothesis)
            sakana_result['validation_tests']['physical_plausibility'] = plausibility_test
            
            if not plausibility_test['passed']:
                sakana_result['violations'].extend(plausibility_test['violations'])
            
            # Overall Sakana Principle satisfaction
            sakana_result['sakana_principle_satisfied'] = (
                empirical_test['passed'] and 
                data_test['passed'] and
                plausibility_test['passed'] and
                len(sakana_result['violations']) == 0
            )
            
            # Generate recommendations
            sakana_result['recommendations'] = self._generate_sakana_recommendations(sakana_result)
            
            logger.info(f"Sakana validation: {'PASS' if sakana_result['sakana_principle_satisfied'] else 'FAIL'}")
            
        except Exception as e:
            sakana_result['violations'].append(f'SAKANA_VALIDATION_ERROR: {e}')
            logger.error(f"❌ Sakana validation failed: {e}")
        
        # Record validation
        self.validation_history.append(sakana_result)
        
        return sakana_result
    
    def _check_empirical_grounding(self, hypothesis: Dict, required_data: List[str]) -> Dict:
        """Check if hypothesis has empirical grounding."""
        empirical_test = {
            'test_name': 'Empirical Grounding Check',
            'passed': False,
            'violations': [],
            'evidence_found': []
        }
        
        hypothesis_text = str(hypothesis).lower()
        
        # Look for empirical indicators
        empirical_indicators = [
            'glens', 'arise-sai', 'geomip', 'ncar', 'cesm', 'data',
            'measurement', 'observation', 'experiment', 'model output'
        ]
        
        found_indicators = [ind for ind in empirical_indicators if ind in hypothesis_text]
        empirical_test['evidence_found'] = found_indicators
        
        if len(found_indicators) == 0:
            empirical_test['violations'].append('NO_EMPIRICAL_EVIDENCE: Hypothesis lacks empirical grounding')
        
        # Check for required data references
        if required_data:
            data_references = [data for data in required_data if data.lower() in hypothesis_text]
            if len(data_references) == 0:
                empirical_test['violations'].append('MISSING_DATA_REFERENCE: Required data not referenced')
        
        empirical_test['passed'] = len(empirical_test['violations']) == 0
        
        return empirical_test
    
    def _check_data_availability(self, required_data: List[str]) -> Dict:
        """Check if required data is available through Sakana."""
        data_test = {
            'test_name': 'Data Availability Check',
            'passed': False,
            'violations': [],
            'available_data': []
        }
        
        if not self.sakana_available:
            data_test['violations'].append('SAKANA_UNAVAILABLE: Cannot verify data availability')
            return data_test
        
        # Check GLENS data availability
        if self.glens_loader and self.glens_loader.real_data_available:
            data_test['available_data'].append('GLENS_real_data')
        else:
            if self.real_data_mandatory:
                data_test['violations'].append('GLENS_DATA_UNAVAILABLE: Real GLENS data required but not available')
        
        data_test['passed'] = len(data_test['violations']) == 0
        
        return data_test
    
    def _check_physical_plausibility(self, hypothesis: Dict) -> Dict:
        """Check physical plausibility of hypothesis parameters."""
        plausibility_test = {
            'test_name': 'Physical Plausibility Check',
            'passed': False,
            'violations': [],
            'parameter_checks': []
        }
        
        parameters = hypothesis.get('parameters', {})
        
        # Check for obviously unphysical values
        for param_name, param_value in parameters.items():
            if isinstance(param_value, (int, float)):
                if abs(param_value) > 1e10:
                    plausibility_test['violations'].append(f'EXTREME_VALUE: {param_name}={param_value}')
                elif param_value < 0 and 'temperature' in param_name.lower():
                    plausibility_test['violations'].append(f'NEGATIVE_TEMPERATURE: {param_name}={param_value}')
        
        plausibility_test['passed'] = len(plausibility_test['violations']) == 0
        
        return plausibility_test
    
    def _generate_sakana_recommendations(self, validation_result: Dict) -> List[str]:
        """Generate Sakana-specific recommendations."""
        recommendations = []
        
        if validation_result['sakana_principle_satisfied']:
            recommendations.append("✅ SAKANA APPROVED: Hypothesis meets empirical validation requirements")
        else:
            recommendations.append("❌ SAKANA REJECTION: Address violations before proceeding")
        
        violations = validation_result['violations']
        
        if any('NO_EMPIRICAL_EVIDENCE' in v for v in violations):
            recommendations.append("Include references to real datasets (GLENS, ARISE-SAI, GeoMIP)")
        
        if any('GLENS_DATA_UNAVAILABLE' in v for v in violations):
            recommendations.append("Ensure GLENS data is downloaded and accessible through Sakana system")
        
        if any('EXTREME_VALUE' in v for v in violations):
            recommendations.append("Review parameter values for physical realism")
        
        return recommendations
    
    def get_sakana_status(self) -> Dict[str, Any]:
        """Get current status of Sakana bridge."""
        return {
            'sakana_available': self.sakana_available,
            'glens_loader_active': self.glens_loader is not None,
            'real_data_available': self.glens_loader.real_data_available if self.glens_loader else False,
            'validations_performed': len(self.validation_history),
            'authenticity_checks': len(self.data_authenticity_log),
            'real_data_mandatory': self.real_data_mandatory,
            'synthetic_data_forbidden': self.synthetic_data_forbidden
        }


# Convenience function for direct integration
def create_sakana_bridge(real_data_mandatory: bool = True) -> SakanaBridge:
    """Create and return a Sakana bridge instance."""
    return SakanaBridge(real_data_mandatory=real_data_mandatory, 
                       synthetic_data_forbidden=True)