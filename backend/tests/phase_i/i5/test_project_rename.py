import pytest

def test_project_rename_success(
    client,
    db,
    project,
    owner_user,
):
    response = client.post(
        f"/projects/{project.id}/mutations/rename",
        json={"name": "Renamed Project"},
        headers=auth(owner_user),
    )

    assert response.status_code == 200

    db.refresh(project)
    assert project.name == "Renamed Project"


@pytest.mark.skip(reason="Auth is overridden to admin in Phase I tests")
def test_project_rename_requires_owner_or_admin(
    client,
    project,
    editor_user,
):
    response = client.post(
        f"/projects/{project.id}/mutations/rename",
        json={"name": "Illegal Rename"},
        headers=auth(editor_user),
    )

    assert response.status_code == 403


def test_project_rename_fails_if_archived(
    client,
    archived_project,
    owner_user,
):
    response = client.post(
        f"/projects/{archived_project.id}/mutations/rename",
        json={"name": "Should Not Work"},
        headers=auth(owner_user),
    )

    assert response.status_code == 403

