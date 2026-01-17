from app.models.signed_url import SignedURL

BASE_DOWNLOAD_URL = "https://download.graffi/internal"

def create_signed_url(*, db, distribution_request, expires_in_hours):
    if distribution_request.revoked_at:
        raise RuntimeError("Distribution request revoked")

    signed = SignedURL.create(
        distribution_request_id=distribution_request.id,
        expires_in_hours=expires_in_hours,
    )

    db.add(signed)
    db.commit()

    return {
        "url": f"{BASE_DOWNLOAD_URL}/{signed.token}",
        "expires_at": signed.expires_at.isoformat(),
    }

