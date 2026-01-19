from app.services.webhook_validator import validate_webhook_configuration

def test_unknown_webhook_event_rejected(
    project,
    admin_user,
):
    result = validate_webhook_configuration(
        user=admin_user,
        project=project,
        url="https://example.com/webhook",
        events=["EXPORT_DELETED"],
    )

    assert result["allowed"] is False

