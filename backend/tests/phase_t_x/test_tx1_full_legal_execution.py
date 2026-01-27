from app.studio import execute_tool
from app.studio import execute_tool

def test_full_legal_execution_succeeds(
    db,
    draft_snapshot,
    editor_user,
):
    result = execute_tool(
        db=db,
        user=editor_user,
        snapshot=draft_snapshot,
        station="geometry",
        tool="transform",
        operation="translate",
        params={"x": 5},
    )

    assert result.status == "draft"
    assert result.parent_snapshot_id == draft_snapshot.id

