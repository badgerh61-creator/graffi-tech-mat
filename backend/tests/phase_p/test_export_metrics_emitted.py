def test_export_metrics_emitted(
    metrics_collector,
    completed_snapshot,
):
    export_snapshot(snapshot=completed_snapshot, format="glb")

    assert metrics_collector.count("export.attempt.count") == 1

