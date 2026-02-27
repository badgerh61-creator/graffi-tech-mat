from app.services.scenario_hashing import compute_scenario_hash

def test_scenario_hash_is_deterministic():
    s1 = {"throttle": 0.6, "duration_s": 10.0}
    s2 = {"duration_s": 10.0, "throttle": 0.6}  # different key order

    h1 = compute_scenario_hash(scenario=s1, template_key="x", template_version="v1", engine_version="pseudo-v1")
    h2 = compute_scenario_hash(scenario=s2, template_key="x", template_version="v1", engine_version="pseudo-v1")
    assert h1 == h2
