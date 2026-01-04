from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.job import Job
from app.models.mutation_journal import MutationJournal
from app.models.model import ModelRecord
from app.crud import require_model_role
from app.services.jobs.executor import JobExecutor

router = APIRouter(prefix="/jobs", tags=["jobs"])


# =====================================================
# LIST JOBS (READ-ONLY)
# =====================================================
@router.get("/")
def list_jobs(
    *,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    """
    Phase I.6:
    - Read-only job surface
    - Adapter-enforced response shape
    - Frontend-safe (never returns undefined)
    """

    jobs = (
        db.query(Job)
        .order_by(Job.created_at.desc())
        .all()
    )

    # -------------------------------------------------
    # 🔌 ADAPTER — Backend → Frontend contract
    # -------------------------------------------------
    def adapt(job: Job) -> dict:
        return {
            "id": job.id,
            "type": job.job_type,
            "status": job.state.lower(),   # CREATED → created
            "progress": (
                0 if job.state == "CREATED"
                else 50 if job.state == "RUNNING"
                else 100 if job.state == "COMPLETED"
                else 0
            ),
            "error": None if job.state != "FAILED" else "Job failed",
            "createdAt": job.created_at.isoformat() if job.created_at else None,
            "updatedAt": job.updated_at.isoformat() if job.updated_at else None,
        }

    return [adapt(job) for job in jobs]


# =====================================================
# MANUAL JOB EXECUTION
# =====================================================
@router.post("/{job_id}/run")
def run_job(
    *,
    job_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    """
    Phase I.6 Option A:
    Manual job execution (explicit trigger).
    """

    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
        )

    if job.state != "CREATED":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Job is already {job.state}",
        )

    # ---- Resolve mutation ----
    mutation = (
        db.query(MutationJournal)
        .filter(MutationJournal.id == job.mutation_id)
        .first()
    )
    if not mutation:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Mutation journal missing for job",
        )

    # ---- Resolve model ----
    if mutation.target_type == "asset":
        model = (
            db.query(ModelRecord)
            .join(ModelRecord.assets)
            .filter(
                ModelRecord.id == mutation.target_model_id
                if hasattr(mutation, "target_model_id")
                else ModelRecord.id.isnot(None)
            )
            .first()
        )
    else:
        model = db.query(ModelRecord).filter(
            ModelRecord.id == mutation.target_id
        ).first()

    if not model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Model not found for job",
        )

    # ---- Permission gate (LOCKED) ----
    try:
        require_model_role(
            db,
            user=user,
            model=model,
            min_role="editor",
        )
    except PermissionError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exc),
        )

    # ---- Execute job ----
    try:
        JobExecutor.execute(db=db, job=job)
        db.commit()
    except Exception as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Job execution failed: {exc}",
        )

    return {
        "status": "ok",
        "jobId": job.id,
        "state": job.state,
    }

