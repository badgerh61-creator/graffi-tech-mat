from app.services.mode_resolver import resolve_mode

class DummySnapshot:
    status = "draft"

def test_validation_station_forces_review():
    mode = resolve_mode(
        snapshot=DummySnapshot(),
        user=None,
        station="validation",
    )

    assert mode.value == "review"

