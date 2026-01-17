def test_owner_can_request_direct_download(
    client,
    completed_export,
    owner_user,
):
    response = client.post(
        "/distributions/requests",
        json={
            "export_id": completed_export.id,
            "target": "direct_download",
            "options": {},
        },
        headers=auth(owner_user),
    )

    assert response.status_code == 200
    assert response.json()["status"] == "accepted"

