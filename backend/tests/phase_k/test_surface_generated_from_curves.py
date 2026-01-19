from app.services.surface_generator import generate_surface_from_curves

def generate_surface_from_curves(
    *,
    curves,
    params=None,
    method="loft",
    enforce_symmetry=True,
):
    if enforce_symmetry and not curves_are_symmetric(curves):
        raise ValueError("Symmetry violation")

    return Surface(
        source_curves=curves,
        params=params or {},
        method=method,
    )

