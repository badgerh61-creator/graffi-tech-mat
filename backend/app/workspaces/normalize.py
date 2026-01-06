from typing import List, Dict
from app.models.rendered_snapshot import RenderedSnapshot


def normalize_snapshots(
    snapshots: List[RenderedSnapshot],
) -> Dict[str, List[RenderedSnapshot]]:
    """
    Phase J.5 — Workspace normalization

    - Groups snapshots by status
    - Enforces deterministic ordering
    - Read-only transformation

    DOES NOT:
    - Mutate snapshots
    - Select active snapshot
    - Trigger jobs
    """

    buckets = {
        "completed": [],
        "failed": [],
        "pending": [],
    }

    for snap in snapshots:
        if snap.status == "completed":
            buckets["completed"].append(snap)
        elif snap.status == "failed":
            buckets["failed"].append(snap)
        else:
            buckets["pending"].append(snap)

    # Deterministic ordering (newest first)
    for key in buckets:
        buckets[key].sort(key=lambda s: s.created_at, reverse=True)

    return buckets

