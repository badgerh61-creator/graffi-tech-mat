# backend/app/services/engines/__init__.py

"""
Simulation engine subpackage.

Contains pluggable simulation engine implementations
(e.g., pseudo-v1, future physx-v1, etc.).
"""

from .pseudo_engine_adapter import PseudoEngine

__all__ = ["PseudoEngine"]
