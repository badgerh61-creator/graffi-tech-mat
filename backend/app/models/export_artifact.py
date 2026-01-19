# backend/app/models/export_artifact.py

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4


@dataclass(frozen=True)
class ExportArtifact:
    id: UUID
    snapshot_id: UUID
    bytes: bytes
    hash: str
    format: str
    status: str  # "completed" | "failed"
    created_at: datetime

    def __getitem__(self, key: str):
        """
        Dict-style, read-only access.

        This exists ONLY for compatibility with tests and API layers
        that treat export artifacts as records.

        Immutability is preserved.
        """
        if not hasattr(self, key):
            raise KeyError(key)
        return getattr(self, key)

    @staticmethod
    def completed(*, bytes: bytes, hash: str, format: str, snapshot_id: UUID):
        return ExportArtifact(
            id=uuid4(),
            snapshot_id=snapshot_id,
            bytes=bytes,
            hash=hash,
            format=format,
            status="completed",
            created_at=datetime.utcnow(),
        )

    @staticmethod
    def failed(*, format: str, snapshot_id: UUID):
        return ExportArtifact(
            id=uuid4(),
            snapshot_id=snapshot_id,
            bytes=b"",
            hash="",
            format=format,
            status="failed",
            created_at=datetime.utcnow(),
        )

