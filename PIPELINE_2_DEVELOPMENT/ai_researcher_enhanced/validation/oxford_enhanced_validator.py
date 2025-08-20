"""
Oxford-Enhanced Validator for Pipeline 2

This module integrates Oxford's dual-system framework (FAISS + Web Search + Solomon)
with Pipeline 2's validation system to provide comprehensive experiment validation
using both historical literature (1100+ PDFs) and real-time research.

Key Features:
- Dual-system validation using Oxford FAISS and web search
- Solomon prompt orchestration for unified validation insights
- Sakana principle compliance for empirical validation
- Domain-agnostic validation framework
- Real data authenticity verification
- Integration with existing Pipeline 2 validators

Architecture:
- Oxford Integration: Connects to dual-system framework without modifications
- Validation Enhancement: Augments Pipeline 2 validation with Oxford knowledge
- Sakana Compliance: Ensures empirical validation requirements
- Domain Flexibility: Adapts to different experimental domains
"""

import os
import sys
import json
import logging
import asyncio
from pathlib import Path
from typing import Dict, List, Optional, Union, Any, Tuple
from datetime import datetime
from dataclasses import dataclass
from enum import Enum

# Pipeline 2 imports
from .experiment_validator import ExperimentValidator
from ..integration.oxford_dual_system_bridge import OxfordDualSystemBridge
from ..integration.sakana_bridge import SakanaBridge

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ValidationLevel(Enum):
    """Validation levels with Oxford enhancement."""
    BASIC = "basic"                    # Standard Pipeline 2 validation
    OXFORD_ENHANCED = "oxford_enhanced"  # Basic + Oxford dual-system
    SAKANA_COMPLETE = "sakana_complete"  # Oxford + Sakana empirical validation
    COMPREHENSIVE = "comprehensive"      # All systems + domain-specific validation


@dataclass
class ValidationContext:
    """Context for Oxford-enhanced validation."""
    experiment_id: str
    experiment_type: str
    domain: str
    validation_level: ValidationLevel
    oxford_enabled: bool = True
    sakana_enabled: bool = True
    real_data_required: bool = True
    use_faiss: bool = True
    use_web_search: bool = True


@dataclass
class ValidationResult:
    """Enhanced validation result with Oxford integration."""
    experiment_id: str
    validation_level: ValidationLevel
    overall_score: float
    pipeline2_validation: Dict[str, Any]
    oxford_validation: Dict[str, Any]
    sakana_validation: Dict[str, Any]
    unified_assessment: Dict[str, Any]
    recommendations: List[str]
    knowledge_gaps: List[str]
    validation_enhancements: List[str]
    success: bool
    error: Optional[str] = None


