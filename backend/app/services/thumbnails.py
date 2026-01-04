# backend/app/services/thumbnails.py

from sqlalchemy.orm import Session

from app.models.asset import Asset


SUPPORTED_IMAGE_TYPES = {
    "image/png",
    "image/jpeg",
    "image/webp",
}


def generate_thumbnail_for_asset(
    *,
    db: Session,
    asset: Asset,
) -> None:
    """
    Phase I.6 — Job-safe thumbnail generation

    RULES:
    - NO engine rendering yet
    - NO Pillow misuse
    - GLB/GLTF MUST FAIL cleanly
    - No commits
    """

    if asset.content_type not in SUPPORTED_IMAGE_TYPES:
        raise RuntimeError(
            f"Thumbnail generation not supported for asset type "
            f"{asset.content_type}"
        )

    raise RuntimeError(
        "Image thumbnails not wired yet (engine renderer pending)"
    )

