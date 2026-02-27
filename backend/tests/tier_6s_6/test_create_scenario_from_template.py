def test_create_scenario_from_template(client, project, viewer_user):
    r = client.post(
        "/simulation/scenarios/from-template",
        json={
            "project_id": project.id,
            "name": "Baseline 0-60",
            "template_key": "accel_0_60_v1",
            "engine_version": "pseudo-v1",
            "overrides": {"mass_kg": 1300.0},
        },
        headers=auth(viewer_user),
    )
    assert r.status_code == 200
    out = r.json()
    assert out["scenario_id"] > 0
    assert isinstance(out["scenario_hash"], str) and len(out["scenario_hash"]) >= 16
    assert out["template_key"] == "accel_0_60_v1"
