def test_admin_can_revoke_distribution(
    client,
    active_distribution_request,
    admin_user,
):
    response = client.post(
        f"/distributions/{active_distribution_request.id}/revoke",
        headers=auth(admin_user),
    )

    assert response.status_code == 200

