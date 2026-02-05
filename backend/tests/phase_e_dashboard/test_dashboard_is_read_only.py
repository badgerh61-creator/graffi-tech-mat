def test_dashboard_is_read_only(client, editor_user):
    response = client.post(
        "/dashboard/projects",
        headers=auth(editor_user),
    )

    assert response.status_code in (404, 405)

