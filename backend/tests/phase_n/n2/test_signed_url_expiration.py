from datetime import datetime, timedelta

def test_signed_url_has_expiration(
    client,
    signed_url_distribution_request,
    admin_user,
):
    response = client.post(
        "/distributions/signed-urls",
        json={"distribution_request_id": signed_url_distribution_request.id},
        headers=auth(admin_user),
    )

    expires_at = datetime.fromisoformat(response.json()["expires_at"])
    assert expires_at > datetime.utcnow()

