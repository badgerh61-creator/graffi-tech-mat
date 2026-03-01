from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.material_catalog import list_materials

router = APIRouter(prefix="/materials", tags=["materials"])

@router.get("/")
def get_materials(
    page: int = 1,
    pageSize: int = 50,
    db: Session = Depends(get_db),
):
    return list_materials(db, page=page, page_size=pageSize)

# ✅ Tier 7.42 additive endpoint (no DB required)
@router.get("/presets")
def get_material_presets(
    db: Session = Depends(get_db),
):
    """
    Canonical preset list for Material Inspector.
    Keep response stable.
    """
    # If your DB materials already ARE the presets, just reuse list_materials:
    # return {"presets": list_materials(db, page=1, page_size=500).get("items", [])}

    # Better: normalize a stable shape:
    res = list_materials(db, page=1, page_size=500)

    # Support either list return or paginated dict return
    items = res.get("items") if isinstance(res, dict) else res
    items = items or []

    presets = []
    for m in items:
        # adapt these fields to your actual material row shape
        pid = str(m.get("id") or m.get("code") or m.get("name") or "")
        if not pid:
            continue
        presets.append({
            "id": pid,
            "name": m.get("name") or pid,
            "kind": m.get("kind") or "standard",
            "color": m.get("color") or m.get("base_color") or None,
            "roughness": m.get("roughness"),
            "metalness": m.get("metalness"),
        })

    presets.sort(key=lambda x: x["id"])
    return {"presets": presets}
