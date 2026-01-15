# models/rendered_snapshot.py

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    UniqueConstraint,
    JSON,
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base

import hashlib
import json


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

    project = relationship(
        "Project",
        foreign_keys=[project_id],
        backref="rendered_snapshots",
    )

    scene_state_hash = Column(String, index=True, nullable=False)
    render_profile = Column(String, nullable=False)
    engine_version = Column(String, nullable=False)

    decor_state = Column(JSON, nullable=True)
    tuning_state = Column(JSON, nullable=True)
    body_state = Column(JSON, nullable=True)

    image_url = Column(String, nullable=True)

    status = Column(String, default=SnapshotStatus.PENDING, nullable=False)
    error_message = Column(String, nullable=True)

    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    @property
    def hash(self) -> str:
        payload = {
            "scene_state_hash": self.scene_state_hash,
            "decor_state": self.decor_state,
            "tuning_state": self.tuning_state,
            "body_state": self.body_state,
            "render_profile": self.render_profile,
            "engine_version": self.engine_version,
        }

        return hashlib.sha256(
            json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()

    @property
    def is_obsolete(self) -> bool:
        return False

    @property
    def vehicle_panels(self) -> set[str]:
        """
        Panels common to ALL standard vehicles.
        Truck-specific panels are intentionally excluded.
        """
        return {
            "door_left",
            "door_right",
            "hood",
            "roof",
            "trunk",
            "fender_front_left",
            "fender_front_right",
            "fender_rear_left",
            "fender_rear_right",
            "bumper_front",
            # ❌ bumper_rear intentionally removed
        }

    @property
    def payload(self) -> dict:
        return {
            "decor": self.decor_state or {},
            "tuning": self.tuning_state or {},
            "body": self.body_state or {},
        }

