"""
Unified Pipeline 2 Framework

This is the main orchestrator for Pipeline 2 that coordinates all enhanced validation systems:
- Oxford dual-system integration (FAISS + Web Search + Solomon)
- Sakana empirical validation
- Data requirement detection
- Domain-specific validation
- Enhanced experiment validation

The framework maintains Pipeline 1 compatibility while providing comprehensive
validation enhancement through integrated external systems.

Key Features:
- Unified API for all Pipeline 2 validation capabilities
- Oxford dual-system coordination without modifying existing codebase
- Sakana compliance enforcement
- Automated data requirement detection
- Domain-agnostic validation framework
- Performance monitoring and statistics
- Comprehensive experiment lifecycle management

Architecture:
- Core Framework: Main orchestration and API
- Validation Engine: Oxford + Sakana + Base validation coordination
- Data Intelligence: Automated requirement detection and source mapping
- Domain Adaptation: Flexible validation for different experimental domains
"""

import os
import sys
import json
import logging
import asyncio
from pathlib import Path
from typing import Dict, List, Optional, Union, Any, Tuple
from datetime import datetime
from dataclasses import dataclass, asdict
from enum import Enum

# Pipeline 2 component imports
from ..validation.oxford_enhanced_validator import OxfordEnhancedValidator, ValidationLevel, ValidationResult
from ..detection.data_requirement_detector import DataRequirementDetector, DataRequirementAnalysis
from ..integration.oxford_dual_system_bridge import OxfordDualSystemBridge
from ..integration.sakana_bridge import SakanaBridge
from ..validation.experiment_validator import ExperimentValidator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Pipeline2Mode(Enum):
    """Operating modes for Pipeline 2."""
    COMPATIBILITY = "compatibility"      # Pipeline 1 compatibility mode
    ENHANCED = "enhanced"                # Oxford + base validation
    COMPREHENSIVE = "comprehensive"      # Oxford + Sakana + all systems
    RESEARCH = "research"                # Research-focused with data intelligence
    PRODUCTION = "production"            # Production-ready with full monitoring


class ExperimentStatus(Enum):
    """Status tracking for experiments in Pipeline 2."""
    SUBMITTED = "submitted"
    ANALYZING_REQUIREMENTS = "analyzing_requirements"
    VALIDATING = "validating"
    OXFORD_PROCESSING = "oxford_processing"
    SAKANA_VERIFICATION = "sakana_verification"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class Pipeline2Configuration:
    """Configuration for Pipeline 2 framework."""
    mode: Pipeline2Mode
    oxford_path: str
    enable_oxford: bool
    enable_sakana: bool
    enable_data_detection: bool
    default_validation_level: ValidationLevel
    default_domain: str
    performance_monitoring: bool
    auto_data_requirement_detection: bool
    sakana_compliance_required: bool


@dataclass
class ExperimentSession:
    """Represents an experiment session in Pipeline 2."""
    session_id: str
    experiment_id: str
    experiment_data: Dict[str, Any]
    domain: str
    status: ExperimentStatus
    validation_level: ValidationLevel
    created_timestamp: str
    updated_timestamp: str
    data_requirement_analysis: Optional[DataRequirementAnalysis]
    validation_result: Optional[ValidationResult]
    oxford_integration_status: Dict[str, Any]
    sakana_compliance_status: Dict[str, Any]
    performance_metrics: Dict[str, Any]
    error_log: List[str]


