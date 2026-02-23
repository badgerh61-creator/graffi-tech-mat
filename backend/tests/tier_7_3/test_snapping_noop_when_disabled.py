from app.services.snapping import apply_snapping_to_transform_payload

def test_snapping_noop_when_disabled():
    payload = {"snap": False, "x": 0.74}
    out = apply_snapping_to_transform_payload(payload=payload)
    assert out["x"] == 0.74
