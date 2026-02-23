def test_editor_can_tune_by_default_when_capabilities_missing(client, project, completed_snapshot, editor_user):
    r = client.post(
        "/mutations/tuning/set-suspension",
        json={
            "project_id": project.id,
            "snapshot_base_id": completed_snapshot.id,
            "preset_id": "sport_low",
        },
        headers=auth(editor_user),
    )
    assert r.status_code == 200
