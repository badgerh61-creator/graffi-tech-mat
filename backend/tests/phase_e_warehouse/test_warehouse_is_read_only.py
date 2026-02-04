def test_warehouse_is_read_only(client, editor_user):
    response = client.post(
        "/warehouse/projects",
        headers=auth(editor_user),
    )

    assert response.status_code in (404, 405)

