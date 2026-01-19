def test_export_is_immutable(
    completed_snapshot,
):
    export1 = export_snapshot(
        snapshot=completed_snapshot,
        format="glb",
    )

    export2 = export_snapshot(
        snapshot=completed_snapshot,
        format="glb",
    )

    assert export1["hash"] == export2["hash"]

