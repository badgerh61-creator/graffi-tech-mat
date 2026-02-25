import uuid
import pytest

from app.api.deps import get_current_user, require_editor
from app.models.asset import Asset, AssetStatus
from app.models.model import ModelRecord


# ---------------------------------------------------------
# Route existence sanity check
# ---------------------------------------------------------

def test__route_exists(client):
    hits = []
    for r in client.app.routes:
        path = getattr(r, "path", "")
        methods = sorted(list(getattr(r, "methods", []) or []))
        if "attach-asset" in path:
            hits.append((path, methods))
    print("ATTACH-ASSET ROUTES:", hits)
    assert hits, "attach-asset route not registered"


# ---------------------------------------------------------
# Auth override
# ---------------------------------------------------------

@pytest.fixture
def as_editor(editor_user):
    """
    Force both get_current_user + require_editor to resolve to editor_user.
    """
    from app.main import app

    app.dependency_overrides[get_current_user] = lambda: editor_user
    app.dependency_overrides[require_editor] = lambda: editor_user

    yield

    app.dependency_overrides.pop(get_current_user, None)
    app.dependency_overrides.pop(require_editor, None)


# ---------------------------------------------------------
# Model + Asset fixtures
# ---------------------------------------------------------

@pytest.fixture
def model_record(db, editor_user):
    """
    Create a real model record so asset.model_id is valid.
    Your schema requires owner_id NOT NULL.
    """
    m = ModelRecord(
        name=f"Test Model {uuid.uuid4().hex[:8]}",
        owner_id=editor_user.id,              # ✅ required
        preview_camera_preset_id="front_iso", # ✅ matches your error insert defaults
        description=None,
    )
    db.add(m)
    db.commit()
    db.refresh(m)
    return m


@pytest.fixture
def asset_ready(db, model_record):
    """
    Create a unique Asset each time (s3_key is UNIQUE).
    Attach it to a real model.
    """
    a = Asset(
        filename="car.glb",
        content_type="model/gltf-binary",
        size=123,
        s3_key=f"assets/test/{uuid.uuid4().hex}.glb",
        thumbnail_key=None,
        asset_metadata={},
        status=AssetStatus.ready,
        model_id=model_record.id,  # ✅ critical
        is_visible=True,
    )
    db.add(a)
    db.commit()
    db.refresh(a)
    return a


@pytest.fixture
def allow_model_access(monkeypatch, model_record):
    """
    Bypass model-level access checks for Tier 6G.2 tests.
    Covers both common patterns:
      - get_model_if_accessible()
      - get_models_accessible_to_user()
    """
    from app import crud

    monkeypatch.setattr(
        crud,
        "get_model_if_accessible",
        lambda *args, **kwargs: model_record,
    )

    monkeypatch.setattr(
        crud,
        "get_models_accessible_to_user",
        lambda db, user_id: [(model_record, "editor")],
    )


# ---------------------------------------------------------
# Tests
# ---------------------------------------------------------

def test_attach_asset_requires_draft(
    client,
    completed_snapshot,
    as_editor,
    asset_ready,
    allow_model_access,
):
    project_id = completed_snapshot.project_id
    snapshot_id = completed_snapshot.id

    r = client.post(
        f"/projects/{project_id}/snapshots/{snapshot_id}/tools/attach-asset",
        json={"object_id": "vehicle-1", "asset_id": asset_ready.id},
    )
    assert r.status_code == 409


def test_attach_asset_sets_asset_ref_pointer(
    client,
    completed_snapshot,
    as_editor,
    asset_ready,
    allow_model_access,
):
    """
    Create a draft from completed_snapshot using the real endpoint,
    then attach the asset to that draft.
    """
    project_id = completed_snapshot.project_id
    base_snapshot_id = completed_snapshot.id

    # 1) Create draft
    d = client.post(f"/projects/{project_id}/snapshots/{base_snapshot_id}/draft")
    assert d.status_code == 200
    draft_id = d.json()["id"]

    # 2) Attach asset
    r = client.post(
        f"/projects/{project_id}/snapshots/{draft_id}/tools/attach-asset",
        json={"object_id": "vehicle-1", "asset_id": asset_ready.id},
    )
    assert r.status_code == 200, r.text
    data = r.json()
    assert data["asset_ref"] == f"asset:{asset_ready.id}"

    # 3) Scene index reflects attachment
    s = client.get(f"/projects/{project_id}/snapshots/{draft_id}/scene")
    assert s.status_code == 200
    scene = s.json()

    assert any(
        o.get("id") == "vehicle-1" and o.get("asset_ref") == f"asset:{asset_ready.id}"
        for o in scene["objects"]
    )
