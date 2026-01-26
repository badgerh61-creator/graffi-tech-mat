# backend/app/models/snapshot.py

"""
Snapshot compatibility alias.

This module exists to provide a stable import path:
    from app.models.snapshot import Snapshot

Authoritative implementation lives in:
    app.models.rendered_snapshot.RenderedSnapshot
"""

from app.models.rendered_snapshot import RenderedSnapshot as Snapshot

__all__ = ["Snapshot"]

