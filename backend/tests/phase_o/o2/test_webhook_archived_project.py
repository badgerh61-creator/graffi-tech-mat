from app.services.webhook_validator import validate_webhook_configuration

def test_archived_project_disables_webhooks(
    archived_project,
    admin_user,
):
    result = validate_webhook_configuration(
        user=admin_user,
        project=archived_project,
        url="https://example.com/webhook",
        events=["SIGNED_URL_CREATED"],
    )

    assert result["allowed"] is False

