def test_remove_decal_missing_instance(
    client,
    project,
    completed_snapshot_with_decal,
    editor_user,
):
    response = client.post(
        "/mutations/decor/exterior/remove-decal",
        json={
            "project_id": project.id,
            "snapshot_base_id": completed_snapshot_with_decal.id,
            "decal_instance_id": "does-not-exist",
        },
        headers=auth(editor_user),
    )

    assert response.status_code == 404
    assert response.json()["error"] == "decal_instance_not_found"

