def test_retention_max_days_allows_purge(
    retention_engine,
    old_snapshot,
):
    allowed = retention_engine.is_purge_allowed(
        record=old_snapshot
    )

    assert allowed is True

