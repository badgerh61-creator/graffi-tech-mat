from fastapi import APIRouter, Depends
from app.api.deps import get_current_user
from app.services.studio_context import get_studio_context

router = APIRouter(prefix="/studio", tags=["studio"])

@router.get("/context")
def read_studio_context(snapshot_id: int, user=Depends(get_current_user)):
    return get_studio_context(snapshot_id=snapshot_id, user=user)

