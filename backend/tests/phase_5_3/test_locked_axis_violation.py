def test_locked_axis_violation(
    client,
    draft_snapshot,
    editor_user,
):
    response = client.post(
        f"/projects/{draft_snapshot.project_id}/snapshots/{draft_snapshot.id}/validate-transform",
        json={
            "target_id": "body.root",
            "operation": "translate",
            "params": {"z": 1},
            "constraints": ["locked_axis:z"],
        },
        headers=auth(editor_user),
    )

    assert response.json()["valid"] is False

