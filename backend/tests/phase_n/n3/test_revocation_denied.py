def test_viewer_cannot_revoke_distribution(
    client,
    active_distribution_request,
    viewer_user,
):
    response = client.post(
        f"/distributions/{active_distribution_request.id}/revoke",
        headers=auth(viewer_user),
    )

    assert response.status_code == 403

