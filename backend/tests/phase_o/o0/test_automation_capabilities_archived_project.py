from app.services.automation_capabilities import compute_automation_capabilities

def test_archived_project_disables_automation(
    archived_project,
    admin_user,
):
    caps = compute_automation_capabilities(
        user=admin_user,
        project=archived_project,
    )

    assert all(value is False for value in caps.values())

