from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..db.session import get_db
from ..services import auth as auth_service

router = APIRouter()

@router.post('/register', response_model=schemas.UserRead)
def register(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = crud.get_user_by_email(db, user_in.email)
    if existing:
        raise HTTPException(status_code=400, detail='email already registered')
    hashed = auth_service.hash_password(user_in.password)
    user = crud.create_user(db, user_in, hashed)
    return user

@router.post('/login', response_model=schemas.Token)
def login(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, user_in.email)
    if not user:
        raise HTTPException(status_code=400, detail='invalid credentials')
    if not auth_service.verify_password(user_in.password, user.hashed_password):
        raise HTTPException(status_code=400, detail='invalid credentials')
    token = auth_service.create_access_token(subject=str(user.id))
    return schemas.Token(access_token=token)
