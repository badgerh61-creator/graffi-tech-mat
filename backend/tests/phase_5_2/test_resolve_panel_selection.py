def test_resolve_panel_selection(
    client,
    draft_snapshot,
    editor_user,
):
    response = client.post(
        f"/projects/{draft_snapshot.project_id}/snapshots/{draft_snapshot.id}/resolve-target",
        json={
            "selection_type": "panel",
            "selection_id": "door.front.left",
        },
        headers=auth(editor_user),
    )

    assert response.status_code == 200
    assert response.json()["target_type"] == "panel"

