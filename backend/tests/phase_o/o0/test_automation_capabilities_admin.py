from app.services.automation_capabilities import compute_automation_capabilities

def test_admin_can_enable_automation(
    project,
    admin_user,
):
    caps = compute_automation_capabilities(
        user=admin_user,
        project=project,
    )

    assert caps["canEnableAutomation"] is True
    assert caps["canConfigureIntegrations"] is True
    assert caps["canViewAutomationLogs"] is True

