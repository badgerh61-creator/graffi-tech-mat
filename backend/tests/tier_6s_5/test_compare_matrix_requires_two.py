def test_compare_matrix_requires_two(client, viewer_user):
    r = client.post(
        "/simulation/compare/matrix",
        json={"artifact_ids": [1]},
        headers=auth(viewer_user),
    )
    assert r.status_code == 422
