from app.services.snapping import apply_snapping_to_transform_payload

def test_snapping_quantizes_payload():
    out = apply_snapping_to_transform_payload(
        payload={"snap": True, "snap_step": 0.5, "x": 0.74, "y": 1.26}
    )
    assert out["x"] == 0.5
    assert out["y"] == 1.5
