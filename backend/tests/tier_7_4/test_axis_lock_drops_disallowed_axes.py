from app.services.axis_locks import apply_axis_lock_to_payload

def test_axis_lock_drops_disallowed_axes():
    out = apply_axis_lock_to_payload(payload={"axis_lock": "x", "x": 5, "y": 6, "z": 7})
    assert out["x"] == 5
    assert "y" not in out
    assert "z" not in out
