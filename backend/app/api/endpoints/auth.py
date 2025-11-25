from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.crud import crud
from app.schemas import schemas
import random

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("/send-code")
def send_code(user_in: schemas.UserLogin, db: Session = Depends(get_db)):
    # Generate 6 digit code
    code = str(random.randint(100000, 999999))
    
    # Save code to DB
    crud.create_auth_code(db, user_in.phone_number, code)
    
    # In a real app, send SMS here
    print(f"SMS Code for {user_in.phone_number}: {code}")
    
    return {"message": "Code sent"}

@router.post("/verify-code")
def verify_code(verify_in: schemas.UserVerify, db: Session = Depends(get_db)):
    # Verify code
    auth_code = crud.verify_auth_code(db, verify_in.phone_number, verify_in.code)
    if not auth_code:
        raise HTTPException(status_code=400, detail="Invalid code")
    
    # Check if user exists, if not create
    user = crud.get_user_by_phone(db, verify_in.phone_number)
    if not user:
        user = crud.create_user(db, schemas.UserCreate(phone_number=verify_in.phone_number))
    
    return {"user": user}
