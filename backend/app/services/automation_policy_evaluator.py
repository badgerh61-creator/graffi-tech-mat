from app.services.automation_capabilities import compute_automation_capabilities
from app.services.automation_policies import (
    ALLOWED_AUTOMATION_POLICIES,
    policy_violates_phase_n,
)

def evaluate_automation_policy(*, user, project, policy, enabled):
    # Project state gate
    is_archived = getattr(project, "archived", False)
    is_suspended = getattr(project, "suspended", False)

    if is_archived or is_suspended:
        return {"allowed": False, "reason": "project_disabled"}


    # Capability gate (Phase O.0)
    caps = compute_automation_capabilities(
        user=user,
        project=project,
    )

    if not caps["canEnableAutomation"]:
        return {"allowed": False, "reason": "capability_missing"}

    # Policy allowlist
    if policy not in ALLOWED_AUTOMATION_POLICIES:
        return {"allowed": False, "reason": "unknown_policy"}

    # Phase N protection
    if policy_violates_phase_n(policy):
        return {"allowed": False, "reason": "violates_phase_n"}

    return {
        "allowed": True,
        "policy": policy,
        "enabled": enabled,
    }

