def test_export_requires_valid_geometry(
    invalid_snapshot,
):
    result = export_snapshot(
        snapshot=invalid_snapshot,
        format="glb",
    )

    assert result["status"] == "failed"

