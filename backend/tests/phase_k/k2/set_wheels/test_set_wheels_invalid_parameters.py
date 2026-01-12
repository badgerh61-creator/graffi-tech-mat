import pytest

@pytest.mark.parametrize(
    "diameter,width,offset",
    [
        (10, 8, 35),    # diameter too small
        (30, 8, 35),    # diameter too large
        (18, 3, 35),    # width too small
        (18, 20, 35),   # width too large
        (18, 8, 200),   # offset too large
    ],
)
def test_set_wheels_invalid_parameters(
    client,
    project,
    completed_snapshot,
    editor_user,
    diameter,
    width,
    offset,
):
    response = client.post(
        "/mutations/tuning/set-wheels",
        json={
            "project_id": project.id,
            "snapshot_base_id": completed_snapshot.id,
            "diameter": diameter,
            "width": width,
            "offset": offset,
        },
        headers=auth(editor_user),
    )

    assert response.status_code == 400
    assert response.json()["error"] == "invalid_wheel_parameters"

