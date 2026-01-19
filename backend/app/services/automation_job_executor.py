from datetime import datetime

from app.services.automation_job_registry import ALLOWED_JOB_TYPES
from app.services.automation_job_audit import record_job_execution
from app.services.automation_policy_evaluator import policy_violates_phase_n


def execute_job(*, db, job):
    """
    Execute a single automation job.

    This function owns:
    - idempotency
    - retry semantics
    - Phase N enforcement
    - audit emission

    It does NOT own:
    - scheduling
    - persistence lifecycle
    - job creation
    """

    # 1️⃣ Idempotency — already succeeded jobs never re-run
    if job.status == "succeeded":
        return {"status": "succeeded"}

    # 2️⃣ Retry exhaustion — terminal failure
    if job.attempt >= job.max_attempts:
        job.status = "failed"
        job.last_error = "retry limit reached"

        record_job_execution(
            job_id=job.id,
            status="failed",
            error=job.last_error,
        )

        return {"status": "failed"}

    # 3️⃣ Job allowlist enforcement
    if job.job_type not in ALLOWED_JOB_TYPES:
        job.status = "failed"
        job.last_error = "unknown job type"

        record_job_execution(
            job_id=job.id,
            status="failed",
            error=job.last_error,
        )

        return {"status": "failed", "error": job.last_error}

    # 4️⃣ Phase N protection (distribution invariants)
    if policy_violates_phase_n(job.policy):
        job.status = "failed"
        job.last_error = "violates Phase N"

        record_job_execution(
            job_id=job.id,
            status="failed",
            error=job.last_error,
        )

        return {"status": "failed"}

    try:
        # 5️⃣ Attempt execution (this is the ONLY place attempt increments)
        job.attempt += 1
        job.status = "running"
        job.updated_at = datetime.utcnow()

        # 🔒 Deterministic failure hook (Phase O.3)
        if job.payload.get("force_fail") is True:
            raise RuntimeError("forced failure")

        # ✅ Success path
        job.status = "succeeded"
        job.updated_at = datetime.utcnow()

        record_job_execution(
            job_id=job.id,
            status="succeeded",
        )

        return {"status": "succeeded"}

    except Exception as exc:
        job.last_error = str(exc)

        # Scheduler-visible state:
        # - retryable → pending
        # - exhausted → failed
        if job.attempt >= job.max_attempts:
            job.status = "failed"
        else:
            job.status = "pending"

        # 🔒 Audit reflects execution outcome, not scheduler intent
        record_job_execution(
            job_id=job.id,
            status="failed",
            error=job.last_error,
        )

        return {"status": job.status}

