"""
Pytest Configuration and Shared Fixtures

Global configuration and shared fixtures for the AI Research Framework test suite.
"""

import pytest
import numpy as np
import xarray as xr
import tempfile
import os
from pathlib import Path
from datetime import datetime
import warnings

# Suppress warnings during testing
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

@pytest.fixture(scope="session")
def test_data_dir():
    """Create a temporary directory for test data that persists for the session."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir

@pytest.fixture(scope="session") 
def sample_climate_dataset():
    """Create a realistic climate dataset for testing."""
    # Create time dimension (monthly data for 5 years)
    time = xr.cftime_range("2020-01", "2024-12", freq="MS", calendar="noleap")
    
    # Create spatial dimensions
    lat = np.linspace(-90, 90, 96)  # ~2-degree resolution
    lon = np.linspace(0, 357.5, 144)  # ~2.5-degree resolution
    
    # Create realistic temperature data (in Kelvin)
    temp_base = 288.15  # Global mean temperature
    temp_seasonal = 10 * np.sin(2 * np.pi * np.arange(len(time)) / 12)  # Seasonal cycle
    temp_latitudinal = 20 * np.cos(lat * np.pi / 180)  # Latitudinal gradient
    temp_trend = 0.02 * np.arange(len(time))  # Warming trend
    
    # Broadcast and add random variability
    temp_data = (temp_base + 
                temp_seasonal[:, None, None] + 
                temp_latitudinal[None, :, None] + 
                temp_trend[:, None, None] +
                np.random.normal(0, 2, (len(time), len(lat), len(lon))))
    
    # Create realistic precipitation data (in m/s)
    precip_base = 3e-6  # Global mean precipitation
    precip_seasonal = 1e-6 * np.sin(2 * np.pi * np.arange(len(time)) / 12)
    precip_latitudinal = 2e-6 * np.abs(np.sin(lat * np.pi / 180))
    precip_noise = np.abs(np.random.normal(0, 1e-6, (len(time), len(lat), len(lon))))
    
    precip_data = (precip_base + 
                  precip_seasonal[:, None, None] + 
                  precip_latitudinal[None, :, None] + 
                  precip_noise)
    
    # Create dataset
    dataset = xr.Dataset({
        'TREFHT': (['time', 'lat', 'lon'], temp_data, {
            'units': 'K',
            'long_name': 'Reference Height Temperature',
            'standard_name': '2m_temperature'
        }),
        'PRECT': (['time', 'lat', 'lon'], precip_data, {
            'units': 'm/s', 
            'long_name': 'Precipitation Rate',
            'standard_name': 'precipitation_flux'
        })
    }, coords={
        'time': time,
        'lat': (['lat'], lat, {'units': 'degrees_north', 'long_name': 'Latitude'}),
        'lon': (['lon'], lon, {'units': 'degrees_east', 'long_name': 'Longitude'})
    })
    
    # Add realistic global attributes
    dataset.attrs = {
        'institution': 'NCAR (National Center for Atmospheric Research)',
        'source': 'CESM1(WACCM)',
        'experiment_id': 'GLENS',
        'project_id': 'GLENS',
        'contact': 'glens@ucar.edu',
        'Conventions': 'CF-1.7',
        'doi': '10.5065/D6JH3JXX',
        'title': 'Geoengineering Large Ensemble (GLENS)',
        'creation_date': datetime.now().isoformat()
    }
    
    return dataset

@pytest.fixture
def mock_snr_data():
    """Create mock SNR analysis data for testing."""
    time = np.arange(100)
    
    # Signal: climate change trend
    signal = 0.03 * time + 0.2 * np.sin(2 * np.pi * time / 12)
    
    # Noise: natural variability
    np.random.seed(42)  # Reproducible
    noise = np.random.normal(0, 0.5, len(time))
    
    # Observed = signal + noise
    observed = signal + noise
    
    return {
        'time': time,
        'signal': signal,
        'noise': noise,
        'observed': observed,
        'true_snr_db': 10 * np.log10(np.var(signal) / np.var(noise))
    }

@pytest.fixture
def sample_validation_evidence():
    """Create sample evidence for validation testing."""
    return {
        'snr_analysis': {
            'snr_db': 6.2,
            'method': 'hansen',
            'signal_power': 2.1,
            'noise_power': 0.8,
            'detectable': True,
            'confidence_level': 0.95
        },
        'statistical_validation': {
            'p_value': 0.003,
            'confidence_interval': [1.1, 2.9],
            'sample_size': 240,
            'effect_size': 0.7,
            'power': 0.89
        },
        'real_data_verification': {
            'authentic_data_confirmed': True,
            'institutional_validation': True,
            'dataset_name': 'GLENS',
            'data_source': 'NCAR CESM1-WACCM',
            'provenance_verified': True,
            'synthetic_data_detected': False,
            'doi': '10.5065/D6JH3JXX'
        }
    }

@pytest.fixture
def plausibility_trap_scenario():
    """Create a typical plausibility trap scenario for testing."""
    return {
        'claim': {
            'text': """
            We propose a novel Volterra kernel spectroscopy framework utilizing advanced 
            eigenvalue decomposition and stochastic optimization techniques. This sophisticated 
            approach employs nonlinear dynamical systems theory with asymptotic perturbation 
            analysis to achieve elegant mathematical formulations for climate signal detection.
            """,
            'sophistication_level': 'VERY_HIGH',
            'mathematical_complexity': 'ADVANCED',
            'empirical_grounding': 'MINIMAL'
        },
        'evidence': {
            'snr_analysis': {
                'snr_db': -18.2,  # Undetectable
                'detectable': False
            },
            'statistical_validation': None,
            'real_data_verification': {
                'authentic_data_confirmed': False,
                'synthetic_data_detected': True
            }
        },
        'expected_outcome': {
            'plausibility_trap_risk': 'CRITICAL',
            'sakana_principle_pass': False,
            'recommendation': 'REJECT'
        }
    }

@pytest.fixture
def well_grounded_scenario():
    """Create a well-grounded research scenario for testing."""
    return {
        'claim': {
            'text': """
            Analysis of NCAR GLENS ensemble data reveals statistically significant temperature 
            response to stratospheric aerosol injection. Using 20-member ensemble with 240 
            monthly observations, we observe p < 0.001 with 95% confidence intervals excluding zero.
            """,
            'sophistication_level': 'MODERATE',
            'empirical_grounding': 'STRONG'
        },
        'evidence': {
            'snr_analysis': {
                'snr_db': 8.7,
                'detectable': True,
                'method': 'hansen'
            },
            'statistical_validation': {
                'p_value': 0.0008,
                'confidence_level': 0.95,
                'sample_size': 240
            },
            'real_data_verification': {
                'authentic_data_confirmed': True,
                'dataset_name': 'GLENS',
                'institutional_validation': True
            }
        },
        'expected_outcome': {
            'plausibility_trap_risk': 'MINIMAL',
            'sakana_principle_pass': True,
            'recommendation': 'ACCEPT'
        }
    }

# Test configuration
def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )

def pytest_collection_modifyitems(config, items):
    """Automatically mark tests based on their location/name."""
    for item in items:
        # Mark integration tests
        if "integration" in item.nodeid.lower():
            item.add_marker(pytest.mark.integration)
        # Mark slow tests
        if "comprehensive" in item.name.lower() or "full" in item.name.lower():
            item.add_marker(pytest.mark.slow)
        # Default to unit test
        if not any(marker.name in ["integration", "slow"] for marker in item.iter_markers()):
            item.add_marker(pytest.mark.unit)

# Session-wide setup and teardown
@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Set up the test environment before running tests."""
    # Set numpy random seed for reproducible tests
    np.random.seed(42)
    
    # Set environment variables for testing
    os.environ['TESTING'] = 'true'
    os.environ['SAKANA_PRINCIPLE_STRICT'] = 'true'
    
    yield
    
    # Cleanup after all tests
    if 'TESTING' in os.environ:
        del os.environ['TESTING']
    if 'SAKANA_PRINCIPLE_STRICT' in os.environ:
        del os.environ['SAKANA_PRINCIPLE_STRICT']