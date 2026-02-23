from app.services.axis_locks import apply_axis_lock_to_payload

def test_axis_lock_default_xyz_keeps_axes():
    out = apply_axis_lock_to_payload(payload={"x": 1, "y": 2, "z": 3})
    assert out["axis_lock"] == "xyz"
    assert out["x"] == 1 and out["y"] == 2 and out["z"] == 3
