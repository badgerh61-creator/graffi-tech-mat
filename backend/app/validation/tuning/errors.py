# backend/app/validation/tuning/errors.py

class TuningValidationError(Exception):
    error_code = "tuning_validation_error"
    status_code = 400

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class CapabilityRequired(TuningValidationError):
    error_code = "tuning_capability_required"
    status_code = 403


class InvalidSnapshotBase(TuningValidationError):
    error_code = "invalid_snapshot_base"
    status_code = 409


class SuspensionPresetNotFound(TuningValidationError):
    error_code = "suspension_preset_not_found"
    status_code = 404

