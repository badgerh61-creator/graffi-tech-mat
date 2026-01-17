def test_admin_can_create_signed_url(
    client,
    signed_url_distribution_request,
    admin_user,
):
    response = client.post(
        "/distributions/signed-urls",
        json={"distribution_request_id": signed_url_distribution_request.id},
        headers=auth(admin_user),
    )

    assert response.status_code == 200
    data = response.json()
    assert "url" in data
    assert "expires_at" in data

