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

    # ---- Deterministic identity (Phase I / J) ----
    scene_state_hash = Column(String, index=True, nullable=False)
    render_profile = Column(String, nullable=False)
    engine_version = Column(String, nullable=False)

    # ---- Snapshot state payloads (Phase K) ----
    # NOTE:
    # There is NO scene_state column by design.
    # Scene state is referenced by hash only.
    decor_state = Column(JSON, nullable=True)
    tuning_state = Column(JSON, nullable=True)
    body_state = Column(JSON, nullable=True)

    # ---- Render output ----
    image_url = Column(String, nullable=True)

    # ---- Lifecycle ----
    status = Column(String, default=SnapshotStatus.PENDING, nullable=False)
    error_message = Column(String, nullable=True)

    # ---- Audit ----
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # ------------------------------------------------------------------
    # Phase K contract: deterministic, immutable snapshot hash
    # ------------------------------------------------------------------
    @property
    def hash(self) -> str:
        """
        Deterministic content hash for snapshot immutability and deduplication.

        IMPORTANT:
        - Computed, not stored
        - Compatible with Phase I/J schema
        - Covers ONLY logical state
        - Excludes DB ids, timestamps, URLs
        """
        payload = {
            "scene_state_hash": self.scene_state_hash,
            "decor_state": self.decor_state,
            "tuning_state": self.tuning_state,
            "body_state": self.body_state,
            "render_profile": self.render_profile,
            "engine_version": self.engine_version,
        }

        encoded = json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")

        return hashlib.sha256(encoded).hexdigest()

    # ------------------------------------------------------------------
    # Phase I.4 compatibility shim — snapshot invalidation
    # ------------------------------------------------------------------
    @property
    def is_obsolete(self) -> bool:
        """
        Phase I.4 placeholder.

        Until snapshot invalidation is implemented,
        snapshots are never obsolete.
        """
        return False

    # ------------------------------------------------------------------
    # Phase K.1 compatibility shim — vehicle surface definition
    # ------------------------------------------------------------------
    @property
    def vehicle_panels(self) -> set[str]:
        """
        Phase K.1 placeholder.

        Until vehicle body schema exists, expose a
        deterministic, fixed exterior surface set.

        This allows decor validation without coupling
        snapshots to vehicle geometry.
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
            "bumper_rear",
        }

