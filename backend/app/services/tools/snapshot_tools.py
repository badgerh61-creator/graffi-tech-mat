# backend/app/services/tools/snapshot_tools.py

def apply_snapshot_restore(snapshot, payload):
    """
    Tier 7.66 — Snapshot restore tool

    NOTE:
    This does NOT mutate snapshot contents.
    It only signals the system to switch active snapshot.
    """
    snapshot_id = payload.get("snapshot_id")

    if not snapshot_id:
        return {"ok": False, "error": "snapshot_id required"}

    return {
        "ok": True,
        "snapshot_id": snapshot_id,
    }
