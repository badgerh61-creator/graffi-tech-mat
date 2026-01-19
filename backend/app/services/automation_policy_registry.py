# backend/app/services/automation_policy_registry.py

from app.services.automation_policies import ALLOWED_AUTOMATION_POLICIES

def list_supported_automation_policies():
    return sorted(ALLOWED_AUTOMATION_POLICIES)

