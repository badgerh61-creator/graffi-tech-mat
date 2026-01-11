def test_swap_bodykit_not_found(
    client,
    project,
    completed_snapshot,
    editor_user,
):
    response = client.post(
        "/mutations/decor/exterior/swap-bodykit",
        json={
            "project_id": project.id,
            "snapshot_base_id": completed_snapshot.id,
            "bodykit_id": "non_existent",
        },
        headers=auth(editor_user),
    )

    assert response.status_code == 404
    assert response.json()["error"] == "bodykit_not_found"

