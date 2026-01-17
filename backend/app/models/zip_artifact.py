from dataclasses import dataclass

@dataclass
class ZipArtifact:
    bytes: bytes

    def namelist(self):
        import zipfile, io
        with zipfile.ZipFile(io.BytesIO(self.bytes), "r") as zf:
            return zf.namelist()

    def read(self, name):
        import zipfile, io
        with zipfile.ZipFile(io.BytesIO(self.bytes), "r") as zf:
            return zf.read(name)

