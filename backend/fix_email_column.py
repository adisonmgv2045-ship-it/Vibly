from sqlalchemy import create_engine, text
from app.core.database import DATABASE_URL

def fix_email_column():
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        try:
            # Check if column exists
            result = conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name='users' AND column_name='email'"))
            if result.fetchone():
                print("Column 'email' already exists.")
            else:
                print("Adding 'email' column...")
                conn.execute(text("ALTER TABLE users ADD COLUMN email VARCHAR"))
                conn.execute(text("CREATE UNIQUE INDEX ix_users_email ON users (email)"))
                conn.commit()
                print("Migration successful: Added email column to users table")
        except Exception as e:
            print(f"Migration failed: {e}")

if __name__ == "__main__":
    fix_email_column()
