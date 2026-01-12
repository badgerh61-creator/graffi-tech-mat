import pytest
import json
import hashlib

from app.models.rendered_snapshot import RenderedSnapshot


def _hash_scene_and_tuning(scene_state, tuning_state):
    """
    Canonical deterministic hash helper for Phase K.2 tests.
    """
    payload = {
        "scene": scene_state or {},
        "tuning": tuning_state or {},
    }
    raw = json.dumps(payload, sort_keys=True)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _clone_snapshot(db, base_snapshot, *, tuning_state=None):
    """
    Create or reuse a snapshot derived from base_snapshot.
    Deterministic + uniqueness-safe.
    """

    scene_state_hash = _hash_scene_and_tuning(
        scene_state={},          # no scene mutation in K.2
        tuning_state=tuning_state,
    )

    existing = (
        db.query(RenderedSnapshot)
        .filter_by(
            project_id=base_snapshot.project_id,
            scene_state_hash=scene_state_hash,
            render_profile=base_snapshot.render_profile,
            engine_version=base_snapshot.engine_version,
        )
        .first()
    )

    if existing:
        return existing

    snap = RenderedSnapshot(
        project_id=base_snapshot.project_id,
        scene_state_hash=scene_state_hash,
        render_profile=base_snapshot.render_profile,
        engine_version=base_snapshot.engine_version,
        status="completed",
        created_by=base_snapshot.created_by,
        tuning_state=tuning_state,
    )

    db.add(snap)
    db.commit()
    db.refresh(snap)
    return snap


@pytest.fixture
def snapshot_factory(db, completed_snapshot):
    """
    Factory to generate snapshots with controlled tuning state.
    Matches Phase K.2 test contract exactly.
    """
    def _factory(*, tuning=None):
        return _clone_snapshot(
            db=db,
            base_snapshot=completed_snapshot,
            tuning_state=tuning or {},
        )
    return _factory

