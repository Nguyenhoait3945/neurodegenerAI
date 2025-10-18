"""
Shared library for Neuro-Trends Suite.

This package provides common utilities, configurations, and components
used across both NeuroDegenerAI and Trend Detector projects.
"""

__version__ = "0.1.0"
__author__ = "Neuro-Trends Team"

from .lib.config import Settings, get_settings
from .lib.logging import setup_logging, get_logger
from .lib.metrics import MetricsCollector
from .lib.viz import VisualizationHelper
from .lib.ml_utils import MLUtils
from .lib.io_utils import IOUtils

__all__ = [
    "Settings",
    "get_settings", 
    "setup_logging",
    "get_logger",
    "MetricsCollector",
    "VisualizationHelper",
    "MLUtils",
    "IOUtils",
]
