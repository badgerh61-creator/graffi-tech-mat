from app.models.mutation_journal import MutationJournal as JournalEntry

def test_archived_project_is_readonly(
    client,
    archived_project,
    owner_user,
):
    # rename forbidden
    rename_response = client.post(
        f"/projects/{archived_project.id}/mutations/rename",
        json={"name": "Nope"},
        headers=auth(owner_user),
    )

    assert rename_response.status_code == 403

    # archive forbidden again
    archive_response = client.post(
        f"/projects/{archived_project.id}/mutations/archive",
        headers=auth(owner_user),
    )

    assert archive_response.status_code == 409

