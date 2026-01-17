def test_invalid_distribution_target_rejected(
    client,
    completed_export,
    admin_user,
):
    response = client.post(
        "/distributions/requests",
        json={
            "export_id": completed_export.id,
            "target": "ftp",
            "options": {},
        },
        headers=auth(admin_user),
    )

    assert response.status_code == 400

