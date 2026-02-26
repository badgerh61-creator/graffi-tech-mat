from app.services.constraints.evaluator import evaluate_constraints_for_tool

class FakeSnap:
    def __init__(self, body_state):
        self.body_state = body_state

def test_locked_axis_blocks_rotate_on_y():
    snap = FakeSnap(body_state={
        "constraints": [
            {
                "id": "c1",
                "kind": "locked_axis",
                "target_id": "vehicle-1::CarRoot/Door_L",
                "params": {"axes": ["y"], "tools": ["ROTATE"]},
                "enabled": True,
            }
        ]
    })

    violations = evaluate_constraints_for_tool(
        snapshot=snap,
        tool="ROTATE",
        payload={"target_id": "vehicle-1::CarRoot/Door_L", "axis": "y", "degrees": 10},
    )

    assert len(violations) == 1
    assert violations[0].kind == "locked_axis"

def test_symmetry_blocks_translate_x():
    snap = FakeSnap(body_state={
        "constraints": [
            {
                "id": "sym1",
                "kind": "symmetry",
                "target_id": "vehicle-1::CarRoot",
                "params": {"plane": "vehicle_centerline"},
                "enabled": True,
            }
        ]
    })

    v = evaluate_constraints_for_tool(
        snapshot=snap,
        tool="TRANSLATE",
        payload={
            "target_id": "vehicle-1::CarRoot",
            "axis": "x",
            "delta": {"x": 1, "y": 0, "z": 0},
        },
    )
    assert len(v) == 1
    assert v[0].kind == "symmetry"
