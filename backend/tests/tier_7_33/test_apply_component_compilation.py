from app.services.components.compiler import compile_component_ops

def test_compile_ride_height_translate():
    ops = compile_component_ops(
        kind="ride_height",
        params={"delta_y": 0.25},
        target_id="vehicle-1::CarRoot",
    )
    assert len(ops) == 1
    assert ops[0]["tool"] == "TRANSLATE"
    assert ops[0]["payload"]["delta"]["y"] == 0.25

def test_unknown_kind_safe_noop():
    ops = compile_component_ops(kind="unknown", params={"x": 1}, target_id="t")
    assert ops == []
