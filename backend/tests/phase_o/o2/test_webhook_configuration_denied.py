from app.services.webhook_validator import validate_webhook_configuration

def test_owner_cannot_configure_webhook(
    project,
    owner_user,
):
    result = validate_webhook_configuration(
        user=owner_user,
        project=project,
        url="https://example.com/webhook",
        events=["SIGNED_URL_CREATED"],
    )

    assert result["allowed"] is False

