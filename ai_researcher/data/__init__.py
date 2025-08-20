"""
AI Researcher Data Package

This package provides data loading, processing, and validation capabilities
for the AI Research Framework Integration system.

Key Components:
- loaders/: Data loading modules for various climate datasets (GLENS, GeoMIP, etc.)
- downloader.py: Orchestrated data downloading with authenticity verification
- needs_detector.py: Automatic data requirement detection from research topics
- authenticity_verifier.py: Real-time synthetic data prevention and verification

Data Authenticity Enforcement:
- REAL_DATA_MANDATORY=true: Enforces authentic dataset usage
- SYNTHETIC_DATA_FORBIDDEN=true: Prevents synthetic data contamination
- Institutional verification through NCAR/UCAR/NOAA provenance tracking
"""

from .loaders.glens_loader import GLENSLoader
from .loaders.geomip_loader import GeoMIPLoader
from .downloader import DataDownloader
from .needs_detector import DataNeedsDetector
from .authenticity_verifier import AuthenticityVerifier

__all__ = [
    'GLENSLoader', 
    'GeoMIPLoader', 
    'DataDownloader', 
    'DataNeedsDetector', 
    'AuthenticityVerifier'
]