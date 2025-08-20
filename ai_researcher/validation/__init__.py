"""
AI Researcher Validation Package

This package implements the Sakana Principle validation framework for empirical 
falsification of theoretical claims in AI-generated research papers.

Key Components:
- sakana_validator.py: Core Sakana Principle implementation
- snr_analyzer.py: Signal-to-noise ratio calculations
- plausibility_checker.py: Prevents theoretical claims without empirical backing
"""

from .sakana_validator import SakanaValidator
from .snr_analyzer import SNRAnalyzer
from .plausibility_checker import PlausibilityChecker

__all__ = ['SakanaValidator', 'SNRAnalyzer', 'PlausibilityChecker']