def test_invalid_selection_rejected(
    client,
    draft_snapshot,
    editor_user,
):
    response = client.post(
        f"/projects/{draft_snapshot.project_id}/snapshots/{draft_snapshot.id}/resolve-target",
        json={
            "selection_type": "panel",
            "selection_id": "non.existent.panel",
        },
        headers=auth(editor_user),
    )

    assert response.status_code == 404

