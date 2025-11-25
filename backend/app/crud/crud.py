from sqlalchemy.orm import Session
from app.models import models
from app.schemas import schemas
from datetime import datetime

def get_chats(db: Session, user_id: int):
    # Get chats for this user
    user_chats = db.query(models.Chat).join(models.ChatMember).filter(models.ChatMember.user_id == int(user_id)).all()
    
    result = []
    for chat in user_chats:
        # Determine display name and avatar
        display_name = chat.name
        display_avatar = chat.avatar_url
        
        if not chat.is_group:
            # Find the other member
            other_member = db.query(models.User).join(models.ChatMember).filter(
                models.ChatMember.chat_id == chat.id,
                models.ChatMember.user_id != int(user_id)
            ).first()
            
            if other_member:
                # Check if there is a contact alias
                contact = db.query(models.Contact).filter(
                    models.Contact.user_id == int(user_id),
                    models.Contact.contact_user_id == other_member.id
                ).first()
                
                display_name = contact.alias if contact else (other_member.full_name or other_member.phone_number)
                display_avatar = other_member.avatar_url

        last_msg = db.query(models.Message).filter(models.Message.chat_id == chat.id).order_by(models.Message.timestamp.desc()).first()
        unread = db.query(models.Message).filter(models.Message.chat_id == chat.id, models.Message.is_read == False).count()
        
        chat_data = schemas.Chat(
            id=chat.id,
            name=display_name,
            avatar_url=display_avatar,
            updated_at=chat.updated_at,
            last_message=last_msg.content if last_msg else "No messages yet",
            unread_count=unread,
            is_group=chat.is_group
        )
        result.append(chat_data)
    return result

def get_chat_messages(db: Session, chat_id: int):
    return db.query(models.Message).filter(models.Message.chat_id == chat_id).order_by(models.Message.timestamp.asc()).all()

def create_message(db: Session, message: schemas.MessageCreate):
    db_message = models.Message(
        content=message.content,
        sender_id=message.sender_id,
        chat_id=message.chat_id,
        timestamp=datetime.utcnow()
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    
    # Update chat timestamp
    chat = db.query(models.Chat).filter(models.Chat.id == message.chat_id).first()
    if chat:
        chat.updated_at = datetime.utcnow()
        db.commit()
        
    return db_message

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        phone_number=user.phone_number,
        email=user.email,
        username=user.username,
        full_name=user.full_name,
        avatar_url=user.avatar_url
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_phone(db: Session, phone_number: str):
    return db.query(models.User).filter(models.User.phone_number == phone_number).first()

def create_auth_code(db: Session, phone_number: str, code: str):
    # Eliminar códigos anteriores
    db.query(models.AuthCode).filter(models.AuthCode.phone_number == phone_number).delete()
    
    db_code = models.AuthCode(
        phone_number=phone_number,
        code=code,
        expires_at=datetime.utcnow()
    )
    db.add(db_code)
    db.commit()
    return db_code

def verify_auth_code(db: Session, phone_number: str, code: str):
    return db.query(models.AuthCode).filter(
        models.AuthCode.phone_number == phone_number,
        models.AuthCode.code == code
    ).first()

def create_chat(db: Session, chat: schemas.ChatCreate):
    db_chat = models.Chat(name=chat.name, avatar_url=chat.avatar_url)
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return db_chat

def create_reel(db: Session, reel: schemas.ReelCreate):
    db_reel = models.Reel(**reel.dict())
    db.add(db_reel)
    db.commit()
    db.refresh(db_reel)
    return db_reel

def get_reels(db: Session):
    return db.query(models.Reel).order_by(models.Reel.created_at.desc()).all()

def create_status(db: Session, status: schemas.StatusCreate):
    db_status = models.Status(**status.dict())
    db.add(db_status)
    db.commit()
    db.refresh(db_status)
    return db_status

def get_active_statuses(db: Session):
    return db.query(models.Status).filter(models.Status.expires_at > datetime.utcnow()).all()

def get_user_settings(db: Session, user_id: int):
    settings = db.query(models.UserSettings).filter(models.UserSettings.user_id == user_id).first()
    if not settings:
        settings = models.UserSettings(user_id=user_id)
        db.add(settings)
        db.commit()
        db.refresh(settings)
    return settings

def update_user_settings(db: Session, user_id: int, settings: schemas.SettingsUpdate):
    db_settings = get_user_settings(db, user_id)
    for key, value in settings.dict().items():
        setattr(db_settings, key, value)
    db.commit()
    db.refresh(db_settings)
    return db_settings

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate):
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    
    update_data = user_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_private_chat(db: Session, user1_id: int, user2_id: int):
    # Find a chat where both users are members and is_group is False
    user1_chats = db.query(models.ChatMember).filter(models.ChatMember.user_id == user1_id).all()
    chat_ids = [cm.chat_id for cm in user1_chats]
    
    common_chat = db.query(models.Chat).join(models.ChatMember).filter(
        models.Chat.id.in_(chat_ids),
        models.ChatMember.user_id == user2_id,
        models.Chat.is_group == False
    ).first()
    
    return common_chat

def create_private_chat(db: Session, user1_id: int, user2_id: int):
    # Get users to set chat name (optional, or handle in frontend)
    user2 = db.query(models.User).filter(models.User.id == user2_id).first()
    
    # Create chat
    # For private chats, name might be redundant if we handle it dynamically, 
    # but for simplicity let's set it to the other user's name for now.
    db_chat = models.Chat(name=user2.full_name or user2.phone_number, is_group=False, avatar_url=user2.avatar_url)
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    
    # Add members
    member1 = models.ChatMember(chat_id=db_chat.id, user_id=user1_id)
    member2 = models.ChatMember(chat_id=db_chat.id, user_id=user2_id)
    db.add(member1)
    db.add(member2)
    db.commit()
    
    return db_chat

def create_contact(db: Session, user_id: int, contact: schemas.ContactCreate):
    existing = db.query(models.Contact).filter(
        models.Contact.user_id == user_id,
        models.Contact.contact_user_id == contact.contact_user_id
    ).first()
    
    if existing:
        existing.alias = contact.alias
        db.commit()
        db.refresh(existing)
        return existing

    db_contact = models.Contact(
        user_id=user_id,
        contact_user_id=contact.contact_user_id,
        alias=contact.alias
    )
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def get_contacts(db: Session, user_id: int):
    return db.query(models.Contact).filter(models.Contact.user_id == user_id).all()

