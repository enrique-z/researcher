"""
Test Suite for Plausibility Checker

Comprehensive tests for the plausibility checker module that prevents
"plausibility trap" scenarios by analyzing theoretical sophistication
versus empirical support.
"""

import pytest
import numpy as np
from unittest.mock import Mock, patch
from datetime import datetime

import sys
sys.path.append('/Users/apple/code/Researcher')
from ai_researcher.validation.plausibility_checker import PlausibilityChecker


class TestPlausibilityChecker:
    """Test suite for plausibility checker functionality."""
    
    @pytest.fixture
    def plausibility_checker(self):
        """Create plausibility checker instance."""
        return PlausibilityChecker()
    
    @pytest.fixture
    def high_sophistication_claim(self):
        """Sample claim with high theoretical sophistication."""
        return """
        We propose a novel Volterra kernel spectroscopy approach using eigenvalue decomposition
        of stochastic optimization manifolds. The nonlinear dynamical systems analysis employs
        advanced perturbation theory with asymptotic expansion techniques to derive elegant
        mathematical formulations for climate signal detection.
        """
    
    @pytest.fixture
    def empirical_claim(self):
        """Sample claim with strong empirical grounding."""
        return """
        Using GLENS dataset from NCAR with 20-member ensemble validation, we performed
        statistical analysis showing p-value < 0.01 and correlation coefficient of 0.85.
        The NetCDF observational data confirms our hypothesis through rigorous measurement
        and experimental verification protocols.
        """
    
    @pytest.fixture
    def strong_empirical_evidence(self):
        """Sample strong empirical evidence."""
        return {
            'snr_analysis': {
                'snr_db': 8.5,
                'method': 'hansen',
                'detectable': True
            },
            'statistical_validation': {
                'p_value': 0.001,
                'confidence_interval': [1.2, 2.8],
                'sample_size': 240
            },
            'real_data_verification': {
                'authentic_data_confirmed': True,
                'institutional_validation': True,
                'synthetic_data_detected': False
            }
        }
    
    @pytest.fixture
    def weak_empirical_evidence(self):
        """Sample weak empirical evidence."""
        return {
            'snr_analysis': None,
            'statistical_validation': None,
            'real_data_verification': {
                'authentic_data_confirmed': False,
                'institutional_validation': False
            }
        }
    
    def test_checker_initialization(self, plausibility_checker):
        """Test proper initialization of plausibility checker."""
        assert len(plausibility_checker.sophistication_indicators) > 0
        assert len(plausibility_checker.empirical_indicators) > 0
        assert len(plausibility_checker.red_flag_patterns) > 0
        assert len(plausibility_checker.check_history) == 0
    
    def test_sophistication_analysis_high(self, plausibility_checker, high_sophistication_claim):
        """Test analysis of highly sophisticated theoretical claims."""
        sophistication_result = plausibility_checker._analyze_sophistication(high_sophistication_claim)
        
        assert isinstance(sophistication_result, dict)
        assert sophistication_result['score'] > 0.6  # Should be high
        assert sophistication_result['sophistication_level'] in ['HIGH', 'VERY_HIGH']
        assert sophistication_result['mathematical_complexity'] in ['HIGH', 'VERY_HIGH']
        
        # Check that sophistication indicators were found
        assert len(sophistication_result['indicators_found']) > 0
        expected_terms = ['Volterra', 'kernel', 'eigenvalue', 'stochastic', 'nonlinear']
        found_terms = sophistication_result['indicators_found']
        assert any(term in ' '.join(found_terms) for term in expected_terms)
    
    def test_sophistication_analysis_low(self, plausibility_checker):
        """Test analysis of low sophistication claims."""
        simple_claim = "The temperature increased by 2 degrees."
        
        sophistication_result = plausibility_checker._analyze_sophistication(simple_claim)
        
        assert sophistication_result['score'] < 0.3  # Should be low
        assert sophistication_result['sophistication_level'] in ['MINIMAL', 'LOW']
        assert sophistication_result['mathematical_complexity'] == 'LOW'
    
    def test_empirical_support_analysis_strong(self, plausibility_checker, empirical_claim, strong_empirical_evidence):
        """Test analysis of strong empirical support."""
        empirical_result = plausibility_checker._analyze_empirical_support(empirical_claim, strong_empirical_evidence)
        
        assert isinstance(empirical_result, dict)
        assert empirical_result['score'] > 0.6  # Should be high
        assert empirical_result['support_level'] in ['STRONG', 'MODERATE']
        assert empirical_result['data_authenticity'] == 'VERIFIED'
        assert empirical_result['quantitative_support'] is True
        
        # Check that empirical indicators were found
        assert len(empirical_result['textual_indicators']) > 0
        expected_terms = ['GLENS', 'NCAR', 'dataset', 'statistical', 'p-value']
        found_terms = empirical_result['textual_indicators']
        assert any(term in ' '.join(found_terms) for term in expected_terms)
    
    def test_empirical_support_analysis_weak(self, plausibility_checker, weak_empirical_evidence):
        """Test analysis of weak empirical support."""
        weak_claim = "Our theoretical framework suggests potential improvements."
        
        empirical_result = plausibility_checker._analyze_empirical_support(weak_claim, weak_empirical_evidence)
        
        assert empirical_result['score'] < 0.4  # Should be low
        assert empirical_result['support_level'] in ['INSUFFICIENT', 'MINIMAL', 'WEAK']
        assert empirical_result['data_authenticity'] == 'FAILED'
        assert empirical_result['quantitative_support'] is False
    
    def test_red_flag_detection(self, plausibility_checker):
        """Test detection of red flag patterns."""
        red_flag_claim = """
        Our elegant and sophisticated approach provides a novel theoretical framework
        that is undetectable below the noise threshold but represents a breakthrough
        in advanced mathematical formulation.
        """
        
        red_flag_result = plausibility_checker._check_red_flags(red_flag_claim)
        
        assert isinstance(red_flag_result, dict)
        assert red_flag_result['score'] > 0.3  # Should detect red flags
        assert red_flag_result['severity_level'] in ['MODERATE', 'HIGH', 'CRITICAL']
        assert len(red_flag_result['flags_detected']) > 0
        assert len(red_flag_result['risk_indicators']) > 0
        
        # Check for specific red flag terms
        expected_flags = ['elegant', 'sophisticated', 'novel', 'undetectable', 'breakthrough']
        detected_flags = ' '.join(red_flag_result['flags_detected']).lower()
        assert any(flag in detected_flags for flag in expected_flags)
    
    def test_plausibility_trap_detection(self, plausibility_checker, high_sophistication_claim, weak_empirical_evidence):
        """Test detection of classic plausibility trap scenario."""
        # High sophistication + Low empirical support = Plausibility trap risk
        analysis_result = plausibility_checker.analyze_claim_plausibility(
            claim_text=high_sophistication_claim,
            evidence=weak_empirical_evidence
        )
        
        assert analysis_result['plausibility_risk_level'] in ['HIGH', 'CRITICAL']
        assert analysis_result['plausibility_assessment'] in ['PLAUSIBILITY_TRAP_LIKELY', 'PLAUSIBILITY_TRAP_POSSIBLE']
        
        # Check risk factors
        risk_factors = analysis_result['risk_factors']
        assert 'High sophistication with low empirical support' in risk_factors
        assert 'Insufficient empirical evidence' in risk_factors
        
        # Check recommendations
        recommendations = analysis_result['recommendations']
        assert any('REJECT' in rec or 'CAUTION' in rec for rec in recommendations)
    
    def test_well_grounded_claim_acceptance(self, plausibility_checker, empirical_claim, strong_empirical_evidence):
        """Test acceptance of well-grounded empirical claims."""
        analysis_result = plausibility_checker.analyze_claim_plausibility(
            claim_text=empirical_claim,
            evidence=strong_empirical_evidence
        )
        
        assert analysis_result['plausibility_risk_level'] in ['MINIMAL', 'LOW']
        assert analysis_result['plausibility_assessment'] in ['EMPIRICALLY_GROUNDED', 'ACCEPTABLE_WITH_CAVEATS']
        
        # Check protective factors
        protective_factors = analysis_result['protective_factors']
        assert 'Strong empirical support' in protective_factors
        assert 'Verified authentic data usage' in protective_factors
        
        # Check recommendations
        recommendations = analysis_result['recommendations']
        assert any('Well-supported' in rec or 'acceptable' in rec for rec in recommendations)
    
    def test_quantitative_grounding_check(self, plausibility_checker):
        """Test quantitative parameter grounding validation."""
        # Test reasonable parameters
        reasonable_params = {
            'temperature_change': 2.5,      # °C - reasonable
            'precipitation_change': 15.0,   # % - reasonable  
            'radiative_forcing': -3.2,      # W/m² - reasonable
            'sai_injection': 5.0,           # Tg/yr - reasonable
            'snr_threshold': 6.0            # dB - reasonable
        }
        
        grounding_result = plausibility_checker.check_quantitative_grounding(reasonable_params)
        
        assert grounding_result['overall_status'] == 'QUANTITATIVELY_GROUNDED'
        assert len(grounding_result['violations']) == 0
        
        for param_check in grounding_result['parameter_checks']:
            if param_check['range_check'] != 'NOT_APPLICABLE':
                assert param_check['status'] == 'VALID'
        
        # Test unreasonable parameters
        unreasonable_params = {
            'temperature_change': 50.0,     # °C - unrealistic
            'precipitation_change': 200.0,  # % - unrealistic
            'radiative_forcing': -100.0,    # W/m² - unrealistic
            'snr_threshold': -50.0          # dB - unrealistic
        }
        
        grounding_result = plausibility_checker.check_quantitative_grounding(unreasonable_params)
        
        assert grounding_result['overall_status'] == 'VIOLATIONS_FOUND'
        assert len(grounding_result['violations']) > 0
    
    def test_historical_plausibility_trap_case(self, plausibility_checker):
        """Test analysis of the historical Hangzhou case that led to Sakana Principle."""
        hangzhou_case = """
        We propose an innovative Volterra kernel spectroscopy framework utilizing 
        eigenvalue decomposition and stochastic optimization for climate signal detection.
        This sophisticated approach employs advanced nonlinear dynamical systems theory
        and asymptotic perturbation analysis to achieve elegant mathematical formulations.
        """
        
        # Evidence that revealed the plausibility trap
        hangzhou_evidence = {
            'snr_analysis': {
                'snr_db': -15.54,  # The critical undetectable threshold
                'detectable': False
            },
            'statistical_validation': None,
            'real_data_verification': {
                'authentic_data_confirmed': False,
                'synthetic_data_detected': True
            }
        }
        
        analysis_result = plausibility_checker.analyze_claim_plausibility(
            claim_text=hangzhou_case,
            evidence=hangzhou_evidence
        )
        
        assert analysis_result['plausibility_risk_level'] == 'CRITICAL'
        assert analysis_result['plausibility_assessment'] == 'PLAUSIBILITY_TRAP_LIKELY'
        assert analysis_result['sophistication_score'] > 0.7  # High sophistication
        assert analysis_result['empirical_support_score'] < 0.3  # Low empirical support
        
        # Should recommend rejection
        recommendations = analysis_result['recommendations']
        assert any('REJECT' in rec for rec in recommendations)
    
    def test_moderate_risk_scenario(self, plausibility_checker):
        """Test moderate plausibility risk scenario."""
        moderate_claim = """
        Our analysis using GLENS data suggests that Volterra kernel methods
        could potentially improve signal detection capabilities through
        advanced mathematical optimization techniques.
        """
        
        moderate_evidence = {
            'snr_analysis': {
                'snr_db': 2.0,  # Low but detectable
                'detectable': True
            },
            'statistical_validation': {
                'p_value': 0.08,  # Marginally significant
                'sample_size': 50
            },
            'real_data_verification': {
                'authentic_data_confirmed': True,
                'institutional_validation': True
            }
        }
        
        analysis_result = plausibility_checker.analyze_claim_plausibility(
            claim_text=moderate_claim,
            evidence=moderate_evidence
        )
        
        assert analysis_result['plausibility_risk_level'] in ['MODERATE', 'LOW']
        assert analysis_result['plausibility_assessment'] in ['REQUIRES_VALIDATION', 'ACCEPTABLE_WITH_CAVEATS']
        
        # Should recommend additional validation
        recommendations = analysis_result['recommendations']
        assert any('validation' in rec.lower() for rec in recommendations)
    
    def test_check_history_tracking(self, plausibility_checker):
        """Test tracking of plausibility check history."""
        # Initially no history
        assert len(plausibility_checker.check_history) == 0
        
        # Perform a check
        sample_claim = "Test theoretical claim"
        sample_evidence = {'snr_analysis': {'snr_db': 5.0}}
        
        plausibility_checker.analyze_claim_plausibility(sample_claim, sample_evidence)
        
        # Check history was recorded
        assert len(plausibility_checker.check_history) == 1
        
        history_entry = plausibility_checker.check_history[0]
        assert 'analysis_timestamp' in history_entry
        assert 'claim_text' in history_entry
        assert 'plausibility_risk_level' in history_entry
        
        # Test summary statistics
        summary = plausibility_checker.get_check_history_summary()
        assert summary['total_checks'] == 1
        assert 'risk_level_distribution' in summary
        assert 'plausibility_trap_detection_rate' in summary
    
    def test_edge_cases_and_error_handling(self, plausibility_checker):
        """Test edge cases and error handling."""
        # Test with empty claim
        empty_result = plausibility_checker.analyze_claim_plausibility("", {})
        assert empty_result['plausibility_assessment'] != 'ERROR'  # Should handle gracefully
        
        # Test with very long claim
        long_claim = "Advanced theoretical framework " * 1000
        long_result = plausibility_checker.analyze_claim_plausibility(long_claim, {})
        assert long_result['sophistication_score'] > 0  # Should still analyze
        
        # Test with special characters and unicode
        unicode_claim = "Νοvel αpproach using ∇ operators and ∫ calculations"
        unicode_result = plausibility_checker.analyze_claim_plausibility(unicode_claim, {})
        assert unicode_result['sophistication_score'] > 0  # Should detect mathematical symbols
    
    def test_risk_assessment_formula(self, plausibility_checker):
        """Test the risk assessment mathematical formula."""
        # Create controlled test cases
        test_cases = [
            # High sophistication, low empirical, high red flags = Critical risk
            {'soph': 0.9, 'emp': 0.1, 'red': 0.8, 'expected_risk': 'HIGH'},
            # Low sophistication, high empirical, no red flags = Low risk  
            {'soph': 0.2, 'emp': 0.8, 'red': 0.0, 'expected_risk': 'LOW'},
            # Balanced case
            {'soph': 0.5, 'emp': 0.5, 'red': 0.2, 'expected_risk': 'MODERATE'}
        ]
        
        for case in test_cases:
            # Mock the analysis scores
            mock_analysis = {
                'sophistication_score': case['soph'],
                'empirical_support_score': case['emp'],
                'red_flag_score': case['red'],
                'detailed_analysis': {
                    'empirical_support': {
                        'data_authenticity': 'VERIFIED' if case['emp'] > 0.5 else 'FAILED'
                    }
                }
            }
            
            risk_assessment = plausibility_checker._assess_plausibility_risk(mock_analysis)
            
            # Check that risk formula behaves as expected
            sophistication_risk = case['soph'] * (1 - case['emp'])
            red_flag_multiplier = 1 + case['red']
            expected_overall_risk = min(sophistication_risk * red_flag_multiplier, 1.0)
            
            np.testing.assert_allclose(
                risk_assessment['overall_risk_score'], 
                expected_overall_risk, 
                rtol=1e-10
            )
    
    def test_integration_with_sakana_validator(self, plausibility_checker):
        """Test integration with Sakana Principle validator."""
        # Test a claim that should trigger Sakana validation
        sakana_relevant_claim = """
        Our elegant Volterra kernel approach provides sophisticated signal detection
        using advanced mathematical frameworks without empirical validation.
        """
        
        # Evidence that would fail Sakana validation
        failed_sakana_evidence = {
            'snr_analysis': {
                'snr_db': -20.0,  # Undetectable
                'detectable': False
            },
            'real_data_verification': {
                'authentic_data_confirmed': False,
                'synthetic_data_detected': True
            }
        }
        
        analysis_result = plausibility_checker.analyze_claim_plausibility(
            claim_text=sakana_relevant_claim,
            evidence=failed_sakana_evidence
        )
        
        # Should detect plausibility trap and recommend Sakana validation
        assert analysis_result['plausibility_risk_level'] in ['HIGH', 'CRITICAL']
        
        # The evidence structure should be compatible with Sakana validator
        assert 'snr_analysis' in failed_sakana_evidence
        assert 'real_data_verification' in failed_sakana_evidence
        
        # Check that the analysis identifies key risk factors
        risk_factors = analysis_result['risk_factors']
        assert any('sophistication' in factor.lower() for factor in risk_factors)


