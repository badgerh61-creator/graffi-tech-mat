"""
Legacy kernel bridge.

Delegates directly to studio kernel.
No logic allowed here.
"""

from app.studio import execute_tool

__all__ = ["execute_tool"]

