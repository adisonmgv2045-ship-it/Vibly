from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas import schemas
from app.crud import crud
from app.models import models

router = APIRouter()

@router.get("/chats", response_model=List[schemas.Chat])
def read_chats(user_id: int, db: Session = Depends(get_db)):
    return crud.get_chats(db, user_id)

@router.get("/chats/{chat_id}/messages", response_model=List[schemas.Message])
def read_messages(chat_id: int, db: Session = Depends(get_db)):
    return crud.get_chat_messages(db, chat_id=chat_id)

@router.post("/messages", response_model=schemas.Message)
def send_message(message: schemas.MessageCreate, db: Session = Depends(get_db)):
    return crud.create_message(db, message=message)

@router.get("/reels", response_model=List[schemas.Reel])
def read_reels(db: Session = Depends(get_db)):
    return crud.get_reels(db)

@router.post("/reels", response_model=schemas.Reel)
def create_reel(reel: schemas.ReelCreate, db: Session = Depends(get_db)):
    return crud.create_reel(db, reel=reel)

@router.get("/statuses", response_model=List[schemas.Status])
def read_statuses(db: Session = Depends(get_db)):
    return crud.get_active_statuses(db)

@router.post("/statuses", response_model=schemas.Status)
def create_status(status: schemas.StatusCreate, db: Session = Depends(get_db)):
    return crud.create_status(db, status=status)

@router.get("/settings/{user_id}", response_model=schemas.Settings)
def read_settings(user_id: int, db: Session = Depends(get_db)):
    return crud.get_user_settings(db, user_id=user_id)

@router.put("/settings/{user_id}", response_model=schemas.Settings)
def update_settings(user_id: int, settings: schemas.SettingsUpdate, db: Session = Depends(get_db)):
    return crud.update_user_settings(db, user_id=user_id, settings=settings)



@router.post("/chats/private", response_model=schemas.Chat)
def create_private_chat(chat_in: schemas.ChatCreatePrivate, db: Session = Depends(get_db)):
    # Check if exists
    existing_chat = crud.get_private_chat(db, chat_in.current_user_id, chat_in.target_user_id)
    if existing_chat:
        return existing_chat
        
    # Create new
    return crud.create_private_chat(db, chat_in.current_user_id, chat_in.target_user_id)

@router.get("/chats/{chat_id}/details")
def get_chat_details(chat_id: int, user_id: int = None, db: Session = Depends(get_db)):
    chat = db.query(models.Chat).filter(models.Chat.id == chat_id).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    
    members = db.query(models.User).join(models.ChatMember).filter(models.ChatMember.chat_id == chat_id).all()
    
    other_user = None
    if not chat.is_group and len(members) == 2 and user_id:
        for m in members:
            if m.id != int(user_id):
                other_user = m
                break
    elif not chat.is_group and len(members) > 0:
         # Fallback if user_id not provided or something else
         other_user = members[0]

    return {
        "chat": chat,
        "members": members,
        "other_user": other_user
    }

