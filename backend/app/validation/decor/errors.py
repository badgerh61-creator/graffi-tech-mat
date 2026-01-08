class DecorValidationError(Exception):
    """
    Base class for all decor validation errors.
    """
    error_code = "decor_validation_error"
    status_code = 400

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class CapabilityRequired(DecorValidationError):
    error_code = "decor_capability_required"
    status_code = 403


class InvalidSnapshotBase(DecorValidationError):
    error_code = "invalid_snapshot_base"
    status_code = 409


class DecalNotFound(DecorValidationError):
    error_code = "decal_not_found"
    status_code = 404


class InvalidTargetPanel(DecorValidationError):
    error_code = "invalid_target_panel"
    status_code = 400


class InvalidUVTransform(DecorValidationError):
    error_code = "invalid_uv_transform"
    status_code = 400


class DecalInstanceNotFound(DecorValidationError):
    error_code = "decal_instance_not_found"
    status_code = 404


class InvalidMaterialDefinition(DecorValidationError):
    error_code = "invalid_material_definition"
    status_code = 400


class BodykitIncompatible(DecorValidationError):
    error_code = "bodykit_incompatible"
    status_code = 409

