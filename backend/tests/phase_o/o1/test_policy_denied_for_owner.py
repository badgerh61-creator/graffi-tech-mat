from app.services.automation_policy_evaluator import evaluate_automation_policy

def test_owner_cannot_enable_policy(
    project,
    owner_user,
):
    result = evaluate_automation_policy(
        user=owner_user,
        project=project,
        policy="auto_expire_links",
        enabled=True,
    )

    assert result["allowed"] is False

