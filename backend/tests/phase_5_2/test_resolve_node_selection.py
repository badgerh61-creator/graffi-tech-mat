def test_resolve_node_selection(
    client,
    draft_snapshot,
    editor_user,
):
    response = client.post(
        f"/projects/{draft_snapshot.project_id}/snapshots/{draft_snapshot.id}/resolve-target",
        json={
            "selection_type": "node",
            "selection_id": "body.root",
        },
        headers=auth(editor_user),
    )

    assert response.status_code == 200
    data = response.json()
    assert data["target_id"] == "body.root"
    assert data["editable"] is True

