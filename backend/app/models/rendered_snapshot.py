from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy.sql import func
from app.db.base import Base

class SnapshotStatus(str):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class RenderedSnapshot(Base):
    __tablename__ = "rendered_snapshots"

    id = Column(Integer, primary_key=True, index=True)

    project_id = Column(Integer, index=True, nullable=False)
    scene_state_hash = Column(String, index=True, nullable=False)
    render_profile = Column(String, nullable=False)

    image_url = Column(String, nullable=True)
    engine_version = Column(String, nullable=False)

    status = Column(String, default=SnapshotStatus.PENDING)
    error_message = Column(String, nullable=True)

    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