class OxfordEnhancedValidator:
    """
    Oxford-enhanced validator for Pipeline 2 experiments.
    
    Integrates Oxford's dual-system framework with Pipeline 2 validation
    to provide comprehensive experiment validation using both historical
    literature and real-time research, while maintaining Sakana compliance.
    """
    
    def __init__(self, 
                 oxford_path: str = "/Users/apple/code/scientificoxford-try-shaun",
                 enable_oxford: bool = True,
                 enable_sakana: bool = True):
        """
        Initialize Oxford-enhanced validator.
        
        Args:
            oxford_path: Path to Oxford framework
            enable_oxford: Enable Oxford dual-system integration
            enable_sakana: Enable Sakana empirical validation
        """
        self.oxford_path = Path(oxford_path)
        self.enable_oxford = enable_oxford
        self.enable_sakana = enable_sakana
        
        # Initialize base Pipeline 2 validator
        self.base_validator = ExperimentValidator()
        
        # Initialize Oxford integration
        self.oxford_bridge = None
        if self.enable_oxford:
            try:
                self.oxford_bridge = OxfordDualSystemBridge(oxford_path)
                logger.info("✅ Oxford dual-system bridge connected")
            except Exception as e:
                logger.error(f"❌ Oxford bridge initialization failed: {e}")
                self.enable_oxford = False
        
        # Initialize Sakana integration
        self.sakana_bridge = None
        if self.enable_sakana:
            try:
                self.sakana_bridge = SakanaBridge()
                logger.info("✅ Sakana bridge connected")
            except Exception as e:
                logger.error(f"❌ Sakana bridge initialization failed: {e}")
                self.enable_sakana = False
        
        # Validation statistics
        self.validation_stats = {
            'total_validations': 0,
            'oxford_enhanced_validations': 0,
            'sakana_validations': 0,
            'comprehensive_validations': 0,
            'average_validation_score': 0.0,
            'successful_validations': 0
        }
        
        # Validation history
        self.validation_history = []
        
        logger.info("🔬 Oxford-Enhanced Validator initialized")
        logger.info(f"Oxford integration: {'ENABLED' if self.enable_oxford else 'DISABLED'}")
        logger.info(f"Sakana integration: {'ENABLED' if self.enable_sakana else 'DISABLED'}")
    
    async def validate_experiment(self, 
                                experiment: Dict[str, Any],
                                validation_level: ValidationLevel = ValidationLevel.OXFORD_ENHANCED,
                                domain: str = "general") -> ValidationResult:
        """
        Perform comprehensive experiment validation with Oxford enhancement.
        
        Args:
            experiment: Experiment data to validate
            validation_level: Level of validation to perform
            domain: Experimental domain (climate, chemical, etc.)
            
        Returns:
            ValidationResult with comprehensive validation assessment
        """
        validation_start = datetime.now()
        self.validation_stats['total_validations'] += 1
        
        # Create validation context
        context = ValidationContext(
            experiment_id=experiment.get('id', 'unknown'),
            experiment_type=experiment.get('type', 'unknown'),
            domain=domain,
            validation_level=validation_level,
            oxford_enabled=self.enable_oxford and validation_level in [
                ValidationLevel.OXFORD_ENHANCED, 
                ValidationLevel.SAKANA_COMPLETE, 
                ValidationLevel.COMPREHENSIVE
            ],
            sakana_enabled=self.enable_sakana and validation_level in [
                ValidationLevel.SAKANA_COMPLETE, 
                ValidationLevel.COMPREHENSIVE
            ]
        )
        
        # Initialize validation result
        validation_result = ValidationResult(
            experiment_id=context.experiment_id,
            validation_level=validation_level,
            overall_score=0.0,
            pipeline2_validation={},
            oxford_validation={},
            sakana_validation={},
            unified_assessment={},
            recommendations=[],
            knowledge_gaps=[],
            validation_enhancements=[],
            success=False
        )
        
        try:
            # Step 1: Base Pipeline 2 validation
            pipeline2_validation = await self._perform_base_validation(experiment, context)
            validation_result.pipeline2_validation = pipeline2_validation
            
            # Step 2: Oxford dual-system validation (if enabled)
            if context.oxford_enabled and self.oxford_bridge:
                oxford_validation = await self._perform_oxford_validation(experiment, context)
                validation_result.oxford_validation = oxford_validation
                self.validation_stats['oxford_enhanced_validations'] += 1
            
            # Step 3: Sakana empirical validation (if enabled)
            if context.sakana_enabled and self.sakana_bridge:
                sakana_validation = await self._perform_sakana_validation(experiment, context)
                validation_result.sakana_validation = sakana_validation
                self.validation_stats['sakana_validations'] += 1
            
            # Step 4: Unified assessment using all validation systems
            unified_assessment = await self._create_unified_assessment(
                validation_result, context
            )
            validation_result.unified_assessment = unified_assessment
            validation_result.overall_score = unified_assessment.get('overall_score', 0.0)
            validation_result.recommendations = unified_assessment.get('recommendations', [])
            validation_result.knowledge_gaps = unified_assessment.get('knowledge_gaps', [])
            validation_result.validation_enhancements = unified_assessment.get('enhancements', [])
            
            # Track comprehensive validations
            if validation_level == ValidationLevel.COMPREHENSIVE:
                self.validation_stats['comprehensive_validations'] += 1
            
            # Update statistics
            self.validation_stats['successful_validations'] += 1
            total_score = (self.validation_stats['average_validation_score'] * 
                          (self.validation_stats['successful_validations'] - 1) + 
                          validation_result.overall_score)
            self.validation_stats['average_validation_score'] = total_score / self.validation_stats['successful_validations']
            
            validation_result.success = True
            logger.info(f"✅ Enhanced validation completed: score {validation_result.overall_score:.2f}")
            
        except Exception as e:
            logger.error(f"❌ Enhanced validation failed: {e}")
            validation_result.error = str(e)
            validation_result.success = False
        
        # Record validation history
        validation_duration = (datetime.now() - validation_start).total_seconds()
        validation_result.unified_assessment['validation_duration_seconds'] = validation_duration
        self.validation_history.append(validation_result)
        
        return validation_result
    
    async def _perform_base_validation(self, 
                                     experiment: Dict[str, Any], 
                                     context: ValidationContext) -> Dict[str, Any]:
        """Perform base Pipeline 2 validation."""
        try:
            # Use existing Pipeline 2 validation logic
            base_result = self.base_validator.validate_experiment(experiment)
            
            return {
                'validation_type': 'Pipeline 2 Base Validation',
                'score': base_result.get('overall_score', 0.0),
                'passes_base_validation': base_result.get('valid', False),
                'base_recommendations': base_result.get('recommendations', []),
                'validation_details': base_result,
                'system_info': {
                    'validator': 'Pipeline 2 Base Validator',
                    'validation_timestamp': datetime.now().isoformat()
                }
            }
            
        except Exception as e:
            logger.error(f"Base validation failed: {e}")
            return {
                'validation_type': 'Pipeline 2 Base Validation',
                'score': 0.0,
                'passes_base_validation': False,
                'error': str(e)
            }
    
    async def _perform_oxford_validation(self, 
                                       experiment: Dict[str, Any], 
                                       context: ValidationContext) -> Dict[str, Any]:
        """Perform Oxford dual-system validation."""
        try:
            # Use Oxford bridge to enhance validation
            oxford_enhancement = self.oxford_bridge.enhance_pipeline2_validation(
                experiment, context.domain
            )
            
            # Extract Oxford validation insights
            faiss_validation = oxford_enhancement.get('oxford_faiss_validation', {})
            web_validation = oxford_enhancement.get('oxford_web_validation', {})
            solomon_validation = oxford_enhancement.get('solomon_unified_validation', {})
            
            # Calculate Oxford validation score
            oxford_score = self._calculate_oxford_validation_score(
                faiss_validation, web_validation, solomon_validation
            )
            
            return {
                'validation_type': 'Oxford Dual-System Validation',
                'score': oxford_score,
                'faiss_knowledge_validation': faiss_validation,
                'web_search_validation': web_validation,
                'solomon_synthesis': solomon_validation,
                'oxford_enhancements': oxford_enhancement.get('validation_improvements', []),
                'literature_support': len(faiss_validation.get('validation_support', [])),
                'current_research_support': len(web_validation.get('current_research', [])),
                'system_info': {
                    'oxford_framework': 'Dual-System (FAISS + Web Search + Solomon)',
                    'knowledge_base_size': '1100+ PDFs',
                    'validation_timestamp': datetime.now().isoformat()
                }
            }
            
        except Exception as e:
            logger.error(f"Oxford validation failed: {e}")
            return {
                'validation_type': 'Oxford Dual-System Validation',
                'score': 0.0,
                'error': str(e)
            }
    
    async def _perform_sakana_validation(self, 
                                       experiment: Dict[str, Any], 
                                       context: ValidationContext) -> Dict[str, Any]:
        """Perform Sakana empirical validation."""
        try:
            # Use Sakana bridge for empirical validation
            sakana_validation = self.sakana_bridge.validate_experiment_empirically(
                experiment, context.domain
            )
            
            return {
                'validation_type': 'Sakana Empirical Validation',
                'score': sakana_validation.get('empirical_score', 0.0),
                'real_data_validation': sakana_validation.get('real_data_validation', {}),
                'empirical_support': sakana_validation.get('empirical_evidence', []),
                'data_authenticity': sakana_validation.get('data_authenticity', {}),
                'sakana_compliance': sakana_validation.get('sakana_compliant', False),
                'system_info': {
                    'sakana_principle': 'Universal Empirical Validation',
                    'data_requirement': 'REAL_DATA_MANDATORY=true',
                    'validation_timestamp': datetime.now().isoformat()
                }
            }
            
        except Exception as e:
            logger.error(f"Sakana validation failed: {e}")
            return {
                'validation_type': 'Sakana Empirical Validation',
                'score': 0.0,
                'error': str(e)
            }
    
    async def _create_unified_assessment(self, 
                                       validation_result: ValidationResult, 
                                       context: ValidationContext) -> Dict[str, Any]:
        """Create unified assessment from all validation systems."""
        
        # Extract scores from different validation systems
        pipeline2_score = validation_result.pipeline2_validation.get('score', 0.0)
        oxford_score = validation_result.oxford_validation.get('score', 0.0)
        sakana_score = validation_result.sakana_validation.get('score', 0.0)
        
        # Calculate weighted overall score based on validation level
        if context.validation_level == ValidationLevel.BASIC:
            overall_score = pipeline2_score
            weight_description = "100% Pipeline 2 base validation"
            
        elif context.validation_level == ValidationLevel.OXFORD_ENHANCED:
            overall_score = (pipeline2_score * 0.4 + oxford_score * 0.6)
            weight_description = "40% Pipeline 2 + 60% Oxford dual-system"
            
        elif context.validation_level == ValidationLevel.SAKANA_COMPLETE:
            overall_score = (pipeline2_score * 0.3 + oxford_score * 0.4 + sakana_score * 0.3)
            weight_description = "30% Pipeline 2 + 40% Oxford + 30% Sakana"
            
        else:  # COMPREHENSIVE
            overall_score = (pipeline2_score * 0.25 + oxford_score * 0.45 + sakana_score * 0.3)
            weight_description = "25% Pipeline 2 + 45% Oxford + 30% Sakana"
        
        # Collect all recommendations
        recommendations = []
        recommendations.extend(validation_result.pipeline2_validation.get('base_recommendations', []))
        recommendations.extend(validation_result.oxford_validation.get('oxford_enhancements', []))
        recommendations.extend(validation_result.sakana_validation.get('empirical_support', []))
        
        # Identify knowledge gaps
        knowledge_gaps = []
        if oxford_score < 0.5:
            knowledge_gaps.append("Limited literature and current research support")
        if sakana_score < 0.5:
            knowledge_gaps.append("Insufficient empirical validation data")
        if pipeline2_score < 0.5:
            knowledge_gaps.append("Base validation requirements not met")
        
        # Identify validation enhancements
        enhancements = []
        if validation_result.oxford_validation.get('literature_support', 0) > 0:
            enhancements.append(f"Enhanced with {validation_result.oxford_validation['literature_support']} literature sources")
        
        if validation_result.oxford_validation.get('current_research_support', 0) > 0:
            enhancements.append(f"Validated against {validation_result.oxford_validation['current_research_support']} current research sources")
        
        if validation_result.sakana_validation.get('sakana_compliance', False):
            enhancements.append("Meets Sakana empirical validation requirements")
        
        # Create validation summary
        validation_summary = self._create_validation_summary(
            validation_result, overall_score, context
        )
        
        return {
            'overall_score': overall_score,
            'score_breakdown': {
                'pipeline2_score': pipeline2_score,
                'oxford_score': oxford_score,
                'sakana_score': sakana_score,
                'weighting_strategy': weight_description
            },
            'validation_level': context.validation_level.value,
            'passes_enhanced_validation': overall_score >= 0.6,
            'recommendations': list(set(recommendations)),  # Remove duplicates
            'knowledge_gaps': knowledge_gaps,
            'enhancements': enhancements,
            'validation_summary': validation_summary,
            'system_integration': {
                'oxford_integrated': context.oxford_enabled,
                'sakana_integrated': context.sakana_enabled,
                'dual_system_active': context.oxford_enabled and self.oxford_bridge is not None,
                'empirical_validation_active': context.sakana_enabled and self.sakana_bridge is not None
            }
        }
    
    def _calculate_oxford_validation_score(self, 
                                         faiss_validation: Dict, 
                                         web_validation: Dict, 
                                         solomon_validation: Dict) -> float:
        """Calculate validation score from Oxford dual-system results."""
        score = 0.0
        
        # FAISS literature support (40% weight)
        literature_support = len(faiss_validation.get('validation_support', []))
        if literature_support > 0:
            score += min(literature_support / 3.0, 1.0) * 0.4
        
        # Web search current research (30% weight)
        current_research = len(web_validation.get('current_research', []))
        if current_research > 0:
            score += min(current_research / 2.0, 1.0) * 0.3
        
        # Solomon synthesis quality (30% weight)
        total_sources = solomon_validation.get('knowledge_sources', {}).get('total_sources', 0)
        if total_sources > 0:
            score += min(total_sources / 5.0, 1.0) * 0.3
        
        return min(score, 1.0)
    
    def _create_validation_summary(self, 
                                 validation_result: ValidationResult, 
                                 overall_score: float, 
                                 context: ValidationContext) -> str:
        """Create human-readable validation summary."""
        
        summary = f"🔬 ENHANCED VALIDATION SUMMARY\n"
        summary += f"Experiment: {context.experiment_id} | Domain: {context.domain}\n"
        summary += f"Validation Level: {context.validation_level.value.upper()}\n"
        summary += f"Overall Score: {overall_score:.2f}/1.0 "
        
        if overall_score >= 0.8:
            summary += "(EXCELLENT) ✅\n"
        elif overall_score >= 0.6:
            summary += "(GOOD) ✅\n"
        elif overall_score >= 0.4:
            summary += "(FAIR) ⚠️\n"
        else:
            summary += "(NEEDS IMPROVEMENT) ❌\n"
        
        summary += "\n"
        
        # System integration status
        if context.oxford_enabled:
            summary += "📚 Oxford dual-system integration: ACTIVE\n"
            summary += f"   Literature validation: {validation_result.oxford_validation.get('literature_support', 0)} sources\n"
            summary += f"   Current research: {validation_result.oxford_validation.get('current_research_support', 0)} sources\n"
        
        if context.sakana_enabled:
            summary += "🧪 Sakana empirical validation: ACTIVE\n"
            sakana_compliant = validation_result.sakana_validation.get('sakana_compliance', False)
            summary += f"   Empirical compliance: {'YES' if sakana_compliant else 'NO'}\n"
        
        # Enhancement summary
        enhancements = validation_result.validation_enhancements
        if enhancements:
            summary += f"\n🎯 VALIDATION ENHANCEMENTS:\n"
            for enhancement in enhancements[:3]:
                summary += f"   • {enhancement}\n"
        
        return summary
    
    def get_validation_statistics(self) -> Dict[str, Any]:
        """Get validation system statistics."""
        return {
            'validator_name': 'Oxford-Enhanced Pipeline 2 Validator',
            'total_validations': self.validation_stats['total_validations'],
            'oxford_enhanced_validations': self.validation_stats['oxford_enhanced_validations'],
            'sakana_validations': self.validation_stats['sakana_validations'],
            'comprehensive_validations': self.validation_stats['comprehensive_validations'],
            'average_validation_score': self.validation_stats['average_validation_score'],
            'success_rate': (self.validation_stats['successful_validations'] / 
                           max(self.validation_stats['total_validations'], 1)),
            'system_integration': {
                'oxford_bridge_active': self.oxford_bridge is not None,
                'sakana_bridge_active': self.sakana_bridge is not None,
                'dual_system_available': self.enable_oxford,
                'empirical_validation_available': self.enable_sakana
            },
            'validation_history_count': len(self.validation_history)
        }
    
    def close(self):
        """Close validator and cleanup resources."""
        if self.oxford_bridge:
            # Oxford bridge cleanup if needed
            pass
        
        if self.sakana_bridge:
            # Sakana bridge cleanup if needed
            pass
        
        logger.info("🔬 Oxford-Enhanced Validator closed")


# Convenience functions for Pipeline 2 integration
def create_enhanced_validator(oxford_path: str = "/Users/apple/code/scientificoxford-try-shaun") -> OxfordEnhancedValidator:
    """Create Oxford-enhanced validator for Pipeline 2."""
    return OxfordEnhancedValidator(oxford_path)

async def validate_with_oxford_enhancement(experiment: Dict[str, Any], 
                                         domain: str = "general",
                                         validation_level: ValidationLevel = ValidationLevel.OXFORD_ENHANCED) -> ValidationResult:
    """
    One-line function to validate experiment with Oxford enhancement.
    
    Usage in Pipeline 2:
    from .oxford_enhanced_validator import validate_with_oxford_enhancement, ValidationLevel
    result = await validate_with_oxford_enhancement(experiment, "climate", ValidationLevel.COMPREHENSIVE)
    """
    validator = create_enhanced_validator()
    try:
        return await validator.validate_experiment(experiment, validation_level, domain)
    finally:
        validator.close()