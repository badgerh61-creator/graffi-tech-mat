def test_invalid_transform_rejected(
    client,
    draft_snapshot,
    editor_user,
):
    response = client.post(
        f"/projects/{draft_snapshot.project_id}/snapshots/{draft_snapshot.id}/transform",
        json={
            "operation": "shear",
            "target_id": "body.root",
            "params": {},
        },
        headers=auth(editor_user),
    )

    assert response.status_code == 422

