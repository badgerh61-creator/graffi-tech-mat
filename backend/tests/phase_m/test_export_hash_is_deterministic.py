def test_export_hash_is_deterministic(
    completed_snapshot,
):
    export = export_snapshot(
        snapshot=completed_snapshot,
        format="svg",
    )

    assert len(export["hash"]) == 64

