def get_studio_context(*, snapshot_id, user):
    snapshot = user.kernel_snapshot_lookup(snapshot_id)

    if snapshot.status == "completed":
        return {
            "station": "review",
            "mode": "read-only",
            "snapshot_id": snapshot.id,
        }

    return {
        "station": user.kernel_station,
        "mode": user.kernel_mode,
        "snapshot_id": snapshot.id,
    }

