def test_login_rate_limit_off_by_default(client):
    body = "username=admin_phase_i@test.com&password=admin123"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    # Spam a few times; should NOT become 429 by default
    for _ in range(5):
        r = client.post("/login", data=body, headers=headers)
        assert r.status_code != 429

