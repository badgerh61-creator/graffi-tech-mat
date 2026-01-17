def test_signed_urls_invalidated(
    db,
    revoked_distribution_request,
):
    for url in revoked_distribution_request.signed_urls:
        assert url.is_revoked is True

