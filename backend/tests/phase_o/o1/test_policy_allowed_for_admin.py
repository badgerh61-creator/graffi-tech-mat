from app.services.automation_policy_evaluator import evaluate_automation_policy

def test_admin_can_enable_allowed_policy(
    project,
    admin_user,
):
    result = evaluate_automation_policy(
        user=admin_user,
        project=project,
        policy="auto_expire_links",
        enabled=True,
    )

    assert result["allowed"] is True

