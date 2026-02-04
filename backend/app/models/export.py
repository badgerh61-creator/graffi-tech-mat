# backend/app/models/export.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func

from app.db.base import Base


class ExportRecord(Base):
    """
    Canonical export request (INTENT).
    Represents user intent, NOT execution.
    Execution lives in ExportJob (Phase M).
    """

    __tablename__ = "exports"

    id = Column(Integer, primary_key=True, index=True)

    # 🔒 Authority anchor — ONLY completed snapshots
    snapshot_id = Column(
        Integer,
        ForeignKey("rendered_snapshots.id", ondelete="CASCADE"),
        nullable=False,
    )

    # image / video / archive (future)
    export_type = Column(
        String,
        nullable=False,
        default="image",
    )

    # png / jpg (future: webp, exr)
    format = Column(String, nullable=False)

    # 2k / 4k / 8k
    resolution = Column(String, nullable=False)

    # Intent-level state (execution state lives elsewhere)
    status = Column(
        String,
        nullable=False,
        default="requested",
    )

    created_by = Column(
        Integer,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # Optional link to execution (Phase M)
    job_id = Column(
        String(36),
        ForeignKey("export_jobs.id", ondelete="SET NULL"),
        nullable=True,
    )
 
