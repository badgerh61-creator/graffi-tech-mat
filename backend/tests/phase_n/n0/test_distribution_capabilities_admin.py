from app.services.distribution_capabilities import compute_distribution_capabilities

def test_admin_can_create_public_links(
    project,
    admin_user,
):
    caps = compute_distribution_capabilities(
        user=admin_user,
        project=project,
    )

    assert caps["canDistributeExports"] is True
    assert caps["canCreatePublicLinks"] is True
    assert caps["canRevokeAccess"] is True

