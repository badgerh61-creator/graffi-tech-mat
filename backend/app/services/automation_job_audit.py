# Phase O.3 — In-memory, append-only job audit log
# DB-backed audit is explicitly deferred to Phase O.4+

_JOB_LOGS = []


def record_job_execution(*, job_id, status, error=None):
    _JOB_LOGS.append(
        {
            "job_id": job_id,
            "status": status,
            "error": error,
        }
    )


def get_latest_job_log(*, job_id):
    for record in reversed(_JOB_LOGS):
        if record["job_id"] == job_id:
            return record
    return None

