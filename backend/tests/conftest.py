import pytest
from datetime import datetime
from dataclasses import dataclass
from fastapi.testclient import TestClient
from sqlalchemy import text

from tests.fixtures.export_job import export_job
from app.main import app
from app.db.session import SessionLocal, engine
from app.db.base import Base
from app.api.deps import get_current_user

from app.models.user import User
from app.models.project import Project
from app.models.rendered_snapshot import RenderedSnapshot
from app.models.export_artifact import ExportArtifact


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
# 🔐 AUTH IDENTITY OVERRIDE (SINGLE SOURCE OF TRUTH)
# -------------------------------------------------

@pytest.fixture(autouse=True)
def override_get_current_user(request, admin_user):
    """
    Priority (DO NOT CHANGE):
    1. request.node.user         (legacy explicit override)
    2. request.node._forced_user (auth(user))
    3. admin_user               (default)
    """

    def _override():
        if hasattr(request.node, "user"):
            return request.node.user
        if hasattr(request.node, "_forced_user"):
            return request.node._forced_user
        return admin_user

    app.dependency_overrides[get_current_user] = _override
    yield
    app.dependency_overrides.clear()


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
        return {}

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

