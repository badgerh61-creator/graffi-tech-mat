from datetime import datetime

from app.services.automation_job_registry import ALLOWED_JOB_TYPES
from app.services.automation_job_audit import record_job_execution
from app.services.automation_policy_evaluator import policy_violates_phase_n


def execute_job(*, db, job):
    # 1️⃣ Idempotency
    if job.status == "succeeded":
        return {"status": "succeeded"}

    # 2️⃣ Retry exhaustion
    if job.attempt >= job.max_attempts:
        job.status = "failed"
        record_job_execution(
            job_id=job.id,
            status="failed",
            error="retry limit reached",
        )
        return {"status": "failed"}

    # 3️⃣ Job allowlist
    if job.job_type not in ALLOWED_JOB_TYPES:
        job.status = "failed"
        job.last_error = "unknown job type"
        record_job_execution(
            job_id=job.id,
            status="failed",
            error=job.last_error,
        )
        return {"status": "failed", "error": job.last_error}

    # 4️⃣ Phase N protection
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
        # 5️⃣ Attempt execution
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

        # Scheduler state (retry vs terminal)
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

