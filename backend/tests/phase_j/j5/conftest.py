import pytest


@pytest.fixture
def workspace_with_multiple_snapshots(
    client,
    project,
    owner_user,
    completed_snapshot,
    override_get_current_user,  # <-- dependency, NOT callable
):
    response = client.get(f"/workspaces/{project.id}")
    return response.json()


@pytest.fixture
def workspace_with_failed_snapshot(
    client,
    project,
    owner_user,
    completed_snapshot,
    failed_snapshot,
    override_get_current_user,
):
    response = client.get(f"/workspaces/{project.id}")
    return response.json()


@pytest.fixture
def workspace_with_mixed_snapshots(
    client,
    project,
    owner_user,
    completed_snapshot,
    failed_snapshot,
    pending_snapshot,
    override_get_current_user,
):
    response = client.get(f"/workspaces/{project.id}")
    return response.json()


@pytest.fixture
def workspace_with_assets_out_of_order(
    client,
    project,
    owner_user,
    artifacts,
    override_get_current_user,
):
    response = client.get(f"/workspaces/{project.id}")
    return response.json()

