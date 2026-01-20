def test_geometry_metrics_emitted(metrics_collector):
    validate_geometry(
        surfaces=[],   # minimal input
        panels=[],
    )

    assert metrics_collector.count(
        "geometry.validation.invocations.count"
    ) == 1

