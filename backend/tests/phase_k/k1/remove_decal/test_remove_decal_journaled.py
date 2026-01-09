def test_remove_decal_journal_entry_created(
    client,
    db,
    project,
    completed_snapshot_with_decal,
    editor_user,
):
    response = client.post(
        "/mutations/decor/exterior/remove-decal",
        json={
            "project_id": project.id,
            "snapshot_base_id": completed_snapshot_with_decal.id,
            "decal_instance_id": "abc123",
        },
        headers=auth(editor_user),
    )

    assert response.status_code == 200

    entries = db.execute(
        "SELECT * FROM journal_entries WHERE mutation_type = 'decor.exterior.remove-decal'"
    ).fetchall()

    assert len(entries) == 1

