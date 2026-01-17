def test_cannot_distribute_incomplete_export(
    client,
    pending_export,
    admin_user,
):
    response = client.post(
        "/distributions/requests",
        json={
            "export_id": pending_export.id,
            "target": "direct_download",
            "options": {},
        },
        headers=auth(admin_user),
    )

    assert response.status_code == 409

