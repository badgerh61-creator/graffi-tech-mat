from fastapi import APIRouter, Depends
from app.api.deps import get_current_user
from app.services.ai_assistant import handle_request

router = APIRouter(prefix="/assistant", tags=["assistant"])

@router.post("/query")
def query_assistant(payload: dict, user=Depends(get_current_user)):
    return handle_request(
        user=user,
        snapshot=payload["snapshot"],
        mode=payload["mode"],
        prompt=payload["prompt"],
    )
