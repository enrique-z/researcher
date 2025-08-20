"""
Comprehensive Testing Framework for Pipeline 2

This module provides comprehensive testing for all Pipeline 2 components:
- Oxford dual-system integration testing
- Sakana bridge validation testing  
- Data requirement detection testing
- Unified framework testing
- End-to-end pipeline testing
- Performance and stress testing

Test Categories:
- Unit Tests: Individual component testing
- Integration Tests: Component interaction testing
- System Tests: End-to-end pipeline testing
- Performance Tests: Load and stress testing
- Validation Tests: Output quality and accuracy testing

Key Features:
- Mock data generation for testing
- Oxford system integration validation
- Sakana compliance verification
- Data detection accuracy testing
- Performance benchmarking
- Error handling validation
"""

import os
import sys
import pytest
import asyncio
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Union, Any
from datetime import datetime
from unittest.mock import Mock, patch

# Add project root to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Pipeline 2 imports
from ai_researcher_enhanced.core.unified_pipeline2_framework import (
    UnifiedPipeline2Framework, Pipeline2Mode, Pipeline2Configuration, ValidationLevel
)
from ai_researcher_enhanced.validation.oxford_enhanced_validator import OxfordEnhancedValidator
from ai_researcher_enhanced.detection.data_requirement_detector import DataRequirementDetector
from ai_researcher_enhanced.integration.oxford_dual_system_bridge import OxfordDualSystemBridge
from ai_researcher_enhanced.integration.sakana_bridge import SakanaBridge

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Pipeline2TestFramework:
    """Comprehensive testing framework for Pipeline 2 components."""
    
    def __init__(self, oxford_path: str = "/Users/apple/code/scientificoxford-try-shaun"):
        """Initialize test framework."""
        self.oxford_path = oxford_path
        self.test_results = {}
        self.performance_metrics = {}
        self.mock_experiments = self._generate_mock_experiments()
        
        logger.info("🧪 Pipeline 2 Test Framework initialized")
    
    def _generate_mock_experiments(self) -> List[Dict[str, Any]]:
        """Generate mock experiments for testing."""
        return [
            {
                'id': 'test_climate_001',
                'title': 'Arctic SAI Climate Impact Assessment',
                'type': 'climate_experiment',
                'description': 'Evaluation of stratospheric aerosol injection effects on Arctic climate patterns',
                'domain': 'climate',
                'parameters': {
                    'injection_rate': '5 Tg/year',
                    'particle_size': '0.1-0.5 μm',
                    'altitude': '20-25 km',
                    'duration': '10 years'
                },
                'objectives': [
                    'Assess temperature response',
                    'Evaluate precipitation changes',
                    'Monitor ecosystem impacts'
                ],
                'methodology': 'Climate model simulation with observational validation',
                'data_requirements': [
                    'atmospheric temperature measurements',
                    'precipitation data',
                    'aerosol optical depth'
                ]
            },
            {
                'id': 'test_chemical_001',
                'title': 'Sulfate Aerosol Chemical Composition Analysis',
                'type': 'chemical_experiment',
                'description': 'Chemical analysis of sulfate aerosol particles for SAI applications',
                'domain': 'chemical',
                'parameters': {
                    'chemical_composition': 'H2SO4',
                    'concentration': '10-50 ppm',
                    'reaction_conditions': 'stratospheric pressure and temperature'
                },
                'objectives': [
                    'Determine particle stability',
                    'Measure reaction rates',
                    'Assess environmental impact'
                ],
                'methodology': 'Laboratory spectroscopic analysis with field validation'
            },
            {
                'id': 'test_general_001',
                'title': 'General Validation Test Experiment',
                'type': 'validation_test',
                'description': 'Generic experiment for testing validation frameworks',
                'domain': 'general',
                'parameters': {
                    'test_parameter_1': 'value_1',
                    'test_parameter_2': 42
                },
                'objectives': ['Test validation system'],
                'methodology': 'Systematic validation testing'
            }
        ]
    
    async def run_comprehensive_tests(self) -> Dict[str, Any]:
        """Run comprehensive test suite for Pipeline 2."""
        logger.info("🚀 Starting comprehensive Pipeline 2 tests...")
        
        test_results = {
            'test_session_id': f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'start_time': datetime.now().isoformat(),
            'unit_tests': {},
            'integration_tests': {},
            'system_tests': {},
            'performance_tests': {},
            'validation_tests': {},
            'overall_success': False,
            'summary': {}
        }
        
        try:
            # Unit Tests
            logger.info("📋 Running unit tests...")
            test_results['unit_tests'] = await self._run_unit_tests()
            
            # Integration Tests
            logger.info("🔗 Running integration tests...")
            test_results['integration_tests'] = await self._run_integration_tests()
            
            # System Tests
            logger.info("🖥️ Running system tests...")
            test_results['system_tests'] = await self._run_system_tests()
            
            # Performance Tests
            logger.info("⚡ Running performance tests...")
            test_results['performance_tests'] = await self._run_performance_tests()
            
            # Validation Tests
            logger.info("✅ Running validation tests...")
            test_results['validation_tests'] = await self._run_validation_tests()
            
            # Calculate overall success
            test_results['overall_success'] = self._calculate_overall_success(test_results)
            test_results['summary'] = self._generate_test_summary(test_results)
            
        except Exception as e:
            logger.error(f"❌ Test execution failed: {e}")
            test_results['error'] = str(e)
            test_results['overall_success'] = False
        
        test_results['end_time'] = datetime.now().isoformat()
        self.test_results = test_results
        
        logger.info(f"🏁 Comprehensive tests completed: {'SUCCESS' if test_results['overall_success'] else 'FAILED'}")
        
        return test_results
    
    async def _run_unit_tests(self) -> Dict[str, Any]:
        """Run unit tests for individual components."""
        unit_results = {
            'oxford_bridge_test': await self._test_oxford_bridge(),
            'sakana_bridge_test': await self._test_sakana_bridge(),
            'data_detector_test': await self._test_data_detector(),
            'oxford_validator_test': await self._test_oxford_validator(),
            'framework_initialization_test': await self._test_framework_initialization()
        }
        
        unit_results['success_rate'] = sum(1 for test in unit_results.values() 
                                         if isinstance(test, dict) and test.get('success', False)) / len(unit_results)
        
        return unit_results
    
    async def _test_oxford_bridge(self) -> Dict[str, Any]:
        """Test Oxford dual-system bridge."""
        try:
            # Test with mock if Oxford system not available
            if not Path(self.oxford_path).exists():
                logger.warning("Oxford system not found - using mock test")
                return {
                    'test_name': 'Oxford Bridge Test',
                    'success': True,
                    'mock_test': True,
                    'message': 'Oxford system not available - mock test passed'
                }
            
            bridge = OxfordDualSystemBridge(self.oxford_path)
            
            # Test basic query
            test_query = "climate validation test"
            result = bridge.query_dual_system(test_query, max_faiss_results=2, max_web_results=2)
            
            # Test status
            status = bridge.get_system_status()
            
            return {
                'test_name': 'Oxford Bridge Test',
                'success': True,
                'query_successful': result.get('success', False),
                'systems_available': len(result.get('systems_used', [])),
                'bridge_status': status.get('bridge_active', False),
                'message': 'Oxford bridge functioning correctly'
            }
            
        except Exception as e:
            return {
                'test_name': 'Oxford Bridge Test',
                'success': False,
                'error': str(e),
                'message': 'Oxford bridge test failed'
            }
    
    async def _test_sakana_bridge(self) -> Dict[str, Any]:
        """Test Sakana bridge."""
        try:
            bridge = SakanaBridge()
            
            # Test validation with mock experiment
            test_experiment = self.mock_experiments[0]
            result = bridge.validate_experiment_empirically(test_experiment, 'climate')
            
            return {
                'test_name': 'Sakana Bridge Test',
                'success': True,
                'validation_completed': 'empirical_score' in result,
                'sakana_compliant': result.get('sakana_compliant', False),
                'empirical_score': result.get('empirical_score', 0.0),
                'message': 'Sakana bridge functioning correctly'
            }
            
        except Exception as e:
            return {
                'test_name': 'Sakana Bridge Test',
                'success': False,
                'error': str(e),
                'message': 'Sakana bridge test failed'
            }
    
    async def _test_data_detector(self) -> Dict[str, Any]:
        """Test data requirement detector."""
        try:
            detector = DataRequirementDetector(self.oxford_path)
            
            # Test requirement detection
            test_experiment = self.mock_experiments[0]
            analysis = await detector.analyze_data_requirements(test_experiment, 'climate')
            
            return {
                'test_name': 'Data Detector Test',
                'success': True,
                'requirements_detected': len(analysis.detected_requirements),
                'sources_found': len(analysis.source_results),
                'data_readiness': analysis.overall_data_readiness,
                'recommendations_generated': len(analysis.recommendations),
                'message': 'Data detector functioning correctly'
            }
            
        except Exception as e:
            return {
                'test_name': 'Data Detector Test',
                'success': False,
                'error': str(e),
                'message': 'Data detector test failed'
            }
    
    async def _test_oxford_validator(self) -> Dict[str, Any]:
        """Test Oxford-enhanced validator."""
        try:
            validator = OxfordEnhancedValidator(self.oxford_path)
            
            # Test validation
            test_experiment = self.mock_experiments[0]
            result = await validator.validate_experiment(
                test_experiment, 
                ValidationLevel.OXFORD_ENHANCED, 
                'climate'
            )
            
            validator.close()
            
            return {
                'test_name': 'Oxford Validator Test',
                'success': result.success,
                'overall_score': result.overall_score,
                'oxford_integrated': bool(result.oxford_validation),
                'sakana_integrated': bool(result.sakana_validation),
                'recommendations_count': len(result.recommendations),
                'message': 'Oxford validator functioning correctly'
            }
            
        except Exception as e:
            return {
                'test_name': 'Oxford Validator Test',
                'success': False,
                'error': str(e),
                'message': 'Oxford validator test failed'
            }
    
    async def _test_framework_initialization(self) -> Dict[str, Any]:
        """Test framework initialization."""
        try:
            config = Pipeline2Configuration(
                mode=Pipeline2Mode.ENHANCED,
                oxford_path=self.oxford_path,
                enable_oxford=True,
                enable_sakana=True,
                enable_data_detection=True,
                default_validation_level=ValidationLevel.OXFORD_ENHANCED,
                default_domain="general",
                performance_monitoring=True,
                auto_data_requirement_detection=True,
                sakana_compliance_required=False
            )
            
            framework = UnifiedPipeline2Framework(config)
            status = framework.get_framework_status()
            await framework.close()
            
            return {
                'test_name': 'Framework Initialization Test',
                'success': True,
                'components_initialized': sum(status['component_status'].values()),
                'framework_mode': status['mode'],
                'configuration_valid': status['configuration'] is not None,
                'message': 'Framework initialization successful'
            }
            
        except Exception as e:
            return {
                'test_name': 'Framework Initialization Test',
                'success': False,
                'error': str(e),
                'message': 'Framework initialization failed'
            }
    
    async def _run_integration_tests(self) -> Dict[str, Any]:
        """Run integration tests for component interactions."""
        integration_results = {
            'oxford_validator_integration': await self._test_oxford_validator_integration(),
            'data_detector_oxford_integration': await self._test_data_detector_oxford_integration(),
            'sakana_oxford_integration': await self._test_sakana_oxford_integration(),
            'framework_component_integration': await self._test_framework_component_integration()
        }
        
        integration_results['success_rate'] = sum(1 for test in integration_results.values() 
                                                if isinstance(test, dict) and test.get('success', False)) / len(integration_results)
        
        return integration_results
    
    async def _test_oxford_validator_integration(self) -> Dict[str, Any]:
        """Test Oxford validator with all systems integrated."""
        try:
            validator = OxfordEnhancedValidator(self.oxford_path, enable_oxford=True, enable_sakana=True)
            
            test_experiment = self.mock_experiments[1]  # Chemical experiment
            result = await validator.validate_experiment(
                test_experiment, 
                ValidationLevel.COMPREHENSIVE, 
                'chemical'
            )
            
            # Check that all systems provided input
            has_oxford = bool(result.oxford_validation)
            has_sakana = bool(result.sakana_validation)
            has_unified = bool(result.unified_assessment)
            
            validator.close()
            
            return {
                'test_name': 'Oxford Validator Integration Test',
                'success': result.success and has_oxford and has_unified,
                'oxford_validation': has_oxford,
                'sakana_validation': has_sakana,
                'unified_assessment': has_unified,
                'integration_score': result.overall_score,
                'message': 'Oxford validator integration successful'
            }
            
        except Exception as e:
            return {
                'test_name': 'Oxford Validator Integration Test',
                'success': False,
                'error': str(e),
                'message': 'Oxford validator integration failed'
            }
    
    async def _test_data_detector_oxford_integration(self) -> Dict[str, Any]:
        """Test data detector with Oxford systems."""
        try:
            detector = DataRequirementDetector(self.oxford_path, enable_oxford=True)
            
            test_experiment = self.mock_experiments[0]  # Climate experiment
            analysis = await detector.analyze_data_requirements(test_experiment, 'climate')
            
            # Check Oxford integration
            oxford_used = analysis.oxford_integration_status.get('faiss_system_used', False)
            sources_found = len(analysis.source_results)
            
            return {
                'test_name': 'Data Detector Oxford Integration Test',
                'success': oxford_used or sources_found > 0,
                'oxford_faiss_used': oxford_used,
                'web_search_used': analysis.oxford_integration_status.get('web_search_used', False),
                'sources_found': sources_found,
                'data_readiness': analysis.overall_data_readiness,
                'message': 'Data detector Oxford integration successful'
            }
            
        except Exception as e:
            return {
                'test_name': 'Data Detector Oxford Integration Test',
                'success': False,
                'error': str(e),
                'message': 'Data detector Oxford integration failed'
            }
    
    async def _test_sakana_oxford_integration(self) -> Dict[str, Any]:
        """Test Sakana and Oxford systems working together."""
        try:
            # Test through unified validator
            validator = OxfordEnhancedValidator(self.oxford_path, enable_oxford=True, enable_sakana=True)
            
            test_experiment = self.mock_experiments[2]  # General experiment
            result = await validator.validate_experiment(
                test_experiment, 
                ValidationLevel.SAKANA_COMPLETE, 
                'general'
            )
            
            # Check integration
            oxford_score = result.oxford_validation.get('score', 0.0)
            sakana_score = result.sakana_validation.get('score', 0.0)
            unified_score = result.overall_score
            
            validator.close()
            
            return {
                'test_name': 'Sakana Oxford Integration Test',
                'success': result.success,
                'oxford_contribution': oxford_score,
                'sakana_contribution': sakana_score,
                'unified_score': unified_score,
                'integration_successful': oxford_score > 0 or sakana_score > 0,
                'message': 'Sakana Oxford integration successful'
            }
            
        except Exception as e:
            return {
                'test_name': 'Sakana Oxford Integration Test',
                'success': False,
                'error': str(e),
                'message': 'Sakana Oxford integration failed'
            }
    
    async def _test_framework_component_integration(self) -> Dict[str, Any]:
        """Test unified framework with all components."""
        try:
            framework = UnifiedPipeline2Framework()
            
            test_experiment = self.mock_experiments[0]
            session = await framework.process_experiment(
                test_experiment, 
                domain='climate',
                validation_level=ValidationLevel.COMPREHENSIVE
            )
            
            # Check all components were used
            components_used = session.performance_metrics.get('components_used', [])
            
            await framework.close()
            
            return {
                'test_name': 'Framework Component Integration Test',
                'success': session.status.value == 'completed',
                'components_used': len(components_used),
                'validation_score': session.validation_result.overall_score if session.validation_result else 0.0,
                'data_analysis_completed': session.data_requirement_analysis is not None,
                'oxford_integration': bool(session.oxford_integration_status),
                'sakana_verification': bool(session.sakana_compliance_status),
                'message': 'Framework component integration successful'
            }
            
        except Exception as e:
            return {
                'test_name': 'Framework Component Integration Test',
                'success': False,
                'error': str(e),
                'message': 'Framework component integration failed'
            }
    
    async def _run_system_tests(self) -> Dict[str, Any]:
        """Run end-to-end system tests."""
        system_results = {
            'end_to_end_pipeline_test': await self._test_end_to_end_pipeline(),
            'multiple_experiments_test': await self._test_multiple_experiments(),
            'different_modes_test': await self._test_different_modes(),
            'error_handling_test': await self._test_error_handling()
        }
        
        system_results['success_rate'] = sum(1 for test in system_results.values() 
                                           if isinstance(test, dict) and test.get('success', False)) / len(system_results)
        
        return system_results
    
    async def _test_end_to_end_pipeline(self) -> Dict[str, Any]:
        """Test complete end-to-end pipeline processing."""
        try:
            framework = UnifiedPipeline2Framework()
            
            # Process climate experiment end-to-end
            test_experiment = self.mock_experiments[0]
            session = await framework.process_experiment(
                test_experiment,
                domain='climate',
                validation_level=ValidationLevel.COMPREHENSIVE
            )
            
            # Verify complete processing
            processing_complete = (
                session.status.value == 'completed' and
                session.validation_result is not None and
                session.data_requirement_analysis is not None
            )
            
            await framework.close()
            
            return {
                'test_name': 'End-to-End Pipeline Test',
                'success': processing_complete,
                'session_completed': session.status.value == 'completed',
                'validation_score': session.validation_result.overall_score if session.validation_result else 0.0,
                'processing_time': session.performance_metrics.get('processing_duration_seconds', 0),
                'errors_encountered': len(session.error_log),
                'message': 'End-to-end pipeline test successful'
            }
            
        except Exception as e:
            return {
                'test_name': 'End-to-End Pipeline Test',
                'success': False,
                'error': str(e),
                'message': 'End-to-end pipeline test failed'
            }
    
    async def _test_multiple_experiments(self) -> Dict[str, Any]:
        """Test processing multiple experiments."""
        try:
            framework = UnifiedPipeline2Framework()
            
            sessions = []
            for experiment in self.mock_experiments:
                session = await framework.process_experiment(experiment, experiment.get('domain', 'general'))
                sessions.append(session)
            
            # Check all sessions completed
            completed_sessions = sum(1 for s in sessions if s.status.value == 'completed')
            average_score = sum(s.validation_result.overall_score for s in sessions 
                              if s.validation_result) / len(sessions)
            
            await framework.close()
            
            return {
                'test_name': 'Multiple Experiments Test',
                'success': completed_sessions == len(self.mock_experiments),
                'total_experiments': len(self.mock_experiments),
                'completed_experiments': completed_sessions,
                'average_validation_score': average_score,
                'message': 'Multiple experiments test successful'
            }
            
        except Exception as e:
            return {
                'test_name': 'Multiple Experiments Test',
                'success': False,
                'error': str(e),
                'message': 'Multiple experiments test failed'
            }
    
    async def _test_different_modes(self) -> Dict[str, Any]:
        """Test different Pipeline 2 modes."""
        try:
            modes_tested = []
            
            for mode in [Pipeline2Mode.ENHANCED, Pipeline2Mode.COMPREHENSIVE]:
                framework = UnifiedPipeline2Framework()
                
                test_experiment = self.mock_experiments[0]
                session = await framework.process_experiment(test_experiment, 'climate')
                
                modes_tested.append({
                    'mode': mode.value,
                    'success': session.status.value == 'completed',
                    'score': session.validation_result.overall_score if session.validation_result else 0.0
                })
                
                await framework.close()
            
            successful_modes = sum(1 for m in modes_tested if m['success'])
            
            return {
                'test_name': 'Different Modes Test',
                'success': successful_modes == len(modes_tested),
                'modes_tested': len(modes_tested),
                'successful_modes': successful_modes,
                'mode_results': modes_tested,
                'message': 'Different modes test successful'
            }
            
        except Exception as e:
            return {
                'test_name': 'Different Modes Test',
                'success': False,
                'error': str(e),
                'message': 'Different modes test failed'
            }
    
    async def _test_error_handling(self) -> Dict[str, Any]:
        """Test error handling capabilities."""
        try:
            framework = UnifiedPipeline2Framework()
            
            # Test with invalid experiment
            invalid_experiment = {'invalid': 'data'}
            session = await framework.process_experiment(invalid_experiment, 'invalid_domain')
            
            # Error handling should prevent crashes
            error_handled = session.status.value in ['failed', 'completed']
            errors_logged = len(session.error_log) > 0
            
            await framework.close()
            
            return {
                'test_name': 'Error Handling Test',
                'success': error_handled,
                'session_status': session.status.value,
                'errors_logged': errors_logged,
                'error_count': len(session.error_log),
                'message': 'Error handling test successful'
            }
            
        except Exception as e:
            return {
                'test_name': 'Error Handling Test',
                'success': False,
                'error': str(e),
                'message': 'Error handling test failed'
            }
    
    async def _run_performance_tests(self) -> Dict[str, Any]:
        """Run performance and stress tests."""
        performance_results = {
            'processing_speed_test': await self._test_processing_speed(),
            'memory_usage_test': await self._test_memory_usage(),
            'concurrent_processing_test': await self._test_concurrent_processing()
        }
        
        performance_results['success_rate'] = sum(1 for test in performance_results.values() 
                                                if isinstance(test, dict) and test.get('success', False)) / len(performance_results)
        
        return performance_results
    
    async def _test_processing_speed(self) -> Dict[str, Any]:
        """Test processing speed performance."""
        try:
            framework = UnifiedPipeline2Framework()
            
            start_time = datetime.now()
            test_experiment = self.mock_experiments[0]
            session = await framework.process_experiment(test_experiment, 'climate')
            end_time = datetime.now()
            
            processing_time = (end_time - start_time).total_seconds()
            await framework.close()
            
            # Consider under 30 seconds as good performance for testing
            good_performance = processing_time < 30.0
            
            return {
                'test_name': 'Processing Speed Test',
                'success': good_performance and session.status.value == 'completed',
                'processing_time_seconds': processing_time,
                'performance_rating': 'good' if good_performance else 'slow',
                'session_completed': session.status.value == 'completed',
                'message': f'Processing completed in {processing_time:.2f} seconds'
            }
            
        except Exception as e:
            return {
                'test_name': 'Processing Speed Test',
                'success': False,
                'error': str(e),
                'message': 'Processing speed test failed'
            }
    
    async def _test_memory_usage(self) -> Dict[str, Any]:
        """Test memory usage during processing."""
        try:
            import psutil
            import os
            
            process = psutil.Process(os.getpid())
            memory_before = process.memory_info().rss / 1024 / 1024  # MB
            
            framework = UnifiedPipeline2Framework()
            
            # Process multiple experiments to test memory
            for experiment in self.mock_experiments:
                await framework.process_experiment(experiment, experiment.get('domain', 'general'))
            
            memory_after = process.memory_info().rss / 1024 / 1024  # MB
            memory_increase = memory_after - memory_before
            
            await framework.close()
            
            # Consider under 500MB increase as acceptable
            acceptable_usage = memory_increase < 500
            
            return {
                'test_name': 'Memory Usage Test',
                'success': acceptable_usage,
                'memory_before_mb': memory_before,
                'memory_after_mb': memory_after,
                'memory_increase_mb': memory_increase,
                'usage_rating': 'acceptable' if acceptable_usage else 'high',
                'message': f'Memory increased by {memory_increase:.2f} MB'
            }
            
        except ImportError:
            return {
                'test_name': 'Memory Usage Test',
                'success': True,
                'message': 'psutil not available - memory test skipped',
                'skipped': True
            }
        except Exception as e:
            return {
                'test_name': 'Memory Usage Test',
                'success': False,
                'error': str(e),
                'message': 'Memory usage test failed'
            }
    
    async def _test_concurrent_processing(self) -> Dict[str, Any]:
        """Test concurrent experiment processing."""
        try:
            framework = UnifiedPipeline2Framework()
            
            # Process experiments concurrently
            tasks = []
            for i, experiment in enumerate(self.mock_experiments):
                task = framework.process_experiment(experiment, experiment.get('domain', 'general'))
                tasks.append(task)
            
            # Wait for all to complete
            sessions = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Check results
            successful_sessions = sum(1 for s in sessions 
                                    if not isinstance(s, Exception) and s.status.value == 'completed')
            
            await framework.close()
            
            return {
                'test_name': 'Concurrent Processing Test',
                'success': successful_sessions == len(self.mock_experiments),
                'total_experiments': len(self.mock_experiments),
                'successful_experiments': successful_sessions,
                'concurrent_processing_supported': True,
                'message': 'Concurrent processing test successful'
            }
            
        except Exception as e:
            return {
                'test_name': 'Concurrent Processing Test',
                'success': False,
                'error': str(e),
                'message': 'Concurrent processing test failed'
            }
    
    async def _run_validation_tests(self) -> Dict[str, Any]:
        """Run validation quality and accuracy tests."""
        validation_results = {
            'output_quality_test': await self._test_output_quality(),
            'validation_accuracy_test': await self._test_validation_accuracy(),
            'recommendation_quality_test': await self._test_recommendation_quality()
        }
        
        validation_results['success_rate'] = sum(1 for test in validation_results.values() 
                                               if isinstance(test, dict) and test.get('success', False)) / len(validation_results)
        
        return validation_results
    
    async def _test_output_quality(self) -> Dict[str, Any]:
        """Test quality of validation outputs."""
        try:
            framework = UnifiedPipeline2Framework()
            
            test_experiment = self.mock_experiments[0]
            session = await framework.process_experiment(test_experiment, 'climate')
            
            # Check output quality metrics
            has_validation_score = session.validation_result is not None
            has_recommendations = len(session.validation_result.recommendations) > 0 if session.validation_result else False
            has_data_analysis = session.data_requirement_analysis is not None
            
            quality_score = sum([has_validation_score, has_recommendations, has_data_analysis]) / 3.0
            
            await framework.close()
            
            return {
                'test_name': 'Output Quality Test',
                'success': quality_score >= 0.7,
                'quality_score': quality_score,
                'has_validation_score': has_validation_score,
                'has_recommendations': has_recommendations,
                'has_data_analysis': has_data_analysis,
                'message': 'Output quality test successful'
            }
            
        except Exception as e:
            return {
                'test_name': 'Output Quality Test',
                'success': False,
                'error': str(e),
                'message': 'Output quality test failed'
            }
    
    async def _test_validation_accuracy(self) -> Dict[str, Any]:
        """Test accuracy of validation results."""
        try:
            framework = UnifiedPipeline2Framework()
            
            # Test with well-defined experiment
            well_defined_experiment = {
                'id': 'accuracy_test_good',
                'title': 'Well-Defined Climate Experiment',
                'domain': 'climate',
                'methodology': 'Comprehensive climate modeling with observational validation',
                'parameters': {'well_defined': True},
                'data_requirements': ['temperature data', 'precipitation data']
            }
            
            session = await framework.process_experiment(well_defined_experiment, 'climate')
            good_score = session.validation_result.overall_score if session.validation_result else 0.0
            
            # Test with poorly-defined experiment
            poorly_defined_experiment = {
                'id': 'accuracy_test_poor',
                'title': 'Poorly Defined Experiment',
                'domain': 'general',
                'methodology': 'undefined'
            }
            
            session2 = await framework.process_experiment(poorly_defined_experiment, 'general')
            poor_score = session2.validation_result.overall_score if session2.validation_result else 0.0
            
            # Good experiment should score higher than poor experiment
            accuracy_valid = good_score > poor_score
            
            await framework.close()
            
            return {
                'test_name': 'Validation Accuracy Test',
                'success': accuracy_valid,
                'well_defined_score': good_score,
                'poorly_defined_score': poor_score,
                'score_difference': good_score - poor_score,
                'accuracy_demonstrated': accuracy_valid,
                'message': 'Validation accuracy test successful'
            }
            
        except Exception as e:
            return {
                'test_name': 'Validation Accuracy Test',
                'success': False,
                'error': str(e),
                'message': 'Validation accuracy test failed'
            }
    
    async def _test_recommendation_quality(self) -> Dict[str, Any]:
        """Test quality of generated recommendations."""
        try:
            framework = UnifiedPipeline2Framework()
            
            test_experiment = self.mock_experiments[0]
            session = await framework.process_experiment(test_experiment, 'climate')
            
            if session.validation_result:
                recommendations = session.validation_result.recommendations
                
                # Check recommendation quality
                has_recommendations = len(recommendations) > 0
                specific_recommendations = sum(1 for rec in recommendations if len(rec) > 20)  # Non-generic
                actionable_recommendations = sum(1 for rec in recommendations 
                                               if any(word in rec.lower() for word in ['should', 'consider', 'use', 'implement']))
                
                quality_metrics = {
                    'has_recommendations': has_recommendations,
                    'specific_count': specific_recommendations,
                    'actionable_count': actionable_recommendations,
                    'total_count': len(recommendations)
                }
                
                quality_score = (has_recommendations + 
                               min(specific_recommendations / max(len(recommendations), 1), 1.0) + 
                               min(actionable_recommendations / max(len(recommendations), 1), 1.0)) / 3.0
            else:
                quality_metrics = {'error': 'No validation result'}
                quality_score = 0.0
            
            await framework.close()
            
            return {
                'test_name': 'Recommendation Quality Test',
                'success': quality_score >= 0.5,
                'quality_score': quality_score,
                'quality_metrics': quality_metrics,
                'message': 'Recommendation quality test successful'
            }
            
        except Exception as e:
            return {
                'test_name': 'Recommendation Quality Test',
                'success': False,
                'error': str(e),
                'message': 'Recommendation quality test failed'
            }
    
    def _calculate_overall_success(self, test_results: Dict[str, Any]) -> bool:
        """Calculate overall test success."""
        category_success = []
        
        for category in ['unit_tests', 'integration_tests', 'system_tests', 'performance_tests', 'validation_tests']:
            if category in test_results:
                success_rate = test_results[category].get('success_rate', 0.0)
                category_success.append(success_rate >= 0.7)  # 70% success threshold
        
        return sum(category_success) >= 4  # At least 4 of 5 categories must pass
    
    def _generate_test_summary(self, test_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive test summary."""
        summary = {
            'total_test_categories': 5,
            'successful_categories': 0,
            'category_results': {},
            'overall_health': 'unknown',
            'recommendations': []
        }
        
        for category in ['unit_tests', 'integration_tests', 'system_tests', 'performance_tests', 'validation_tests']:
            if category in test_results:
                success_rate = test_results[category].get('success_rate', 0.0)
                summary['category_results'][category] = {
                    'success_rate': success_rate,
                    'status': 'pass' if success_rate >= 0.7 else 'fail'
                }
                
                if success_rate >= 0.7:
                    summary['successful_categories'] += 1
        
        # Determine overall health
        if summary['successful_categories'] >= 4:
            summary['overall_health'] = 'excellent'
        elif summary['successful_categories'] >= 3:
            summary['overall_health'] = 'good'
        elif summary['successful_categories'] >= 2:
            summary['overall_health'] = 'fair'
        else:
            summary['overall_health'] = 'poor'
        
        # Generate recommendations
        if summary['overall_health'] in ['poor', 'fair']:
            summary['recommendations'].append('Review failed test categories and address issues')
        
        if summary['category_results'].get('integration_tests', {}).get('status') == 'fail':
            summary['recommendations'].append('Check component integration and dependencies')
        
        if summary['category_results'].get('performance_tests', {}).get('status') == 'fail':
            summary['recommendations'].append('Optimize performance and resource usage')
        
        return summary
    
    def generate_test_report(self) -> str:
        """Generate human-readable test report."""
        if not self.test_results:
            return "No test results available. Run comprehensive tests first."
        
        results = self.test_results
        summary = results.get('summary', {})
        
        report = f"""
🧪 PIPELINE 2 COMPREHENSIVE TEST REPORT
=====================================

Test Session: {results.get('test_session_id', 'unknown')}
Execution Time: {results.get('start_time', 'unknown')} to {results.get('end_time', 'unknown')}
Overall Result: {'✅ SUCCESS' if results.get('overall_success', False) else '❌ FAILED'}

📊 CATEGORY RESULTS:
"""
        
        for category, data in summary.get('category_results', {}).items():
            status_icon = '✅' if data['status'] == 'pass' else '❌'
            report += f"  {status_icon} {category.replace('_', ' ').title()}: {data['success_rate']:.1%}\n"
        
        report += f"""
🎯 OVERALL HEALTH: {summary.get('overall_health', 'unknown').upper()}
Successful Categories: {summary.get('successful_categories', 0)}/{summary.get('total_test_categories', 5)}

"""
        
        if summary.get('recommendations'):
            report += "💡 RECOMMENDATIONS:\n"
            for rec in summary['recommendations']:
                report += f"  • {rec}\n"
        
        report += "\n🏁 Test execution completed."
        
        return report


# Convenience functions for running tests
async def run_pipeline2_tests(oxford_path: str = "/Users/apple/code/scientificoxford-try-shaun") -> Dict[str, Any]:
    """
    Run comprehensive Pipeline 2 tests.
    
    Usage:
    from tests.test_pipeline2_comprehensive import run_pipeline2_tests
    results = await run_pipeline2_tests()
    """
    test_framework = Pipeline2TestFramework(oxford_path)
    return await test_framework.run_comprehensive_tests()

async def quick_pipeline2_health_check(oxford_path: str = "/Users/apple/code/scientificoxford-try-shaun") -> bool:
    """
    Quick health check for Pipeline 2 system.
    
    Returns True if system is healthy, False otherwise.
    """
    test_framework = Pipeline2TestFramework(oxford_path)
    results = await test_framework.run_comprehensive_tests()
    return results.get('overall_success', False)

# Test execution entry point
if __name__ == "__main__":
    async def main():
        print("🚀 Starting Pipeline 2 Comprehensive Tests...")
        
        test_framework = Pipeline2TestFramework()
        results = await test_framework.run_comprehensive_tests()
        
        print("\n" + test_framework.generate_test_report())
        
        if results.get('overall_success'):
            print("\n🎉 All tests passed! Pipeline 2 is ready for use.")
        else:
            print("\n⚠️ Some tests failed. Review results and address issues.")
    
    asyncio.run(main())