from uuid import uuid4
from datetime import datetime, timedelta

from app.models.signed_url import SignedURL

# 🔍 Phase P — observability
import app.observability.metrics as metrics_module

BASE_DOWNLOAD_URL = "https://download.graffi/internal"


def create_signed_url(*, db, distribution_request, expires_in_hours):
    if distribution_request.revoked_at:
        raise RuntimeError("Distribution request revoked")

    signed = SignedURL(
        distribution_request_id=distribution_request.id,
        token=uuid4().hex,
        expires_at=datetime.utcnow() + timedelta(hours=expires_in_hours),
    )

    db.add(signed)
    db.commit()
    db.refresh(signed)

    metrics_module.metrics.inc("distribution.signed_url.created.count")

    return {
        "url": f"{BASE_DOWNLOAD_URL}/{signed.token}",
        "expires_at": signed.expires_at.isoformat(),
    }

