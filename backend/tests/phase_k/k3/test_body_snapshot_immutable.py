def test_body_snapshot_immutable(db, snapshot):
    db.refresh(snapshot)
    assert snapshot.body_state is None

