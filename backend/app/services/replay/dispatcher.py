from app.models.asset import Asset
from app.models.model import ModelRecord

from app.services.mutations.rename_asset import RenameAssetAdapter
from app.services.mutations.toggle_asset_visibility import ToggleAssetVisibilityAdapter
from app.services.mutations.set_preview_camera_preset import (
    SetPreviewCameraPresetAdapter,
)


class DispatchResult:
    def __init__(self, *, adapter, target, value):
        self.adapter = adapter
        self.target = target
        self.value = value


class AdapterDispatcher:
    @staticmethod
    def dispatch(*, db, journal, direction: str) -> DispatchResult:
        if direction not in ("undo", "redo"):
            raise ValueError("Invalid replay direction")

        intent = journal.intent_type
        target_type = journal.target_type

        # Resolve state value
        if direction == "undo":
            state = journal.before_state
        else:
            state = journal.after_state

        # -------- RenameAsset --------
        if intent == "RenameAsset" and target_type == "asset":
            asset = db.query(Asset).filter(Asset.id == journal.target_id).first()
            if not asset:
                raise LookupError("Target asset not found")

            return DispatchResult(
                adapter=RenameAssetAdapter,
                target=asset,
                value=state["filename"],
            )

        # -------- ToggleAssetVisibility --------
        if intent == "ToggleAssetVisibility" and target_type == "asset":
            asset = db.query(Asset).filter(Asset.id == journal.target_id).first()
            if not asset:
                raise LookupError("Target asset not found")

            return DispatchResult(
                adapter=ToggleAssetVisibilityAdapter,
                target=asset,
                value=state["is_visible"],
            )

        # -------- SetPreviewCameraPreset --------
        if intent == "SetPreviewCameraPreset" and target_type == "model":
            model = (
                db.query(ModelRecord)
                .filter(ModelRecord.id == journal.target_id)
                .first()
            )
            if not model:
                raise LookupError("Target model not found")

            return DispatchResult(
                adapter=SetPreviewCameraPresetAdapter,
                target=model,
                value=state["preset"],
            )

        # -------- Unknown mutation --------
        raise ValueError(f"Unsupported replay intent: {intent}")

