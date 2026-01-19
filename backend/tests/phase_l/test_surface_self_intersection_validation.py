from app.services.geometry_validator import validate_geometry

def test_surface_self_intersection_detected(
    self_intersecting_surface,
):
    result = validate_geometry(
        surfaces=[self_intersecting_surface],
        panels=[],
    )

    assert result["valid"] is False
    assert any(
        e["code"] == "SELF_INTERSECTION"
        for e in result["errors"]
    )

