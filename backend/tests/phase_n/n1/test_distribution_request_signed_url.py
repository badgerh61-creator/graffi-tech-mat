def test_admin_can_request_signed_url(
    client,
    completed_export,
    admin_user,
):
    response = client.post(
        "/distributions/requests",
        json={
            "export_id": completed_export.id,
            "target": "signed_url",
            "options": {"expires_in_hours": 24},
        },
        headers=auth(admin_user),
    )

    assert response.status_code == 200

