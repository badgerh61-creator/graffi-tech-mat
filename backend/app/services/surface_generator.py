from app.models.surface import Surface


def generate_surface_from_curves(
    *,
    curves,
    params=None,
    enforce_symmetry: bool = False,
):
    """
    Deterministically generate a Level-2 surface from curves.

    Canonicalization rules (MANDATORY):
    - Curves are ordered by stable ID
    - Params are copied verbatim
    - Method is explicit and constant

    Symmetry rules:
    - If enforce_symmetry=True, all curves must be symmetric
    """

    if not curves:
        raise ValueError("At least one curve is required to generate a surface")

    # 🔒 Symmetry enforcement (Phase K contract)
    if enforce_symmetry:
        for curve in curves:
            if not getattr(curve, "is_symmetric", True):
                raise ValueError("Asymmetric curve detected while symmetry is enforced")

    # 🔒 Canonical curve ordering (CRITICAL FOR DETERMINISM)
    ordered_curves = sorted(
        curves,
        key=lambda c: c.id,
    )

    # 🔒 Explicit method (never inferred)
    method = "loft"

    return Surface(
        source_curves=ordered_curves,
        params=params or {},
        method=method,
    )

