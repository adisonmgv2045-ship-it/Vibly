from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.core.database import engine, Base, SessionLocal
from app.api.endpoints import chats, auth, users, contacts
from app.models import models
from app.schemas import schemas
from app.crud import crud

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Vibly API", description="Backend para la red social Vibly")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chats.router)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(contacts.router)

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de Vibly"}

# Seed data on startup
@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    if db.query(models.User).count() == 0:
        # Create users
        user1 = crud.create_user(db, schemas.UserCreate(phone_number="+1234567890", username="me", full_name="Yo", avatar_url="https://i.pravatar.cc/150?u=0"))
        user2 = crud.create_user(db, schemas.UserCreate(phone_number="+1987654321", username="ana", full_name="Ana García", avatar_url="https://i.pravatar.cc/150?u=1"))
        user3 = crud.create_user(db, schemas.UserCreate(phone_number="+1122334455", username="dev", full_name="Dev Team", avatar_url="https://i.pravatar.cc/150?u=2"))
        
        # Create chats
        chat1 = crud.create_chat(db, schemas.ChatCreate(name="Ana García", avatar_url="https://i.pravatar.cc/150?u=1"))
        chat2 = crud.create_chat(db, schemas.ChatCreate(name="Dev Team", avatar_url="https://i.pravatar.cc/150?u=2"))
        
        # Create messages
        crud.create_message(db, schemas.MessageCreate(content="Hola, ¿cómo estás?", sender_id=user2.id, chat_id=chat1.id))
        crud.create_message(db, schemas.MessageCreate(content="¡Hola! Todo bien por aquí, trabajando en Vibly 🚀", sender_id=user1.id, chat_id=chat1.id))
        crud.create_message(db, schemas.MessageCreate(content="¿Viste el nuevo post?", sender_id=user2.id, chat_id=chat1.id))
        
        crud.create_message(db, schemas.MessageCreate(content="Reunión a las 3pm", sender_id=user3.id, chat_id=chat2.id))
        
    db.close()
