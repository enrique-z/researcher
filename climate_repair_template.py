#!/usr/bin/env python3
"""
Climate Repair Template - Domain-Flexible Research Framework

This module provides an abstract base class for domain-flexible climate repair research
that can be easily forked and adapted for different scientific domains while maintaining
the complete 11-tool integration architecture.

DESIGN PHILOSOPHY:
- Domain-agnostic core architecture
- Pluggable validation systems
- Easy inheritance for new domains
- Complete tool integration maintained
- Flexible hypothesis and validation frameworks

USAGE PATTERN:
1. Inherit from ClimateRepairTemplate
2. Implement abstract methods for domain specifics
3. Configure Reality Check Engine for domain
4. Define domain-specific validation criteria
5. Test with domain-specific hypotheses

EXAMPLE DOMAINS:
- Stratospheric Aerosol Injection (SAI)
- Marine Cloud Brightening (MCB)  
- Direct Air Capture (DAC)
- Ocean Alkalinization (OA)
- Solar Radiation Management (SRM)
- Ecosystem Restoration (ER)
"""

import os
import sys
import json
import time
import logging
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

# Import universal pipeline base
from execute_qbo_sai_experiment import UniversalExperimentPipeline

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ClimateRepairTemplate(UniversalExperimentPipeline, ABC):
    """
    Abstract base class for domain-flexible climate repair research.
    
    This template provides the foundation for any climate repair domain while
    maintaining complete 11-tool integration and universal pipeline architecture.
    """
    
    def __init__(self, 
                 repair_domain: str,
                 experiment_name: str,
                 domain_config: Dict[str, Any] = None,
                 **kwargs):
        """
        Initialize climate repair template with domain-specific configuration.
        
        Args:
            repair_domain: Specific climate repair domain (e.g., 'sai', 'mcb', 'dac')
            experiment_name: Name for this specific experiment
            domain_config: Domain-specific configuration parameters
            **kwargs: Additional configuration passed to parent
        """
        
        # Store domain-specific information
        self.repair_domain = repair_domain
        self.domain_config = domain_config or {}
        
        # Configure universal pipeline for climate science
        super().__init__(
            experiment_name=experiment_name,
            research_domain="climate_science",
            experiment_config={
                'domain': 'climate_science',
                'repair_type': repair_domain,
                'repair_config': self.domain_config,
                'validation_level': 'comprehensive',
                'template_version': '1.0'
            },
            **kwargs
        )
        
        # Initialize domain-specific components
        self.domain_specifics = self.configure_domain_specifics()
        self.reality_checks = self.setup_reality_checks()
        self.validation_criteria = self.define_validation_criteria()
        
        logger.info(f"🌍 Climate Repair Template initialized: {repair_domain}")
        logger.info(f"🔧 Domain config: {len(self.domain_config)} parameters")
        logger.info(f"✅ Template ready for {repair_domain.upper()} research")
    
    @abstractmethod
    def configure_domain_specifics(self) -> Dict[str, Any]:
        """
        Configure domain-specific parameters and settings.
        
        This method must be implemented by each domain to define:
        - Intervention mechanisms
        - Target parameters (cooling, pH, CO2, etc.)
        - Deployment methods
        - Measurement approaches
        - Success criteria
        
        Returns:
            Dictionary with domain-specific configuration
        """
        pass
    
    @abstractmethod
    def setup_reality_checks(self) -> Dict[str, Any]:
        """
        Configure domain-specific Reality Check Engine validation.
        
        Each domain has different physical constraints and feasibility limits:
        - SAI: Injection altitude, aerosol properties, atmospheric chemistry
        - MCB: Droplet size, cloud microphysics, marine environment
        - DAC: Energy requirements, sorbent materials, scaling limits
        - OA: Ocean chemistry, ecosystem impacts, alkalinity sources
        
        Returns:
            Dictionary with reality check configuration for this domain
        """
        pass
    
    @abstractmethod
    def define_validation_criteria(self) -> Dict[str, Any]:
        """
        Define domain-specific validation criteria and success metrics.
        
        Each domain requires different validation approaches:
        - Effectiveness measures
        - Side effect assessments  
        - Risk evaluation criteria
        - Deployment feasibility
        - Cost-benefit thresholds
        
        Returns:
            Dictionary with validation criteria for this domain
        """
        pass
    
    @abstractmethod
    def generate_domain_hypothesis_template(self) -> str:
        """
        Generate a template hypothesis for this domain.
        
        Provides a starting point for hypothesis generation that includes
        domain-specific terminology, mechanisms, and expected outcomes.
        
        Returns:
            Template hypothesis string for this domain
        """
        pass
    
    def validate_domain_hypothesis(self, hypothesis: str) -> Dict[str, Any]:
        """
        Validate hypothesis using domain-specific criteria.
        
        This method combines universal validation (FAISS + Reality Check Engine)
        with domain-specific validation criteria.
        
        Args:
            hypothesis: Research hypothesis to validate
            
        Returns:
            Comprehensive validation results including domain-specific assessment
        """
        logger.info(f"🔍 Validating {self.repair_domain.upper()} hypothesis...")
        
        try:
            # Universal validation using FAISS and Reality Check Engine
            universal_assessment = self.assess_research_idea(hypothesis)
            
            # Domain-specific validation
            domain_assessment = self._assess_domain_specifics(hypothesis)
            
            # Combined assessment
            combined_results = {
                'hypothesis': hypothesis,
                'repair_domain': self.repair_domain,
                'universal_assessment': universal_assessment,
                'domain_assessment': domain_assessment,
                'validation_timestamp': datetime.now().isoformat()
            }
            
            # Calculate combined score
            universal_score = universal_assessment.get('combined_assessment', {}).get('combined_score', 0)
            domain_score = domain_assessment.get('domain_score', 0)
            
            # Weighted combination: 70% universal, 30% domain-specific
            final_score = (universal_score * 0.7) + (domain_score * 0.3)
            
            # Final recommendation
            if final_score > 0.8:
                recommendation = "HIGHLY_RECOMMENDED"
            elif final_score > 0.65:
                recommendation = "RECOMMENDED"
            elif final_score > 0.5:
                recommendation = "CONDITIONAL"
            else:
                recommendation = "NOT_RECOMMENDED"
            
            combined_results['final_assessment'] = {
                'recommendation': recommendation,
                'final_score': round(final_score, 3),
                'universal_contribution': round(universal_score * 0.7, 3),
                'domain_contribution': round(domain_score * 0.3, 3),
                'confidence': 'HIGH' if final_score > 0.75 or final_score < 0.3 else 'MODERATE'
            }
            
            logger.info(f"✅ {self.repair_domain.upper()} validation complete: {recommendation} ({final_score:.3f})")
            return combined_results
            
        except Exception as e:
            logger.error(f"❌ {self.repair_domain.upper()} validation failed: {e}")
            return {
                'error': str(e),
                'hypothesis': hypothesis,
                'repair_domain': self.repair_domain,
                'status': 'validation_failed'
            }
    
    def _assess_domain_specifics(self, hypothesis: str) -> Dict[str, Any]:
        """
        Internal method to assess domain-specific aspects of hypothesis.
        
        Args:
            hypothesis: Research hypothesis to assess
            
        Returns:
            Domain-specific assessment results
        """
        
        # Extract domain-specific criteria
        criteria = self.validation_criteria
        specifics = self.domain_specifics
        
        # Initialize assessment
        domain_assessment = {
            'intervention_feasibility': 0.0,
            'mechanism_validity': 0.0,
            'deployment_practicality': 0.0,
            'risk_profile': 0.0,
            'effectiveness_potential': 0.0
        }
        
        # Assess intervention feasibility
        domain_assessment['intervention_feasibility'] = self._assess_intervention_feasibility(
            hypothesis, specifics.get('intervention_mechanisms', {})
        )
        
        # Assess mechanism validity  
        domain_assessment['mechanism_validity'] = self._assess_mechanism_validity(
            hypothesis, specifics.get('target_parameters', {})
        )
        
        # Assess deployment practicality
        domain_assessment['deployment_practicality'] = self._assess_deployment_practicality(
            hypothesis, specifics.get('deployment_methods', {})
        )
        
        # Assess risk profile
        domain_assessment['risk_profile'] = self._assess_risk_profile(
            hypothesis, criteria.get('risk_thresholds', {})
        )
        
        # Assess effectiveness potential
        domain_assessment['effectiveness_potential'] = self._assess_effectiveness_potential(
            hypothesis, criteria.get('effectiveness_measures', {})
        )
        
        # Calculate overall domain score
        scores = list(domain_assessment.values())
        domain_score = sum(scores) / len(scores) if scores else 0.0
        
        return {
            'domain_aspects': domain_assessment,
            'domain_score': round(domain_score, 3),
            'domain_strengths': [k for k, v in domain_assessment.items() if v > 0.7],
            'domain_concerns': [k for k, v in domain_assessment.items() if v < 0.4],
            'domain_validation': f"{self.repair_domain}_specific_assessment"
        }
    
    def _assess_intervention_feasibility(self, hypothesis: str, mechanisms: Dict[str, Any]) -> float:
        """Assess feasibility of proposed intervention mechanism."""
        # Basic keyword-based assessment - can be overridden by domains
        score = 0.6  # Default moderate score
        
        hypothesis_lower = hypothesis.lower()
        
        # Check for mechanism keywords
        if any(mech.lower() in hypothesis_lower for mech in mechanisms.get('primary', [])):
            score += 0.2
        
        # Check for implementation keywords
        if any(impl.lower() in hypothesis_lower for impl in mechanisms.get('implementation', [])):
            score += 0.1
        
        # Check for constraint keywords (reduce score)
        if any(const.lower() in hypothesis_lower for const in mechanisms.get('constraints', [])):
            score -= 0.1
        
        return max(0.0, min(1.0, score))
    
    def _assess_mechanism_validity(self, hypothesis: str, targets: Dict[str, Any]) -> float:
        """Assess validity of proposed mechanism for target parameters."""
        score = 0.6  # Default moderate score
        
        hypothesis_lower = hypothesis.lower()
        
        # Check for target parameter mentions
        if any(target.lower() in hypothesis_lower for target in targets.get('primary', [])):
            score += 0.2
        
        # Check for quantitative mentions
        import re
        if re.search(r'\d+\.?\d*\s*(°C|K|ppm|%|m|km)', hypothesis):
            score += 0.1
        
        return max(0.0, min(1.0, score))
    
    def _assess_deployment_practicality(self, hypothesis: str, methods: Dict[str, Any]) -> float:
        """Assess practicality of proposed deployment methods."""
        score = 0.6  # Default moderate score
        
        hypothesis_lower = hypothesis.lower()
        
        # Check for deployment method keywords
        if any(method.lower() in hypothesis_lower for method in methods.get('approaches', [])):
            score += 0.2
        
        # Check for scale considerations
        scale_keywords = ['global', 'regional', 'local', 'pilot', 'large-scale', 'small-scale']
        if any(scale in hypothesis_lower for scale in scale_keywords):
            score += 0.1
        
        return max(0.0, min(1.0, score))
    
    def _assess_risk_profile(self, hypothesis: str, thresholds: Dict[str, Any]) -> float:
        """Assess risk profile against domain-specific thresholds."""
        score = 0.7  # Default moderate-high score (assumes reasonable risk)
        
        hypothesis_lower = hypothesis.lower()
        
        # Check for risk mitigation mentions
        risk_keywords = ['risk', 'safety', 'mitigation', 'monitoring', 'reversible']
        if any(keyword in hypothesis_lower for keyword in risk_keywords):
            score += 0.2
        
        # Check for concerning keywords (reduce score)
        concern_keywords = ['irreversible', 'catastrophic', 'uncontrolled', 'permanent']
        if any(keyword in hypothesis_lower for keyword in concern_keywords):
            score -= 0.3
        
        return max(0.0, min(1.0, score))
    
    def _assess_effectiveness_potential(self, hypothesis: str, measures: Dict[str, Any]) -> float:
        """Assess potential effectiveness against domain-specific measures."""
        score = 0.6  # Default moderate score
        
        hypothesis_lower = hypothesis.lower()
        
        # Check for effectiveness keywords
        effectiveness_keywords = ['effective', 'efficient', 'significant', 'substantial', 'measurable']
        if any(keyword in hypothesis_lower for keyword in effectiveness_keywords):
            score += 0.2
        
        # Check for quantitative effectiveness claims
        import re
        if re.search(r'(reduce|increase|decrease)\s+\w+\s+by\s+\d+', hypothesis_lower):
            score += 0.1
        
        return max(0.0, min(1.0, score))
    
    def execute_domain_pipeline(self, hypothesis: str = None) -> Dict[str, Any]:
        """
        Execute complete pipeline for this domain with optional custom hypothesis.
        
        Args:
            hypothesis: Optional custom hypothesis (uses domain template if None)
            
        Returns:
            Complete pipeline execution results
        """
        
        if hypothesis is None:
            hypothesis = self.generate_domain_hypothesis_template()
        
        logger.info(f"🚀 Executing {self.repair_domain.upper()} pipeline...")
        logger.info(f"💡 Hypothesis: {hypothesis[:100]}...")
        
        try:
            # Phase 0: Domain-specific hypothesis validation
            logger.info("🔍 Phase 0: Domain Hypothesis Validation")
            validation_results = self.validate_domain_hypothesis(hypothesis)
            
            # Check if we should proceed
            final_score = validation_results.get('final_assessment', {}).get('final_score', 0)
            if final_score < 0.4:
                logger.warning(f"⚠️ Low validation score ({final_score:.3f}), proceeding with caution")
            
            # Execute universal pipeline
            logger.info("🔄 Executing Universal 11-Tool Pipeline...")
            pipeline_results = self.execute_complete_pipeline()
            
            # Combine results
            complete_results = {
                'repair_domain': self.repair_domain,
                'hypothesis': hypothesis,
                'domain_validation': validation_results,
                'pipeline_execution': pipeline_results,
                'execution_timestamp': datetime.now().isoformat(),
                'status': 'completed_successfully'
            }
            
            logger.info(f"✅ {self.repair_domain.upper()} pipeline completed successfully!")
            return complete_results
            
        except Exception as e:
            logger.error(f"❌ {self.repair_domain.upper()} pipeline failed: {e}")
            return {
                'repair_domain': self.repair_domain,
                'hypothesis': hypothesis,
                'error': str(e),
                'status': 'pipeline_failed'
            }
    
    def create_domain_fork_template(self, new_domain: str) -> str:
        """
        Generate template code for creating a new domain implementation.
        
        Args:
            new_domain: Name of the new domain to create
            
        Returns:
            Template code string for new domain implementation
        """
        
        template_code = f'''#!/usr/bin/env python3
"""
{new_domain.upper()} Climate Repair Implementation

Auto-generated template for {new_domain} climate repair research.
Customize the abstract methods below for your specific domain.
"""

from climate_repair_template import ClimateRepairTemplate
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class {new_domain.title().replace('_', '')}ClimateRepair(ClimateRepairTemplate):
    """
    {new_domain.upper()} Climate Repair implementation.
    
    Customize this class for {new_domain} specific research requirements.
    """
    
    def __init__(self, experiment_name: str = "{new_domain}_experiment"):
        """Initialize {new_domain.upper()} climate repair system."""
        
        domain_config = {{
            'intervention_type': '{new_domain}',
            'target_parameter': 'CUSTOMIZE_THIS',  # e.g., 'temperature', 'co2', 'ph'
            'deployment_scale': 'CUSTOMIZE_THIS',  # e.g., 'global', 'regional', 'local'
            'effectiveness_metric': 'CUSTOMIZE_THIS'  # e.g., 'cooling_efficiency', 'co2_removed'
        }}
        
        super().__init__(
            repair_domain="{new_domain}",
            experiment_name=experiment_name,
            domain_config=domain_config
        )
    
    def configure_domain_specifics(self) -> Dict[str, Any]:
        """Configure {new_domain.upper()}-specific parameters."""
        
        return {{
            'intervention_mechanisms': {{
                'primary': ['CUSTOMIZE_THIS'],  # Primary intervention methods
                'implementation': ['CUSTOMIZE_THIS'],  # Implementation approaches
                'constraints': ['CUSTOMIZE_THIS']  # Physical/practical constraints
            }},
            'target_parameters': {{
                'primary': ['CUSTOMIZE_THIS'],  # Main parameters affected
                'secondary': ['CUSTOMIZE_THIS']  # Secondary effects
            }},
            'deployment_methods': {{
                'approaches': ['CUSTOMIZE_THIS'],  # Deployment approaches
                'requirements': ['CUSTOMIZE_THIS']  # Infrastructure requirements
            }}
        }}
    
    def setup_reality_checks(self) -> Dict[str, Any]:
        """Configure {new_domain.upper()}-specific Reality Check Engine validation."""
        
        return {{
            'domain': '{new_domain}',
            'specific_checks': [
                'CUSTOMIZE_THIS',  # Domain-specific physical constraints
                'CUSTOMIZE_THIS',  # Feasibility checks
                'CUSTOMIZE_THIS'   # Safety/risk checks
            ],
            'validation_focus': 'CUSTOMIZE_THIS'  # e.g., 'physical_feasibility', 'environmental_impact'
        }}
    
    def define_validation_criteria(self) -> Dict[str, Any]:
        """Define {new_domain.upper()}-specific validation criteria."""
        
        return {{
            'effectiveness_measures': [
                'CUSTOMIZE_THIS'  # How to measure success
            ],
            'risk_thresholds': {{
                'environmental': 'CUSTOMIZE_THIS',  # Environmental risk limits
                'technical': 'CUSTOMIZE_THIS',      # Technical risk limits
                'social': 'CUSTOMIZE_THIS'          # Social/ethical risk limits
            }},
            'success_criteria': {{
                'minimum_effectiveness': 0.0,  # Minimum effectiveness threshold
                'maximum_risk': 1.0,          # Maximum acceptable risk
                'deployment_feasibility': 0.5  # Deployment feasibility threshold
            }}
        }}
'''
        
        return template_code
    
    def generate_domain_hypothesis_template(self) -> str:
        """Generate template hypothesis for domain research."""
        
        return '''
        CUSTOMIZE THIS HYPOTHESIS TEMPLATE FOR YOUR DOMAIN:
        
        Example: Your domain could [MECHANISM] to [TARGET_EFFECT]
        through [IMPLEMENTATION_METHOD], potentially achieving [QUANTITATIVE_OUTCOME] 
        with [RISK_MITIGATION_APPROACH].
        
        Make sure to include:
        - Specific intervention mechanism
        - Target climate parameter
        - Implementation approach  
        - Quantitative outcomes
        - Risk mitigation strategies
        '''.strip()
    
    def get_domain_status(self) -> Dict[str, Any]:
        """Get comprehensive status of this domain implementation."""
        
        return {
            'repair_domain': self.repair_domain,
            'experiment_name': self.experiment_name,
            'domain_config': self.domain_config,
            'tools_available': {
                'faiss_database': True,  # Always available
                'reality_check_engine': True,  # Always available
                'agent_lightning': hasattr(self, 'AGENT_LIGHTNING_AVAILABLE'),
                'iris': hasattr(self, 'IRIS_AVAILABLE'),
                'guide': hasattr(self, 'GUIDE_AVAILABLE')
            },
            'validation_criteria_defined': bool(self.validation_criteria),
            'reality_checks_configured': bool(self.reality_checks),
            'domain_specifics_configured': bool(self.domain_specifics),
            'template_version': '1.0',
            'ready_for_execution': True
        }

