from app.services.automation_policy_evaluator import evaluate_automation_policy

def test_policy_cannot_weaken_phase_n(
    project,
    admin_user,
):
    result = evaluate_automation_policy(
        user=admin_user,
        project=project,
        policy="auto_extend_link_lifetime",
        enabled=True,
    )

    assert result["allowed"] is False

