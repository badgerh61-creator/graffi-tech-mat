# backend/app/api/organizations.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.deps import get_current_user   # ✅ CORRECT SOURCE
from app.models.user import User
from app.models.organization import Organization
from app.models.organization_member import OrganizationMember
from app.schemas import OrganizationCreate, OrganizationRead

router = APIRouter(
    prefix="/organizations",
    tags=["organizations"],
)


@router.post(
    "",
    response_model=OrganizationRead,
    status_code=status.HTTP_201_CREATED,
)
def create_organization(
    org_in: OrganizationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    existing = (
        db.query(Organization)
        .filter(Organization.name == org_in.name)
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Organization name already exists",
        )

    org = Organization(name=org_in.name)
    db.add(org)
    db.flush()  # get org.id safely

    membership = OrganizationMember(
        organization_id=org.id,
        user_id=current_user.id,
        role="owner",
    )
    db.add(membership)

    db.commit()
    db.refresh(org)
    return org


@router.get(
    "",
    response_model=list[OrganizationRead],
)
def list_my_organizations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(Organization)
        .join(
            OrganizationMember,
            OrganizationMember.organization_id == Organization.id,
        )
        .filter(OrganizationMember.user_id == current_user.id)
        .order_by(Organization.created_at.desc())
        .all()
    )

