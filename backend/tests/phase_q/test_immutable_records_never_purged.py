def test_immutable_records_never_purged(
    retention_engine,
    audit_record,
):
    result = retention_engine.is_purge_allowed(
        record=audit_record
    )

    assert result is False

