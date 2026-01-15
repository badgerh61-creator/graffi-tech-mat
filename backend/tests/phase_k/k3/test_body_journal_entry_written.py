def test_body_journal_entry_written(
    db,
    client,
    completed_snapshot,
    admin_user,
):
    client.post(
        "/mutations/body/apply-morph",
        json={
            "project_id": completed_snapshot.project_id,
            "base_snapshot_id": completed_snapshot.id,
            "preset_id": "widebody_v1",
            "parameters": {},
        },
    )

    entries = db.execute(
        "SELECT * FROM journal_entries WHERE mutation_type = 'body.apply_morph'"
    ).fetchall()

    assert len(entries) == 1
