# backend/app/services/snapshot_guard.py

"""
Phase T / U — Snapshot lifecycle guards.

This module exists to provide authoritative snapshot state checks
for tool execution and kernel orchestration.
"""

from fastapi import HTTPException


def require_draft_snapshot(snapshot):
    """
    Guard: only draft snapshots may be mutated.
    """

    if snapshot.status != "draft":
        raise HTTPException(409, "Snapshot is not draft")

    return snapshot

