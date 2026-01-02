from fastapi import APIRouter, Depends
from app.api.deps import get_current_user

router = APIRouter(prefix="/jobs", tags=["jobs"])

@router.get("/")
def list_jobs(user=Depends(get_current_user)):
    """
    Phase H3 — READ-ONLY job surface
    Stub implementation.
    """
    return {
        "items": []
    }