# Base testing function for template validation
def test_climate_repair_template():
    """Test the climate repair template with a dummy implementation."""
    
    class TestDomain(ClimateRepairTemplate):
        """Test implementation of climate repair template."""
        
        def __init__(self):
            super().__init__(
                repair_domain="test_domain",
                experiment_name="template_test",
                domain_config={'test': True}
            )
        
        def configure_domain_specifics(self):
            return {
                'intervention_mechanisms': {
                    'primary': ['test_intervention'],
                    'implementation': ['test_method'],
                    'constraints': ['test_constraint']
                },
                'target_parameters': {
                    'primary': ['temperature'],
                    'secondary': ['precipitation']
                },
                'deployment_methods': {
                    'approaches': ['test_deployment'],
                    'requirements': ['test_infrastructure']
                }
            }
        
        def setup_reality_checks(self):
            return {
                'domain': 'test_domain',
                'specific_checks': ['feasibility', 'safety'],
                'validation_focus': 'comprehensive'
            }
        
        def define_validation_criteria(self):
            return {
                'effectiveness_measures': ['cooling_efficiency'],
                'risk_thresholds': {
                    'environmental': 'low',
                    'technical': 'moderate',
                    'social': 'low'
                },
                'success_criteria': {
                    'minimum_effectiveness': 0.5,
                    'maximum_risk': 0.3,
                    'deployment_feasibility': 0.6
                }
            }
        
        def generate_domain_hypothesis_template(self):
            return "Test domain intervention could reduce global temperature by 1°C through test mechanisms."
    
    # Test the template
    test_domain = TestDomain()
    status = test_domain.get_domain_status()
    print(f"✅ Template test successful: {status['repair_domain']}")
    return test_domain

if __name__ == "__main__":
    print("🧪 Testing Climate Repair Template...")
    test_domain = test_climate_repair_template()
    print("✅ Climate Repair Template ready for domain implementations!")