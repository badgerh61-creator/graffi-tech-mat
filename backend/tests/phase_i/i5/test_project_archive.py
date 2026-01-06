import pytest

def test_project_archive_success(
    client,
    db,
    project,
    owner_user,
):
    response = client.post(
        f"/projects/{project.id}/mutations/archive",
        headers=auth(owner_user),
    )

    assert response.status_code == 200

    db.refresh(project)
    assert project.archived_at is not None


@pytest.mark.skip(reason="Auth is overridden to admin in Phase I tests")
def test_project_archive_requires_owner_or_admin(
    client,
    project,
    editor_user,
):
    response = client.post(
        f"/projects/{project.id}/mutations/archive",
        headers=auth(editor_user),
    )

    assert response.status_code == 403


def test_project_cannot_be_archived_twice(
    client,
    archived_project,
    owner_user,
):
    response = client.post(
        f"/projects/{archived_project.id}/mutations/archive",
        headers=auth(owner_user),
    )

    assert response.status_code == 409

