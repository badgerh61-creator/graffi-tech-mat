def test_retention_min_days_enforced(
    retention_engine,
    recent_snapshot,
):
    allowed = retention_engine.is_purge_allowed(
        record=recent_snapshot
    )

    assert allowed is False

