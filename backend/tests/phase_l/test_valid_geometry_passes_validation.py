from app.services.geometry_validator import validate_geometry

def test_valid_geometry_passes_validation(
    valid_surfaces,
    valid_panels,
):
    result = validate_geometry(
        surfaces=valid_surfaces,
        panels=valid_panels,
    )

    assert result["valid"] is True
    assert result["errors"] == []

