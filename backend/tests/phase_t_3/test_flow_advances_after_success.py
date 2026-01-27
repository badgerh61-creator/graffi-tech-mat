from app.services.flow_advance import advance_flow_state

class DummySnapshot:
    last_flow_state = "transform"

def test_flow_advances_after_success():
    snapshot = DummySnapshot()
    advance_flow_state(snapshot, "validate")
    assert snapshot.last_flow_state == "validate"

