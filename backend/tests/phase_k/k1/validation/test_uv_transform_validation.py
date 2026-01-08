from app.validation.decor.rules import validate_uv_transform


def test_valid_uv_transform():
    ok, reason = validate_uv_transform({
        "x": 0.5,
        "y": 0.5,
        "scale": 1.0,
        "rotation": 0
    })

    assert ok is True
    assert reason is None


def test_uv_out_of_bounds():
    ok, reason = validate_uv_transform({
        "x": 1.5,
        "y": 0.5,
        "scale": 1.0,
        "rotation": 0
    })

    assert ok is False
    assert "between 0.0 and 1.0" in reason


def test_invalid_rotation():
    ok, reason = validate_uv_transform({
        "x": 0.5,
        "y": 0.5,
        "scale": 1.0,
        "rotation": 300
    })

    assert ok is False

