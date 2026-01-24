def test_transform_applies_to_draft_snapshot(
    client,
    draft_snapshot,
    editor_user,
):
    response = client.post(
        f"/projects/{draft_snapshot.project_id}/snapshots/{draft_snapshot.id}/transform",
        json={
            "operation": "translate",
            "target_id": "body.root",
            "params": {"x": 1, "y": 0, "z": 0},
        },
        headers=auth(editor_user),
    )

    assert response.status_code == 200
    assert response.json()["status"] == "applied"

