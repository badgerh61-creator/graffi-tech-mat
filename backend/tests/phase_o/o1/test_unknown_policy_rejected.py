from app.services.automation_policy_evaluator import evaluate_automation_policy

def test_unknown_policy_is_rejected(
    project,
    admin_user,
):
    result = evaluate_automation_policy(
        user=admin_user,
        project=project,
        policy="auto_delete_exports",
        enabled=True,
    )

    assert result["allowed"] is False
    assert result["reason"] == "unknown_policy"

