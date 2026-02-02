# backend/app/models/rendered_snapshot.py

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    JSON,
    Boolean, 
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, backref
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
    ABANDONED = "abandoned"

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
  
    # Phase S — corruption flag (hard safety gate)
    is_corrupted = Column(
        Boolean,
        default=False,
        nullable=False,
    )

    parent_snapshot_id = Column(
        Integer,
        ForeignKey("rendered_snapshots.id"),
        nullable=True,
    )
    parent_snapshot = relationship(
        "RenderedSnapshot",
        remote_side=[id],
        backref=backref(
            "child_snapshots",
            order_by="RenderedSnapshot.created_at",
        ),
    )

    error_message = Column(String, nullable=True)

    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # -------------------------------------------------
    # Phase U — Multi-user ownership & locking (AUTHORITATIVE)
    # -------------------------------------------------

    owner_user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True,
        index=True,
    )

    locked_at = Column(
        DateTime(timezone=True),
        nullable=True,
    )

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

    # Phase S — finalization gate (AUTHORITATIVE)
    @property
    def is_finalizable(self) -> bool:
        """
        A snapshot may be finalized ONLY if:
        - it is a draft
        - it is not corrupted
        """
        return (
            self.status == SnapshotStatus.DRAFT.value
            and not self.is_corrupted
        )

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
        return RenderedSnapshot(
            project_id=self.project_id,
            scene_state_hash=self.scene_state_hash,
            render_profile=self.render_profile,
            engine_version=self.engine_version,
            decor_state=self.decor_state,
            tuning_state=self.tuning_state,
            body_state=self.body_state,
            status=SnapshotStatus.DRAFT.value,
            parent_snapshot_id=self.id,
            created_by=created_by,
        )

    # =====================================================
    # Phase K — Legacy Compatibility Accessors (DO NOT REMOVE)
    # =====================================================

    @property
    def vehicle_panels(self):
        return (self.body_state or {}).get("panels", [])

    @property
    def vehicle_nodes(self):
        return (self.body_state or {}).get("nodes", [])

    @property
    def vehicle_curves(self):
        return (self.body_state or {}).get("curves", [])

    # =====================================================
    # Phase 5 — Scene Graph Projection (AUTHORITATIVE)
    # =====================================================

    @property
    def scene_graph_data(self) -> dict:
        body = self.body_state or {}

        def normalize(value):
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
        from app.services.scene_graph import SceneGraphView
        data = self.scene_graph_data
        return SceneGraphView(
            nodes=data["nodes"],
            panels=data["panels"],
            curves=data["curves"],
            reference_planes=data["reference_planes"],
        )


# =====================================================
# Phase 5.3 — Constraint helpers
# =====================================================

def is_symmetric(self, target_id: str, plane: str, params: dict) -> bool:
    graph = self.scene_graph
    target = (
        graph.get_panel(target_id)
        or graph.get_node(target_id)
        or graph.get_curve(target_id)
    )
    if not target:
        return True
    if getattr(target, "_data", {}).get("symmetric", True) is False:
        return True
    if plane == "vehicle_centerline" and params.get("x", 0) != 0:
        return False
    return True

RenderedSnapshot.is_symmetric = is_symmetric


# =====================================================
# Phase 5.4 — Authoritative Mutation Entry Point
# =====================================================

def _apply_transform_internal(self, *, target_id: str, operation: str, params: dict):
    from app.services.mutable_scene_graph import MutableSceneGraph
    graph = MutableSceneGraph(body_state=self.body_state)
    graph.apply_transform(
        target_id=target_id,
        operation=operation,
        params=params,
    )
    self.body_state = graph.serialize()

RenderedSnapshot._apply_transform_internal = _apply_transform_internal

def apply_transform(self, *args, **kwargs):
    raise RuntimeError(
        "Direct snapshot mutation is forbidden. "
        "Use snapshot_mutations.apply_transform()."
    )

RenderedSnapshot.apply_transform = apply_transform


# =====================================================
# Phase 5.5 — Undo / Redo Snapshot Navigation
# =====================================================

from app.services.snapshot_navigation import undo_snapshot, redo_snapshot

