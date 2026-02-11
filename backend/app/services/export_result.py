from dataclasses import dataclass

@dataclass(frozen=True)
class ExportResult:
    """
    PURE export result.

    - No DB
    - No side effects
    - Deterministic
    - Safe for tests
    """

    bytes: bytes
    hash: str
    format: str
    snapshot_id: int

