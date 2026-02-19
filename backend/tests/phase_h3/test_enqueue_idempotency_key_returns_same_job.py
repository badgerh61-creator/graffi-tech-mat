def test_enqueue_idempotency_key_returns_same_job(db, mutation_journal_entry):
    from app.services.job_enqueue import enqueue_job

    j1 = enqueue_job(
        db=db,
        name="x",
        payload={"a": 1},
        idempotency_key="k1",
        max_attempts=3,
        mutation_id=mutation_journal_entry.id,
    )
    j2 = enqueue_job(
        db=db,
        name="x",
        payload={"a": 1},
        idempotency_key="k1",
        max_attempts=3,
        mutation_id=mutation_journal_entry.id,
    )

    assert j1.id == j2.id

