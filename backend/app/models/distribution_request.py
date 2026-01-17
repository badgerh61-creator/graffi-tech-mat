from sqlalchemy import Column, String, DateTime, JSON
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

    export_id = Column(String(36), nullable=False)
    target = Column(String, nullable=False)
    options = Column(JSON, nullable=True)

    status = Column(String, default="accepted", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

