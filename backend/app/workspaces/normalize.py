"""
PHASE J.5 — WORKSPACE SNAPSHOT NORMALIZATION

Responsibilities:
- Deterministic ordering
- Read-only transformation
- NO grouping
- NO filtering
- NO mutation
"""

from typing import List
from app.models.rendered_snapshot import RenderedSnapshot


def normalize_snapshots(
    snapshots: List[RenderedSnapshot],
) -> List[RenderedSnapshot]:
    """
    Normalize workspace snapshots for editor boot.

    Guarantees:
    - Flat list
    - Deterministic ordering (newest first)
    - No mutation of snapshot objects
    """

    return sorted(
        snapshots,
        key=lambda s: (s.created_at, s.id),
        reverse=True,  # 🔑 THIS WAS MISSING
    )

