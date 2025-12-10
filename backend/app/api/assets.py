from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db.session import get_db
from .. import crud, schemas
from ..services.s3 import get_object_url

router = APIRouter()

@router.get('/', response_model=list[schemas.AssetRead])
def list_assets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.list_assets(db, skip=skip, limit=limit)

@router.get('/{asset_id}', response_model=schemas.AssetRead)
def get_asset(asset_id: int, db: Session = Depends(get_db)):
    a = crud.get_asset(db, asset_id)
    if not a:
        raise HTTPException(status_code=404, detail='asset not found')
    return a

@router.get('/{asset_id}/url')
def asset_url(asset_id: int, db: Session = Depends(get_db)):
    a = crud.get_asset(db, asset_id)
    if not a:
        raise HTTPException(status_code=404, detail='asset not found')
    return {'url': get_object_url(a.s3_key), 'thumbnail': get_object_url(a.thumbnail_key) if a.thumbnail_key else None}
