# backend/app/models/signed_url.py

from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
import uuid

from app.db.base import Base


class SignedURL(Base):
    __tablename__ = "signed_urls"

    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    distribution_request_id = Column(
        String(36),
        ForeignKey("distribution_requests.id", ondelete="CASCADE"),
        nullable=False,
    )

    token = Column(String, unique=True, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    revoked_at = Column(DateTime, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # 🔁 Back-reference
    distribution_request = relationship(
        "DistributionRequest",
        back_populates="signed_urls",
    )

    # =========================
    # PHASE N.3 — REVOCATION
    # =========================

    def revoke(self):
        if self.revoked_at is None:
            self.revoked_at = datetime.utcnow()

    @property
    def is_revoked(self) -> bool:
        return self.revoked_at is not None

