"""
Test Suite for SNR Analyzer

Comprehensive tests for the Signal-to-Noise Ratio analysis module including
Hansen's classical methodology, GLENS project thresholds, and integration
with empirical falsification framework.
"""

import pytest
import numpy as np
import xarray as xr
from datetime import datetime
from unittest.mock import Mock, patch

import sys
sys.path.append('/Users/apple/code/Researcher')
from ai_researcher.validation.snr_analyzer import SNRAnalyzer


class TestSNRAnalyzer:
    """Test suite for SNR analysis functionality."""
    
    @pytest.fixture
    def snr_analyzer(self):
        """Create SNR analyzer instance."""
        return SNRAnalyzer()
    
    @pytest.fixture
    def sample_climate_data(self):
        """Create sample climate data for testing."""
        # Create realistic time series data
        time = np.arange(100)  # 100 time steps
        
        # Signal: gradual warming trend
        signal = 0.02 * time + 0.1 * np.sin(2 * np.pi * time / 12)  # Trend + seasonal
        
        # Noise: natural variability
        noise = np.random.normal(0, 0.5, len(time))
        
        # Combined: signal + noise
        observed = signal + noise
        
        return {
            'signal': signal,
            'noise': noise,
            'observed': observed,
            'time': time
        }
    
    def test_analyzer_initialization(self, snr_analyzer):
        """Test proper initialization of SNR analyzer."""
        assert snr_analyzer.hansen_methodology_enabled is True
        assert snr_analyzer.glens_thresholds is not None
        
        # Check GLENS thresholds
        thresholds = snr_analyzer.glens_thresholds
        assert 'undetectable_limit' in thresholds
        assert 'minimum_detectable' in thresholds
        assert 'standard_threshold' in thresholds
        assert 'high_confidence' in thresholds
        
        # Verify threshold values
        assert thresholds['undetectable_limit'] == -15.54
        assert thresholds['minimum_detectable'] == 0.0
        assert thresholds['standard_threshold'] == 6.0
        assert thresholds['high_confidence'] == 9.5
    
    def test_calculate_snr_hansen_method(self, snr_analyzer, sample_climate_data):
        """Test SNR calculation using Hansen's classical methodology."""
        signal = sample_climate_data['signal']
        noise = sample_climate_data['noise']
        
        # Test Hansen method
        snr_result = snr_analyzer.calculate_snr(signal, noise, method='hansen')
        
        assert isinstance(snr_result, dict)
        assert 'snr_linear' in snr_result
        assert 'snr_db' in snr_result
        assert 'method' in snr_result
        assert 'signal_power' in snr_result
        assert 'noise_power' in snr_result
        
        assert snr_result['method'] == 'hansen'
        assert snr_result['snr_linear'] > 0
        assert isinstance(snr_result['snr_db'], float)
        
        # Check mathematical relationship: SNR_dB = 10 * log10(SNR_linear)
        expected_db = 10 * np.log10(snr_result['snr_linear'])
        np.testing.assert_allclose(snr_result['snr_db'], expected_db, rtol=1e-10)
    
    def test_calculate_snr_welch_method(self, snr_analyzer, sample_climate_data):
        """Test SNR calculation using Welch's method."""
        signal = sample_climate_data['signal']
        noise = sample_climate_data['noise']
        
        snr_result = snr_analyzer.calculate_snr(signal, noise, method='welch')
        
        assert snr_result['method'] == 'welch'
        assert 'frequency_analysis' in snr_result
        assert 'peak_frequency' in snr_result['frequency_analysis']
        assert 'bandwidth' in snr_result['frequency_analysis']
    
    def test_snr_with_xarray_data(self, snr_analyzer):
        """Test SNR calculation with xarray DataArrays."""
        # Create xarray data
        time = np.arange(50)
        signal_data = 0.1 * time
        noise_data = np.random.normal(0, 0.2, len(time))
        
        signal_da = xr.DataArray(signal_data, dims=['time'], coords={'time': time})
        noise_da = xr.DataArray(noise_data, dims=['time'], coords={'time': time})
        
        snr_result = snr_analyzer.calculate_snr(signal_da, noise_da, method='hansen')
        
        assert isinstance(snr_result, dict)
        assert snr_result['method'] == 'hansen'
        assert 'snr_db' in snr_result
    
    def test_glens_threshold_evaluation(self, snr_analyzer):
        """Test evaluation against GLENS project thresholds."""
        # Test different SNR values
        test_cases = [
            {'snr_db': -20.0, 'expected': 'UNDETECTABLE'},
            {'snr_db': -10.0, 'expected': 'BELOW_THRESHOLD'},
            {'snr_db': 3.0, 'expected': 'MARGINALLY_DETECTABLE'},
            {'snr_db': 7.0, 'expected': 'DETECTABLE'},
            {'snr_db': 12.0, 'expected': 'HIGH_CONFIDENCE'}
        ]
        
        for case in test_cases:
            threshold_result = snr_analyzer.evaluate_glens_thresholds(case['snr_db'])
            
            assert threshold_result['classification'] == case['expected']
            assert threshold_result['snr_db'] == case['snr_db']
            assert 'meets_minimum' in threshold_result
            assert 'sakana_principle_pass' in threshold_result
    
    def test_sakana_principle_integration(self, snr_analyzer):
        """Test integration with Sakana Principle validation."""
        # Test case that should pass Sakana Principle
        high_snr = 8.0  # Above minimum detectable threshold
        result = snr_analyzer.evaluate_glens_thresholds(high_snr)
        
        assert result['sakana_principle_pass'] is True
        assert result['meets_minimum'] is True
        
        # Test case that should fail Sakana Principle
        low_snr = -20.0  # Below undetectable limit
        result = snr_analyzer.evaluate_glens_thresholds(low_snr)
        
        assert result['sakana_principle_pass'] is False
        assert result['meets_minimum'] is False
    
    def test_comprehensive_analysis(self, snr_analyzer, sample_climate_data):
        """Test comprehensive SNR analysis with full validation."""
        signal = sample_climate_data['signal']
        observed = sample_climate_data['observed']
        
        analysis = snr_analyzer.comprehensive_analysis(
            theoretical_signal=signal,
            real_dataset=observed,
            experiment_name='test_experiment'
        )
        
        assert isinstance(analysis, dict)
        assert 'experiment_name' in analysis
        assert 'snr_analysis' in analysis
        assert 'glens_evaluation' in analysis
        assert 'sakana_validation' in analysis
        assert 'recommendations' in analysis
        
        # Check nested structure
        snr_analysis = analysis['snr_analysis']
        assert 'hansen_method' in snr_analysis
        assert 'welch_method' in snr_analysis
        
        glens_eval = analysis['glens_evaluation']
        assert 'classification' in glens_eval
        assert 'sakana_principle_pass' in glens_eval
    
    def test_noise_floor_estimation(self, snr_analyzer):
        """Test noise floor estimation functionality."""
        # Create data with known noise characteristics
        np.random.seed(42)  # Reproducible results
        time = np.arange(1000)
        
        # Pure noise with known standard deviation
        noise_std = 0.3
        noise_data = np.random.normal(0, noise_std, len(time))
        
        noise_floor = snr_analyzer.estimate_noise_floor(noise_data)
        
        assert isinstance(noise_floor, dict)
        assert 'noise_power' in noise_floor
        assert 'noise_std' in noise_floor
        assert 'estimation_method' in noise_floor
        
        # Check that estimated noise std is close to actual
        estimated_std = noise_floor['noise_std']
        np.testing.assert_allclose(estimated_std, noise_std, rtol=0.1)
    
    def test_detectability_assessment(self, snr_analyzer):
        """Test signal detectability assessment."""
        # Test various signal strengths
        signal_strengths = [0.1, 0.5, 1.0, 2.0]
        noise_level = 0.5
        
        for signal_strength in signal_strengths:
            time = np.arange(100)
            signal = signal_strength * np.ones(len(time))
            noise = np.random.normal(0, noise_level, len(time))
            
            assessment = snr_analyzer.assess_detectability(signal, noise)
            
            assert isinstance(assessment, dict)
            assert 'detectable' in assessment
            assert 'confidence_level' in assessment
            assert 'required_improvement' in assessment
            
            # Stronger signals should be more detectable
            if signal_strength >= noise_level:
                assert assessment['detectable'] is True
    
    def test_temporal_snr_analysis(self, snr_analyzer):
        """Test time-varying SNR analysis."""
        # Create signal that grows stronger over time
        time = np.arange(200)
        
        # Signal grows from weak to strong
        signal = 0.01 * time  # Linear growth
        noise = np.random.normal(0, 0.1, len(time))
        combined = signal + noise
        
        temporal_analysis = snr_analyzer.analyze_temporal_snr(
            combined, 
            window_size=50,
            overlap=25
        )
        
        assert isinstance(temporal_analysis, dict)
        assert 'time_windows' in temporal_analysis
        assert 'snr_evolution' in temporal_analysis
        assert 'detection_onset' in temporal_analysis
        
        # SNR should generally increase over time
        snr_values = temporal_analysis['snr_evolution']
        assert len(snr_values) > 1
        
        # Check for detection onset
        if temporal_analysis['detection_onset'] is not None:
            assert isinstance(temporal_analysis['detection_onset'], int)
    
    def test_multi_variable_snr(self, snr_analyzer):
        """Test SNR analysis for multiple climate variables."""
        variables = ['temperature', 'precipitation', 'cloud_cover']
        
        # Create synthetic data for each variable
        time = np.arange(100)
        data = {}
        
        for var in variables:
            # Different signal characteristics for each variable
            if var == 'temperature':
                signal = 0.02 * time  # Warming trend
                noise = np.random.normal(0, 0.5, len(time))
            elif var == 'precipitation':
                signal = 0.001 * time  # Slight increase
                noise = np.random.normal(0, 0.1, len(time))
            else:  # cloud_cover
                signal = -0.01 * time  # Slight decrease
                noise = np.random.normal(0, 0.2, len(time))
            
            data[var] = signal + noise
        
        multi_analysis = snr_analyzer.analyze_multiple_variables(data)
        
        assert isinstance(multi_analysis, dict)
        assert len(multi_analysis) == len(variables)
        
        for var in variables:
            assert var in multi_analysis
            assert 'snr_db' in multi_analysis[var]
            assert 'glens_classification' in multi_analysis[var]
    
    def test_error_handling(self, snr_analyzer):
        """Test error handling for invalid inputs."""
        # Test with invalid method
        with pytest.raises(ValueError):
            snr_analyzer.calculate_snr([1, 2, 3], [1, 2, 3], method='invalid_method')
        
        # Test with mismatched array lengths
        with pytest.raises(ValueError):
            snr_analyzer.calculate_snr([1, 2, 3], [1, 2], method='hansen')
        
        # Test with all-zero signal
        zero_signal = np.zeros(10)
        noise = np.random.randn(10)
        
        result = snr_analyzer.calculate_snr(zero_signal, noise, method='hansen')
        assert result['snr_db'] == -np.inf or result['snr_db'] < -100
    
    def test_statistical_significance(self, snr_analyzer):
        """Test statistical significance assessment."""
        # Create signal with known properties
        np.random.seed(123)
        time = np.arange(200)
        
        # Weak but consistent signal
        true_signal = 0.05 * time
        noise = np.random.normal(0, 1.0, len(time))
        observed = true_signal + noise
        
        significance = snr_analyzer.assess_statistical_significance(
            observed, 
            confidence_level=0.95
        )
        
        assert isinstance(significance, dict)
        assert 'significant' in significance
        assert 'p_value' in significance
        assert 'confidence_level' in significance
        assert 'test_statistic' in significance
    
    def test_analysis_history(self, snr_analyzer):
        """Test analysis history tracking."""
        # Initially no history
        assert len(snr_analyzer.analysis_history) == 0
        
        # Perform analysis
        signal = np.array([1, 2, 3, 4, 5])
        noise = np.array([0.1, 0.2, 0.1, 0.3, 0.2])
        
        snr_analyzer.calculate_snr(signal, noise, method='hansen')
        
        # Check history was recorded
        assert len(snr_analyzer.analysis_history) == 1
        
        history_entry = snr_analyzer.analysis_history[0]
        assert 'timestamp' in history_entry
        assert 'method' in history_entry
        assert 'snr_db' in history_entry
    
    def test_glens_specific_scenarios(self, snr_analyzer):
        """Test scenarios specific to GLENS project requirements."""
        # Test the critical -15.54 dB threshold from Sakana analysis
        critical_snr = -15.54
        
        result = snr_analyzer.evaluate_glens_thresholds(critical_snr)
        
        assert result['classification'] == 'UNDETECTABLE'
        assert result['sakana_principle_pass'] is False
        assert 'undetectable_limit' in result['threshold_details']
        
        # Test just above the critical threshold
        barely_detectable = -15.0
        result = snr_analyzer.evaluate_glens_thresholds(barely_detectable)
        
        # Should still be below minimum but not undetectable
        assert result['classification'] in ['BELOW_THRESHOLD', 'UNDETECTABLE']
        
        # Test SAI signal detection scenario
        sai_snr = 8.0  # Typical SAI signal strength
        result = snr_analyzer.evaluate_glens_thresholds(sai_snr)
        
        assert result['classification'] in ['DETECTABLE', 'HIGH_CONFIDENCE']
        assert result['sakana_principle_pass'] is True


