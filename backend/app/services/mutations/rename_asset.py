# backend/app/services/mutations/rename_asset.py

from sqlalchemy.orm import Session

from app.models.asset import Asset


class RenameAssetAdapter:
    @staticmethod
    def execute(
        db: Session,
        *,
        asset: Asset,
        next_name: str,
    ):
        """
        Pure mutation adapter.
        No permissions. No journaling. No side effects.
        """

        asset.filename = next_name
        db.add(asset)

