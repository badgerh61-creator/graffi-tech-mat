from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app import schemas, crud
from app.api.deps import require_admin

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[schemas.UserRead])
def list_users(
    db: Session = Depends(get_db),
    admin=Depends(require_admin),
):
    return crud.list_users(db)

