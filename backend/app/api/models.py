from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db.session import get_db
from .. import crud, schemas

router = APIRouter()

@router.post('/', response_model=schemas.ModelRead)
def create_model(model_in: schemas.ModelCreate, db: Session = Depends(get_db)):
    return crud.create_model(db, model_in)

@router.get('/', response_model=list[schemas.ModelRead])
def list_models(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.list_models(db, skip=skip, limit=limit)

@router.get('/{model_id}', response_model=schemas.ModelRead)
def get_model(model_id: int, db: Session = Depends(get_db)):
    m = crud.get_model(db, model_id)
    if not m:
        raise HTTPException(status_code=404, detail='model not found')
    return m
