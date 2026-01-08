from app.validation.decor.errors import (
    CapabilityRequired,
    InvalidSnapshotBase,
    DecalNotFound,
    InvalidTargetPanel,
    InvalidUVTransform,
)
from app.validation.decor.rules import validate_uv_transform


def validate_apply_decal(
    *,
    capabilities: dict,
    snapshot,
    decal,
    target: dict,
):
    # Capability check
    if not capabilities.get("canDecorateExterior"):
        raise CapabilityRequired("Exterior decor capability required")

    # Snapshot validation
    if snapshot.status != "completed" or snapshot.is_obsolete:
        raise InvalidSnapshotBase("Snapshot is not valid for mutation")

    # Decal validation
    if decal is None or not decal.is_exterior:
        raise DecalNotFound("Decal not found or not exterior-compatible")

    # Panel validation
    panel = target.get("panel")
    if panel not in snapshot.vehicle_panels:
        raise InvalidTargetPanel(f"Invalid target panel: {panel}")

    # UV validation
    ok, reason = validate_uv_transform(target.get("uv_transform", {}))
    if not ok:
        raise InvalidUVTransform(reason)

