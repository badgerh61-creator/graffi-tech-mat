from sqlalchemy import Column, String, DateTime, ForeignKey
from datetime import datetime, timedelta
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
        ForeignKey("distribution_requests.id"),
        nullable=False,
    )

    token = Column(String, nullable=False, unique=True)
    expires_at = Column(DateTime, nullable=False)
    revoked_at = Column(DateTime, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    @property
    def is_revoked(self) -> bool:
        return self.revoked_at is not None

    @classmethod
    def create(cls, distribution_request_id: str, expires_in_hours: int):
        return cls(
            distribution_request_id=distribution_request_id,
            token=uuid.uuid4().hex,
            expires_at=datetime.utcnow() + timedelta(hours=expires_in_hours),
        )

