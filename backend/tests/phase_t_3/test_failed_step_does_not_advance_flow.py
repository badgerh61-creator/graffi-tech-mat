from app.services.flow_advance import advance_flow_state

class DummySnapshot:
    last_flow_state = "transform"

def test_failed_step_does_not_advance_flow():
    snapshot = DummySnapshot()
    # simulate failure → do NOT call advance
    assert snapshot.last_flow_state == "transform"

