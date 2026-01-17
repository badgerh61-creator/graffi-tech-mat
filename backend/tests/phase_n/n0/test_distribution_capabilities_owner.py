from app.services.distribution_capabilities import compute_distribution_capabilities

def test_owner_can_distribute_exports(
    project,
    owner_user,
):
    caps = compute_distribution_capabilities(
        user=owner_user,
        project=project,
    )

    assert caps["canDistributeExports"] is True
    assert caps["canCreatePublicLinks"] is False
    assert caps["canRevokeAccess"] is True

