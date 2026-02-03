from fastapi import APIRouter, Depends
from app.api.deps import get_current_user
from app.services.tool_availability import get_tool_availability
from app.services.kernel_snapshot_lookup import kernel_snapshot_lookup

from fastapi import Query

router = APIRouter(prefix="/studio", tags=["studio"])


@router.get("/tools")
def read_tool_availability(
    snapshot_id: int = Query(...),
    user=Depends(get_current_user),
):
    snapshot = kernel_snapshot_lookup(snapshot_id=snapshot_id)

    return get_tool_availability(
        user=user,
        snapshot=snapshot,
        station=user.current_station,
    )

