from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True, nullable=True)
    username = Column(String, unique=True, index=True, nullable=True)
    full_name = Column(String, nullable=True)
    bio = Column(String, nullable=True)
    avatar_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    messages = relationship("Message", back_populates="sender")
    settings = relationship("UserSettings", back_populates="user", uselist=False)
    reels = relationship("Reel", back_populates="user")
    statuses = relationship("Status", back_populates="user")
    chats = relationship("ChatMember", back_populates="user")
    saved_contacts = relationship("Contact", foreign_keys="Contact.user_id", back_populates="owner")

class UserSettings(Base):
    __tablename__ = "user_settings"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    privacy_last_seen = Column(String, default="everyone") # everyone, contacts, nobody
    privacy_profile_photo = Column(String, default="everyone")
    theme = Column(String, default="light")
    notifications_enabled = Column(Boolean, default=True)
    
    user = relationship("User", back_populates="settings")

class ChatMember(Base):
    __tablename__ = "chat_members"
    
    chat_id = Column(Integer, ForeignKey("chats.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    is_admin = Column(Boolean, default=False)
    
    chat = relationship("Chat", back_populates="members")
    user = relationship("User", back_populates="chats")

class AuthCode(Base):
    __tablename__ = "auth_codes"
    
    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, index=True)
    code = Column(String)
    expires_at = Column(DateTime)

class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    is_group = Column(Boolean, default=False)
    avatar_url = Column(String)
    updated_at = Column(DateTime, default=datetime.utcnow)
    
    messages = relationship("Message", back_populates="chat")
    members = relationship("ChatMember", back_populates="chat")

class Reel(Base):
    __tablename__ = "reels"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    video_url = Column(String)
    caption = Column(String)
    likes = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="reels")

class Status(Base):
    __tablename__ = "statuses"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    image_url = Column(String)
    caption = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)
    
    user = relationship("User", back_populates="statuses")

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    is_read = Column(Boolean, default=False)
    
    sender_id = Column(Integer, ForeignKey("users.id"))
    chat_id = Column(Integer, ForeignKey("chats.id"))
    
    sender = relationship("User", back_populates="messages")
    chat = relationship("Chat", back_populates="messages")

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    contact_user_id = Column(Integer, ForeignKey("users.id"))
    alias = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", foreign_keys=[user_id], back_populates="saved_contacts")
    contact_user = relationship("User", foreign_keys=[contact_user_id])
