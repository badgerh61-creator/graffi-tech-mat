def test_security_headers_present(client):
    # any existing endpoint that returns 200 in your suite
    r = client.get("/jobs/")
    assert r.status_code in (200, 401, 403)  # depends on auth in your client fixture

    # Even on errors, middleware should attach headers
    assert "X-Content-Type-Options" in r.headers
    assert r.headers["X-Content-Type-Options"] == "nosniff"
    assert r.headers.get("X-Frame-Options") == "DENY"
    assert "Referrer-Policy" in r.headers
    assert "Permissions-Policy" in r.headers

