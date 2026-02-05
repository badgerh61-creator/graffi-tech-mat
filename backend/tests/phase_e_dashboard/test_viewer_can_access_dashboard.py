def test_viewer_can_access_dashboard(client, viewer_user):
    response = client.get(
        "/dashboard/projects",
        headers=auth(viewer_user),
    )
    assert response.status_code == 200

