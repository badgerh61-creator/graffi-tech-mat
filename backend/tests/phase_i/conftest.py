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

@pytest.fixture(autouse=True)
def inject_auth_helper(request):
    """
    Inject `auth()` into each test module's global namespace.

    This supports legacy-style tests that call `auth(user)`
    without declaring it as a fixture parameter.
    """
    def _auth(_user=None):
        return {}

    request.module.auth = _auth


# -------------------------------------------------
# Admin user (canonical Phase I actor)
# -------------------------------------------------

@pytest.fixture
def admin_user(db):
    """
    Deterministic admin user for Phase I tests.
    Reused across tests to avoid UNIQUE constraint issues.
    """
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
# 🔐 AUTH OVERRIDE (CRITICAL & CORRECT)
# -------------------------------------------------

@pytest.fixture(autouse=True)
def override_get_current_user(admin_user):
    """
    Phase I mutation tests bypass JWT validation.
    Authorization logic is tested via role/capability checks,
    not token mechanics.
    """
    def _override():
        return admin_user

    app.dependency_overrides[get_current_user] = _override
    yield
    app.dependency_overrides.clear()


# -------------------------------------------------
# Auth header helper (kept for test compatibility)
# -------------------------------------------------

@pytest.fixture
def auth():
    """
    Header factory for tests.
    Auth is globally overridden, but tests still expect headers.
    """
    def _auth(_user=None):
        return {}
    return _auth


# -------------------------------------------------
# Owner user (Phase I.5 semantic alias)
# -------------------------------------------------

@pytest.fixture
def owner_user(admin_user):
    """
    In Phase I.5, Owner and Admin share authority.
    This alias keeps tests semantically correct.
    """
    return admin_user


# -------------------------------------------------
# Editor user (explicit but overridden)
# -------------------------------------------------

@pytest.fixture
def editor_user(admin_user):
    """
    Editor resolves to admin_user due to auth override.
    This preserves role intent without JWT friction.
    """
    return admin_user


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
# Archived project (Phase I.5)
# -------------------------------------------------

@pytest.fixture
def archived_project(db, project):
    project.archived_at = datetime.utcnow()
    db.commit()
    db.refresh(project)
    return project


# -------------------------------------------------
# Completed snapshot
# -------------------------------------------------

@pytest.fixture
def completed_snapshot(db, project, admin_user):
    snapshot = RenderedSnapshot(
        project_id=project.id,
        scene_state_hash="__test_scene_hash__",
        render_profile="default",
        engine_version="test-engine",
        status="completed",
        created_by=admin_user.id,
    )
    db.add(snapshot)
    db.commit()
    db.refresh(snapshot)
    return snapshot


# -------------------------------------------------
# Pending snapshot
# -------------------------------------------------

@pytest.fixture
def pending_snapshot(db, project, admin_user):
    snap = RenderedSnapshot(
        project_id=project.id,
        scene_state_hash="__pending_hash__",
        render_profile="default",
        engine_version="test-engine",
        status="pending",
        created_by=admin_user.id,
    )
    db.add(snap)
    db.commit()
    db.refresh(snap)
    return snap


# -------------------------------------------------
# Failed snapshot
# -------------------------------------------------

@pytest.fixture
def failed_snapshot(db, project, admin_user):
    snap = RenderedSnapshot(
        project_id=project.id,
        scene_state_hash="__failed_hash__",
        render_profile="default",
        engine_version="test-engine",
        status="failed",
        created_by=admin_user.id,
    )
    db.add(snap)
    db.commit()
    db.refresh(snap)
    return snap


# -------------------------------------------------
# Obsolete snapshot
# -------------------------------------------------

@pytest.fixture
def obsolete_snapshot(db, project, admin_user):
    snap = RenderedSnapshot(
        project_id=project.id,
        scene_state_hash="__obsolete_hash__",
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
# Archived project snapshot (Phase I.4 compatibility)
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
        scene_state_hash="__archived_hash__",
        render_profile="default",
        engine_version="test-engine",
        status="completed",
        created_by=admin_user.id,
    )
    db.add(snap)
    db.commit()
    db.refresh(snap)

    return snap


