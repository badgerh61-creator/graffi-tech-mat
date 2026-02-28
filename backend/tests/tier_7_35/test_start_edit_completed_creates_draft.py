def test_start_edit_completed_creates_draft(client, db, completed_snapshot, editor_user, monkeypatch):
    monkeypatch.setattr("app.services.draft_workspace_service._require_lock_services", lambda: (
        lambda **kwargs: None,  # require_draft_owner
        lambda **kwargs: None,  # acquire_draft_lock
        lambda **kwargs: None,  # release_draft_lock
    ))

    r = client.post(f"/snapshots/{completed_snapshot.id}/start-edit", headers=auth(editor_user))
    assert r.status_code == 200
    data = r.json()
    assert data["mode"] == "edit"
    draft_id = data["draft_snapshot_id"]
    assert draft_id != completed_snapshot.id

    child = child = db.query(completed_snapshot.__class__).filter_by(id=draft_id).first()
    assert child is not None
    assert child.status == "draft"
    if hasattr(child, "parent_snapshot_id"):
        assert child.parent_snapshot_id == completed_snapshot.id
