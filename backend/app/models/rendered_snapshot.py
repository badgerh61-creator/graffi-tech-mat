# models/rendered_snapshot.py

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    JSON,
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base

import hashlib
import json
from enum import Enum


# =====================================================
# Snapshot Lifecycle Status (AUTHORITATIVE)
# =====================================================

class SnapshotStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    OBSOLETE = "obsolete"
    DRAFT = "draft"
    FINALIZED = "finalized"


# =====================================================
# Rendered Snapshot Model
# =====================================================

class RenderedSnapshot(Base):
    __tablename__ = "rendered_snapshots"

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

    # -------------------------------------------------
    # Deterministic inputs (render identity)
    # -------------------------------------------------

    scene_state_hash = Column(String, index=True, nullable=False)
    render_profile = Column(String, nullable=False)
    engine_version = Column(String, nullable=False)

    deterministic_key = Column(String, nullable=True, index=True)

    # -------------------------------------------------
    # Editable state payloads (DRAFT / MUTATION SOURCE)
    # -------------------------------------------------

    decor_state = Column(JSON, nullable=True)
    tuning_state = Column(JSON, nullable=True)
    body_state = Column(JSON, nullable=True)

    # -------------------------------------------------
    # Render output
    # -------------------------------------------------

    image_url = Column(String, nullable=True)

    # -------------------------------------------------
    # Lifecycle
    # -------------------------------------------------

    status = Column(
        String,
        default=SnapshotStatus.PENDING.value,
        nullable=False,
    )

    parent_snapshot_id = Column(
        Integer,
        ForeignKey("rendered_snapshots.id"),
        nullable=True,
    )

    error_message = Column(String, nullable=True)

    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # =====================================================
    # Derived helpers
    # =====================================================

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
            json.dumps(
                payload,
                sort_keys=True,
                separators=(",", ":"),
            ).encode("utf-8")
        ).hexdigest()

    @property
    def is_draft(self) -> bool:
        return self.status == SnapshotStatus.DRAFT.value

    @property
    def is_completed(self) -> bool:
        return self.status == SnapshotStatus.COMPLETED.value

    @property
    def is_obsolete(self) -> bool:
        return self.status == SnapshotStatus.OBSOLETE.value

    @property
    def payload(self) -> dict:
        return {
            "decor": self.decor_state or {},
            "tuning": self.tuning_state or {},
            "body": self.body_state or {},
        }

    # =====================================================
    # Phase K — Snapshot Cloning (CRITICAL)
    # =====================================================

    def clone_for_mutation(self, *, created_by: int):
        """
        Phase K invariant:
        All mutations MUST operate on a cloned snapshot.
        """
        return RenderedSnapshot(
            project_id=self.project_id,
            scene_state_hash=self.scene_state_hash,
            render_profile=self.render_profile,
            engine_version=self.engine_version,
            decor_state=self.decor_state,
            tuning_state=self.tuning_state,
            body_state=self.body_state,
            status=SnapshotStatus.COMPLETED.value,
            parent_snapshot_id=self.id,
            created_by=created_by,
        )

    # =====================================================
    # Phase 5 — Scene Graph Projection (AUTHORITATIVE)
    # =====================================================

    @property
    def scene_graph_data(self) -> dict:
        body = self.body_state or {}

        def normalize(value):
            """
            Accept dict or list and always return list.
            """
            if isinstance(value, dict):
                return list(value.values())
            if isinstance(value, list):
                return value
            return []

        return {
            "nodes": normalize(body.get("nodes")),
            "panels": normalize(body.get("panels")),
            "curves": normalize(body.get("curves")),
            "reference_planes": normalize(body.get("reference_planes")),
        }

    @property
    def scene_graph(self):
        """
        Lazy scene graph adapter (prevents circular imports)
        """
        from app.services.scene_graph import SceneGraphView

        data = self.scene_graph_data

        return SceneGraphView(
            nodes=data["nodes"],
            panels=data["panels"],
            curves=data["curves"],
            reference_planes=data["reference_planes"],
        )

