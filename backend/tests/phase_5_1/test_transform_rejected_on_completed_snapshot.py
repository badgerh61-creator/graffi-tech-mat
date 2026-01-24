def test_transform_rejected_on_completed_snapshot(
    client,
    completed_snapshot,
    editor_user,
):
    response = client.post(
        f"/projects/{completed_snapshot.project_id}/snapshots/{completed_snapshot.id}/transform",
        json={
            "operation": "translate",
            "target_id": "body.root",
            "params": {"x": 1, "y": 0, "z": 0},
        },
        headers=auth(editor_user),
    )

    assert response.status_code == 409