RenderedSnapshot.undo = lambda self, *, db, user: undo_snapshot(db=db, snapshot=self, user=user)
RenderedSnapshot.redo = lambda self, *, db, user: redo_snapshot(db=db, snapshot=self, user=user)


# =====================================================
# Phase J.3 — Constraint Solving Helpers (STUBS)
# =====================================================

RenderedSnapshot.check_constraints_satisfiable = lambda self: True
RenderedSnapshot.apply_solved_parameters_from = lambda self, other: None


# =====================================================
# Phase J — Curve View Adapter (READ-ONLY)
# =====================================================

class CurveView:
    def __init__(self, data: dict):
        self._data = data

    @property
    def id(self):
        return self._data.get("id")

    @property
    def parameters(self):
        return self._data.get("parameters", {})

    @property
    def constraints(self):
        return self._data.get("constraints", [])

    def __repr__(self):
        return f"<CurveView {self.id}>"


@property
def curves(self):
    raw = (self.body_state or {}).get("curves", [])
    return [CurveView(c) for c in raw]

RenderedSnapshot.curves = curves


# =====================================================
# Phase K.1 — Surface View Adapter (READ-ONLY) ✅ ADDITIVE
# =====================================================

class SurfaceView:
    """
    Lightweight read-only adapter for surface dicts.
    Storage remains dict-based.
    Compatible with Phase K.1, K.2, K.3.
    """

    def __init__(self, data: dict):
        self._data = data

    # -------------------------
    # Attribute-style access (Phase K.1)
    # -------------------------

    @property
    def id(self):
        return self._data.get("id")

    @property
    def method(self):
        return self._data.get("method")

    @property
    def vertices(self):
        return self._data.get("vertices")

    @property
    def faces(self):
        return self._data.get("faces")

    @property
    def metadata(self):
        return self._data.get("metadata", {})

    # -------------------------
    # Dict-style access (Phase K.2 / K.3)
    # -------------------------

    def __getitem__(self, key):
        return self._data[key]

    def get(self, key, default=None):
        return self._data.get(key, default)

    def __repr__(self):
        return f"<SurfaceView method={self.method}>"


# =====================================================
# Phase K.2 — Surface Compatibility Accessor (WRAPPED)
# =====================================================

@property
def surfaces(self):
    raw = (self.body_state or {}).get("surfaces", [])
    return [SurfaceView(s) for s in raw]

RenderedSnapshot.surfaces = surfaces


# =====================================================
# Phase K.2 — Panels (UNCHANGED)
# =====================================================

from sqlalchemy.orm.attributes import flag_modified

@property
def panels(self):
    return (self.body_state or {}).get("panels", [])

@panels.setter
def panels(self, value):
    if self.body_state is None:
        self.body_state = {}
    self.body_state["panels"] = value
    flag_modified(self, "body_state")

RenderedSnapshot.panels = panels


# =====================================================
# Phase U — Legacy Compatibility Accessors (ADAPTERS)
# =====================================================
# These are READ-ONLY shims to preserve Phase U.2 / U.4
# test contracts after ownership authority was moved
# onto RenderedSnapshot itself.
#
# ⚠️ DO NOT add logic here.
# ⚠️ DO NOT use these in new production code.
# ⚠️ Safe to remove once legacy tests are retired.
# =====================================================

@property
def snapshot_id(self):
    """
    Phase U.2 compatibility accessor.

    Legacy Phase U.2 tests expect acquire_draft_lock()
    to return an object with `.snapshot_id` (DraftLock-like).

    Authority is on RenderedSnapshot, so this aliases to `id`.
    """
    return self.id


@property
def user_id(self):
    """
    Phase U.4 compatibility accessor.

    Legacy Phase U.4 tests expect handoff_draft_ownership()
    to return an object with `.user_id` (DraftLock-like).

    Authority is on RenderedSnapshot, so this aliases to
    `owner_user_id`.
    """
    return self.owner_user_id


# 🔒 Bind compatibility accessors to model
RenderedSnapshot.snapshot_id = snapshot_id
RenderedSnapshot.user_id = user_id

