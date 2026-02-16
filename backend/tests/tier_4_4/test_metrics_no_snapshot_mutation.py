from app.models.snapshot import Snapshot

def test_metrics_do_not_mutate_snapshot(
    db,
    client,
    draft_snapshot,
    viewer_user,
):
    before = draft_snapshot.tuning_state

    r = client.get(
        f"/snapshots/{draft_snapshot.id}/metrics/performance",
        headers=auth(viewer_user),
    )
    assert r.status_code == 200

    after = db.query(Snapshot).get(draft_snapshot.id).tuning_state
    assert after == before

