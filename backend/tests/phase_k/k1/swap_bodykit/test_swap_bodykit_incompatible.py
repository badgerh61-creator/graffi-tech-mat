def test_swap_bodykit_incompatible(
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
            "bodykit_id": "truck_bodykit_on_sedan",
        },
        headers=auth(editor_user),
    )

    assert response.status_code == 409
    assert response.json()["error"] == "bodykit_incompatible"

