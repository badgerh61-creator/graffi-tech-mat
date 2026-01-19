from app.services.webhook_validator import validate_webhook_configuration

def test_admin_can_configure_webhook(
    project,
    admin_user,
):
    result = validate_webhook_configuration(
        user=admin_user,
        project=project,
        url="https://example.com/webhook",
        events=["SIGNED_URL_CREATED"],
    )

    assert result["allowed"] is True

