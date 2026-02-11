def test_list_decor_presets_returns_records(client, db):
    response = client.get("/decor-presets")

    assert response.status_code == 200
    data = response.json()

    assert "items" in data
    assert isinstance(data["items"], list)

