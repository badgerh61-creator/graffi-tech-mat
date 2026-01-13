from app.models.journal_entry import JournalEntry

def test_engine_tune_writes_journal(
    db,
    client,
    override_get_current_user,
    admin_user,
    completed_snapshot,
):
    client.post(
        "/mutations/tuning/set-engine-tune",
        json={
            "project_id": completed_snapshot.project_id,
            "snapshot_base_id": completed_snapshot.id,
            "preset_id": "sport",
        },
    )

    entry = (
        db.query(JournalEntry)
        .filter_by(mutation_type="tuning.set-engine-tune")
        .first()
    )

    assert entry is not None
    assert entry.snapshot_before == completed_snapshot.id

