def test_finalize_creates_completed_snapshot(
    db,
    draft_snapshot,
    editor_user,
):
    completed = finalize_snapshot(
        db=db,
        snapshot=draft_snapshot,
        user=editor_user,
    )

    assert completed.status == "completed"
    assert completed.id != draft_snapshot.id

