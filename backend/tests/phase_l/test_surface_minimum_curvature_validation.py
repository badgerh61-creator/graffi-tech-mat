from app.services.geometry_validator import validate_geometry

def test_surface_minimum_curvature_violation(
    invalid_curvature_surface,
):
    result = validate_geometry(
        surfaces=[invalid_curvature_surface],
        panels=[],
    )

    assert result["valid"] is False
    assert any(
        e["code"] == "MIN_CURVATURE_VIOLATION"
        for e in result["errors"]
    )