class TestSNRAnalyzerIntegration:
    """Integration tests for SNR analyzer with other system components."""
    
    def test_integration_with_glens_loader(self):
        """Test integration with GLENS data loader."""
        # This would test how SNR analyzer works with real GLENS data
        analyzer = SNRAnalyzer()
        
        # Mock GLENS data structure
        mock_glens_data = {
            'experiment': np.random.randn(100),
            'control': np.random.randn(100)
        }
        
        # Calculate signal as difference
        signal = mock_glens_data['experiment'] - mock_glens_data['control']
        noise = mock_glens_data['control']  # Treat control as noise baseline
        
        result = analyzer.calculate_snr(signal, noise, method='hansen')
        
        assert isinstance(result, dict)
        assert 'snr_db' in result
        
        # Should integrate with GLENS thresholds
        threshold_eval = analyzer.evaluate_glens_thresholds(result['snr_db'])
        assert 'sakana_principle_pass' in threshold_eval
    
    def test_integration_with_sakana_validator(self):
        """Test integration with Sakana Principle validator."""
        analyzer = SNRAnalyzer()
        
        # Test data that should pass Sakana validation
        strong_signal = np.array([0, 1, 2, 3, 4, 5])
        weak_noise = np.array([0.1, 0.1, 0.2, 0.1, 0.2, 0.1])
        
        snr_result = analyzer.calculate_snr(strong_signal, weak_noise, method='hansen')
        glens_eval = analyzer.evaluate_glens_thresholds(snr_result['snr_db'])
        
        # For Sakana integration
        sakana_evidence = {
            'snr_analysis': snr_result,
            'glens_evaluation': glens_eval,
            'real_data_verification': {'authentic_data_confirmed': True}
        }
        
        assert sakana_evidence['snr_analysis']['snr_db'] > -15.54  # Above undetectable
        assert sakana_evidence['glens_evaluation']['sakana_principle_pass'] is True


if __name__ == '__main__':
    pytest.main([__file__, '-v'])