import pytest
from datetime import datetime
from dataclasses import dataclass
from fastapi.testclient import TestClient
from sqlalchemy import text
import app.models.rendered_snapshot  # noqa: F401

from tests.fixtures.export_job import export_job
from app.main import app
from app.db.session import SessionLocal, engine
from app.db.base import Base
from app.api.deps import get_current_user

from app.models.user import User
from app.models.project import Project
from app.models.rendered_snapshot import RenderedSnapshot
from app.models.export_artifact import ExportArtifact
from app.models.rendered_snapshot import RenderedSnapshot, SnapshotStatus

from app.services.distribution_revocation import revoke_distribution_request
from app.services.distribution_capabilities import compute_distribution_capabilities
from app.services.snapshot_finalize import finalize_snapshot

from app.core.security import oauth2_scheme


# -------------------------------------------------
# HTTP client
# -------------------------------------------------

@pytest.fixture
def client():
    return TestClient(app)


# -------------------------------------------------
# Test database schema (Phase K canonical)
# -------------------------------------------------

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    with engine.connect() as conn:
        conn.execute(text("PRAGMA foreign_keys=OFF"))
        Base.metadata.drop_all(bind=conn)
        Base.metadata.create_all(bind=conn)
        conn.execute(text("PRAGMA foreign_keys=ON"))


# -------------------------------------------------
# Database session
# -------------------------------------------------

@pytest.fixture
def db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------------------------------------
# 🧹 Test isolation — clear journal entries
# -------------------------------------------------

@pytest.fixture(autouse=True)
def clear_journal_entries(db):
    db.execute(text("DELETE FROM journal_entries"))
    db.commit()


# -------------------------------------------------
# 🔐 OAUTH2 SCHEME OVERRIDE (TESTS ONLY)
# -------------------------------------------------

@pytest.fixture(autouse=True)
def override_oauth2_scheme():
    """
    Disable OAuth2 header enforcement in tests.

    This allows get_current_user to be controlled via
    override_get_current_user without requiring
    Authorization: Bearer headers.
    """
    app.dependency_overrides[oauth2_scheme] = lambda: "test-token"
    yield
    app.dependency_overrides.pop(oauth2_scheme, None)


# -------------------------------------------------
# 🔐 AUTH IDENTITY OVERRIDE (SINGLE SOURCE OF TRUTH)
# -------------------------------------------------

@pytest.fixture(autouse=True)
def override_get_current_user(request, admin_user):
    """
    Canonical test-time identity resolver.
    Bypasses OAuth2 completely.
    """

    def _override():
        if hasattr(request.node, "user"):
            return request.node.user
        if hasattr(request.node, "_forced_user"):
            return request.node._forced_user
        return admin_user

    app.dependency_overrides[get_current_user] = _override
    yield
    app.dependency_overrides.pop(get_current_user, None)
    

# -------------------------------------------------
# 📦 Phase M — inject export_snapshot into tests
# -------------------------------------------------

@pytest.fixture(autouse=True)
def inject_export_snapshot(request):
    """
    Injects export_snapshot into EVERY test module's globals.

    Required because Phase M tests call export_snapshot(...)
    without importing it explicitly.
    """
    from app.services import export_snapshot
    request.module.export_snapshot = export_snapshot


# -------------------------------------------------
# 📦 Phase 4.5 — inject finalize_snapshot into tests
# -------------------------------------------------

@pytest.fixture(autouse=True)
def inject_finalize_snapshot(request):
    """
    Injects finalize_snapshot into EVERY test module's globals.

    Required because Phase 4.5 tests call finalize_snapshot(...)
    without importing it explicitly.
    """
    from app.services.snapshot_finalize import finalize_snapshot
    request.module.finalize_snapshot = finalize_snapshot


# -------------------------------------------------
# 📜 Phase 4.5 — inject get_audit_events into tests
# -------------------------------------------------

