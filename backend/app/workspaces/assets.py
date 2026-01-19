"""
PHASE J.5 — WORKSPACE ASSET NORMALIZATION

Responsibilities:
- Deterministic ordering
- Read-only access
- NO filtering
- NO ownership inference
- NO mutation

Asset scope is defined earlier in the pipeline.
"""

from app.models.asset import Asset


def get_workspace_assets(*, db):
    """
    Phase J.5 rule:
    - Return assets in deterministic order only
    - Do NOT infer workspace/project ownership
    """
    return (
        db.query(Asset)
        .order_by(
            Asset.created_at.asc(),
            Asset.id.asc(),
        )
        .all()
    )

