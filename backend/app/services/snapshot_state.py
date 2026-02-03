# backend/app/services/snapshot_state.py

from app.services.kernel_snapshot_lookup import kernel_snapshot_lookup


def get_snapshot_state(*, snapshot_id, user):
    """
    Phase E.3 — Read-only snapshot state exposure.

    - No mutation
    - No authority
    - Reflects persisted truth only
    """

    snapshot = kernel_snapshot_lookup(snapshot_id=snapshot_id)

    return {
        "snapshot_id": snapshot.id,
        "status": snapshot.status,
        "immutable": snapshot.status != "draft",

        # 🔒 Canonical lifecycle field (actual model)
        "locked_at": snapshot.locked_at,
    }