@pytest.fixture(autouse=True)
def inject_get_audit_events(request):
    """
    Injects get_audit_events into EVERY test module's globals.

    Required because Phase 4.5 audit tests call
    get_audit_events(...) without importing it.
    """
    from app.services.audit import get_audit_events
    request.module.get_audit_events = get_audit_events


# -------------------------------------------------
# 🔐 LEGACY auth() INJECTION (THE CRITICAL FIX)
# -------------------------------------------------

@pytest.fixture(autouse=True)
def inject_auth_helper(request):
    """
    Injects auth(user) into EVERY test module's globals.

    This is REQUIRED because tests call auth(...)
    without declaring it as a fixture.
    """

    def auth(user):
        request.node._forced_user = user
        return {"Authorization": "Bearer test-token"}

    request.module.auth = auth


# -------------------------------------------------
# Users
# -------------------------------------------------

@pytest.fixture
def admin_user(db):
    user = db.query(User).filter_by(email="admin_phase_i@test.com").first()
    if not user:
        user = User(
            email="admin_phase_i@test.com",
            hashed_password="__test_hash__",
            role="admin",
            is_active=True,
            is_admin=True,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    return user


@pytest.fixture
def owner_user(db):
    user = db.query(User).filter_by(email="owner_phase_k@test.com").first()
    if not user:
        user = User(
            email="owner_phase_k@test.com",
            hashed_password="__test_hash__",
            role="owner",
            is_active=True,
            is_admin=False,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    return user


@pytest.fixture
def editor_user(db):
    user = db.query(User).filter_by(email="editor_phase_k@test.com").first()
    if not user:
        user = User(
            email="editor_phase_k@test.com",
            hashed_password="__test_hash__",
            role="editor",
            is_active=True,
            is_admin=False,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    return user


@pytest.fixture
def editor_user_without_tuning_capability(db):
    """
    Editor role, but lacking canTune capability.
    Safe for reuse across multiple tests.
    """
    user = db.query(User).filter_by(email="editor_no_tune@test.com").first()
    if not user:
        user = User(
            email="editor_no_tune@test.com",
            hashed_password="__test_hash__",
            role="editor",
            is_active=True,
            is_admin=False,
            can_tune=False,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    return user


@pytest.fixture
def viewer_user(db):
    user = db.query(User).filter_by(email="viewer_phase_i@test.com").first()
    if not user:
        user = User(
            email="viewer_phase_i@test.com",
            hashed_password="__test_hash__",
            role="viewer",
            is_active=True,
            is_admin=False,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    return user


# -------------------------------------------------
# Projects
# -------------------------------------------------

@pytest.fixture
def project(db, admin_user):
    project = Project(
        name="Phase I Test Project",
        owner_id=admin_user.id,
        active_snapshot_id=None,
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


@pytest.fixture
def archived_project(db, project):
    project.archived_at = datetime.utcnow()
    db.commit()
    db.refresh(project)
    return project


# -------------------------------------------------
# Snapshots
# -------------------------------------------------

@pytest.fixture
def draft_snapshot(existing_draft_snapshot):
    """
    Canonical Phase 4 alias.
    Tests depend on this exact fixture name.
    """
    return existing_draft_snapshot


@pytest.fixture
def non_completed_snapshot(pending_snapshot):
    """
    Canonical Phase 4 alias:
    any snapshot that is NOT completed.
    """
    return pending_snapshot


@pytest.fixture
def completed_snapshot(db, project, admin_user):
    snap = RenderedSnapshot(
        project_id=project.id,
        scene_state_hash="__completed__",
        render_profile="default",
        engine_version="test-engine",
        status="completed",
        created_by=admin_user.id,
    )
    db.add(snap)
    db.commit()
    db.refresh(snap)
    return snap


@pytest.fixture
def existing_snapshot(db, project, admin_user):
    """
    Existing completed snapshot used to verify that
    Phase I.7 scene save does NOT mutate prior snapshots.
    """
    snap = RenderedSnapshot(
        project_id=project.id,
        scene_state_hash="__existing__",
        render_profile="default",
        engine_version="test-engine",
        status="completed",
        created_by=admin_user.id,
    )
    db.add(snap)
    db.commit()
    db.refresh(snap)
    return snap


@pytest.fixture
def pending_snapshot(db, project, admin_user):
    snap = RenderedSnapshot(
        project_id=project.id,
        scene_state_hash="__pending__",
        render_profile="default",
        engine_version="test-engine",
        status="pending",
        created_by=admin_user.id,
    )
    db.add(snap)
    db.commit()
    db.refresh(snap)
    return snap


@pytest.fixture
def failed_snapshot(db, project, admin_user):
    snap = RenderedSnapshot(
        project_id=project.id,
        scene_state_hash="__failed__",
        render_profile="default",
        engine_version="test-engine",
        status="failed",
        created_by=admin_user.id,
    )
    db.add(snap)
    db.commit()
    db.refresh(snap)
    return snap


@pytest.fixture
def obsolete_snapshot(db, project, admin_user):
    snap = RenderedSnapshot(
        project_id=project.id,
        scene_state_hash="__obsolete__",
        render_profile="default",
        engine_version="test-engine",
        status="obsolete",
        created_by=admin_user.id,
    )
    db.add(snap)
    db.commit()
    db.refresh(snap)
    return snap


@pytest.fixture
def archived_project_snapshot(db, admin_user):
    project = Project(
        name="Archived Snapshot Project",
        owner_id=admin_user.id,
        archived_at=datetime.utcnow(),
    )
    db.add(project)
    db.commit()
    db.refresh(project)

    snap = RenderedSnapshot(
        project_id=project.id,
        scene_state_hash="__archived__",
        render_profile="default",
        engine_version="test-engine",
        status="completed",
        created_by=admin_user.id,
    )
    db.add(snap)
    db.commit()
    db.refresh(snap)
    return snap

@pytest.fixture
def existing_draft_snapshot(db, completed_snapshot, editor_user):
    """
    Existing draft snapshot for the same project.
    Used by Phase 4+ editor mutation & selection tests.
    """

    draft = RenderedSnapshot(
        project_id=completed_snapshot.project_id,
        scene_state_hash=completed_snapshot.scene_state_hash,
        render_profile=completed_snapshot.render_profile,
        engine_version=completed_snapshot.engine_version,
        status=SnapshotStatus.DRAFT.value,
        parent_snapshot_id=completed_snapshot.id,
        created_by=editor_user.id,
        body_state={
            "nodes": [
                {"id": "body.root", "type": "node", "editable": True},
            ],
            "panels": [
                {"id": "door.front.left", "type": "panel", "editable": True},
            ],
            "curves": [],
            "reference_planes": [],
        },
    )

    db.add(draft)
    db.commit()
    db.refresh(draft)
    return draft


# -------------------------------------------------
# Scene helpers
# -------------------------------------------------

@pytest.fixture
def valid_scene_state():
    return {
        "models": [],
        "materials": [],
        "decals": [],
        "lights": [],
        "camera": {
            "position": [0, 0, 5],
            "target": [0, 0, 0],
        },
    }


class _SceneHandle:
    def __init__(self, project_id: int):
        self.id = project_id


@pytest.fixture
def scene(project):
    return _SceneHandle(project.id)


@pytest.fixture
def archived_scene(archived_project):
    return _SceneHandle(archived_project.id)


# -------------------------------------------------
# 📦 Phase M — Export Artifacts (REQUIRED FOR M.5)
# -------------------------------------------------

@dataclass
class DummyExportArtifact:
    path: str
    bytes: bytes


@pytest.fixture
def export_artifacts():
    """
    Canonical derived artifacts used by Phase M.5 ZIP packaging tests.
    These are NOT snapshots and MUST remain immutable.
    """
    return [
        DummyExportArtifact("render.png", b"render-bytes"),
        DummyExportArtifact("print/design.tiff", b"print-bytes"),
        DummyExportArtifact("vector/decals.svg", b"vector-bytes"),
        DummyExportArtifact("3d/model.glb", b"3d-bytes"),
    ]


# -------------------------------------------------
# 📦 Phase M — Export Records (REQUIRED FOR Phase N)
# -------------------------------------------------

@pytest.fixture
def completed_export(db, export_job, project, completed_snapshot):
    """
    Canonical completed export used by Phase N distribution tests.
    """
    export_job.project_id = project.id
    export_job.snapshot_id = completed_snapshot.id
    export_job.export_type = "image"
    export_job.status = "completed"

    db.commit()
    db.refresh(export_job)
    return export_job


@pytest.fixture
def pending_export(db, export_job, project, completed_snapshot):
    """
    Non-distributable export (used to assert rejection paths).
    """
    export_job.project_id = project.id
    export_job.snapshot_id = completed_snapshot.id
    export_job.export_type = "image"
    export_job.status = "pending"

    db.commit()
    db.refresh(export_job)
    return export_job


# -------------------------------------------------
# 🔁 Fixture alias (Phase M.5 contract compatibility)
# -------------------------------------------------

@pytest.fixture
def artifacts(export_artifacts):
    """
    Alias required by Phase M.5 ZIP packaging tests.
    Do NOT remove — tests depend on this name.
    """
    return export_artifacts


# -------------------------------------------------
# 🔗 Phase N.2 — Distribution Request Fixtures
# -------------------------------------------------

from app.models.distribution_request import DistributionRequest


@pytest.fixture
def signed_url_distribution_request(db, completed_export):
    """
    Valid Phase N.1 distribution request targeting signed URLs.
    Used by Phase N.2 signed URL delivery tests.
    """
    req = DistributionRequest(
        export_id=completed_export.id,
        target="signed_url",
        options={"expires_in_hours": 24},
    )
    db.add(req)
    db.commit()
    db.refresh(req)
    return req


@pytest.fixture
def distribution_request_with_pending_export(db, pending_export):
    """
    Distribution request pointing at a non-completed export.
    Must be rejected by Phase N.2.
    """
    req = DistributionRequest(
        export_id=pending_export.id,
        target="signed_url",
        options={"expires_in_hours": 24},
    )
    db.add(req)
    db.commit()
    db.refresh(req)
    return req


# -------------------------------------------------
# 🔗 Phase N.3 — Active Distribution Request
# -------------------------------------------------

@pytest.fixture
def active_distribution_request(db, completed_export):
    """
    A valid, non-revoked distribution request.
    Used by Phase N.3 revocation tests.
    """
    req = DistributionRequest(
        export_id=completed_export.id,
        target="direct_download",
        options={},
    )
    db.add(req)
    db.commit()
    db.refresh(req)
    return req


@pytest.fixture
def revoked_distribution_request(db, completed_export, admin_user):
    """
    Revoked distribution request created via the real revocation service.
    This guarantees audit integrity (Phase N.4).
    """
    req = DistributionRequest(
        export_id=completed_export.id,
        target="signed_url",
        options={"expires_in_hours": 24},
    )
    db.add(req)
    db.commit()
    db.refresh(req)

    caps = compute_distribution_capabilities(
        user=admin_user,
        project=completed_export.project,
    )

    revoke_distribution_request(
        db=db,
        user=admin_user,
        distribution_request=req,
        capabilities=caps,
    )

    return req


# -------------------------------------------------
# 🔁 Phase M fixture aliases (REQUIRED)
# -------------------------------------------------

@pytest.fixture
def invalid_snapshot(failed_snapshot):
    """
    Alias required by Phase M tests.
    Invalid geometry == failed snapshot.
    """
    return failed_snapshot


@pytest.fixture
def snapshot_that_triggers_export_error(failed_snapshot):
    """
    Alias required by Phase M failure-path tests.
    """
    return failed_snapshot

