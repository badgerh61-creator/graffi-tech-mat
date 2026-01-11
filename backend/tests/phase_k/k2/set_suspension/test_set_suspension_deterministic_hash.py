def test_set_suspension_is_deterministic(
    snapshot_factory,
):
    s1 = snapshot_factory(
        tuning={
            "suspension": {"preset_id": "sport_low"}
        }
    )

    s2 = snapshot_factory(
        tuning={
            "suspension": {"preset_id": "sport_low"}
        }
    )

    assert s1.hash == s2.hash

