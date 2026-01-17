def test_owner_cannot_request_signed_url(
    client,
    completed_export,
    owner_user,
):
    response = client.post(
        "/distributions/requests",
        json={
            "export_id": completed_export.id,
            "target": "signed_url",
            "options": {"expires_in_hours": 24},
        },
        headers=auth(owner_user),
    )

    assert response.status_code == 403

