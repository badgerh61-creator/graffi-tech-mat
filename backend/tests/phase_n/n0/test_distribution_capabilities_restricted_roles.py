from app.services.distribution_capabilities import compute_distribution_capabilities


def test_viewer_cannot_distribute(
    project,
    viewer_user,
):
    caps = compute_distribution_capabilities(
        user=viewer_user,
        project=project,
    )

    assert caps["canDistributeExports"] is False
    assert caps["canCreatePublicLinks"] is False
    assert caps["canRevokeAccess"] is False


def test_editor_cannot_distribute(
    project,
    editor_user,
):
    caps = compute_distribution_capabilities(
        user=editor_user,
        project=project,
    )

    assert caps["canDistributeExports"] is False
    assert caps["canCreatePublicLinks"] is False
    assert caps["canRevokeAccess"] is False

