from sqlalchemy.orm import Session
from app.models.asset import Asset


class ToggleAssetVisibilityAdapter:
    @staticmethod
    def execute(
        db: Session,
        *,
        asset: Asset,
        next_is_visible: bool,
    ):
        """
        Phase I.2 pure mutation adapter.
        - No permissions
        - No journaling
        - No side effects
        """

        asset.is_visible = next_is_visible
        db.add(asset)

