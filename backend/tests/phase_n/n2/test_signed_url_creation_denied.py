def test_owner_cannot_create_signed_url(
    client,
    signed_url_distribution_request,
    owner_user,
):
    response = client.post(
        "/distributions/signed-urls",
        json={"distribution_request_id": signed_url_distribution_request.id},
        headers=auth(owner_user),
    )

    assert response.status_code == 403

