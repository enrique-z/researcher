"""
Framework Bridge: Connects Researcher and Sakana validation systems
Implements domain-agnostic validation gateway
"""

import json
import logging
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass
from pathlib import Path

from ..validation.experiment_validator import ExperimentValidator
from ..validation.sakana_validator import SakanaValidator
from ..data.loaders.glens_loader import GLENSLoader

logger = logging.getLogger(__name__)


@dataclass
class BridgeConfig:
    """Configuration for framework bridge"""
    glens_data_path: str
    enable_pre_validation: bool = True
    enable_post_validation: bool = True
    enforcement_level: str = 'strict'
    max_retries: int = 3
    cache_validated_data: bool = True


class FrameworkBridge:
    """
    Bridges Researcher paper generation with Sakana validation
    Ensures all experiments pass empirical validation before paper generation
    """
    
    def __init__(self, config: BridgeConfig):
        """Initialize framework bridge with configuration"""
        self.config = config
        self.experiment_validator = ExperimentValidator()
        self.sakana_validator = SakanaValidator(
            glens_data_path=config.glens_data_path,
            enforcement_level=config.enforcement_level
        )
        self.glens_loader = GLENSLoader(config.glens_data_path)
        self._validated_cache = {}
        
    def pre_validate_experiment(self, experiment: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        """
        Pre-validate experiment before sending to Researcher
        Prevents wasted effort on experiments that will fail validation
        
        Args:
            experiment: Experiment configuration
            
        Returns:
            Tuple of (validation_passed, validation_details)
        """
        if not self.config.enable_pre_validation:
            return True, {"skipped": True, "reason": "Pre-validation disabled"}
            
        logger.info(f"Pre-validating experiment: {experiment.get('title', 'Unknown')}")
        
        # Detect experiment domain
        domain = self.experiment_validator.detect_experiment_domain(experiment)
        logger.info(f"Detected experiment domain: {domain}")
        
        # Apply domain-specific validation
        validation_result = self.experiment_validator.validate_experiment({
            'parameters': experiment.get('parameters', {}),
            'hypothesis': experiment.get('hypothesis', ''),
            'methodology': experiment.get('methodology', ''),
            'domain': domain
        })
        
        # If domain validation passes, apply Sakana Principle
        if validation_result['validation_passed']:
            sakana_result = self.sakana_validator.validate(experiment)
            if not sakana_result['validation_passed']:
                validation_result = sakana_result
                
        # Cache if validated successfully
        if validation_result['validation_passed'] and self.config.cache_validated_data:
            exp_id = experiment.get('id', hash(json.dumps(experiment, sort_keys=True)))
            self._validated_cache[exp_id] = validation_result
            
        return validation_result['validation_passed'], validation_result
        
    def enhance_with_real_data(self, experiment: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enhance experiment with real GLENS data before paper generation
        
        Args:
            experiment: Validated experiment configuration
            
        Returns:
            Enhanced experiment with real data context
        """
        logger.info("Enhancing experiment with real GLENS data")
        
        # Detect domain and get appropriate variables
        domain = self.experiment_validator.detect_experiment_domain(experiment)
        recommended_vars = self.glens_loader.recommend_variables_for_experiment(
            experiment.get('title', ''),
            experiment.get('methodology', '')
        )
        
        # Load relevant data
        enhanced_experiment = experiment.copy()
        enhanced_experiment['real_data'] = {
            'domain': domain,
            'glens_variables': recommended_vars,
            'data_availability': True,
            'validation_context': {
                'empirical_grounding': 'Required - Sakana Principle enforced',
                'data_source': 'NCAR GLENS authentic climate data',
                'validation_method': f'Domain-specific validation for {domain}'
            }
        }
        
        # Add domain-specific enhancements
        if domain == 'chemical_composition':
            enhanced_experiment['real_data']['chemical_constraints'] = {
                'h2so4_range': '10-98% (stratospheric conditions)',
                'temperature_range': '200-250K',
                'pressure_range': '10-100 hPa'
            }
        elif domain == 'climate_response':
            enhanced_experiment['real_data']['climate_metrics'] = {
                'temperature_variables': ['TREFHT', 'TS'],
                'precipitation_variables': ['PRECT', 'PRECC', 'PRECL'],
                'ensemble_size': 20
            }
            
        return enhanced_experiment
        
    def post_validate_paper(self, paper: str, experiment: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        """
        Post-validate generated paper to ensure consistency with validation
        
        Args:
            paper: Generated paper text
            experiment: Original experiment configuration
            
        Returns:
            Tuple of (validation_passed, validation_details)
        """
        if not self.config.enable_post_validation:
            return True, {"skipped": True, "reason": "Post-validation disabled"}
            
        logger.info("Post-validating generated paper")
        
        # Check for consistency between paper claims and validated parameters
        validation_results = {
            'validation_passed': True,
            'checks': []
        }
        
        # Extract claims from paper (simplified - would use NLP in production)
        paper_lower = paper.lower()
        
        # Check for plausibility trap indicators
        trap_indicators = [
            'theoretically possible',
            'could potentially',
            'might achieve',
            'hypothetically'
        ]
        
        for indicator in trap_indicators:
            if indicator in paper_lower and 'empirical' not in paper_lower[max(0, paper_lower.index(indicator)-100):paper_lower.index(indicator)+100]:
                validation_results['checks'].append({
                    'issue': 'Potential plausibility trap',
                    'detail': f'Found "{indicator}" without empirical grounding',
                    'severity': 'warning'
                })
                
        # Check for data authenticity claims
        if 'glens' in paper_lower or 'ncar' in paper_lower:
            if 'synthetic' in paper_lower or 'simulated' in paper_lower:
                validation_results['validation_passed'] = False
                validation_results['checks'].append({
                    'issue': 'Data authenticity violation',
                    'detail': 'Paper claims both real GLENS data and synthetic data',
                    'severity': 'error'
                })
                
        # Verify domain-specific content
        domain = self.experiment_validator.detect_experiment_domain(experiment)
        if domain == 'chemical_composition':
            if 'h2so4' not in paper_lower and 'sulfuric acid' not in paper_lower:
                validation_results['checks'].append({
                    'issue': 'Missing chemical composition discussion',
                    'detail': 'Chemical composition experiment lacks H2SO4 analysis',
                    'severity': 'warning'
                })
                
        return validation_results['validation_passed'], validation_results
        
    def bridge_data_flow(self, 
                        experiment: Dict[str, Any],
                        researcher_callback: Optional[callable] = None) -> Dict[str, Any]:
        """
        Complete bridge flow: pre-validation → enhancement → generation → post-validation
        
        Args:
            experiment: Experiment configuration
            researcher_callback: Optional callback to Researcher generation
            
        Returns:
            Complete results including paper and validation
        """
        results = {
            'experiment_id': experiment.get('id', 'unknown'),
            'stages': {}
        }
        
        # Stage 1: Pre-validation
        pre_valid, pre_details = self.pre_validate_experiment(experiment)
        results['stages']['pre_validation'] = {
            'passed': pre_valid,
            'details': pre_details
        }
        
        if not pre_valid:
            results['final_status'] = 'REJECTED_AT_PRE_VALIDATION'
            logger.warning(f"Experiment rejected at pre-validation: {pre_details}")
            return results
            
        # Stage 2: Enhancement with real data
        enhanced_exp = self.enhance_with_real_data(experiment)
        results['stages']['enhancement'] = {
            'enhanced': True,
            'domain': enhanced_exp['real_data']['domain'],
            'variables': enhanced_exp['real_data']['glens_variables']
        }
        
        # Stage 3: Paper generation (if callback provided)
        if researcher_callback:
            logger.info("Generating paper with Researcher framework")
            paper = researcher_callback(enhanced_exp)
            results['generated_paper'] = paper
            
            # Stage 4: Post-validation
            post_valid, post_details = self.post_validate_paper(paper, experiment)
            results['stages']['post_validation'] = {
                'passed': post_valid,
                'details': post_details
            }
            
            results['final_status'] = 'SUCCESS' if post_valid else 'POST_VALIDATION_FAILED'
        else:
            results['final_status'] = 'READY_FOR_GENERATION'
            
        return results
        
    def get_validation_statistics(self) -> Dict[str, Any]:
        """Get statistics about validation performance"""
        return {
            'cache_size': len(self._validated_cache),
            'cache_hits': sum(1 for v in self._validated_cache.values() if v.get('cache_hit', False)),
            'enforcement_level': self.config.enforcement_level,
            'pre_validation_enabled': self.config.enable_pre_validation,
            'post_validation_enabled': self.config.enable_post_validation
        }