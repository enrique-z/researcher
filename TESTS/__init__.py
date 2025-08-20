"""
Test Suite for AI Research Framework Integration

This package contains comprehensive tests for the AI Research Framework Integration
system, covering all core components including GLENS data loading, SNR analysis,
Sakana Principle validation, and plausibility checking.

Test Structure:
- test_glens_loader.py: GLENS dataset loader functionality and Mac M3 optimization
- test_snr_analyzer.py: Signal-to-Noise Ratio analysis and Hansen methodology
- test_sakana_validator.py: Sakana Principle validation and empirical falsification
- test_plausibility_checker.py: Plausibility trap detection and prevention

Usage:
    Run all tests: pytest TESTS/
    Run specific module: pytest TESTS/test_glens_loader.py -v
    Run with coverage: pytest TESTS/ --cov=ai_researcher
"""

import sys
from pathlib import Path

# Add the main project directory to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

__version__ = "1.0.0"
__author__ = "AI Research Framework Integration Team"