def test_set_wheels_is_deterministic(snapshot_factory):
    s1 = snapshot_factory(
        tuning={"wheels": {"diameter": 19, "width": 9.5, "offset": 35}}
    )
    s2 = snapshot_factory(
        tuning={"wheels": {"diameter": 19, "width": 9.5, "offset": 35}}
    )

    assert s1.hash == s2.hash

