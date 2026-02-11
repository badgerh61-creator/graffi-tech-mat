def test_list_materials_returns_records(client, db):
    response = client.get("/materials")

    assert response.status_code == 200
    data = response.json()

    assert "items" in data
    assert isinstance(data["items"], list)

