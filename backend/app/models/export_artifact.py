# backend/app/models/export_artifact.py

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.db.base import Base


class ExportArtifact(Base):
    __tablename__ = "export_artifacts"

    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    export_job_id = Column(
        String(36),
        ForeignKey("export_jobs.id", ondelete="CASCADE"),
        nullable=False,
    )

    snapshot_id = Column(
        Integer,
        nullable=False,
    )

    bytes = Column(String, nullable=False)
    hash = Column(String, nullable=False)
    format = Column(String, nullable=False)

    status = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    export_job = relationship(
        "ExportJob",
        back_populates="artifacts",
    )

    # -------------------------------------------------
    # Constructors (PHASE M CANONICAL)
    # -------------------------------------------------

    @staticmethod
    def completed(*, bytes: bytes, hash: str, format: str, snapshot_id, export_job_id):
        return ExportArtifact(
            bytes=bytes,
            hash=hash,
            format=format,
            snapshot_id=snapshot_id,
            export_job_id=export_job_id,
            status="completed",
        )

    @staticmethod
    def failed(*, format: str, snapshot_id, export_job_id):
        return ExportArtifact(
            export_job_id=export_job_id,
            bytes=b"",
            hash="",
            format=format,
            snapshot_id=snapshot_id,
            status="failed",
        )

    # -------------------------------------------------
    # Phase M legacy compatibility (READ-ONLY)
    # -------------------------------------------------

    def __getitem__(self, key):
        """
        Phase M compatibility layer.

        Allows legacy tests to access artifacts like:
            artifact["hash"]
            artifact["bytes"]
            artifact["format"]
            artifact["status"]

        This MUST be removed in Phase N.
        """
        if not hasattr(self, key):
            raise KeyError(key)
        return getattr(self, key)

