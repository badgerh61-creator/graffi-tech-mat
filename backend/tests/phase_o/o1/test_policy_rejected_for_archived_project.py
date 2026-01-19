from app.services.automation_policy_evaluator import evaluate_automation_policy

def test_policy_rejected_for_archived_project(
    archived_project,
    admin_user,
):
    result = evaluate_automation_policy(
        user=admin_user,
        project=archived_project,
        policy="auto_expire_links",
        enabled=True,
    )

    assert result["allowed"] is False