class TestPlausibilityCheckerIntegration:
    """Integration tests for plausibility checker with other system components."""
    
    def test_integration_with_snr_analyzer_results(self):
        """Test integration with SNR analyzer results."""
        checker = PlausibilityChecker()
        
        # Mock SNR analyzer results
        snr_results = {
            'snr_analysis': {
                'snr_db': 3.5,
                'method': 'hansen',
                'signal_power': 2.1,
                'noise_power': 0.8,
                'detectable': True
            },
            'glens_evaluation': {
                'classification': 'DETECTABLE',
                'sakana_principle_pass': True
            }
        }
        
        # Test claim with moderate sophistication
        claim = "Using GLENS ensemble data, we apply statistical analysis to detect climate signals."
        
        result = checker.analyze_claim_plausibility(claim, snr_results)
        
        assert result['empirical_support_score'] > 0.5  # Should recognize SNR evidence
        assert result['plausibility_risk_level'] in ['LOW', 'MINIMAL']
    
    def test_comprehensive_validation_pipeline(self):
        """Test the complete validation pipeline integration."""
        checker = PlausibilityChecker()
        
        # Simulate a complete research validation scenario
        research_claim = """
        Analysis of NCAR GLENS dataset reveals statistically significant temperature
        response to stratospheric aerosol injection with p < 0.01 confidence level.
        The 20-member ensemble shows consistent signal across all realizations.
        """
        
        comprehensive_evidence = {
            'snr_analysis': {
                'snr_db': 7.8,
                'method': 'hansen',
                'detectable': True
            },
            'statistical_validation': {
                'p_value': 0.003,
                'confidence_level': 0.99,
                'effect_size': 1.2,
                'sample_size': 240
            },
            'real_data_verification': {
                'authentic_data_confirmed': True,
                'institutional_validation': True,
                'dataset_name': 'GLENS',
                'provenance_verified': True
            }
        }
        
        validation_result = checker.analyze_claim_plausibility(
            claim_text=research_claim,
            evidence=comprehensive_evidence
        )
        
        # Should pass all plausibility checks
        assert validation_result['plausibility_assessment'] == 'EMPIRICALLY_GROUNDED'
        assert validation_result['plausibility_risk_level'] == 'MINIMAL'
        assert len(validation_result['protective_factors']) > 0
        assert 'Strong empirical support' in validation_result['protective_factors']


if __name__ == '__main__':
    pytest.main([__file__, '-v'])