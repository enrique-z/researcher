# AI Research Framework Integration - Test Suite

This directory contains comprehensive tests for the AI Research Framework Integration system, ensuring robust validation of all core components including GLENS data loading, SNR analysis, Sakana Principle validation, and plausibility checking.

## Test Structure

### Core Test Modules

- **`test_glens_loader.py`** - GLENS dataset loader functionality
  - Mac M3 optimization testing
  - Authenticity verification
  - NetCDF file processing
  - Ensemble data loading
  - Error handling and edge cases

- **`test_snr_analyzer.py`** - Signal-to-Noise Ratio analysis
  - Hansen's classical methodology
  - GLENS project thresholds (-15.54 dB undetectable limit)
  - Temporal SNR analysis
  - Multi-variable SNR calculations
  - Integration with empirical falsification

- **`test_sakana_validator.py`** - Sakana Principle validation
  - Empirical falsification framework
  - Real data enforcement (`REAL_DATA_MANDATORY=true`)
  - Plausibility trap prevention
  - Statistical significance validation
  - Historical case analysis

- **`test_plausibility_checker.py`** - Plausibility trap detection
  - Theoretical sophistication analysis
  - Empirical support assessment
  - Red flag pattern detection
  - Risk level classification
  - Quantitative parameter grounding

### Supporting Files

- **`conftest.py`** - Shared fixtures and test configuration
- **`pytest.ini`** - Pytest configuration and markers
- **`__init__.py`** - Test package initialization
- **`README.md`** - This documentation file

## Running Tests

### Prerequisites

```bash
# Install test dependencies
pip install pytest pytest-cov pytest-mock xarray numpy scipy

# Ensure the main package is installed
pip install -e /Users/apple/code/Researcher
```

### Basic Usage

```bash
# Run all tests
pytest TESTS/

# Run with verbose output
pytest TESTS/ -v

# Run specific test module
pytest TESTS/test_glens_loader.py -v

# Run specific test function
pytest TESTS/test_snr_analyzer.py::TestSNRAnalyzer::test_calculate_snr_hansen_method -v
```

### Test Categories

```bash
# Run only unit tests
pytest TESTS/ -m unit

# Run only integration tests
pytest TESTS/ -m integration

# Skip slow tests
pytest TESTS/ -m "not slow"

# Run tests by component
pytest TESTS/ -m glens          # GLENS loader tests
pytest TESTS/ -m snr            # SNR analysis tests
pytest TESTS/ -m sakana         # Sakana validation tests
pytest TESTS/ -m plausibility   # Plausibility checking tests
```

### Coverage Analysis

```bash
# Run tests with coverage report
pytest TESTS/ --cov=ai_researcher --cov-report=html

# View coverage report
open htmlcov/index.html
```

## Test Coverage Areas

### 1. GLENS Data Loader Tests

**Core Functionality:**
- ✅ Paired experiment/control data loading
- ✅ Multi-member ensemble loading
- ✅ Calendar conversion and time alignment
- ✅ Unit conversions (precipitation m/s → mm/day)
- ✅ Mac M3 optimized chunking strategies

**Data Authenticity:**
- ✅ Institutional metadata verification (NCAR/UCAR markers)
- ✅ GLENS-specific attribute validation
- ✅ Synthetic data pattern detection
- ✅ Provenance chain verification
- ✅ CF compliance checking

**Error Handling:**
- ✅ Missing file scenarios
- ✅ Corrupted NetCDF handling
- ✅ Authentication failures
- ✅ Quality check warnings

### 2. SNR Analyzer Tests

**Analysis Methods:**
- ✅ Hansen's classical methodology
- ✅ Welch's power spectral density method
- ✅ Temporal SNR evolution analysis
- ✅ Multi-variable SNR calculations

**GLENS Thresholds:**
- ✅ -15.54 dB undetectable limit validation
- ✅ 0 dB minimum detectable threshold
- ✅ 6 dB standard detection threshold
- ✅ 9.5 dB high confidence threshold

**Integration:**
- ✅ xarray DataArray compatibility
- ✅ Sakana Principle threshold evaluation
- ✅ Statistical significance assessment
- ✅ Analysis history tracking

### 3. Sakana Validator Tests

**Core Validation:**
- ✅ Theoretical claim validation
- ✅ Empirical falsification framework
- ✅ Real data enforcement mechanisms
- ✅ Statistical significance validation

**Plausibility Prevention:**
- ✅ Plausibility trap detection
- ✅ High sophistication + low evidence scenarios
- ✅ Synthetic data rejection
- ✅ SNR threshold enforcement

