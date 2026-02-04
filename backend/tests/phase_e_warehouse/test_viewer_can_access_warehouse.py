def test_viewer_can_access_warehouse(client, viewer_user):
    response = client.get(
        "/warehouse/projects",
        headers=auth(viewer_user),
    )
    assert response.status_code == 200

