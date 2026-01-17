def test_cannot_create_url_for_revoked_request(
    client,
    revoked_distribution_request,
    admin_user,
):
    response = client.post(
        "/distributions/signed-urls",
        json={"distribution_request_id": revoked_distribution_request.id},
        headers=auth(admin_user),
    )

    assert response.status_code == 410

