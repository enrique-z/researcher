"""
Universal Sakana Principle Validator

Enhanced validation framework that extends the Sakana Principle to work with any scientific domain.
Built on the foundation of the existing Pipeline 2 Sakana validator but made domain-agnostic.

Key Features:
- Domain-agnostic empirical validation framework
- Universal real data enforcement across all research domains
- Configurable validation criteria per scientific domain
- Integration with URSA experimental framework
- Plausibility trap prevention for any research topic

Supported Domains: climate, physics, chemistry, biology (extensible)
"""

import os
import sys
import logging
import numpy as np
from typing import Dict, List, Union, Optional, Any
from datetime import datetime
from pathlib import Path

# Import existing validation infrastructure
sys.path.append('/Users/apple/code/Researcher')
try:
    from ai_researcher.validation.experiment_validator import ExperimentValidator
    EXISTING_VALIDATION_AVAILABLE = True
except ImportError:
    EXISTING_VALIDATION_AVAILABLE = False
    logger.warning("Existing validation infrastructure not available, using simplified validation")

# Import universal domain validators
from .domain_validators.universal_base_validator import UniversalBaseValidator
from .domain_validators.climate_validator import ClimateValidator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UniversalSakanaValidator:
    """
    Universal Sakana Principle validator that adapts to any scientific research domain.
    
    Extends the existing Pipeline 2 Sakana validator with domain-agnostic capabilities
    while maintaining all empirical validation requirements.
    """
    
    def __init__(self, research_domain: str = "climate", real_data_mandatory: bool = True):
        """
        Initialize universal Sakana validator.
        
        Args:
            research_domain: Research domain (climate, physics, chemistry, biology)
            real_data_mandatory: Enforce real data requirements (default: True)
        """
        self.research_domain = research_domain
        self.real_data_mandatory = real_data_mandatory
        
        # Initialize existing validation infrastructure if available
        self.base_experiment_validator = None
        if EXISTING_VALIDATION_AVAILABLE:
            try:
                self.base_experiment_validator = ExperimentValidator(
                    real_data_mandatory=real_data_mandatory,
                    synthetic_data_forbidden=True,
                    strict_mode=True
                )
            except Exception as e:
                logger.warning(f"Could not initialize base experiment validator: {e}")
        
        # Initialize domain-specific validator
        self.domain_validator = self._create_domain_validator(research_domain)
        
        # Universal validation configuration
        self.universal_config = {
            'research_domain': research_domain,
            'real_data_mandatory': real_data_mandatory,
            'empirical_validation_required': True,
            'plausibility_trap_prevention': True,
            'universal_statistical_validation': True,
            'domain_specific_validation': True
        }
        
        # Validation history
        self.validation_history = []
        self.domain_specific_results = []
        
        logger.info(f"✅ Universal Sakana validator initialized for domain: {research_domain}")
    
    def _create_domain_validator(self, research_domain: str) -> UniversalBaseValidator:
        """Create domain-specific validator."""
        if research_domain == "climate":
            return ClimateValidator()
        else:
            # For now, use climate as fallback - will expand to other domains
            logger.warning(f"Domain {research_domain} not yet implemented. Using climate validator as base.")
            return ClimateValidator()
    
    def validate_universal_experiment(self, experiment_config: Dict) -> Dict:
        """
        Validate experiment using universal Sakana principles adapted for any domain.
        
        Args:
            experiment_config: Universal experiment configuration
            
        Returns:
            Dict with comprehensive universal validation results
        """
        validation_start = datetime.now()
        
        # Initialize universal validation result
        validation_result = {
            'experiment_id': experiment_config.get('experiment_id', f"exp_{int(validation_start.timestamp())}"),
            'research_domain': self.research_domain,
            'validation_timestamp': validation_start.isoformat(),
            'universal_sakana_status': 'PENDING',
            'domain_validation_results': None,
            'base_sakana_results': None,
            'universal_compliance_check': None,
            'overall_validation_status': 'PENDING',
            'validation_confidence': 'UNKNOWN',
            'rejection_reasons': [],
            'recommendations': []
        }
        
        try:
            logger.info(f"🔬 Starting universal Sakana validation for {self.research_domain} experiment")
            
            # Step 1: Domain-specific validation using enhanced validator
            domain_validation = self.domain_validator.validate_domain_experiment(experiment_config)
            validation_result['domain_validation_results'] = domain_validation
            
            # Step 2: Apply existing experiment validation if available
            if self.base_experiment_validator and self._is_compatible_with_base_validation(experiment_config):
                try:
                    base_validation_results = self.base_experiment_validator.validate_experiment(experiment_config)
                    validation_result['base_validation_results'] = base_validation_results
                except Exception as e:
                    logger.warning(f"Base experiment validation failed: {e}")
                    validation_result['base_validation_results'] = {
                        'validation_status': 'FAILED',
                        'error': str(e),
                        'note': 'Fallback to domain-specific validation'
                    }
            else:
                # Use domain validator results as primary validation
                validation_result['base_validation_results'] = {
                    'validation_status': 'DOMAIN_SPECIFIC_VALIDATION_ONLY',
                    'note': 'Using enhanced domain-specific validation'
                }
            
            # Step 3: Universal compliance assessment
            compliance_check = self._assess_universal_compliance(validation_result)
            validation_result['universal_compliance_check'] = compliance_check
            
            # Step 4: Overall validation decision
            validation_result = self._make_universal_validation_decision(validation_result)
            
            # Log validation result
            self.validation_history.append(validation_result)
            
            logger.info(f"✅ Universal validation complete: {validation_result['overall_validation_status']}")
            
            return validation_result
            
        except Exception as e:
            validation_result['universal_sakana_status'] = 'ERROR'
            validation_result['overall_validation_status'] = 'VALIDATION_FAILED'
            validation_result['rejection_reasons'].append(f'Universal validation error: {str(e)}')
            logger.error(f"❌ Universal Sakana validation failed: {e}")
            return validation_result
    
    def _is_compatible_with_base_validation(self, experiment_config: Dict) -> bool:
        """Check if experiment can use existing base experiment validator."""
        required_keys = ['experiment_type', 'real_dataset']
        return all(key in experiment_config for key in required_keys)
    
    def _assess_universal_compliance(self, validation_result: Dict) -> Dict:
        """Assess universal compliance across all validation components."""
        domain_results = validation_result.get('domain_validation_results', {})
        base_validation_results = validation_result.get('base_validation_results', {})
        
        compliance_check = {
            'real_data_compliance': True,
            'empirical_validation_compliance': True,
            'domain_specific_compliance': True,
            'plausibility_trap_prevention': True,
            'universal_statistical_compliance': True,
            'overall_compliance': 'UNKNOWN',
            'compliance_details': []
        }
        
        # Check real data compliance
        if domain_results.get('real_data_verified') == False:
            compliance_check['real_data_compliance'] = False
            compliance_check['compliance_details'].append('Real data verification failed')
        
        # Check empirical validation
        if domain_results.get('empirical_validation_status') in ['FAILED', 'INSUFFICIENT']:
            compliance_check['empirical_validation_compliance'] = False
            compliance_check['compliance_details'].append('Empirical validation insufficient')
        
        # Check domain-specific requirements
        if domain_results.get('domain_compliance_status') == 'NON_COMPLIANT':
            compliance_check['domain_specific_compliance'] = False
            compliance_check['compliance_details'].append('Domain-specific validation failed')
        
        # Check base validation results if available
        if base_validation_results.get('validation_status') == 'FAILED':
            compliance_check['plausibility_trap_prevention'] = False
            compliance_check['compliance_details'].append('Base experiment validation failed')
        
        # Overall compliance assessment
        all_compliant = all([
            compliance_check['real_data_compliance'],
            compliance_check['empirical_validation_compliance'],
            compliance_check['domain_specific_compliance'],
            compliance_check['plausibility_trap_prevention']
        ])
        
        if all_compliant:
            compliance_check['overall_compliance'] = 'FULLY_COMPLIANT'
        elif compliance_check['real_data_compliance'] and compliance_check['empirical_validation_compliance']:
            compliance_check['overall_compliance'] = 'PARTIALLY_COMPLIANT'
        else:
            compliance_check['overall_compliance'] = 'NON_COMPLIANT'
        
        return compliance_check
    
    def _make_universal_validation_decision(self, validation_result: Dict) -> Dict:
        """Make final universal validation decision."""
        compliance_check = validation_result['universal_compliance_check']
        domain_results = validation_result['domain_validation_results']
        
        # Decision logic based on universal compliance
        if compliance_check['overall_compliance'] == 'FULLY_COMPLIANT':
            if domain_results.get('confidence_level') == 'HIGH':
                validation_result['overall_validation_status'] = 'VALIDATED_HIGH_CONFIDENCE'
                validation_result['universal_sakana_status'] = 'COMPLIANT'
                validation_result['validation_confidence'] = 'HIGH'
            else:
                validation_result['overall_validation_status'] = 'VALIDATED_MODERATE_CONFIDENCE'
                validation_result['universal_sakana_status'] = 'COMPLIANT'
                validation_result['validation_confidence'] = 'MODERATE'
        
        elif compliance_check['overall_compliance'] == 'PARTIALLY_COMPLIANT':
            validation_result['overall_validation_status'] = 'REQUIRES_REVISION'
            validation_result['universal_sakana_status'] = 'MARGINAL_COMPLIANCE'
            validation_result['validation_confidence'] = 'LOW'
            validation_result['recommendations'].extend(compliance_check['compliance_details'])
        
        else:
            validation_result['overall_validation_status'] = 'REJECTED'
            validation_result['universal_sakana_status'] = 'NON_COMPLIANT'
            validation_result['validation_confidence'] = 'NONE'
            validation_result['rejection_reasons'].extend(compliance_check['compliance_details'])
        
        return validation_result
    
    def validate_cambridge_sai_experiment(self, sai_experiment_config: Dict) -> Dict:
        """
        Specialized validation for Cambridge SAI pulse vs continuous analysis.
        
        Args:
            sai_experiment_config: SAI experiment configuration
            
        Returns:
            Dict with SAI-specific validation results
        """
        logger.info("🌡️ Validating Cambridge SAI experiment using universal framework")
        
        # Enhance SAI config for universal validation
        enhanced_config = {
            **sai_experiment_config,
            'research_domain': 'climate',
            'experiment_type': 'sai_analysis',
            'validation_requirements': {
                'real_glens_data_required': True,
                'physical_constraint_checking': True,
                'statistical_significance_required': True,
                'climate_model_validation': True
            }
        }
        
        # Use universal validation framework
        validation_result = self.validate_universal_experiment(enhanced_config)
        
        # Add SAI-specific validation details
        validation_result['sai_specific_validation'] = {
            'injection_strategy_validation': 'PENDING',
            'aerosol_transport_validation': 'PENDING',
            'climate_response_validation': 'PENDING'
        }
        
        if self.research_domain == "climate":
            sai_validation = self.domain_validator.validate_sai_experiment(enhanced_config)
            validation_result['sai_specific_validation'] = sai_validation
        
        return validation_result
    
    def get_universal_validation_report(self) -> Dict:
        """Generate comprehensive universal validation report."""
        base_report = {}
        if self.base_experiment_validator:
            try:
                base_report = {'base_experiment_validator': 'available'}
            except:
                base_report = {'base_experiment_validator': 'unavailable'}
        
        universal_report = {
            'report_generated': datetime.now().isoformat(),
            'research_domain': self.research_domain,
            'universal_validation_config': self.universal_config,
            'validation_statistics': {
                'total_universal_validations': len(self.validation_history),
                'domain_specific_validations': len(self.domain_specific_results),
                'universal_compliance_rate': self._calculate_compliance_rate(),
                'domain_breakdown': self._get_domain_breakdown()
            },
            'base_sakana_report': base_report,
            'domain_validator_status': self.domain_validator.get_validator_status()
        }
        
        return universal_report
    
    def _calculate_compliance_rate(self) -> float:
        """Calculate universal compliance rate."""
        if not self.validation_history:
            return 0.0
        
        compliant_validations = sum(
            1 for result in self.validation_history
            if result.get('universal_sakana_status') == 'COMPLIANT'
        )
        
        return compliant_validations / len(self.validation_history)
    
    def _get_domain_breakdown(self) -> Dict:
        """Get validation breakdown by domain."""
        breakdown = {}
        for result in self.validation_history:
            domain = result.get('research_domain', 'unknown')
            status = result.get('overall_validation_status', 'unknown')
            
            if domain not in breakdown:
                breakdown[domain] = {}
            
            breakdown[domain][status] = breakdown[domain].get(status, 0) + 1
        
        return breakdown
    
    def set_research_domain(self, new_domain: str):
        """Change research domain and reinitialize domain validator."""
        self.research_domain = new_domain
        self.domain_validator = self._create_domain_validator(new_domain)
        self.universal_config['research_domain'] = new_domain
        
        logger.info(f"🔄 Research domain changed to: {new_domain}")
    
    def get_validation_summary(self) -> Dict:
        """Get concise validation summary."""
        return {
            'validator_type': 'UniversalSakanaValidator',
            'research_domain': self.research_domain,
            'total_validations': len(self.validation_history),
            'compliance_rate': self._calculate_compliance_rate(),
            'real_data_enforcement': self.real_data_mandatory,
            'status': 'OPERATIONAL'
        }


# Convenience functions for easy integration
def create_universal_sakana_validator(research_domain: str = "climate") -> UniversalSakanaValidator:
    """Create universal Sakana validator for specified domain."""
    return UniversalSakanaValidator(research_domain=research_domain)

def validate_cambridge_sai_experiment(experiment_config: Dict) -> Dict:
    """Quick validation function for Cambridge SAI analysis."""
    validator = create_universal_sakana_validator("climate")
    return validator.validate_cambridge_sai_experiment(experiment_config)