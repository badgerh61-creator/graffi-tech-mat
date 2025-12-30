from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.deps import get_current_user, require_editor
from app.models.user import User
from app.models.organization import Organization
from app.models.organization_member import OrganizationMember
from app.schemas import OrganizationCreate, OrganizationRead, ModelCreate, ModelRead
from app import crud

router = APIRouter(prefix="/organizations", tags=["organizations"])


@router.post("", response_model=OrganizationRead, status_code=status.HTTP_201_CREATED)
def create_organization(
    org_in: OrganizationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if db.query(Organization).filter(Organization.name == org_in.name).first():
        raise HTTPException(400, "Organization name already exists")

    org = Organization(name=org_in.name)
    db.add(org)
    db.flush()

    db.add(
        OrganizationMember(
            organization_id=org.id,
            user_id=current_user.id,
            role="owner",
        )
    )

    db.commit()
    db.refresh(org)
    return org


@router.get("", response_model=list[OrganizationRead])
def list_my_organizations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(Organization)
        .join(OrganizationMember)
        .filter(OrganizationMember.user_id == current_user.id)
        .order_by(Organization.created_at.desc())
        .all()
    )


@router.post(
    "/{org_id}/models",
    response_model=ModelRead,
    status_code=status.HTTP_201_CREATED,
)
def create_org_model(
    org_id: int,
    model_in: ModelCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_editor),
):
    membership = (
        db.query(OrganizationMember)
        .filter(
            OrganizationMember.organization_id == org_id,
            OrganizationMember.user_id == user.id,
        )
        .first()
    )
    if not membership:
        raise HTTPException(403, "Not a member of this organization")

    model = crud.create_model(db, model_in, owner_id=user.id)

    return ModelRead(
        id=model.id,
        name=model.name,
        description=model.description,
        owner_id=model.owner_id,
        created_at=model.created_at,
        role="owner",
        assets=model.assets,
    )

