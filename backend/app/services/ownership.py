# backend/app/services/ownership.py

from sqlalchemy.orm import Session
from app.models.model_owner import ModelOwner
from app.models.model import ModelRecord


def get_model_owner(db: Session, model: ModelRecord) -> dict:
    """
    Resolve the canonical owner of a model.

    Returns:
        {
          "type": "user" | "organization",
          "id": int
        }

    Backward compatibility:
    - If no ModelOwner row exists, falls back to models.owner_id (user ownership)
    """

    owner = (
        db.query(ModelOwner)
        .filter(ModelOwner.model_id == model.id)
        .first()
    )

    # 🔁 Legacy fallback — user-owned model
    if not owner:
        return {
            "type": "user",
            "id": model.owner_id,
        }

    if owner.owner_type == "user":
        if not owner.owner_user_id:
            raise RuntimeError(
                f"Invalid model_owner row for model {model.id}: "
                "owner_type='user' but owner_user_id is NULL"
            )
        return {
            "type": "user",
            "id": owner.owner_user_id,
        }

    if owner.owner_type == "organization":
        if not owner.owner_org_id:
            raise RuntimeError(
                f"Invalid model_owner row for model {model.id}: "
                "owner_type='organization' but owner_org_id is NULL"
            )
        return {
            "type": "organization",
            "id": owner.owner_org_id,
        }

    raise RuntimeError(
        f"Unknown owner_type '{owner.owner_type}' "
        f"for model {model.id}"
    )

