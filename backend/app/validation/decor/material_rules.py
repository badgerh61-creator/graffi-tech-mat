# backend/app/validation/decor/material_rules.py

def validate_set_material(
    *,
    capabilities: dict,
    snapshot,
    panel: str,
    material: dict,
):
    if not capabilities.get("canDecorateExterior"):
        raise CapabilityRequired("Exterior decor capability required")

    if snapshot.status != "completed" or snapshot.is_obsolete:
        raise InvalidSnapshotBase("Snapshot is not valid for mutation")

    if panel not in snapshot.vehicle_panels:
        raise InvalidTargetPanel(f"Invalid target panel: {panel}")

    params = material.get("parameters", {})
    color = params.get("color")
    finish = params.get("finish")

    if not isinstance(color, str) or not color.startswith("#"):
        raise InvalidMaterialDefinition("Invalid color format")

    if finish not in {"matte", "gloss", "metallic"}:
        raise InvalidMaterialDefinition("Invalid finish")

