from sqlalchemy.orm import Session
from app.models.model import ModelRecord


class SetPreviewCameraPresetAdapter:
    @staticmethod
    def execute(
        db: Session,
        *,
        model: ModelRecord,
        next_preset: str,
    ):
        """
        Pure mutation adapter.
        No permissions.
        No validation.
        No journaling.
        """
        model.preview_camera_preset_id = next_preset
        db.add(model)

