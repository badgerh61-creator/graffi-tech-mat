from fastapi import HTTPException
from sqlalchemy.orm.attributes import flag_modified

from app.services.snapshot_cloner import clone_snapshot
from app.services.audit import log_event
from app.services.surface_generator import generate_surface_from_curves


def _serialize_surface(surface):
    """
    Phase K.1 adapter.
    Converts a domain Surface into JSON-safe payload.
    """

    # Already JSON-safe
    if isinstance(surface, dict):
        return surface

    # Domain Surface object
    return {
        "id": getattr(surface, "id", None),
        "type": surface.__class__.__name__,

        # 🔒 REQUIRED BY Phase K.1 tests
        "method": getattr(surface, "method", "loft"),

        # Geometry payload (may be None in tests)
        "vertices": getattr(surface, "vertices", None),
        "faces": getattr(surface, "faces", None),

        # Free-form metadata
        "metadata": getattr(surface, "metadata", {}),
    }


def generate_surfaces_for_snapshot(
    *,
    db,
    snapshot,
    user,
    params=None,
    enforce_symmetry=False,
):
    # 🔒 Lifecycle enforcement
    if snapshot.status != "draft":
        raise HTTPException(409, "Snapshot not editable")

    # 1️⃣ Clone snapshot (immutability preserved)
    new_snapshot = clone_snapshot(
        db=db,
        snapshot=snapshot,
        user=user,
    )

    try:
        # 2️⃣ Pure geometry (existing generator)
        surface = generate_surface_from_curves(
            curves=new_snapshot.curves,
            params=params,
            enforce_symmetry=enforce_symmetry,
        )

        # 3️⃣ Phase K.1 — JSON-safe persistence (AUTHORITATIVE)
        if new_snapshot.body_state is None:
            new_snapshot.body_state = {}

        new_snapshot.body_state["surfaces"] = [
            _serialize_surface(surface)
        ]

        flag_modified(new_snapshot, "body_state")

    except ValueError as e:
        new_snapshot.status = "failed"
        new_snapshot.error_message = str(e)

    db.commit()

    # 4️⃣ Audit (authoritative)
    log_event(
        db=db,
        user_id=user.id,
        action="surface.generated",
        resource_type="snapshot",
        resource_id=new_snapshot.id,
        extra={
            "parent_snapshot_id": snapshot.id,
            "method": "loft",
        },
    )

    return new_snapshot

