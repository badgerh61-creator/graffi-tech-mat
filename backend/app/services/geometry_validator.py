from app.services.geometry_validation_codes import *
from app.services.geometry_checks import (
    violates_min_curvature,
    is_self_intersecting,
    panels_overlap,
    panels_are_continuous,
    adjacent_panel_pairs,
)

# 🔍 Phase P — observability
import app.observability.metrics as metrics_module


def validate_geometry(
    *,
    surfaces,
    panels,
    enforce_symmetry=True,
):
    # --------------------------------------------------
    # Phase P — REQUIRED invocation metric
    # --------------------------------------------------
    metrics_module.metrics.inc(
        "geometry.validation.invocations.count"
    )

    # --------------------------------------------------
    # Phase P — EMPTY GEOMETRY IS INVALID
    # --------------------------------------------------
    if not surfaces and not panels:
        metrics_module.metrics.inc(
            "geometry.validation.failures.count"
        )
        return {
            "valid": False,
            "errors": [{
                "code": "EMPTY_GEOMETRY",
                "message": "No surfaces or panels provided for validation",
                "entity_id": None,
            }],
        }

    errors = []

    # --------------------------------------------------
    # Surface-level validation
    # --------------------------------------------------
    for surface in surfaces:
        if violates_min_curvature(surface):
            errors.append({
                "code": MIN_CURVATURE_VIOLATION,
                "message": "Surface curvature below minimum threshold",
                "entity_id": surface.id,
            })

        if is_self_intersecting(surface):
            errors.append({
                "code": SELF_INTERSECTION,
                "message": "Surface self-intersects",
                "entity_id": surface.id,
            })

        if enforce_symmetry and not surface.is_symmetric:
            errors.append({
                "code": SYMMETRY_VIOLATION,
                "message": "Surface violates symmetry constraint",
                "entity_id": surface.id,
            })

    # --------------------------------------------------
    # Panel-level validation
    # --------------------------------------------------
    for panel_pair in adjacent_panel_pairs(panels):
        if panels_overlap(panel_pair):
            errors.append({
                "code": PANEL_OVERLAP,
                "message": "Panels overlap",
                "entity_id": [p.id for p in panel_pair],
            })

        if not panels_are_continuous(panel_pair):
            errors.append({
                "code": CONTINUITY_ERROR,
                "message": "Panel continuity violation",
                "entity_id": [p.id for p in panel_pair],
            })

    # --------------------------------------------------
    # Phase P — failure metric
    # --------------------------------------------------
    if errors:
        metrics_module.metrics.inc(
            "geometry.validation.failures.count"
        )

    return {
        "valid": len(errors) == 0,
        "errors": errors,
    }

