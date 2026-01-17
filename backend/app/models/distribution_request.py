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

    # 🔗 REQUIRED FK — THIS IS WHAT FIXES THE ERROR
    export_id = Column(
        String(36),
        ForeignKey("export_jobs.id", ondelete="CASCADE"),
        nullable=False,
    )

    target = Column(String, nullable=False)
    options = Column(JSON, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    revoked_at = Column(DateTime, nullable=True)

    # 🔁 Back-reference (optional but clean)
    export = relationship("ExportJob", back_populates="distribution_requests")

