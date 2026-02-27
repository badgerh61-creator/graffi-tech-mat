def test_scenarios_create_and_list(client, project, viewer_user):
    r1 = client.post(
        "/simulation/scenarios",
        json={"project_id": project.id, "name": "Baseline", "scenario": {"throttle": 0.6, "duration_s": 5.0}},
        headers=auth(viewer_user),
    )
    assert r1.status_code == 200
    sid = r1.json()["scenario_id"]
    assert sid is not None

    r2 = client.get(f"/simulation/scenarios?project_id={project.id}", headers=auth(viewer_user))
    assert r2.status_code == 200
    data = r2.json()
    assert data["project_id"] == project.id
    assert any(s["id"] == sid for s in data["scenarios"])
