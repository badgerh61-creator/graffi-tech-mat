def test_studio_state_is_read_only(client, editor_user):
    response = client.get(
        "/studio/state",
        headers=auth(editor_user),
    )

    assert response.status_code == 200
    assert "station" in response.json()
    assert "mode" in response.json()

