from app.services.snapshot_stability import enforce_draft_ttl

def test_draft_snapshot_ttl_expires(
    db,
    expired_draft_snapshot,
):
    enforce_draft_ttl(expired_draft_snapshot)
    db.commit()
    db.refresh(expired_draft_snapshot)

    assert expired_draft_snapshot.status == "abandoned"

