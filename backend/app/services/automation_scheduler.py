def enqueue_job(*, db, job):
    db.add(job)
    db.commit()
    return job

