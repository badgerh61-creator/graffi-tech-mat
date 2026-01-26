import pytest
from app.models.rendered_snapshot import RenderedSnapshot
from app.models.project import Project
from app.services.ai_assistant import AssistantService

@pytest.fixture
def snapshot(db, editor_user):
    # 🔒 Ensure project exists (FK invariant)
    project = Project(
        name="Test Project",
        owner_id=editor_user.id,
    ) 
    db.add(project)
    db.commit()

    snapshot = RenderedSnapshot(
        project_id=project.id,
        status="draft",
        scene_state_hash="abc123",
        render_profile="default",
        engine_version="test",
        created_by=editor_user.id,
    )
    db.add(snapshot)
    db.commit()
    db.refresh(snapshot)
    return snapshot

@pytest.fixture
def assistant_service(db):
    """
    Phase R adapter.

    Provides `.handle_request()` with db injected,
    without modifying service or tests.
    """

    service = AssistantService()

    class _Adapter:
        def handle_request(self, **kwargs):
            return service.handle_request(db=db, **kwargs)

    return _Adapter()
