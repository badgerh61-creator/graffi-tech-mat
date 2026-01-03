class ReplaySafetyGate:
    @staticmethod
    def validate(*, journal, dispatch, direction: str):
        if direction not in ("undo", "redo"):
            raise ValueError("Invalid replay direction")

        target = dispatch.target
        value = dispatch.value

        # --- RenameAsset ---
        if journal.intent_type == "RenameAsset":
            current = target.filename
            if current == value:
                raise RuntimeError("No-op rename replay blocked")

        # --- ToggleAssetVisibility ---
        elif journal.intent_type == "ToggleAssetVisibility":
            current = target.is_visible
            if current == value:
                raise RuntimeError("No-op visibility replay blocked")

        # --- SetPreviewCameraPreset ---
        elif journal.intent_type == "SetPreviewCameraPreset":
            current = target.preview_camera_preset_id
            if current == value:
                raise RuntimeError("No-op camera preset replay blocked")

        else:
            raise ValueError("Unsupported mutation for replay")

        # If we reach here → safe
        return

