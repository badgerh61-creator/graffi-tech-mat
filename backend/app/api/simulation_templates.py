from __future__ import annotations

from typing import Any, Dict, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.services.scenario_templates import list_templates, materialize_template, get_template_meta
from app.services.simulation_scenarios import create_scenario

router = APIRouter(prefix="/simulation", tags=["simulation-templates"])


@router.get("/templates")
def templates_list(user=Depends(get_current_user)):
    return {"templates": list_templates()}


@router.post("/scenarios/from-template")
def scenario_from_template(
    body: Dict[str, Any],
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    project_id = body.get("project_id")
    name = body.get("name")
    template_key = body.get("template_key")
    engine_version = body.get("engine_version", "pseudo-v1")
    overrides = body.get("overrides") or {}

    if not isinstance(project_id, int) or project_id <= 0:
        raise HTTPException(422, "project_id required")
    if not isinstance(name, str) or not name.strip():
        raise HTTPException(422, "name required")
    if not isinstance(template_key, str) or not template_key.strip():
        raise HTTPException(422, "template_key required")
    if not isinstance(overrides, dict):
        raise HTTPException(422, "overrides must be object")

    try:
        tmpl = get_template_meta(template_key)
        scenario = materialize_template(template_key=template_key, overrides=overrides)
    except KeyError as e:
        raise HTTPException(404, str(e)) from e
    except ValueError as e:
        raise HTTPException(422, str(e)) from e

    out = create_scenario(
        db=db,
        project_id=project_id,
        name=name,
        scenario=scenario,
        user_id=user.id,
        engine_version=engine_version,
        template_key=tmpl.key,
        template_version=tmpl.version,
    )

    return {
        "scenario_id": out["scenario_id"],
        "scenario_hash": out["scenario_hash"],
        "template_key": tmpl.key,
    }
