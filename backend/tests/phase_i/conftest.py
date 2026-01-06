import pytest
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
# Admin user (bypasses permission gates)
# -------------------------------------------------

@pytest.fixture
def admin_user(db):
    """
    Deterministic admin user for Phase I tests.
    Reuses user if already present to avoid UNIQUE violations.
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
# 🔐 AUTH OVERRIDE (CRITICAL)
# -------------------------------------------------

@pytest.fixture(autouse=True)
def override_get_current_user(admin_user):
    """
    Override FastAPI auth dependency so Phase I
    mutation tests are not blocked by JWT validation.
    """
    def _override():
        return admin_user

    app.dependency_overrides[get_current_user] = _override
    yield
    app.dependency_overrides.clear()


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
# Completed snapshot fixture
# -------------------------------------------------

@pytest.fixture
def completed_snapshot(db, project, admin_user):
    snapshot = RenderedSnapshot(
        project_id=project.id,
        scene_state_hash="__test_scene_hash__",
        render_profile="default",     # REQUIRED by schema
        engine_version="test-engine",
        status="completed",
        created_by=admin_user.id,
    )
    db.add(snapshot)
    db.commit()
    db.refresh(snapshot)
    return snapshot


# -------------------------------------------------
# Editor user (non-admin, still allowed by override)
# -------------------------------------------------

@pytest.fixture
def editor_user(admin_user):
    """
    For Phase I tests, editor_user resolves to admin_user
    because auth is overridden anyway.
    This keeps role semantics explicit without JWT friction.
    """
    return admin_user


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
# Archived project snapshot
# -------------------------------------------------

@pytest.fixture
def archived_project_snapshot(db, admin_user):
    """
    Placeholder fixture.
    Project archiving is implemented in Phase I.5,
    so this snapshot is used only for xfail tests.
    """
    project = Project(
        name="Future Archived Project",
        owner_id=admin_user.id,
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

