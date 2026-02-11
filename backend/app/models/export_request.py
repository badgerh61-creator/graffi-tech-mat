# backend/app/models/export_request.py

from sqlalchemy import Column, Integer, String, ForeignKey, JSON, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.base import Base


class ExportRequest(Base):
    """
    Canonical Phase M export intent.
    Represents a validated request to export a snapshot.
    """

    __tablename__ = "export_requests"

    id = Column(Integer, primary_key=True)

    # 🔗 Authority graph
    project_id = Column(
        Integer,
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
    )

    snapshot_id = Column(
        Integer,
        ForeignKey("rendered_snapshots.id", ondelete="CASCADE"),
        nullable=False,
    )

    # 📦 Export intent
    export_type = Column(String, nullable=False)  # image / vector / 3d / zip
    options = Column(JSON, nullable=False, default=dict)

    status = Column(
        String,
        nullable=False,
        default="pending",  # pending → accepted → rejected
    )

    created_at = Column(DateTime, default=datetime.utcnow)

    # -------------------------------------------------
    # Relationships
    # -------------------------------------------------

    snapshot = relationship("RenderedSnapshot")
    project = relationship("Project")

    jobs = relationship(
        "ExportJob",
        back_populates="export_request",
        cascade="all, delete-orphan",
    )

