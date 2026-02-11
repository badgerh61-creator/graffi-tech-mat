# backend/app/models/export.py
"""
LEGACY MODEL — DISABLED

This file previously defined ExportRecord (Phase E).
It is intentionally disabled in Phase M+.

DO NOT:
- Add fields
- Add logic
- Re-enable mappings

Kept ONLY to satisfy legacy imports.
"""

from app.db.base import Base


class ExportRecord(Base):
    """
    LEGACY PLACEHOLDER — NOT MAPPED
    """

    __abstract__ = True

