def test_get_result_404(client, viewer_user):
    r = client.get("/testing/results/999999", headers=auth(viewer_user))
    assert r.status_code == 404
