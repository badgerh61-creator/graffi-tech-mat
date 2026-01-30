from app.services import resolve_conflict
from app.services.conflict_detector import detect_conflict
from app.services.transform_executor import apply_transform

def test_conflict_resolution_rebase(
    db,
    conflicted_draft_snapshot,
    latest_snapshot,
    editor_user,
):
    new_draft = resolve_conflict(
        db=db,
        snapshot=conflicted_draft_snapshot,
        user=editor_user,
        strategy="rebase",
    )

    assert new_draft.parent_snapshot_id == latest_snapshot.id
    assert new_draft.status == "draft"

