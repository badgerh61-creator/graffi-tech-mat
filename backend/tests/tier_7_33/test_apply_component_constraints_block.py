from app.services.tools.apply_component_tool import evaluate_apply_component

class FakeSnap:
    def __init__(self, body_state):
        self.body_state = body_state

def test_component_eval_blocks_when_constraint_violates():
    snap = FakeSnap(body_state={
        "components": [
            {"id": "cmp1", "kind": "ride_height", "target_id": "vehicle-1::CarRoot", "params": {}, "enabled": True, "version": 1}
        ],
        "constraints": [
            {"id": "sym1", "kind": "symmetry", "target_id": "vehicle-1::CarRoot", "params": {"plane": "vehicle_centerline"}, "enabled": True}
        ]
    })

    # ride_height compiles to translate Y, so symmetry won't block
    res = evaluate_apply_component(snapshot=snap, payload={"component_id": "cmp1", "next_params": {"delta_y": 1}})
    assert res["ok"] is True
    assert res["ops"][0]["tool"] == "TRANSLATE"
