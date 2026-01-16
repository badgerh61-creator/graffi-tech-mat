from dataclasses import dataclass

@dataclass
class ExportArtifact:
    bytes: bytes
    hash: str
    format: str

