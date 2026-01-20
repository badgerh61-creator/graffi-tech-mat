def test_validation_failure_metric_emitted(metrics_collector):
    validate_geometry(
        surfaces=[],   # deliberately invalid
        panels=[],
    )

    assert metrics_collector.count(
        "geometry.validation.failures.count"
    ) == 1

