from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.rendered_snapshot import RenderedSnapshot
from app.services.transform_executor import execute_transform

router = APIRouter(
    prefix="/projects/{project_id}/snapshots/{snapshot_id}",
    tags=["snapshots"],
)

@router.post("/execute-transform")
def execute_transform_endpoint(
    project_id: int,
    snapshot_id: int,
    payload: dict,
    db=Depends(get_db),
    user=Depends(get_current_user),
):
    snapshot = (
        db.query(RenderedSnapshot)
        .filter(RenderedSnapshot.id == snapshot_id)
        .first()
    )

    if not snapshot:
        raise HTTPException(404, "Snapshot not found")

    if snapshot.project_id != project_id:
        raise HTTPException(404, "Snapshot not in project")

    if snapshot.status != "draft":
        raise HTTPException(409, "Snapshot not editable")

    if user.role not in ("editor", "owner", "admin"):
        raise HTTPException(403)

    return execute_transform(
        db=db,
        snapshot=snapshot,
        target_id=payload["target_id"],
        operation=payload["operation"],
        params=payload.get("params", {}),
        constraints=payload.get("constraints", []),
        user=user,
    )

