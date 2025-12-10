import io
from PIL import Image
from ..core.config import settings

def create_thumbnail_from_fileobj(fileobj, size: int | None = None) -> bytes:
    size = size or settings.THUMBNAIL_SIZE
    image = Image.open(fileobj)
    if image.mode not in ('RGB', 'RGBA'):
        image = image.convert('RGBA' if image.mode == 'P' else 'RGB')
    image.thumbnail((size, size))
    out = io.BytesIO()
    image.save(out, format='PNG')
    out.seek(0)
    return out.read()
