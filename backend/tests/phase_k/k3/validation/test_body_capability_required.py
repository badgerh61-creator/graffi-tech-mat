def test_body_capability_required(client, editor_user, snapshot):
    payload = {
        "project_id": snapshot.project_id,
        "base_snapshot_id": snapshot.id,
        "preset_id": "widebody_v1",
        "parameters": {}
    }

    res = client.post(
        "/mutations/body/apply-morph",
        json=payload,
        user=editor_user,
        override_caps={"canModifyBody": False},
    )

    assert res.status_code == 403

