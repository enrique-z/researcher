"""
Data Loaders Package

Climate dataset loaders implementing optimal loading patterns for Mac M3 64GB systems.
All loaders enforce authentic data requirements and integrate with Sakana Principle validation.

Available Loaders:
- GLENSLoader: NCAR CESM1-WACCM GLENS dataset loader
- GeoMIPLoader: GeoMIP comparison dataset loader
"""

from .glens_loader import GLENSLoader
from .geomip_loader import GeoMIPLoader

__all__ = ['GLENSLoader', 'GeoMIPLoader']