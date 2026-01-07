import pytest
from datetime import datetime
from fastapi.testclient import TestClient

from app.main import app
from app.db.session import SessionLocal
from app.models.user import User
from app.models.project import Project
from app.models.rendered_snapshot import RenderedSnapshot
from app.api.deps import get_current_user


# -------------------------------------------------
# HTTP client
# -------------------------------------------------

@pytest.fixture
def client():
    return TestClient(app)


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
# Legacy auth() helper injection
# -------------------------------------------------

@pytest.fixture(autouse=True)
def inject_auth_helper(request):
    """
    Inject `auth()` into each test module's global namespace.

    Supports legacy tests that still call:
        headers=auth(user)
    """
    def _auth(_user=None):
        return {}

    request.module.auth = _auth


# -------------------------------------------------
# Admin user (canonical Phase I actor)
# -------------------------------------------------

@pytest.fixture
def admin_user(db):
    user = (
        db.query(User)
        .filter(User.email == "admin_phase_i@test.com")
        .first()
    )

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


# -------------------------------------------------
# 🔐 AUTH OVERRIDE (authoritative, Phase K safe)
# -------------------------------------------------

@pytest.fixture(autouse=True)
def override_get_current_user(request, admin_user):
    """
    Global auth override.

    - Defaults to admin_user
    - Tests may inject a user explicitly via:
          request.node.user = <fixture_user>
    """
    def _override():
        return getattr(request.node, "user", admin_user)

    app.dependency_overrides[get_current_user] = _override
    yield
    app.dependency_overrides.clear()


# -------------------------------------------------
# Auth header helper (kept for compatibility)
# -------------------------------------------------

@pytest.fixture
def auth():
    def _auth(_user=None):
        return {}
    return _auth


# -------------------------------------------------
# Owner user (distinct from admin in Phase K)
# -------------------------------------------------

@pytest.fixture
def owner_user(db):
    user = (
        db.query(User)
        .filter(User.email == "owner_phase_k@test.com")
        .first()
    )

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


# -------------------------------------------------
# Editor user (REAL editor, not admin)
# -------------------------------------------------

@pytest.fixture
def editor_user(db):
    user = (
        db.query(User)
        .filter(User.email == "editor_phase_k@test.com")
        .first()
    )

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


# -------------------------------------------------
# Viewer user (read-only)
# -------------------------------------------------

@pytest.fixture
def viewer_user(db):
    user = (
        db.query(User)
        .filter(User.email == "viewer_phase_i@test.com")
        .first()
    )

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
# Project fixture
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


# -------------------------------------------------
# Archived project
# -------------------------------------------------

@pytest.fixture
def archived_project(db, project):
    project.archived_at = datetime.utcnow()
    db.commit()
    db.refresh(project)
    return project


# -------------------------------------------------
# Snapshot fixtures
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


# -------------------------------------------------
# Archived project snapshot
# -------------------------------------------------

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
# Scene state fixtures (Phase I.7)
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


@pytest.fixture
def existing_snapshot(db, project, admin_user):
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


# -------------------------------------------------
# Scene compatibility helpers
# -------------------------------------------------

class _SceneHandle:
    def __init__(self, project_id: int):
        self.id = project_id


@pytest.fixture
def scene(project):
    return _SceneHandle(project.id)


@pytest.fixture
def archived_scene(archived_project):
    return _SceneHandle(archived_project.id)

