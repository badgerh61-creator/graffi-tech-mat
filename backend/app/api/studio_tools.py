from fastapi import APIRouter, Depends
from app.api.deps import get_current_user
from app.services.tool_availability import get_tool_availability

router = APIRouter(prefix="/studio", tags=["studio"])

@router.get("/tools")
def read_tool_availability(user=Depends(get_current_user)):
    return get_tool_availability(user=user)

