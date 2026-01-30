from app.services import resolve_conflict
from app.services.conflict_detector import detect_conflict
from app.services.transform_executor import apply_transform

def test_conflict_resolution_abandon(
    db,
    conflicted_draft_snapshot,
    editor_user,
):
    result = resolve_conflict(
        db=db,
        snapshot=conflicted_draft_snapshot,
        user=editor_user,
        strategy="abandon",
    )

    assert result.status == "abandoned"

