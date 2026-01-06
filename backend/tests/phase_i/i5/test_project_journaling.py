from app.models.mutation_journal import MutationJournal

def test_project_rename_writes_journal_entry(
    client,
    db,
    project,
    owner_user,
):
    client.post(
        f"/projects/{project.id}/mutations/rename",
        json={"name": "Journaled Rename"},
        headers=auth(owner_user),
    )

    entry = (
        db.query(MutationJournal)
        .filter(
            MutationJournal.target_type == "project",
            MutationJournal.target_id == project.id,
            MutationJournal.intent_type == "rename",
        )
        .one()
    )

    assert entry.before_state["name"] != entry.after_state["name"]
    assert entry.issued_by_user_id == owner_user.id


def test_project_archive_writes_journal_entry(
    client,
    db,
    project,
    owner_user,
):
    client.post(
        f"/projects/{project.id}/mutations/archive",
        headers=auth(owner_user),
    )

    entry = (
        db.query(MutationJournal)
        .filter(
            MutationJournal.target_type == "project",
            MutationJournal.target_id == project.id,
            MutationJournal.intent_type == "archive",
        )
        .one()
    )

    assert entry.issued_by_user_id == owner_user.id

