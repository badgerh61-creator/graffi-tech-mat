from app.services.geometry_validator import validate_geometry

def test_panel_continuity_required(
    discontinuous_panels,
):
    result = validate_geometry(
        surfaces=[],
        panels=discontinuous_panels,
    )

    assert result["valid"] is False
    assert any(
        e["code"] == "CONTINUITY_ERROR"
        for e in result["errors"]
    )

