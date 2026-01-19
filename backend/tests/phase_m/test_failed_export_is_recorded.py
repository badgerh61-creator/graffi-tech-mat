def test_failed_export_is_recorded(
    snapshot_that_triggers_export_error,
):
    result = export_snapshot(
        snapshot=snapshot_that_triggers_export_error,
        format="pdf",
    )

    assert result["status"] == "failed"

