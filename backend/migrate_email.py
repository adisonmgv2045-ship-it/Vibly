from sqlalchemy import create_engine, text
from app.core.database import DATABASE_URL

def migrate_email():
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        try:
            conn.execute(text("ALTER TABLE users ADD COLUMN email VARCHAR"))
            conn.execute(text("CREATE UNIQUE INDEX ix_users_email ON users (email)"))
            print("Migration successful: Added email column to users table")
        except Exception as e:
            print(f"Migration failed (maybe column exists?): {e}")

if __name__ == "__main__":
    migrate_email()
