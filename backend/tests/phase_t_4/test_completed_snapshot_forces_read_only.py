from app.services.mode_resolver import resolve_mode

class DummySnapshot:
    status = "completed"

def test_completed_snapshot_forces_read_only():
    mode = resolve_mode(
        snapshot=DummySnapshot(),
        user=None,
        station="geometry",
    )

    assert mode.value == "read_only"