class UnifiedPipeline2Framework:
    """
    Unified framework for Pipeline 2 enhanced validation.
    
    Orchestrates all Pipeline 2 components to provide comprehensive
    experiment validation using Oxford dual-system, Sakana validation,
    and automated data intelligence while maintaining Pipeline 1 compatibility.
    """
    
    def __init__(self, 
                 config: Optional[Pipeline2Configuration] = None,
                 oxford_path: str = "/Users/apple/code/scientificoxford-try-shaun"):
        """
        Initialize unified Pipeline 2 framework.
        
        Args:
            config: Pipeline 2 configuration (uses defaults if None)
            oxford_path: Path to Oxford framework
        """
        # Set default configuration if none provided
        if config is None:
            config = Pipeline2Configuration(
                mode=Pipeline2Mode.ENHANCED,
                oxford_path=oxford_path,
                enable_oxford=True,
                enable_sakana=True,
                enable_data_detection=True,
                default_validation_level=ValidationLevel.OXFORD_ENHANCED,
                default_domain="general",
                performance_monitoring=True,
                auto_data_requirement_detection=True,
                sakana_compliance_required=False
            )
        
        self.config = config
        self.oxford_path = Path(config.oxford_path)
        
        # Initialize core components
        self.oxford_validator = None
        self.data_detector = None
        self.oxford_bridge = None
        self.sakana_bridge = None
        self.base_validator = None
        
        # Session management
        self.active_sessions = {}
        self.session_history = []
        
        # Framework statistics
        self.framework_stats = {
            'total_experiments': 0,
            'successful_experiments': 0,
            'oxford_enhanced_experiments': 0,
            'sakana_compliant_experiments': 0,
            'data_detection_runs': 0,
            'average_validation_score': 0.0,
            'framework_uptime_start': datetime.now().isoformat()
        }
        
        logger.info("🚀 Unified Pipeline 2 Framework initializing...")
        logger.info(f"Mode: {config.mode.value}")
        logger.info(f"Oxford path: {self.oxford_path}")
        
        # Initialize components based on configuration
        self._initialize_components()
    
    def _initialize_components(self):
        """Initialize Pipeline 2 components based on configuration."""
        try:
            # Always initialize base validator for compatibility
            self.base_validator = ExperimentValidator()
            logger.info("✅ Base validator initialized")
            
            # Initialize Oxford-enhanced validator
            if self.config.enable_oxford:
                self.oxford_validator = OxfordEnhancedValidator(
                    oxford_path=self.config.oxford_path,
                    enable_oxford=True,
                    enable_sakana=self.config.enable_sakana
                )
                logger.info("✅ Oxford-enhanced validator initialized")
                
                # Initialize Oxford bridge for direct access
                self.oxford_bridge = OxfordDualSystemBridge(self.config.oxford_path)
                logger.info("✅ Oxford dual-system bridge initialized")
            
            # Initialize data requirement detector
            if self.config.enable_data_detection:
                self.data_detector = DataRequirementDetector(
                    oxford_path=self.config.oxford_path,
                    enable_oxford=self.config.enable_oxford,
                    enable_sakana=self.config.enable_sakana
                )
                logger.info("✅ Data requirement detector initialized")
            
            # Initialize Sakana bridge if needed
            if self.config.enable_sakana:
                self.sakana_bridge = SakanaBridge()
                logger.info("✅ Sakana bridge initialized")
            
            logger.info("🎯 Pipeline 2 framework initialization completed")
            
        except Exception as e:
            logger.error(f"❌ Component initialization failed: {e}")
            raise
    
    async def process_experiment(self, 
                               experiment: Dict[str, Any],
                               domain: str = None,
                               validation_level: ValidationLevel = None,
                               session_options: Dict[str, Any] = None) -> ExperimentSession:
        """
        Process an experiment through the complete Pipeline 2 validation framework.
        
        Args:
            experiment: Experiment data to process
            domain: Experimental domain (uses config default if None)
            validation_level: Validation level (uses config default if None)
            session_options: Additional session configuration
            
        Returns:
            ExperimentSession with complete processing results
        """
        session_start = datetime.now()
        self.framework_stats['total_experiments'] += 1
        
        # Set defaults from configuration
        if domain is None:
            domain = self.config.default_domain
        if validation_level is None:
            validation_level = self.config.default_validation_level
        
        # Create experiment session
        session = ExperimentSession(
            session_id=f"pipeline2_{session_start.strftime('%Y%m%d_%H%M%S')}_{len(self.active_sessions)}",
            experiment_id=experiment.get('id', 'unknown'),
            experiment_data=experiment,
            domain=domain,
            status=ExperimentStatus.SUBMITTED,
            validation_level=validation_level,
            created_timestamp=session_start.isoformat(),
            updated_timestamp=session_start.isoformat(),
            data_requirement_analysis=None,
            validation_result=None,
            oxford_integration_status={},
            sakana_compliance_status={},
            performance_metrics={},
            error_log=[]
        )
        
        # Add to active sessions
        self.active_sessions[session.session_id] = session
        
        logger.info(f"🧪 Processing experiment {session.experiment_id} (Session: {session.session_id})")
        logger.info(f"Domain: {domain}, Validation Level: {validation_level.value}")
        
        try:
            # Phase 1: Data Requirement Analysis (if enabled)
            if self.config.enable_data_detection and self.data_detector:
                await self._update_session_status(session, ExperimentStatus.ANALYZING_REQUIREMENTS)
                data_analysis = await self._analyze_data_requirements(session)
                session.data_requirement_analysis = data_analysis
                self.framework_stats['data_detection_runs'] += 1
            
            # Phase 2: Enhanced Validation
            await self._update_session_status(session, ExperimentStatus.VALIDATING)
            validation_result = await self._perform_enhanced_validation(session)
            session.validation_result = validation_result
            
            # Phase 3: Oxford Processing (if enabled and not already done in validation)
            if self.config.enable_oxford and self.oxford_bridge:
                await self._update_session_status(session, ExperimentStatus.OXFORD_PROCESSING)
                oxford_status = await self._process_oxford_integration(session)
                session.oxford_integration_status = oxford_status
                self.framework_stats['oxford_enhanced_experiments'] += 1
            
            # Phase 4: Sakana Verification (if enabled)
            if self.config.enable_sakana and self.sakana_bridge:
                await self._update_session_status(session, ExperimentStatus.SAKANA_VERIFICATION)
                sakana_status = await self._verify_sakana_compliance(session)
                session.sakana_compliance_status = sakana_status
                
                if sakana_status.get('compliant', False):
                    self.framework_stats['sakana_compliant_experiments'] += 1
            
            # Phase 5: Final Assessment and Completion
            await self._finalize_session(session)
            await self._update_session_status(session, ExperimentStatus.COMPLETED)
            
            # Update framework statistics
            self.framework_stats['successful_experiments'] += 1
            if session.validation_result:
                current_avg = self.framework_stats['average_validation_score']
                total_success = self.framework_stats['successful_experiments']
                new_score = session.validation_result.overall_score
                self.framework_stats['average_validation_score'] = (
                    (current_avg * (total_success - 1) + new_score) / total_success
                )
            
            logger.info(f"✅ Experiment {session.experiment_id} completed successfully")
            logger.info(f"Validation Score: {session.validation_result.overall_score:.2f}")
            
        except Exception as e:
            logger.error(f"❌ Experiment processing failed: {e}")
            session.error_log.append(f"Processing failed: {str(e)}")
            await self._update_session_status(session, ExperimentStatus.FAILED)
        
        # Calculate performance metrics
        session.performance_metrics = self._calculate_session_metrics(session, session_start)
        
        # Move to history and clean up active sessions
        self.session_history.append(session)
        if session.session_id in self.active_sessions:
            del self.active_sessions[session.session_id]
        
        return session
    
    async def _analyze_data_requirements(self, session: ExperimentSession) -> DataRequirementAnalysis:
        """Analyze data requirements for the experiment."""
        try:
            logger.info(f"🔍 Analyzing data requirements for {session.experiment_id}")
            
            analysis = await self.data_detector.analyze_data_requirements(
                session.experiment_data, 
                session.domain
            )
            
            logger.info(f"📊 Data analysis completed: {len(analysis.detected_requirements)} requirements")
            logger.info(f"Data readiness: {analysis.overall_data_readiness:.2f}")
            
            return analysis
            
        except Exception as e:
            logger.error(f"Data requirement analysis failed: {e}")
            session.error_log.append(f"Data analysis failed: {str(e)}")
            raise
    
    async def _perform_enhanced_validation(self, session: ExperimentSession) -> ValidationResult:
        """Perform enhanced validation using available systems."""
        try:
            logger.info(f"🔬 Performing enhanced validation for {session.experiment_id}")
            
            # Choose validator based on configuration
            if self.config.enable_oxford and self.oxford_validator:
                # Use Oxford-enhanced validator
                validation_result = await self.oxford_validator.validate_experiment(
                    session.experiment_data,
                    session.validation_level,
                    session.domain
                )
            else:
                # Fall back to base validator
                base_result = self.base_validator.validate_experiment(session.experiment_data)
                
                # Convert to enhanced format
                validation_result = ValidationResult(
                    experiment_id=session.experiment_id,
                    validation_level=ValidationLevel.BASIC,
                    overall_score=base_result.get('overall_score', 0.0),
                    pipeline2_validation=base_result,
                    oxford_validation={},
                    sakana_validation={},
                    unified_assessment={'score_breakdown': {'pipeline2_score': base_result.get('overall_score', 0.0)}},
                    recommendations=base_result.get('recommendations', []),
                    knowledge_gaps=[],
                    validation_enhancements=[],
                    success=base_result.get('valid', False)
                )
            
            logger.info(f"✅ Validation completed: score {validation_result.overall_score:.2f}")
            
            return validation_result
            
        except Exception as e:
            logger.error(f"Enhanced validation failed: {e}")
            session.error_log.append(f"Validation failed: {str(e)}")
            raise
    
    async def _process_oxford_integration(self, session: ExperimentSession) -> Dict[str, Any]:
        """Process Oxford dual-system integration."""
        try:
            logger.info(f"🎓 Processing Oxford integration for {session.experiment_id}")
            
            # Query Oxford dual-system for additional insights
            query = f"Validation analysis for {session.experiment_data.get('title', session.experiment_id)} in {session.domain} domain"
            
            oxford_result = self.oxford_bridge.query_dual_system(
                query,
                use_faiss=True,
                use_web_search=True,
                max_faiss_results=3,
                max_web_results=2
            )
            
            oxford_status = {
                'query_successful': oxford_result.get('success', False),
                'systems_used': oxford_result.get('systems_used', []),
                'faiss_results_count': len(oxford_result.get('faiss_results', {}).get('results', [])),
                'web_results_count': len(oxford_result.get('web_search_results', {}).get('results', [])),
                'solomon_synthesis': oxford_result.get('solomon_synthesis', {}),
                'unified_response': oxford_result.get('unified_response', ''),
                'integration_timestamp': datetime.now().isoformat()
            }
            
            logger.info(f"🎭 Oxford integration completed: {len(oxford_status['systems_used'])} systems used")
            
            return oxford_status
            
        except Exception as e:
            logger.error(f"Oxford integration failed: {e}")
            session.error_log.append(f"Oxford integration failed: {str(e)}")
            return {'error': str(e), 'integration_successful': False}
    
    async def _verify_sakana_compliance(self, session: ExperimentSession) -> Dict[str, Any]:
        """Verify Sakana compliance for the experiment."""
        try:
            logger.info(f"🧪 Verifying Sakana compliance for {session.experiment_id}")
            
            # Use Sakana bridge for verification
            sakana_result = self.sakana_bridge.validate_experiment_empirically(
                session.experiment_data,
                session.domain
            )
            
            sakana_status = {
                'compliant': sakana_result.get('sakana_compliant', False),
                'empirical_score': sakana_result.get('empirical_score', 0.0),
                'real_data_validation': sakana_result.get('real_data_validation', {}),
                'data_authenticity': sakana_result.get('data_authenticity', {}),
                'compliance_recommendations': sakana_result.get('recommendations', []),
                'verification_timestamp': datetime.now().isoformat()
            }
            
            compliance_status = "COMPLIANT" if sakana_status['compliant'] else "NON-COMPLIANT"
            logger.info(f"⚖️ Sakana verification completed: {compliance_status}")
            
            return sakana_status
            
        except Exception as e:
            logger.error(f"Sakana verification failed: {e}")
            session.error_log.append(f"Sakana verification failed: {str(e)}")
            return {'error': str(e), 'compliant': False}
    
    async def _finalize_session(self, session: ExperimentSession):
        """Finalize experiment session with comprehensive assessment."""
        try:
            # Create comprehensive session summary
            session_summary = {
                'experiment_processed': True,
                'validation_successful': session.validation_result.success if session.validation_result else False,
                'data_requirements_analyzed': session.data_requirement_analysis is not None,
                'oxford_integration_used': bool(session.oxford_integration_status),
                'sakana_verification_performed': bool(session.sakana_compliance_status),
                'overall_assessment': self._create_overall_assessment(session)
            }
            
            # Add comprehensive recommendations
            recommendations = []
            
            if session.validation_result:
                recommendations.extend(session.validation_result.recommendations)
            
            if session.data_requirement_analysis:
                recommendations.extend(session.data_requirement_analysis.recommendations)
            
            if session.oxford_integration_status.get('unified_response'):
                recommendations.append("Oxford dual-system insights incorporated")
            
            if session.sakana_compliance_status.get('compliant'):
                recommendations.append("Meets Sakana empirical validation requirements")
            elif session.sakana_compliance_status:
                recommendations.extend(session.sakana_compliance_status.get('compliance_recommendations', []))
            
            session_summary['final_recommendations'] = list(set(recommendations))  # Remove duplicates
            
            # Store session summary in performance metrics
            session.performance_metrics['session_summary'] = session_summary
            
            logger.info(f"📋 Session finalized for {session.experiment_id}")
            
        except Exception as e:
            logger.error(f"Session finalization failed: {e}")
            session.error_log.append(f"Finalization failed: {str(e)}")
    
    def _create_overall_assessment(self, session: ExperimentSession) -> str:
        """Create overall assessment summary for the session."""
        assessment_parts = []
        
        # Validation assessment
        if session.validation_result:
            score = session.validation_result.overall_score
            if score >= 0.8:
                assessment_parts.append("EXCELLENT validation results")
            elif score >= 0.6:
                assessment_parts.append("GOOD validation results")
            elif score >= 0.4:
                assessment_parts.append("ACCEPTABLE validation results")
            else:
                assessment_parts.append("VALIDATION NEEDS IMPROVEMENT")
        
        # Data readiness assessment
        if session.data_requirement_analysis:
            readiness = session.data_requirement_analysis.overall_data_readiness
            if readiness >= 0.8:
                assessment_parts.append("data requirements well-covered")
            elif readiness >= 0.6:
                assessment_parts.append("adequate data coverage")
            else:
                assessment_parts.append("data gaps identified")
        
        # Oxford integration assessment
        if session.oxford_integration_status.get('query_successful'):
            systems_used = len(session.oxford_integration_status.get('systems_used', []))
            assessment_parts.append(f"Oxford {systems_used}-system enhancement active")
        
        # Sakana compliance assessment
        if session.sakana_compliance_status.get('compliant'):
            assessment_parts.append("Sakana empirical compliance achieved")
        elif session.sakana_compliance_status:
            assessment_parts.append("Sakana compliance pending")
        
        return f"Pipeline 2 processing: {', '.join(assessment_parts)}"
    
    async def _update_session_status(self, session: ExperimentSession, status: ExperimentStatus):
        """Update session status and timestamp."""
        session.status = status
        session.updated_timestamp = datetime.now().isoformat()
        logger.info(f"📈 Session {session.session_id} status: {status.value}")
    
    def _calculate_session_metrics(self, session: ExperimentSession, start_time: datetime) -> Dict[str, Any]:
        """Calculate performance metrics for the session."""
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        metrics = {
            'processing_duration_seconds': duration,
            'status': session.status.value,
            'validation_score': session.validation_result.overall_score if session.validation_result else 0.0,
            'data_readiness': session.data_requirement_analysis.overall_data_readiness if session.data_requirement_analysis else 0.0,
            'oxford_integration_successful': session.oxford_integration_status.get('query_successful', False),
            'sakana_compliant': session.sakana_compliance_status.get('compliant', False),
            'components_used': [],
            'errors_encountered': len(session.error_log)
        }
        
        # Track which components were used
        if session.validation_result:
            metrics['components_used'].append('enhanced_validation')
        if session.data_requirement_analysis:
            metrics['components_used'].append('data_detection')
        if session.oxford_integration_status:
            metrics['components_used'].append('oxford_integration')
        if session.sakana_compliance_status:
            metrics['components_used'].append('sakana_verification')
        
        return metrics
    
    def get_framework_status(self) -> Dict[str, Any]:
        """Get comprehensive framework status."""
        return {
            'framework_name': 'Unified Pipeline 2 Framework',
            'mode': self.config.mode.value,
            'configuration': asdict(self.config),
            'component_status': {
                'base_validator': self.base_validator is not None,
                'oxford_validator': self.oxford_validator is not None,
                'data_detector': self.data_detector is not None,
                'oxford_bridge': self.oxford_bridge is not None,
                'sakana_bridge': self.sakana_bridge is not None
            },
            'statistics': self.framework_stats.copy(),
            'active_sessions': len(self.active_sessions),
            'completed_sessions': len(self.session_history),
            'uptime_hours': (datetime.now() - datetime.fromisoformat(self.framework_stats['framework_uptime_start'])).total_seconds() / 3600
        }
    
    def get_session_status(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a specific session."""
        if session_id in self.active_sessions:
            session = self.active_sessions[session_id]
            return {
                'session_id': session.session_id,
                'experiment_id': session.experiment_id,
                'status': session.status.value,
                'domain': session.domain,
                'validation_level': session.validation_level.value,
                'created': session.created_timestamp,
                'updated': session.updated_timestamp,
                'current_score': session.validation_result.overall_score if session.validation_result else None,
                'errors': len(session.error_log)
            }
        
        # Check history
        for session in self.session_history:
            if session.session_id == session_id:
                return {
                    'session_id': session.session_id,
                    'experiment_id': session.experiment_id,
                    'status': session.status.value,
                    'final_score': session.validation_result.overall_score if session.validation_result else None,
                    'completed': True
                }
        
        return None
    
    async def close(self):
        """Close framework and cleanup resources."""
        logger.info("🔄 Closing Pipeline 2 framework...")
        
        # Close component resources
        if self.oxford_validator:
            self.oxford_validator.close()
        
        # Clear active sessions
        self.active_sessions.clear()
        
        logger.info("✅ Pipeline 2 framework closed")


# Convenience functions for Pipeline 2 integration
def create_pipeline2_framework(mode: Pipeline2Mode = Pipeline2Mode.ENHANCED,
                              oxford_path: str = "/Users/apple/code/scientificoxford-try-shaun") -> UnifiedPipeline2Framework:
    """Create unified Pipeline 2 framework."""
    config = Pipeline2Configuration(
        mode=mode,
        oxford_path=oxford_path,
        enable_oxford=True,
        enable_sakana=True,
        enable_data_detection=True,
        default_validation_level=ValidationLevel.OXFORD_ENHANCED,
        default_domain="general",
        performance_monitoring=True,
        auto_data_requirement_detection=True,
        sakana_compliance_required=False
    )
    return UnifiedPipeline2Framework(config)

async def process_experiment_pipeline2(experiment: Dict[str, Any],
                                     domain: str = "general",
                                     mode: Pipeline2Mode = Pipeline2Mode.ENHANCED) -> ExperimentSession:
    """
    One-line function to process experiment through Pipeline 2.
    
    Usage:
    from .unified_pipeline2_framework import process_experiment_pipeline2, Pipeline2Mode
    session = await process_experiment_pipeline2(experiment, "climate", Pipeline2Mode.COMPREHENSIVE)
    """
    framework = create_pipeline2_framework(mode)
    try:
        return await framework.process_experiment(experiment, domain)
    finally:
        await framework.close()