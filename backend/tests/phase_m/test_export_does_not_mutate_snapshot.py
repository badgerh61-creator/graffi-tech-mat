def test_export_does_not_mutate_snapshot(
    completed_snapshot,
):
    original_hash = completed_snapshot.hash

    export_snapshot(
        snapshot=completed_snapshot,
        format="png",
    )

    assert completed_snapshot.hash == original_hash

