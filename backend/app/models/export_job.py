from sqlalchemy import Column, String, Integer, DateTime
from datetime import datetime
import uuid

from app.db.base import Base


class ExportJob(Base):
    __tablename__ = "export_jobs"

    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    export_request_id = Column(
        String(36),
        nullable=False,
    )

    status = Column(String, nullable=False, default="requested")
    progress = Column(Integer, default=0)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

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

