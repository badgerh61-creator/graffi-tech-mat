def test_corrupted_snapshot_blocked(
    corrupted_snapshot,
):
    assert corrupted_snapshot.is_finalizable is False

