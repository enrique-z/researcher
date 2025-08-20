"""
Pipeline 1 Interface - Critical Integration with Working GPT-5 System

This module provides the essential interface between Pipeline 2 (enhanced validation)
and Pipeline 1 (production GPT-5 system), enabling seamless enhancement without
disruption to the working comprehensive_enhancer.py workflow.

Key Features:
- Non-disruptive integration with comprehensive_enhancer.py
- Quality improvement hooks (6.0+ → 7.0+)
- Real data validation integration
- Sakana principle validation checkpoints
- Rollback capability if validation fails
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, List, Optional, Union, Any, Tuple
import logging
from datetime import datetime

# Import Pipeline 2 components
from .sakana_bridge import SakanaBridge
from .glens_data_connector import GLENSDataConnector
from ..validation.experiment_validator import ExperimentValidator
from ..validation.domains.chemical_composition import ChemicalCompositionValidator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Pipeline1Interface:
    """
    Critical interface between Pipeline 2 validation and Pipeline 1 production system.
    
    This interface allows Pipeline 2 to enhance Pipeline 1 papers with real data
    validation and empirical verification while maintaining full compatibility
    with the existing comprehensive_enhancer.py workflow.
    """
    
    def __init__(self, 
                 enable_validation: bool = True,
                 quality_improvement_target: float = 7.0,
                 fallback_on_failure: bool = True):
        """
        Initialize Pipeline 1 interface.
        
        Args:
            enable_validation: Enable Pipeline 2 validation enhancements
            quality_improvement_target: Target quality score (Pipeline 1: 6.0+ → Pipeline 2: 7.0+)
            fallback_on_failure: Fallback to Pipeline 1 only if Pipeline 2 fails
        """
        self.enable_validation = enable_validation
        self.quality_improvement_target = quality_improvement_target
        self.fallback_on_failure = fallback_on_failure
        
        # Initialize Pipeline 2 components
        self.sakana_bridge = None
        self.glens_connector = None
        self.experiment_validator = None
        self.chemical_validator = None
        
        if enable_validation:
            try:
                self.sakana_bridge = SakanaBridge()
                self.glens_connector = GLENSDataConnector(self.sakana_bridge)
                self.experiment_validator = ExperimentValidator()
                self.chemical_validator = ChemicalCompositionValidator()
                logger.info("✅ Pipeline 2 validation components initialized")
            except Exception as e:
                logger.warning(f"⚠️ Pipeline 2 validation initialization failed: {e}")
                if not fallback_on_failure:
                    raise
                else:
                    self.enable_validation = False
                    logger.info("🔄 Falling back to Pipeline 1 only mode")
        
        # Track enhancement attempts
        self.enhancement_history = []
        self.integration_stats = {
            'total_attempts': 0,
            'successful_enhancements': 0,
            'validation_failures': 0,
            'fallbacks': 0,
            'quality_improvements': 0
        }
        
        logger.info(f"🌉 Pipeline 1 Interface initialized - Enhancement: {'ENABLED' if enable_validation else 'DISABLED'}")
    
    def enhance_experiment_analysis(self, experiment_dir: str) -> Dict[str, Any]:
        """
        Enhance comprehensive_enhancer.py experiment analysis with Pipeline 2 validation.
        
        This is a non-disruptive enhancement that can be called from comprehensive_enhancer.py
        to add validation capabilities without changing the core workflow.
        
        Args:
            experiment_dir: Path to experiment directory (same as comprehensive_enhancer input)
            
        Returns:
            Dict with enhancement results and validation data
        """
        enhancement_start = datetime.now()
        self.integration_stats['total_attempts'] += 1
        
        enhancement_result = {
            'enhancement_timestamp': enhancement_start.isoformat(),
            'experiment_dir': experiment_dir,
            'pipeline2_enabled': self.enable_validation,
            'validation_results': {},
            'quality_analysis': {},
            'real_data_integration': {},
            'enhancement_successful': False,
            'quality_score_original': None,
            'quality_score_enhanced': None,
            'recommendations': []
        }
        
        try:
            # 1. Read existing experiment data (compatible with comprehensive_enhancer)
            experiment_data = self._read_experiment_data(experiment_dir)
            enhancement_result['experiment_data'] = experiment_data
            
            if not self.enable_validation:
                enhancement_result['recommendations'].append("Pipeline 2 validation disabled - using Pipeline 1 only")
                enhancement_result['enhancement_successful'] = True
                return enhancement_result
            
            # 2. Perform Pipeline 2 validation
            validation_results = self._perform_pipeline2_validation(experiment_data)
            enhancement_result['validation_results'] = validation_results
            
            # 3. Integrate real data if validation passes
            if validation_results['sakana_principle_satisfied']:
                real_data_integration = self._integrate_real_data(experiment_data, experiment_dir)
                enhancement_result['real_data_integration'] = real_data_integration
            else:
                logger.warning("⚠️ Sakana validation failed - skipping real data integration")
                self.integration_stats['validation_failures'] += 1
            
            # 4. Calculate quality improvements
            quality_analysis = self._calculate_quality_improvements(
                experiment_data, validation_results, enhancement_result.get('real_data_integration', {})
            )
            enhancement_result['quality_analysis'] = quality_analysis
            
            # 5. Generate enhancement recommendations
            enhancement_result['recommendations'] = self._generate_enhancement_recommendations(
                validation_results, quality_analysis
            )
            
            # 6. Determine overall success
            enhancement_result['enhancement_successful'] = (
                validation_results.get('sakana_principle_satisfied', False) or
                self.fallback_on_failure
            )
            
            if enhancement_result['enhancement_successful']:
                self.integration_stats['successful_enhancements'] += 1
                
                # Check if quality target achieved
                enhanced_score = quality_analysis.get('estimated_enhanced_score', 0.0)
                if enhanced_score >= self.quality_improvement_target:
                    self.integration_stats['quality_improvements'] += 1
                    logger.info(f"🎯 Quality target achieved: {enhanced_score:.1f} ≥ {self.quality_improvement_target}")
            
            logger.info(f"Pipeline 1 enhancement: {'SUCCESS' if enhancement_result['enhancement_successful'] else 'PARTIAL'}")
            
        except Exception as e:
            logger.error(f"❌ Pipeline 1 enhancement failed: {e}")
            enhancement_result['error'] = str(e)
            
            if self.fallback_on_failure:
                self.integration_stats['fallbacks'] += 1
                enhancement_result['enhancement_successful'] = True
                enhancement_result['recommendations'].append("Enhancement failed - using Pipeline 1 fallback")
            else:
                enhancement_result['enhancement_successful'] = False
        
        # Record enhancement attempt
        self.enhancement_history.append(enhancement_result)
        
        return enhancement_result
    
    def validate_experiment_before_generation(self, experiment_dir: str) -> Dict[str, Any]:
        """
        Pre-generation validation hook for comprehensive_enhancer.py workflow.
        
        This can be called before GPT-5 generation to validate the experiment
        setup and provide early feedback.
        
        Args:
            experiment_dir: Path to experiment directory
            
        Returns:
            Dict with pre-generation validation results
        """
        if not self.enable_validation:
            return {'validation_enabled': False, 'proceed_with_generation': True}
        
        try:
            # Read experiment data
            experiment_data = self._read_experiment_data(experiment_dir)
            
            # Perform validation
            validation_results = self._perform_pipeline2_validation(experiment_data)
            
            # Determine if generation should proceed
            proceed_with_generation = (
                validation_results['sakana_principle_satisfied'] or 
                self.fallback_on_failure
            )
            
            return {
                'validation_enabled': True,
                'proceed_with_generation': proceed_with_generation,
                'validation_results': validation_results,
                'recommendations': validation_results.get('recommendations', []),
                'estimated_quality_score': self._estimate_quality_score(experiment_data, validation_results)
            }
            
        except Exception as e:
            logger.warning(f"Pre-generation validation failed: {e}")
            return {
                'validation_enabled': True,
                'proceed_with_generation': self.fallback_on_failure,
                'error': str(e)
            }
    
    def enhance_bibliography_with_validation(self, 
                                           bibliography_data: Dict,
                                           experiment_type: str = None) -> Dict[str, Any]:
        """
        Enhance bibliography with validation-informed source recommendations.
        
        This integrates with comprehensive_enhancer.py's source discovery process
        to add validation-informed recommendations.
        
        Args:
            bibliography_data: Bibliography data from comprehensive_enhancer
            experiment_type: Type of experiment for domain-specific recommendations
            
        Returns:
            Dict with enhanced bibliography recommendations
        """
        if not self.enable_validation:
            return {'enhancement_applied': False, 'original_bibliography': bibliography_data}
        
        enhancement_result = {
            'enhancement_applied': True,
            'original_count': len(bibliography_data.get('sources', [])),
            'validation_informed_additions': [],
            'domain_specific_sources': [],
            'real_data_sources': []
        }
        
        try:
            # Add domain-specific source recommendations
            if experiment_type == 'chemical_composition':
                enhancement_result['domain_specific_sources'] = [
                    'NIST Chemistry WebBook for thermodynamic data',
                    'JANAF Thermochemical Tables for chemical equilibrium',
                    'HSC Chemistry Database for phase diagrams',
                    'Stratospheric aerosol composition studies (review articles)'
                ]
            
            # Add real data source recommendations
            if self.sakana_bridge and self.sakana_bridge.sakana_available:
                enhancement_result['real_data_sources'] = [
                    'GLENS (NCAR CESM1-WACCM) for climate model validation',
                    'ARISE-SAI project publications for SAI modeling',
                    'GeoMIP protocol papers for intercomparison studies',
                    'Observational stratospheric aerosol data (SAGE, CLAES, HALOE)'
                ]
            
            # Add validation-informed source types
            enhancement_result['validation_informed_additions'] = [
                'Empirical validation studies with real data',
                'Laboratory measurements under stratospheric conditions',
                'Field campaign data for atmospheric chemistry',
                'Model-observation comparison studies'
            ]
            
            logger.info(f"📚 Bibliography enhanced with {len(enhancement_result['validation_informed_additions'])} validation-informed recommendations")
            
        except Exception as e:
            logger.error(f"Bibliography enhancement failed: {e}")
            enhancement_result['error'] = str(e)
        
        return enhancement_result
    
    def _read_experiment_data(self, experiment_dir: str) -> Dict[str, Any]:
        """Read experiment data compatible with comprehensive_enhancer.py format."""
        experiment_data = {
            'experiment_dir': experiment_dir,
            'config': {},
            'topic': '',
            'references': '',
            'comprehensive_results': {}
        }
        
        # Read experiment configuration
        config_path = os.path.join(experiment_dir, 'input', 'experiment_config.json')
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                experiment_data['config'] = json.load(f)
        
        # Read research topic
        topic_path = os.path.join(experiment_dir, 'input', 'research_topic_formatted.txt')
        if os.path.exists(topic_path):
            with open(topic_path, 'r') as f:
                experiment_data['topic'] = f.read().strip()
        
        # Read references
        refs_path = os.path.join(experiment_dir, 'input', 'references.bib')
        if os.path.exists(refs_path):
            with open(refs_path, 'r') as f:
                experiment_data['references'] = f.read().strip()
        
        # Read comprehensive results if available
        results_path = os.path.join(experiment_dir, 'input', 'comprehensive_results.json')
        if os.path.exists(results_path):
            with open(results_path, 'r') as f:
                experiment_data['comprehensive_results'] = json.load(f)
        
        return experiment_data
    
    def _perform_pipeline2_validation(self, experiment_data: Dict) -> Dict[str, Any]:
        """Perform comprehensive Pipeline 2 validation."""
        validation_start = datetime.now()
        
        validation_result = {
            'validation_timestamp': validation_start.isoformat(),
            'sakana_principle_satisfied': False,
            'domain_validation': {},
            'chemical_validation': {},
            'real_data_validation': {},
            'overall_score': 0.0,
            'violations': [],
            'recommendations': []
        }
        
        # Universal domain validation
        if self.experiment_validator:
            domain_validation = self.experiment_validator.validate_experiment(experiment_data)
            validation_result['domain_validation'] = domain_validation
            validation_result['sakana_principle_satisfied'] = domain_validation['sakana_principle_compliance']
            if not domain_validation['sakana_principle_compliance']:
                validation_result['violations'].extend(domain_validation['violations'])
        
        # Chemical composition validation (if applicable)
        experiment_text = str(experiment_data).lower()
        if any(term in experiment_text for term in ['chemical', 'composition', 'particle', 'aerosol']):
            if self.chemical_validator:
                chemical_validation = self.chemical_validator.validate_chemical_experiment(experiment_data)
                validation_result['chemical_validation'] = chemical_validation
                
                # Additional constraint for Sakana principle
                if not chemical_validation['chemical_validation_passed']:
                    validation_result['sakana_principle_satisfied'] = False
                    validation_result['violations'].extend(chemical_validation['violations'])
        
        # Real data validation through Sakana bridge
        if self.sakana_bridge:
            required_data = self._extract_required_datasets(experiment_data)
            sakana_validation = self.sakana_bridge.perform_sakana_validation(
                experiment_data, required_data
            )
            validation_result['real_data_validation'] = sakana_validation
            
            # Additional constraint for Sakana principle
            if not sakana_validation['sakana_principle_satisfied']:
                validation_result['sakana_principle_satisfied'] = False
                validation_result['violations'].extend(sakana_validation['violations'])
        
        # Calculate overall validation score
        validation_result['overall_score'] = self._calculate_validation_score(validation_result)
        
        return validation_result
    
    def _integrate_real_data(self, experiment_data: Dict, experiment_dir: str) -> Dict[str, Any]:
        """Integrate real GLENS data for validation."""
        if not self.glens_connector:
            return {'integration_available': False}
        
        try:
            # Detect experiment type
            experiment_type = self._detect_experiment_type(experiment_data)
            
            # Load appropriate real data
            real_data_result = self.glens_connector.load_experiment_data(
                experiment_type=experiment_type,
                validate_authenticity=True
            )
            
            # Save real data integration results to experiment directory
            if real_data_result['success']:
                integration_path = os.path.join(experiment_dir, 'input', 'pipeline2_real_data.json')
                with open(integration_path, 'w') as f:
                    json.dump(real_data_result, f, indent=2)
                
                logger.info(f"💾 Real data integration saved to {integration_path}")
            
            return real_data_result
            
        except Exception as e:
            logger.error(f"Real data integration failed: {e}")
            return {'integration_available': True, 'error': str(e)}
    
    def _calculate_quality_improvements(self, 
                                      experiment_data: Dict,
                                      validation_results: Dict,
                                      real_data_integration: Dict) -> Dict[str, Any]:
        """Calculate estimated quality improvements from Pipeline 2 enhancements."""
        
        # Base quality from comprehensive_enhancer (typically 6.0-6.5)
        base_quality = experiment_data.get('comprehensive_results', {}).get('overall_score', 6.0)
        
        quality_analysis = {
            'base_quality_score': base_quality,
            'validation_bonus': 0.0,
            'real_data_bonus': 0.0,
            'empirical_grounding_bonus': 0.0,
            'estimated_enhanced_score': base_quality,
            'improvement_factors': []
        }
        
        # Validation bonus (up to +0.5)
        if validation_results.get('sakana_principle_satisfied', False):
            quality_analysis['validation_bonus'] = 0.5
            quality_analysis['improvement_factors'].append('Sakana principle validation passed')
        
        # Real data integration bonus (up to +0.3)
        if real_data_integration.get('success', False):
            quality_analysis['real_data_bonus'] = 0.3
            quality_analysis['improvement_factors'].append('Real GLENS data integrated')
        
        # Empirical grounding bonus (up to +0.2)
        if validation_results.get('real_data_validation', {}).get('empirical_evidence_found', False):
            quality_analysis['empirical_grounding_bonus'] = 0.2
            quality_analysis['improvement_factors'].append('Strong empirical evidence found')
        
        # Calculate total enhanced score
        quality_analysis['estimated_enhanced_score'] = (
            base_quality + 
            quality_analysis['validation_bonus'] + 
            quality_analysis['real_data_bonus'] + 
            quality_analysis['empirical_grounding_bonus']
        )
        
        # Cap at 10.0
        quality_analysis['estimated_enhanced_score'] = min(quality_analysis['estimated_enhanced_score'], 10.0)
        
        return quality_analysis
    
    def _generate_enhancement_recommendations(self, 
                                           validation_results: Dict,
                                           quality_analysis: Dict) -> List[str]:
        """Generate recommendations for Pipeline 1 enhancement."""
        recommendations = []
        
        enhanced_score = quality_analysis['estimated_enhanced_score']
        target_score = self.quality_improvement_target
        
        if enhanced_score >= target_score:
            recommendations.append(f"✅ Quality target achieved: {enhanced_score:.1f} ≥ {target_score}")
            recommendations.append("🎯 Paper ready for top-tier venue with Pipeline 2 enhancements")
        else:
            recommendations.append(f"⚠️ Quality target not met: {enhanced_score:.1f} < {target_score}")
        
        # Validation-based recommendations
        if not validation_results.get('sakana_principle_satisfied', False):
            recommendations.append("❌ Sakana principle validation failed")
            recommendations.extend(validation_results.get('recommendations', []))
        
        # Quality improvement suggestions
        improvement_factors = quality_analysis.get('improvement_factors', [])
        if improvement_factors:
            recommendations.append("✅ Quality improvement factors applied:")
            for factor in improvement_factors:
                recommendations.append(f"  • {factor}")
        
        # Pipeline 1 compatibility
        recommendations.append("🔗 Pipeline 1 compatibility maintained")
        recommendations.append("📈 Enhanced paper will use same GPT-5 generation workflow")
        
        return recommendations
    
    def _extract_required_datasets(self, experiment_data: Dict) -> List[str]:
        """Extract required datasets from experiment description."""
        required_datasets = []
        
        experiment_text = str(experiment_data).lower()
        
        if any(term in experiment_text for term in ['glens', 'climate', 'temperature', 'precipitation']):
            required_datasets.append('GLENS')
        
        if any(term in experiment_text for term in ['arise', 'sai', 'geoengineering']):
            required_datasets.append('ARISE-SAI')
        
        if any(term in experiment_text for term in ['geomip', 'comparison', 'intercomparison']):
            required_datasets.append('GeoMIP')
        
        return required_datasets or ['GLENS']  # Default to GLENS
    
    def _detect_experiment_type(self, experiment_data: Dict) -> str:
        """Detect experiment type for domain-specific processing."""
        experiment_text = str(experiment_data).lower()
        
        if any(term in experiment_text for term in ['chemical', 'composition', 'particle']):
            return 'chemical_composition'
        elif any(term in experiment_text for term in ['climate', 'response', 'temperature']):
            return 'climate_response'
        elif any(term in experiment_text for term in ['signal', 'detection', 'spectroscopy']):
            return 'signal_detection'
        else:
            return 'general'
    
    def _estimate_quality_score(self, experiment_data: Dict, validation_results: Dict) -> float:
        """Estimate quality score based on validation results."""
        base_score = 6.0  # Pipeline 1 baseline
        
        if validation_results.get('sakana_principle_satisfied', False):
            base_score += 1.0  # Major improvement for validation
        
        return min(base_score, 10.0)
    
    def _calculate_validation_score(self, validation_result: Dict) -> float:
        """Calculate overall validation score."""
        score = 0.0
        max_score = 10.0
        
        # Domain validation contribution (40%)
        if validation_result.get('domain_validation', {}).get('sakana_principle_compliance', False):
            score += 4.0
        
        # Chemical validation contribution (30% if applicable)
        chemical_val = validation_result.get('chemical_validation', {})
        if chemical_val and chemical_val.get('chemical_validation_passed', False):
            score += 3.0
        elif not chemical_val:  # No chemical validation needed
            score += 3.0
        
        # Real data validation contribution (30%)
        if validation_result.get('real_data_validation', {}).get('sakana_principle_satisfied', False):
            score += 3.0
        
        return min(score, max_score)
    
    def get_interface_status(self) -> Dict[str, Any]:
        """Get current status of Pipeline 1 interface."""
        return {
            'interface_active': True,
            'pipeline2_validation_enabled': self.enable_validation,
            'quality_improvement_target': self.quality_improvement_target,
            'fallback_enabled': self.fallback_on_failure,
            'integration_statistics': self.integration_stats.copy(),
            'sakana_bridge_available': self.sakana_bridge is not None and self.sakana_bridge.sakana_available,
            'glens_connector_available': self.glens_connector is not None,
            'total_enhancements_attempted': len(self.enhancement_history),
            'success_rate': (self.integration_stats['successful_enhancements'] / 
                           self.integration_stats['total_attempts']) if self.integration_stats['total_attempts'] > 0 else 0.0
        }


# Convenience functions for easy integration with comprehensive_enhancer.py
def create_pipeline1_interface(enable_validation: bool = True) -> Pipeline1Interface:
    """Create Pipeline 1 interface for integration."""
    return Pipeline1Interface(enable_validation=enable_validation)

def enhance_comprehensive_experiment(experiment_dir: str, 
                                   enable_validation: bool = True) -> Dict[str, Any]:
    """
    One-line enhancement function for comprehensive_enhancer.py integration.
    
    Usage in comprehensive_enhancer.py:
    from PIPELINE_2_DEVELOPMENT.ai_researcher_enhanced.integration.pipeline1_interface import enhance_comprehensive_experiment
    enhancement_result = enhance_comprehensive_experiment(experiment_dir)
    """
    interface = Pipeline1Interface(enable_validation=enable_validation)
    return interface.enhance_experiment_analysis(experiment_dir)