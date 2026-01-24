# app/validation/body/rules.py

from typing import Dict, Any

from app.validation.body.errors import (
    InvalidSnapshotBase,
    BodyPresetNotFound,
    BodyPresetIncompatible,
    BodyParametersOutOfBounds,
)


def validate_base_snapshot(base_snapshot):
    if base_snapshot is None:
        raise InvalidSnapshotBase("Snapshot not found")

    if base_snapshot.status != "completed":
        raise InvalidSnapshotBase("Snapshot is not completed")

    if getattr(base_snapshot, "is_obsolete", False):
        raise InvalidSnapshotBase("Snapshot is obsolete")


def validate_body_preset(preset, *, snapshot):
    if preset is None:
        raise BodyPresetNotFound("Body preset not found")

    required_panels = set(preset.get("required_panels", set()))

    # ✅ Phase K default body contract
    available_panels = set(snapshot.vehicle_panels or [])

    if not available_panels:
        # Default passenger car panels
        available_panels = {
            "door_left",
            "door_right",
            "hood",
            "roof",
            "trunk",
            "fender_front_left",
            "fender_front_right",
            "fender_rear_left",
            "fender_rear_right",
        }

    if not required_panels.issubset(available_panels):
        raise BodyPresetIncompatible(
            "Body preset incompatible with snapshot vehicle"
        )


def validate_body_parameters(
    preset: dict,
    parameters: Dict[str, Any],
):
    limits = preset.get("limits", {})

    for key, value in parameters.items():
        if key not in limits:
            raise BodyParametersOutOfBounds(f"Unknown parameter '{key}'")

        low, high = limits[key]
        if not (low <= value <= high):
            raise BodyParametersOutOfBounds(
                f"Parameter '{key}' out of bounds ({low}–{high})"
            )

