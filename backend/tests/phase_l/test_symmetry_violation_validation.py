from app.services.geometry_validator import validate_geometry

def test_symmetry_violation_is_detected(
    asymmetric_surface,
):
    result = validate_geometry(
        surfaces=[asymmetric_surface],
        panels=[],
        enforce_symmetry=True,
    )

    assert result["valid"] is False
    assert any(
        e["code"] == "SYMMETRY_VIOLATION"
        for e in result["errors"]
    )

