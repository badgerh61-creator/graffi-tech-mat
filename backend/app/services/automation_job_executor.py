from datetime import datetime

from app.services.automation_job_registry import ALLOWED_JOB_TYPES
from app.services.automation_job_audit import record_job_execution
from app.services.automation_policy_evaluator import policy_violates_phase_n

# 🔍 Phase P — observability
import app.observability.metrics as metrics_module


def execute_job(*, db, job):
    metrics_module.metrics.inc("automation.job.run.count")

    if job.status == "succeeded":
        return {"status": "succeeded"}

    if job.attempt >= job.max_attempts:
        job.status = "failed"
        job.last_error = "retry limit reached"

        record_job_execution(
            job_id=job.id,
            status="failed",
            error=job.last_error,
        )

        metrics_module.metrics.inc("automation.job.failure.count")
        return {"status": "failed"}

    if job.job_type not in ALLOWED_JOB_TYPES:
        job.status = "failed"
        job.last_error = "unknown job type"

        record_job_execution(
            job_id=job.id,
            status="failed",
            error=job.last_error,
        )

        metrics_module.metrics.inc("automation.job.failure.count")
        return {"status": "failed", "error": job.last_error}

    if policy_violates_phase_n(job.policy):
        job.status = "failed"
        job.last_error = "violates Phase N"

        record_job_execution(
            job_id=job.id,
            status="failed",
            error=job.last_error,
        )

        metrics_module.metrics.inc("automation.job.failure.count")
        return {"status": "failed"}

    try:
        job.attempt += 1
        job.status = "running"
        job.updated_at = datetime.utcnow()

        if job.payload.get("force_fail") is True:
            raise RuntimeError("forced failure")

        job.status = "succeeded"
        job.updated_at = datetime.utcnow()

        record_job_execution(
            job_id=job.id,
            status="succeeded",
        )

        metrics_module.metrics.inc("automation.job.success.count")
        return {"status": "succeeded"}

    except Exception as exc:
        job.last_error = str(exc)

        if job.attempt >= job.max_attempts:
            job.status = "failed"
        else:
            job.status = "pending"

        record_job_execution(
            job_id=job.id,
            status="failed",
            error=job.last_error,
        )

        metrics_module.metrics.inc("automation.job.failure.count")
        return {"status": job.status}

