from app.services.webhook_validator import validate_webhook_configuration

def test_webhook_requires_https(
    project,
    admin_user,
):
    result = validate_webhook_configuration(
        user=admin_user,
        project=project,
        url="http://example.com/webhook",
        events=["SIGNED_URL_CREATED"],
    )

    assert result["allowed"] is False
    assert result["reason"] == "https_required"

