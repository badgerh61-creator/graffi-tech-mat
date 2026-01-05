from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from app.db.base import Base


class SnapshotStatus(str):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class RenderedSnapshot(Base):
    __tablename__ = "rendered_snapshots"

    __table_args__ = (
        UniqueConstraint(
            "project_id",
            "scene_state_hash",
            "render_profile",
            "engine_version",
            name="uq_snapshot_deterministic",
        ),
    )

    id = Column(Integer, primary_key=True, index=True)

    project_id = Column(
    Integer,
    ForeignKey("projects.id", ondelete="CASCADE"),
    nullable=False,
    index=True,
    )

    scene_state_hash = Column(String, index=True, nullable=False)
    render_profile = Column(String, nullable=False)

    image_url = Column(String, nullable=True)
    engine_version = Column(String, nullable=False)

    status = Column(String, default=SnapshotStatus.PENDING, nullable=False)
    error_message = Column(String, nullable=True)

    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

