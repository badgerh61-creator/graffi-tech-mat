def test_scenarios_detail_404_for_unknown(client, viewer_user):
    r = client.get("/testing/scenarios/does-not-exist", headers=auth(viewer_user))
    assert r.status_code == 404
