from fastapi import HTTPException


class BodyValidationError(HTTPException):
    """
    Base class for all Phase K.3 body validation errors.
    """
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)


class BodyCapabilityRequired(BodyValidationError):
    def __init__(self, detail="body_capability_required"):
        super().__init__(status_code=403, detail=detail)


class InvalidSnapshotBase(BodyValidationError):
    def __init__(self, detail="invalid_snapshot_base"):
        super().__init__(status_code=409, detail=detail)


class BodyPresetNotFound(BodyValidationError):
    def __init__(self, detail="body_preset_not_found"):
        super().__init__(status_code=404, detail=detail)


class BodyPresetIncompatible(BodyValidationError):
    def __init__(self, detail="body_preset_incompatible"):
        super().__init__(status_code=409, detail=detail)


class BodyParametersOutOfBounds(BodyValidationError):
    def __init__(self, detail="body_parameters_out_of_bounds"):
        super().__init__(status_code=400, detail=detail)

