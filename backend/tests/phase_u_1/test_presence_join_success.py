from app.services.presence_sessions import start_session

def test_presence_join_success(
    db,
    editor_user,
    project,
):
    session = start_session(
        db=db,
        user=editor_user,
        project_id=project.id,
    )
    assert session.user_id == editor_user.id

