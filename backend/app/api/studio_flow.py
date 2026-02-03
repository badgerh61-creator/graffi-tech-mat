from fastapi import APIRouter, Depends
from app.api.deps import get_current_user
from app.services.flow_guidance import get_flow_guidance

router = APIRouter(prefix="/studio", tags=["studio"])

@router.get("/flow")
def read_flow_guidance(user=Depends(get_current_user)):
    return get_flow_guidance(user=user)

