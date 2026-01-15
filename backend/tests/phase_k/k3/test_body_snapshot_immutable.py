def test_body_snapshot_immutable(db, completed_snapshot):
    db.refresh(completed_snapshot)
    assert completed_snapshot.body_state is None
   
