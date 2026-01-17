def test_cannot_revoke_twice(
    client,
    revoked_distribution_request,
    admin_user,
):
    response = client.post(
        f"/distributions/{revoked_distribution_request.id}/revoke",
        headers=auth(admin_user),
    )

    assert response.status_code == 409

