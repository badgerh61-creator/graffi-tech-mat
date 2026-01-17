def test_cannot_create_url_for_incomplete_export(
    client,
    distribution_request_with_pending_export,
    admin_user,
):
    response = client.post(
        "/distributions/signed-urls",
        json={"distribution_request_id": distribution_request_with_pending_export.id},
        headers=auth(admin_user),
    )

    assert response.status_code == 409

