# backend/app/models/export_job.py

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.db.base import Base


class ExportJob(Base):
    """
    Execution record for an export.
    Created AFTER ExportRecord (intent).
    """

    __tablename__ = "export_jobs"

    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    # 🔗 Phase N authority anchor
    # MUST remain nullable
    project_id = Column(
        String(36),
        ForeignKey("projects.id"),
        nullable=True,  # ❗ DO NOT CHANGE
    )

    # 🔒 Canonical link to export intent
    export_request_id = Column(
        Integer,
        ForeignKey("exports.id", ondelete="CASCADE"),
        nullable=False,
    )

    status = Column(String, nullable=False, default="requested")
    progress = Column(Integer, default=0)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    # 🔒 Read-only authority links (Phase N)
    project = relationship("Project")

    distribution_requests = relationship(
        "DistributionRequest",
        back_populates="export",
        cascade="all, delete-orphan",
    )

    def mark_running(self):
        self.status = "running"
        self.updated_at = datetime.utcnow()

    def mark_completed(self):
        self.status = "completed"
        self.updated_at = datetime.utcnow()

    def mark_failed(self, reason=None):
        self.status = "failed"
        self.updated_at = datetime.utcnow()

    def cancel(self):
        self.status = "cancelled"
        self.updated_at = datetime.utcnow()
