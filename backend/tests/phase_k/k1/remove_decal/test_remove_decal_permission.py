def test_viewer_cannot_remove_decal(
    request,
    client,
    project,
    completed_snapshot_with_decal,
    viewer_user,
):
    """
    Phase K.1 — Permission enforcement

    A viewer must NOT be allowed to remove an exterior decal.
    This test explicitly sets the request user to viewer_user
    because authentication is globally overridden in conftest.py.
    """

    # 🔐 Explicitly set viewer as the acting user
    request.node.user = viewer_user

    response = client.post(
        "/mutations/decor/exterior/remove-decal",
        json={
            "project_id": project.id,
            "snapshot_base_id": completed_snapshot_with_decal.id,
            "decal_instance_id": "abc123",
        },
    )

    assert response.status_code == 403
    assert response.json()["error"] == "decor_capability_required"

