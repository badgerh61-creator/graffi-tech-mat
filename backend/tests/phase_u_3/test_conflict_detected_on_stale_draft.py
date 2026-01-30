from app.services.conflict_detector import detect_conflict
from app.services.transform_executor import apply_transform

def test_conflict_detected_on_stale_draft(
    db,
    stale_draft_snapshot,
    editor_user,
):
    conflict = detect_conflict(
        db=db,
        snapshot=stale_draft_snapshot,
        user=editor_user,
    )

    assert conflict.is_conflicted is True

