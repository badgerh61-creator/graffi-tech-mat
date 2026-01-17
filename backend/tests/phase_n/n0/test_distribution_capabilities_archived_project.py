from app.services.distribution_capabilities import compute_distribution_capabilities

def test_archived_project_disables_distribution(
    archived_project,
    admin_user,
):
    caps = compute_distribution_capabilities(
        user=admin_user,
        project=archived_project,
    )

    assert all(value is False for value in caps.values())

