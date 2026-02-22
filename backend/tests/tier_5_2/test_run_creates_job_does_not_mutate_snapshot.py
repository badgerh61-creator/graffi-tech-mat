from app.models.rendered_snapshot import RenderedSnapshot as Snapshot

def test_run_creates_job_does_not_mutate_snapshot(db, client, draft_snapshot, editor_user):
    before_hash = draft_snapshot.scene_state_hash

    r = client.post(
        f"/snapshots/{draft_snapshot.id}/testing/run",
        headers=auth(editor_user),
        json={"scenario_id": "track-dry-day-v1"},
    )
    assert r.status_code == 200
    assert "job_id" in r.json()

    after = db.query(Snapshot).get(draft_snapshot.id)
    assert after.scene_state_hash == before_hash
