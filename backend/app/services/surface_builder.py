def build_surfaces(*, curves, method):
    """
    Stub surface builder.
    Real implementations may use:
    - NURBS lofting
    - Sweep along guide curves
    - Boundary patching
    """
    if not curves or len(curves) < 2:
        raise ValueError("curve_topology_invalid")

    return [
        {
            "id": f"surface-{i}",
            "method": method,
            "curve_refs": [c.id for c in curves],
        }
        for i in range(1)
    ]

