def test_legal_hold_blocks_purge(
    retention_engine,
    snapshot_under_legal_hold,
):
    allowed = retention_engine.is_purge_allowed(
        record=snapshot_under_legal_hold
    )

    assert allowed is False

