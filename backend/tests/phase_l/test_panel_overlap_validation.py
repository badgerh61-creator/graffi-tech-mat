from app.services.geometry_validator import validate_geometry

def test_panels_may_not_overlap(
    overlapping_panels,
):
    result = validate_geometry(
        surfaces=[],
        panels=overlapping_panels,
    )

    assert result["valid"] is False
    assert any(
        e["code"] == "PANEL_OVERLAP"
        for e in result["errors"]
    )

