# Phase O.3 — In-memory, append-only job audit log
# DB-backed audit is explicitly deferred to Phase O.4+

_JOB_LOGS = []


def record_job_execution(*, db=None, job_id, status, error=None):
    """
    Records execution of an automation job.

    - Phase O.3: in-memory append-only log
    - Phase O.4: worker passes db explicitly (unused here)
    - Phase P+: db-backed persistence may be added
    """
    _JOB_LOGS.append(
        {
            "job_id": job_id,
            "status": status,
            "error": error,
        }
    )

    return {
        "job_id": job_id,
        "status": status,
        "error": error,
    }


def get_latest_job_log(job_id):
    for record in reversed(_JOB_LOGS):
        if record["job_id"] == job_id:
            return record
    return None

