from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class MessageBase(BaseModel):
    content: str

class MessageCreate(MessageBase):
    chat_id: int
    sender_id: int

class Message(MessageBase):
    id: int
    timestamp: datetime
    is_read: bool
    sender_id: int
    chat_id: int

    class Config:
        from_attributes = True

class ChatBase(BaseModel):
    name: str
    avatar_url: Optional[str] = None
    is_group: bool = False

class ChatCreate(ChatBase):
    pass

class ChatCreatePrivate(BaseModel):
    target_user_id: int
    current_user_id: int

class Chat(ChatBase):
    id: int
    updated_at: datetime
    last_message: Optional[str] = None
    unread_count: int = 0

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    phone_number: str
    username: Optional[str] = None
    full_name: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None

class UserCreate(UserBase):
    pass

class UserLogin(BaseModel):
    phone_number: str

class UserVerify(BaseModel):
    phone_number: str
    code: str

class User(UserBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    username: Optional[str] = None
    full_name: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None

class ReelBase(BaseModel):
    video_url: str
    caption: Optional[str] = None

class ReelCreate(ReelBase):
    user_id: int

class Reel(ReelBase):
    id: int
    likes: int
    created_at: datetime
    user: User

    class Config:
        from_attributes = True

class StatusBase(BaseModel):
    image_url: str
    caption: Optional[str] = None

class StatusCreate(StatusBase):
    user_id: int
    expires_at: datetime

class Status(StatusBase):
    id: int
    created_at: datetime
    user: User

    class Config:
        from_attributes = True

class SettingsBase(BaseModel):
    privacy_last_seen: str = "everyone"
    privacy_profile_photo: str = "everyone"
    theme: str = "light"
    notifications_enabled: bool = True

class SettingsUpdate(SettingsBase):
    pass

class Settings(SettingsBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True

class ContactBase(BaseModel):
    alias: str

class ContactCreate(ContactBase):
    contact_user_id: int

class Contact(ContactBase):
    id: int
    user_id: int
    contact_user_id: int
    contact_user: User

    class Config:
        from_attributes = True

