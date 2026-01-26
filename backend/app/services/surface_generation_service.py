from fastapi import HTTPException
from app.services.snapshot_cloner import clone_snapshot
from app.services.audit import log_event
from app.services.surface_generator import generate_surface_from_curves


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

        # 3️⃣ Phase K.1 contract: attach surfaces at runtime
        new_snapshot.surfaces = [surface]

    except ValueError as e:
        new_snapshot.status = "failed"
        new_snapshot.error_message = str(e)

    db.commit()

    # 4️⃣ Audit
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

