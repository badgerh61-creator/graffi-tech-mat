def compute_automation_capabilities(*, user, project):
    # Archived or suspended projects disable automation
    if getattr(project, "archived_at", None) is not None or getattr(project, "suspended", False):
        return {
            "canEnableAutomation": False,
            "canConfigureIntegrations": False,
            "canViewAutomationLogs": False,
        }

    if user.role == "admin":
        return {
            "canEnableAutomation": True,
            "canConfigureIntegrations": True,
            "canViewAutomationLogs": True,
        }

    return {
        "canEnableAutomation": False,
        "canConfigureIntegrations": False,
        "canViewAutomationLogs": False,
    }

