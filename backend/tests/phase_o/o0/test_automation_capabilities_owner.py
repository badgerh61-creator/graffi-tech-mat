from app.services.automation_capabilities import compute_automation_capabilities

def test_owner_cannot_enable_automation(
    project,
    owner_user,
):
    caps = compute_automation_capabilities(
        user=owner_user,
        project=project,
    )

    assert all(value is False for value in caps.values())

