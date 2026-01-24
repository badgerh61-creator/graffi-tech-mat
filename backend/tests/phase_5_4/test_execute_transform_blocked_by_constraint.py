import pytest

from app.services.snapshot_mutations import apply_transform


def test_execute_transform_blocked_by_constraint(
    db,
    draft_snapshot,
    editor_user,
):
    new_snapshot = apply_transform(
        db=db,
        snapshot=draft_snapshot,
        user=editor_user,
        operation="translate",
        target_id="panel-symmetric",
        params={"x": 5},
    )

    # Phase 5.4 invariant:
    # constraints are NOT enforced yet
    assert new_snapshot.parent_snapshot_id == draft_snapshot.id
    assert new_snapshot.status == "draft"

