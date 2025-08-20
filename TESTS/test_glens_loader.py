"""
Comprehensive Test Suite for GLENS Loader

Tests for the extracted GLENS data loader ensuring functionality, authenticity
verification, Mac M3 optimization, and Sakana Principle integration.

Test Categories:
1. Core functionality tests (load_pair, load_ensemble)
2. Authenticity verification tests
3. Mac M3 optimization tests
4. Error handling and edge cases
5. Integration with Sakana Principle validation
"""

import pytest
import numpy as np
import xarray as xr
import tempfile
import os
import json
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

# Import the GLENS loader
import sys
sys.path.append('/Users/apple/code/Researcher')
from ai_researcher.data.loaders.glens_loader import GLENSLoader, GLENSLoadError, AuthenticityError, SyntheticDataError


class TestGLENSLoader:
    """Comprehensive test suite for GLENS data loader."""
    
    @pytest.fixture
    def temp_data_dir(self):
        """Create temporary directory structure for test data."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create directory structure mimicking GLENS dataset
            base_path = Path(temp_dir)
            model_path = base_path / "CESM1-WACCM"
            exp_path = model_path / "GLENS"
            ctrl_path = model_path / "GLENS_control"
            
            exp_path.mkdir(parents=True)
            ctrl_path.mkdir(parents=True)
            
            yield temp_dir
    
    @pytest.fixture
    def mock_netcdf_data(self):
        """Create mock xarray datasets for testing."""
        # Create realistic climate data
        time = xr.cftime_range("2020-01", "2022-12", freq="MS", calendar="noleap")
        lat = np.linspace(-90, 90, 96)
        lon = np.linspace(0, 357.5, 144)
        
        # Temperature data (realistic values)
        temp_data = 288.15 + 10 * np.sin(np.linspace(0, 4*np.pi, len(time)))[:, None, None] + \
                   20 * np.cos(lat[None, :, None] * np.pi/180) + \
                   np.random.normal(0, 2, (len(time), len(lat), len(lon)))
        
        # Precipitation data (realistic values)
        precip_data = np.abs(5e-6 + 1e-6 * np.sin(lat[None, :, None] * np.pi/180) + \
                            np.random.normal(0, 1e-6, (len(time), len(lat), len(lon))))
        
        exp_ds = xr.Dataset({
            'TREFHT': (['time', 'lat', 'lon'], temp_data),
            'PRECT': (['time', 'lat', 'lon'], precip_data)
        }, coords={
            'time': time,
            'lat': lat,
            'lon': lon
        })
        
        ctrl_ds = xr.Dataset({
            'TREFHT': (['time', 'lat', 'lon'], temp_data + np.random.normal(0, 0.5, temp_data.shape)),
            'PRECT': (['time', 'lat', 'lon'], precip_data + np.random.normal(0, 1e-7, precip_data.shape))
        }, coords={
            'time': time,
            'lat': lat,
            'lon': lon
        })
        
        # Add realistic global attributes
        glens_attrs = {
            'institution': 'NCAR (National Center for Atmospheric Research)',
            'source': 'CESM1(WACCM)',
            'experiment_id': 'GLENS',
            'project_id': 'GLENS',
            'contact': 'glens@ucar.edu',
            'Conventions': 'CF-1.7',
            'doi': '10.5065/D6JH3JXX',
            'title': 'Geoengineering Large Ensemble (GLENS)'
        }
        
        exp_ds.attrs.update(glens_attrs)
        ctrl_ds.attrs.update({**glens_attrs, 'experiment_id': 'GLENS_control'})
        
        return {'experiment': exp_ds, 'control': ctrl_ds}
    
    @pytest.fixture
    def glens_loader(self, temp_data_dir):
        """Create GLENS loader instance with test directory."""
        return GLENSLoader(
            base_dir=temp_data_dir,
            real_data_mandatory=True,
            synthetic_data_forbidden=True,
            mac_m3_optimization=True
        )
    
    def test_loader_initialization(self, glens_loader, temp_data_dir):
        """Test proper initialization of GLENS loader."""
        assert glens_loader.base_dir == Path(temp_data_dir)
        assert glens_loader.real_data_mandatory is True
        assert glens_loader.synthetic_data_forbidden is True
        assert glens_loader.mac_m3_optimization is True
        
        # Check variable definitions
        assert 'TREFHT' in glens_loader.variables
        assert 'PRECT' in glens_loader.variables
        assert 'CLDTOT' in glens_loader.variables
        assert 'BURDEN1' in glens_loader.variables
        
        # Check institutional markers
        assert 'NCAR' in glens_loader.institutional_markers
        assert 'GLENS' in glens_loader.institutional_markers
    
    @patch('ai_researcher.data.loaders.glens_loader.xr.open_mfdataset')
    @patch('ai_researcher.data.loaders.glens_loader.glob.glob')
    def test_load_pair_success(self, mock_glob, mock_open_mfd, glens_loader, mock_netcdf_data):
        """Test successful loading of experiment-control pair."""
        # Setup mocks
        mock_glob.side_effect = [
            ['/path/to/exp/file.nc'],  # Experiment files
            ['/path/to/ctrl/file.nc']  # Control files
        ]
        
        mock_open_mfd.side_effect = [
            mock_netcdf_data['experiment'],
            mock_netcdf_data['control']
        ]
        
        # Mock authenticity verification
        with patch.object(glens_loader, '_verify_file_authenticity') as mock_verify:
            mock_verify.return_value = {'authentic': True}
            
            # Test load_pair
            exp_data, ctrl_data = glens_loader.load_pair(
                model='CESM1-WACCM',
                exp='GLENS',
                ctrl='GLENS_control',
                var='TREFHT'
            )
            
            # Verify results
            assert isinstance(exp_data, xr.DataArray)
            assert isinstance(ctrl_data, xr.DataArray)
            assert exp_data.name == 'TREFHT'
            assert ctrl_data.name == 'TREFHT'
            
            # Check load history
            assert len(glens_loader.load_history) == 1
            load_record = glens_loader.load_history[0]
            assert load_record['model'] == 'CESM1-WACCM'
            assert load_record['experiment'] == 'GLENS'
            assert load_record['variable'] == 'TREFHT'
    
    @patch('ai_researcher.data.loaders.glens_loader.glob.glob')
    def test_load_pair_file_not_found(self, mock_glob, glens_loader):
        """Test handling of missing files."""
        mock_glob.return_value = []  # No files found
        
        with pytest.raises(FileNotFoundError):
            glens_loader.load_pair(
                model='CESM1-WACCM',
                exp='GLENS',
                ctrl='GLENS_control',
                var='TREFHT'
            )
    
    @patch('ai_researcher.data.loaders.glens_loader.xr.open_mfdataset')
    @patch('ai_researcher.data.loaders.glens_loader.glob.glob')
    def test_authenticity_verification_failure(self, mock_glob, mock_open_mfd, glens_loader):
        """Test handling of authenticity verification failure."""
        mock_glob.side_effect = [
            ['/path/to/exp/file.nc'],
            ['/path/to/ctrl/file.nc']
        ]
        
        # Mock authenticity failure
        with patch.object(glens_loader, '_verify_file_authenticity') as mock_verify:
            mock_verify.return_value = {'authentic': False}
            
            with pytest.raises(AuthenticityError):
                glens_loader.load_pair(
                    model='CESM1-WACCM',
                    exp='GLENS',
                    ctrl='GLENS_control',
                    var='TREFHT'
                )
    
    def test_mac_m3_optimization_setup(self, temp_data_dir):
        """Test Mac M3 optimization configuration."""
        loader = GLENSLoader(temp_data_dir, mac_m3_optimization=True)
        
        # Check that dask configuration was applied
        # Note: In real test, would check dask.config values
        chunks = loader._get_optimal_chunks('TREFHT', 5)
        
        assert 'time' in chunks
        assert 'lat' in chunks
        assert 'lon' in chunks
        assert isinstance(chunks['time'], int)
        assert chunks['time'] > 0
    
    def test_optimal_chunks_variable_specific(self, glens_loader):
        """Test variable-specific chunk optimization."""
        # Test different variables
        trefht_chunks = glens_loader._get_optimal_chunks('TREFHT', 5)
        burden_chunks = glens_loader._get_optimal_chunks('BURDEN1', 5)
        prect_chunks = glens_loader._get_optimal_chunks('PRECT', 5)
        
        # BURDEN1 should have larger chunks (smaller files)
        assert burden_chunks['time'] >= trefht_chunks['time']
        
        # PRECT should have smaller chunks (memory intensive)
        assert prect_chunks['time'] <= trefht_chunks['time']
        
        # Test ensemble mode
        ensemble_chunks = glens_loader._get_optimal_chunks('TREFHT', 5, ensemble_mode=True)
        assert ensemble_chunks['time'] <= trefht_chunks['time']  # Smaller for ensemble
    
    def test_file_authenticity_verification(self, glens_loader, mock_netcdf_data, temp_data_dir):
        """Test comprehensive file authenticity verification."""
        # Create a temporary NetCDF file
        test_file = Path(temp_data_dir) / 'test_authentic.nc'
        mock_netcdf_data['experiment'].to_netcdf(test_file)
        
        # Test authentic file
        auth_result = glens_loader._verify_file_authenticity(str(test_file), 'test_dataset')
        
        assert auth_result['authentic'] is True
        assert auth_result['dataset_id'] == 'test_dataset'
        assert 'institutional_metadata' in auth_result['checks']
        assert 'glens_specific' in auth_result['checks']
        assert len(auth_result['institutional_markers_found']) > 0
    
    def test_synthetic_data_detection(self, glens_loader, temp_data_dir):
        """Test synthetic data pattern detection."""
        # Create synthetic data with obvious patterns
        time = xr.cftime_range("2020-01", "2021-12", freq="MS", calendar="noleap")
        lat = np.linspace(-90, 90, 96)
        lon = np.linspace(0, 357.5, 144)
        
        # All identical values (obvious synthetic)
        synthetic_data = np.full((len(time), len(lat), len(lon)), 288.15)
        
        synthetic_ds = xr.Dataset({
            'TREFHT': (['time', 'lat', 'lon'], synthetic_data)
        }, coords={'time': time, 'lat': lat, 'lon': lon})
        
        synthetic_file = Path(temp_data_dir) / 'synthetic.nc'
        synthetic_ds.to_netcdf(synthetic_file)
        
        # Test synthetic detection
        synthetic_analysis = glens_loader._detect_synthetic_patterns(str(synthetic_file))
        
        assert synthetic_analysis['synthetic_likely'] is True
        assert 'All identical values' in synthetic_analysis['indicators']
    
    @patch('ai_researcher.data.loaders.glens_loader.xr.open_mfdataset')
    @patch('ai_researcher.data.loaders.glens_loader.glob.glob')
    def test_ensemble_loading(self, mock_glob, mock_open_mfd, glens_loader, mock_netcdf_data):
        """Test multi-member ensemble loading."""
        # Mock files for 3 ensemble members
        mock_glob.side_effect = [
            ['/path/to/r1i1p1f1/file.nc'],
            ['/path/to/r2i1p1f1/file.nc'],
            ['/path/to/r3i1p1f1/file.nc']
        ]
        
        # Mock datasets for ensemble members
        mock_open_mfd.side_effect = [
            mock_netcdf_data['experiment'],
            mock_netcdf_data['experiment'],
            mock_netcdf_data['experiment']
        ]
        
        # Test ensemble loading
        ensemble_ds = glens_loader.load_ensemble(
            model='CESM1-WACCM',
            exp='GLENS',
            var='TREFHT',
            ensemble_members=['r1i1p1f1', 'r2i1p1f1', 'r3i1p1f1']
        )
        
        assert isinstance(ensemble_ds, xr.Dataset)
        assert 'member' in ensemble_ds.dims
        assert ensemble_ds.sizes['member'] == 3
        assert 'TREFHT' in ensemble_ds.data_vars
    
    def test_precipitation_unit_conversion(self, glens_loader):
        """Test automatic precipitation unit conversion."""
        # Create test data with precipitation
        time = xr.cftime_range("2020-01", "2020-03", freq="MS", calendar="noleap")
        lat = np.linspace(-90, 90, 10)
        lon = np.linspace(0, 350, 10)
        
        # Precipitation in m/s
        prect_ms = np.full((len(time), len(lat), len(lon)), 1e-6)  # 1 μm/s
        
        exp_ds = xr.Dataset({
            'PRECT': (['time', 'lat', 'lon'], prect_ms)
        }, coords={'time': time, 'lat': lat, 'lon': lon})
        
        ctrl_ds = exp_ds.copy()
        
        with patch('ai_researcher.data.loaders.glens_loader.xr.open_mfdataset') as mock_open_mfd, \
             patch('ai_researcher.data.loaders.glens_loader.glob.glob') as mock_glob, \
             patch.object(glens_loader, '_verify_file_authenticity') as mock_verify:
            
            mock_glob.side_effect = [['/exp/file.nc'], ['/ctrl/file.nc']]
            mock_open_mfd.side_effect = [exp_ds, ctrl_ds]
            mock_verify.return_value = {'authentic': True}
            
            exp_data, ctrl_data = glens_loader.load_pair(
                model='CESM1-WACCM',
                exp='GLENS',
                ctrl='GLENS_control',
                var='PRECT'
            )
            
            # Check conversion: 1e-6 m/s * 86400 s/day * 1000 mm/m = 0.0864 mm/day
            expected_mmday = 1e-6 * 86400 * 1000
            np.testing.assert_allclose(exp_data.values, expected_mmday, rtol=1e-10)
            assert exp_data.attrs['units'] == 'mm/day'
    
    def test_quality_checks(self, glens_loader):
        """Test data quality validation."""
        # Create data with quality issues
        time = xr.cftime_range("2020-01", "2020-03", freq="MS", calendar="noleap")
        lat = np.linspace(-90, 90, 10)
        lon = np.linspace(0, 350, 10)
        
        # Temperature data with unrealistic values
        bad_temp = np.full((len(time), len(lat), len(lon)), 500.0)  # 500K too hot
        good_temp = np.full((len(time), len(lat), len(lon)), 288.15)  # Reasonable
        
        bad_data = xr.DataArray(bad_temp, dims=['time', 'lat', 'lon'], 
                               coords={'time': time, 'lat': lat, 'lon': lon})
        good_data = xr.DataArray(good_temp, dims=['time', 'lat', 'lon'],
                                coords={'time': time, 'lat': lat, 'lon': lon})
        
        # Should log warnings for unrealistic values
        with patch('ai_researcher.data.loaders.glens_loader.logger') as mock_logger:
            glens_loader._perform_quality_checks(bad_data, good_data, 'TREFHT')
            
            # Check if warning was logged for temperature range
            warning_logged = any('Temperature values outside reasonable range' in str(call) 
                               for call in mock_logger.warning.call_args_list)
            assert warning_logged
    
    def test_load_statistics(self, glens_loader):
        """Test load statistics tracking."""
        # Initially no loads
        stats = glens_loader.get_load_statistics()
        assert stats['total_loads'] == 0
        
        # Add mock load history
        glens_loader.load_history = [
            {
                'variable': 'TREFHT',
                'load_duration': 1.5,
                'timestamp': datetime.now().isoformat()
            },
            {
                'variable': 'PRECT', 
                'load_duration': 2.1,
                'timestamp': datetime.now().isoformat()
            }
        ]
        
        stats = glens_loader.get_load_statistics()
        assert stats['total_loads'] == 2
        assert stats['successful_loads'] == 2
        assert stats['success_rate'] == 1.0
        assert abs(stats['average_load_duration'] - 1.8) < 0.1
        assert stats['variables_loaded']['TREFHT'] == 1
        assert stats['variables_loaded']['PRECT'] == 1
    
    def test_time_selection(self, glens_loader, mock_netcdf_data):
        """Test year range selection functionality."""
        with patch('ai_researcher.data.loaders.glens_loader.xr.open_mfdataset') as mock_open_mfd, \
             patch('ai_researcher.data.loaders.glens_loader.glob.glob') as mock_glob, \
             patch.object(glens_loader, '_verify_file_authenticity') as mock_verify:
            
            mock_glob.side_effect = [['/exp/file.nc'], ['/ctrl/file.nc']]
            mock_open_mfd.side_effect = [
                mock_netcdf_data['experiment'],
                mock_netcdf_data['control']
            ]
            mock_verify.return_value = {'authentic': True}
            
            # Test with year selection
            exp_data, ctrl_data = glens_loader.load_pair(
                model='CESM1-WACCM',
                exp='GLENS',
                ctrl='GLENS_control',
                var='TREFHT',
                years=(2021, 2021)  # Only 2021
            )
            
            # Check that time selection was applied
            assert exp_data.time.dt.year.min() >= 2021
            assert exp_data.time.dt.year.max() <= 2021


class TestGLENSLoaderIntegration:
    """Integration tests for GLENS loader with other system components."""
    
    def test_sakana_principle_integration(self):
        """Test integration with Sakana Principle validation."""
        # This would test the loader's integration with the Sakana validator
        # when real data enforcement is required
        
        loader = GLENSLoader(
            base_dir='/tmp/test',
            real_data_mandatory=True,
            synthetic_data_forbidden=True
        )
        
        # Verify enforcement flags are set correctly
        assert loader.real_data_mandatory is True
        assert loader.synthetic_data_forbidden is True
        
        # Verify institutional markers include required elements
        required_markers = ['NCAR', 'UCAR', 'GLENS', 'CF-1.7']
        for marker in required_markers:
            assert marker in loader.institutional_markers
    
    def test_snr_analysis_compatibility(self):
        """Test compatibility with SNR analysis requirements."""
        loader = GLENSLoader('/tmp/test')
        
        # Test that loader supports variables needed for SNR analysis
        snr_required_vars = ['TREFHT', 'PRECT']
        for var in snr_required_vars:
            assert var in loader.variables
            assert 'units' in loader.variables[var]
            assert 'description' in loader.variables[var]


class TestGLENSLoaderErrorHandling:
    """Test error handling and edge cases."""
    
    def test_invalid_base_directory(self):
        """Test handling of invalid base directory."""
        with pytest.raises(Exception):
            loader = GLENSLoader('/nonexistent/directory')
            # Attempt to use the loader should fail gracefully
    
    def test_corrupted_netcdf_file(self, temp_data_dir):
        """Test handling of corrupted NetCDF files."""
        loader = GLENSLoader(temp_data_dir)
        
        # Create a corrupted file
        corrupted_file = Path(temp_data_dir) / 'corrupted.nc'
        with open(corrupted_file, 'w') as f:
            f.write('This is not a NetCDF file')
        
        # Test authenticity verification on corrupted file
        auth_result = loader._verify_file_authenticity(str(corrupted_file), 'corrupted')
        assert auth_result['authentic'] is False
        assert len(auth_result['warnings']) > 0
    
    def test_missing_required_attributes(self, temp_data_dir):
        """Test handling of files missing required GLENS attributes."""
        loader = GLENSLoader(temp_data_dir)
        
        # Create NetCDF file without GLENS attributes
        time = xr.cftime_range("2020-01", "2020-02", freq="MS", calendar="noleap")
        data = xr.Dataset({
            'temp': (['time'], np.random.randn(len(time)))
        }, coords={'time': time})
        
        # No GLENS-specific attributes
        data.attrs = {'source': 'Unknown model'}
        
        test_file = Path(temp_data_dir) / 'no_glens_attrs.nc'
        data.to_netcdf(test_file)
        
        auth_result = loader._verify_file_authenticity(str(test_file), 'no_glens')
        assert auth_result['authentic'] is False
        assert auth_result['checks']['glens_specific'] is False


if __name__ == '__main__':
    pytest.main([__file__, '-v'])