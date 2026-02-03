def get_studio_state(*, user):
    return {
        "station": user.current_station,
        "mode": user.current_mode,
        "snapshot_state": user.active_snapshot.status,
        "draft_ownership": user.active_snapshot.resolve_ownership(user),
        "block_reason": user.last_block_reason,
    }

