from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.crud import crud
from app.schemas import schemas
import shutil
import os
from typing import Optional

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.get("/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user_update: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = crud.update_user(db, user_id=user_id, user_update=user_update)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.post("/{user_id}/avatar")
async def upload_avatar(user_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Create directory if not exists
    upload_dir = "static/avatars"
    os.makedirs(upload_dir, exist_ok=True)
    
    # Generate filename
    file_extension = file.filename.split(".")[-1]
    filename = f"user_{user_id}_avatar.{file_extension}"
    file_path = f"{upload_dir}/{filename}"
    
    # Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # Update user avatar_url
    # Assuming the server is running on localhost:8000. In production, use env var.
    avatar_url = f"http://localhost:8000/static/avatars/{filename}"
    crud.update_user(db, user_id, schemas.UserUpdate(avatar_url=avatar_url))
    
    return {"avatar_url": avatar_url}

@router.get("/search/", response_model=schemas.User)
def search_user(phone: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_phone(db, phone_number=phone)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
