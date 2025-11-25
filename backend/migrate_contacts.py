from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv
import urllib.parse

load_dotenv(encoding="utf-8")

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:1234@localhost:5432/vibly_db")

if "postgresql" in DATABASE_URL:
    try:
        prefix, suffix = DATABASE_URL.split("://", 1)
        credentials, host_db = suffix.rsplit("@", 1)
        user, password = credentials.split(":", 1)
        encoded_password = urllib.parse.quote_plus(password)
        DATABASE_URL = f"{prefix}://{user}:{encoded_password}@{host_db}"
    except:
        pass

engine = create_engine(DATABASE_URL)

with engine.connect() as connection:
    try:
        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS contacts (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id),
                contact_user_id INTEGER REFERENCES users(id),
                alias VARCHAR,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """))
        print("Table 'contacts' created successfully.")
    except Exception as e:
        print(f"Error: {e}")