**Historical Cases:**
- ✅ Hangzhou case analysis (Volterra kernel spectroscopy)
- ✅ -15.54 dB critical threshold validation
- ✅ Lessons learned implementation

### 4. Plausibility Checker Tests

**Sophistication Analysis:**
- ✅ Mathematical complexity assessment
- ✅ Theoretical depth evaluation
- ✅ Sophistication indicator detection
- ✅ Pattern matching algorithms

**Empirical Support:**
- ✅ Textual evidence analysis
- ✅ Quantitative evidence validation
- ✅ Data authenticity verification
- ✅ Support level classification

**Risk Assessment:**
- ✅ Risk factor identification
- ✅ Protective factor recognition
- ✅ Mathematical risk scoring formula
- ✅ Recommendation generation

## Key Test Scenarios

### 1. Successful Validation (Well-Grounded Research)

```python
# Example: Strong empirical evidence with moderate sophistication
claim = "GLENS ensemble analysis shows significant temperature response"
evidence = {
    'snr_analysis': {'snr_db': 8.7, 'detectable': True},
    'statistical_validation': {'p_value': 0.001, 'sample_size': 240},
    'real_data_verification': {'authentic_data_confirmed': True}
}
# Expected: PASS, EMPIRICALLY_GROUNDED, LOW_RISK
```

### 2. Plausibility Trap Detection (Critical Risk)

```python
# Example: High sophistication with inadequate empirical support
claim = "Novel Volterra kernel eigenvalue optimization framework"
evidence = {
    'snr_analysis': {'snr_db': -15.54, 'detectable': False},
    'real_data_verification': {'synthetic_data_detected': True}
}
# Expected: FAIL, PLAUSIBILITY_TRAP_LIKELY, CRITICAL_RISK
```

### 3. Moderate Risk Scenario (Requires Additional Validation)

```python
# Example: Moderate sophistication with weak but present evidence
claim = "GLENS data suggests potential signal detection improvements"
evidence = {
    'snr_analysis': {'snr_db': 2.0, 'detectable': True},
    'statistical_validation': {'p_value': 0.08}  # Marginally significant
}
# Expected: REQUIRES_VALIDATION, MODERATE_RISK
```

## Integration Testing

The test suite includes comprehensive integration tests that verify:

1. **Cross-Component Integration:**
   - GLENS Loader → SNR Analyzer data flow
   - SNR Analyzer → Sakana Validator threshold checking
   - Plausibility Checker → Sakana Validator evidence integration

2. **End-to-End Workflows:**
   - Complete validation pipeline execution
   - Multi-stage empirical falsification
   - Historical case reproduction

3. **Mac M3 Optimization:**
   - Memory usage patterns
   - Chunking strategy effectiveness
   - Performance under realistic loads

## Continuous Integration

The test suite is designed for CI/CD integration:

```yaml
# Example GitHub Actions workflow
- name: Run Test Suite
  run: |
    pytest TESTS/ --junitxml=test-results.xml
    pytest TESTS/ --cov=ai_researcher --cov-report=xml
```

## Test Data Management

- **Fixtures:** Shared test data created in `conftest.py`
- **Mock Data:** Realistic climate datasets for testing
- **Temporary Files:** Automatic cleanup using pytest temporary directories
- **Reproducibility:** Fixed random seeds for consistent results

## Debugging Failed Tests

```bash
# Run with detailed output
pytest TESTS/test_glens_loader.py::test_function_name -vvv -s

# Drop into debugger on failure
pytest TESTS/ --pdb

# Only run failed tests from last run
pytest TESTS/ --lf

# Stop on first failure
pytest TESTS/ -x
```

## Performance Testing

```bash
# Run performance-sensitive tests
pytest TESTS/ -m "not slow" --durations=10

# Profile memory usage (requires pytest-monitor)
pytest TESTS/ --monitor

# Benchmark specific functions
pytest TESTS/test_glens_loader.py -k "load_pair" --benchmark-only
```

## Contributing Test Cases

When adding new functionality:

1. **Add corresponding tests** in the appropriate test module
2. **Include edge cases** and error conditions
3. **Add integration tests** for cross-component functionality
4. **Update fixtures** in `conftest.py` if needed
5. **Document test purpose** and expected behavior

## Test Quality Standards

- **Coverage Target:** >90% code coverage
- **Performance:** Tests should complete in <5 minutes total
- **Reliability:** All tests must be deterministic and reproducible
- **Documentation:** Each test function should have clear docstrings
- **Isolation:** Tests should not depend on external services or files

---

This comprehensive test suite ensures the reliability and correctness of the AI Research Framework Integration system, with particular focus on preventing plausibility trap scenarios and maintaining the highest standards of empirical validation.