from app.validation.decor.errors import (
    CapabilityRequired,
    InvalidSnapshotBase,
    DecalNotFound,
    InvalidTargetPanel,
    InvalidUVTransform,
    DecalInstanceNotFound,
)
from app.validation.decor.rules import validate_uv_transform


# -------------------------------------------------
# APPLY DECAL (UNCHANGED)
# -------------------------------------------------

def validate_apply_decal(
    *,
    capabilities: dict,
    snapshot,
    decal,
    target: dict,
):
    if not capabilities.get("canDecorateExterior"):
        raise CapabilityRequired("Exterior decor capability required")

    if snapshot.status != "completed" or snapshot.is_obsolete:
        raise InvalidSnapshotBase("Snapshot is not valid for mutation")

    if decal is None or not decal.is_exterior:
        raise DecalNotFound("Decal not found or not exterior-compatible")

    panel = target.get("panel")
    if panel not in snapshot.vehicle_panels:
        raise InvalidTargetPanel(f"Invalid target panel: {panel}")

    ok, reason = validate_uv_transform(target.get("uv_transform", {}))
    if not ok:
        raise InvalidUVTransform(reason)


# -------------------------------------------------
# REMOVE DECAL (NEW)
# -------------------------------------------------

def validate_remove_decal(
    *,
    capabilities: dict,
    snapshot,
    decal_instance_id: str,
):
    if not capabilities.get("canDecorateExterior"):
        raise CapabilityRequired("Exterior decor capability required")

    if snapshot.status != "completed" or snapshot.is_obsolete:
        raise InvalidSnapshotBase("Snapshot is not valid for mutation")

    decals = (snapshot.decor_state or {}).get("decals", [])
    if not any(d["instance_id"] == decal_instance_id for d in decals):
        raise DecalInstanceNotFound("Decal instance not found")

