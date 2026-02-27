from app.services.simulation_engine_registry import engine_registry


def test_registry_has_pseudo_engine():
    eng = engine_registry.get("pseudo-v1")
    assert eng is not None
    assert getattr(eng, "engine_version") == "pseudo-v1"


def test_registry_unknown_engine():
    try:
        engine_registry.get("unknown-v9")
        assert False
    except ValueError as e:
        assert "Unknown engine_version" in str(e)
