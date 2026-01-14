def test_body_journal_entry_written(db, client, admin_user, snapshot):
    client.post("/mutations/body/apply-morph", json={
        "project_id": snapshot.project_id,
        "base_snapshot_id": snapshot.id,
        "preset_id": "widebody_v1",
        "parameters": {}
    }, user=admin_user)

    entries = db.execute("SELECT * FROM journal_entries WHERE mutation_type='body.apply_morph'").fetchall()
    assert len(entries) == 1

