import pytest

@pytest.fixture
def snapshot_with_empty_tuning(db, draft_snapshot):
    # Reuse a snapshot that already satisfies all NOT NULL invariants
    draft_snapshot.tuning_state = {}
    db.commit()
    db.refresh(draft_snapshot)
    return draft_snapshot

