# app/schemas/organizations.py
from pydantic import BaseModel
from datetime import datetime


class OrganizationCreate(BaseModel):
    name: str


class OrganizationRead(BaseModel):
    id: int
    name: str
    created_at: datetime

    class Config:
        orm_mode = True

