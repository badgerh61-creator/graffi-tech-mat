# backend/app/models/distribution_request.py

from sqlalchemy import Column, String, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.db.base import Base


class DistributionRequest(Base):
    __tablename__ = "distribution_requests"

    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    # 🔗 REQUIRED FK — authoritative export linkage
    export_id = Column(
        String(36),
        ForeignKey("export_jobs.id", ondelete="CASCADE"),
        nullable=False,
    )

    target = Column(String, nullable=False)
    options = Column(JSON, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    revoked_at = Column(DateTime, nullable=True)

    # 🔁 Back-references
    export = relationship(
        "ExportJob",
        back_populates="distribution_requests",
    )

    signed_urls = relationship(
        "SignedURL",
        back_populates="distribution_request",
        cascade="all, delete-orphan",
    )

    # =========================
    # PHASE N.3 — REVOCATION
    # =========================

    def revoke(self):
        """
        Revoke this distribution request and all derived access.
        """
        if self.revoked_at is not None:
            raise RuntimeError("Distribution request already revoked")

        self.revoked_at = datetime.utcnow()

        for url in self.signed_urls:
            url.revoke()

    @property
    def is_revoked(self) -> bool:
        return self.revoked_at is not None

