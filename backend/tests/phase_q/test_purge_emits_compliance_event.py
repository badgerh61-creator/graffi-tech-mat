def test_purge_emits_compliance_event(
    retention_engine,
    old_snapshot,
):
    result = retention_engine.purge(record=old_snapshot)

    assert result["purged"] is True
    assert result["event_emitted"] is True

