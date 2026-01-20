from app.models.surface import Surface

# 🔍 Phase P — observability
import app.observability.metrics as metrics_module
import time


def generate_surface_from_curves(
    *,
    curves,
    params=None,
    enforce_symmetry: bool = False,
):
    start = time.time()

    if not curves:
        raise ValueError("At least one curve is required to generate a surface")

    if enforce_symmetry:
        for curve in curves:
            if not getattr(curve, "is_symmetric", True):
                raise ValueError("Asymmetric curve detected while symmetry is enforced")

    ordered_curves = sorted(
        curves,
        key=lambda c: c.id,
    )

    method = "loft"

    surface = Surface(
        source_curves=ordered_curves,
        params=params or {},
        method=method,
    )

    metrics_module.metrics.inc("geometry.regeneration.count")
    metrics_module.metrics.timing(
        "geometry.regeneration.duration_ms",
        (time.time() - start) * 1000,
    )

    return surface

