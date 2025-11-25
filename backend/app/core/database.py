from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
import urllib.parse

# Force loading .env with utf-8 encoding explicitly
load_dotenv(encoding="utf-8")

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./vibly.db")
# DATABASE_URL = "postgresql://postgres:1234@localhost:5432/vibly_db"
print(f"DEBUG: DATABASE_URL type: {type(DATABASE_URL)}")
print(f"DEBUG: DATABASE_URL repr: {repr(DATABASE_URL)}")


# Fix for special characters in password
if "postgresql" in DATABASE_URL:
    try:
        # Parse the URL manually to encode password if needed
        prefix, suffix = DATABASE_URL.split("://", 1)
        # Use rsplit to handle '@' in password correctly
        credentials, host_db = suffix.rsplit("@", 1)
        user, password = credentials.split(":", 1)
        
        # Encode password
        encoded_password = urllib.parse.quote_plus(password)
        
        # Reconstruct URL
        SQLALCHEMY_DATABASE_URL = f"{prefix}://{user}:{encoded_password}@{host_db}"
    except Exception as e:
        print(f"Error parsing DATABASE_URL: {e}")
        # Fallback if parsing fails
        SQLALCHEMY_DATABASE_URL = DATABASE_URL
else:
    SQLALCHEMY_DATABASE_URL = DATABASE_URL

if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
