from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.crud import crud
from app.schemas import schemas

router = APIRouter(
    prefix="/contacts",
    tags=["contacts"]
)

@router.post("/", response_model=schemas.Contact)
def create_contact(contact: schemas.ContactCreate, user_id: int, db: Session = Depends(get_db)):
    # In a real app, user_id would come from the token
    return crud.create_contact(db, user_id=user_id, contact=contact)

@router.get("/", response_model=List[schemas.Contact])
def read_contacts(user_id: int, db: Session = Depends(get_db)):
    return crud.get_contacts(db, user_id=user_id)
