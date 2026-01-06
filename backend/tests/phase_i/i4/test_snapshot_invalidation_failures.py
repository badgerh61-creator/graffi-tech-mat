import pytest


def test_cannot_invalidate_pending_snapshot(
    client,
    pending_snapshot,
):
    response = client.post(
        f"/snapshots/{pending_snapshot.id}/mutations/invalidate"
    )
    assert response.status_code == 409


def test_cannot_invalidate_failed_snapshot(
    client,
    failed_snapshot,
):
    response = client.post(
        f"/snapshots/{failed_snapshot.id}/mutations/invalidate"
    )
    assert response.status_code == 409


def test_cannot_invalidate_already_obsolete_snapshot(
    client,
    obsolete_snapshot,
):
    response = client.post(
        f"/snapshots/{obsolete_snapshot.id}/mutations/invalidate"
    )
    assert response.status_code == 409


@pytest.mark.xfail(reason="Project archiving not implemented until Phase I.5")
def test_cannot_invalidate_snapshot_of_archived_project(
    client,
    archived_project_snapshot,
):
    response = client.post(
        f"/snapshots/{archived_project_snapshot.id}/mutations/invalidate"
    )
    assert response.status_code == 403

