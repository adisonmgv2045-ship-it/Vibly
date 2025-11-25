from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.crud import crud
from app.schemas import schemas
import random
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

def send_email_code(to_email: str, code: str):
    sender_email = os.getenv("EMAIL_HOST_USER")
    sender_password = os.getenv("EMAIL_HOST_PASSWORD")
    
    if not sender_email or not sender_password:
        print("--- EMAIL CONFIG MISSING: PRINTING CODE TO CONSOLE ---")
        print(f"--- EMAIL CODE FOR {to_email}: {code} ---")
        return False

    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = to_email
        msg['Subject'] = "Tu código de verificación de Vibly"

        body = f"""
        <html>
          <body>
            <h2>Bienvenido a Vibly</h2>
            <p>Tu código de verificación es:</p>
            <h1 style="color: #d31027; letter-spacing: 5px;">{code}</h1>
            <p>Úsalo para iniciar sesión. No lo compartas con nadie.</p>
          </body>
        </html>
        """
        msg.attach(MIMEText(body, 'html'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, to_email, text)
        server.quit()
        print(f"Email sent to {to_email}")
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        print(f"--- FALLBACK EMAIL CODE FOR {to_email}: {code} ---")
        return False

@router.post("/send-code")
def send_code(user_in: schemas.UserLogin, db: Session = Depends(get_db)):
    # Generate 6 digit code
    code = str(random.randint(100000, 999999))
    
    # Save code to DB (associated with phone number for now as primary key logic)
    crud.create_auth_code(db, user_in.phone_number, code)
    
    # Send Email
    send_email_code(user_in.email, code)
    
    return {"message": "Code sent"}

@router.post("/verify-code")
def verify_code(verify_in: schemas.UserVerify, db: Session = Depends(get_db)):
    # Verify code
    auth_code = crud.verify_auth_code(db, verify_in.phone_number, verify_in.code)
    if not auth_code:
        raise HTTPException(status_code=400, detail="Invalid code")
    
    # Check if user exists, if not create
    user = crud.get_user_by_phone(db, verify_in.phone_number)
    if not user:
        user = crud.create_user(db, schemas.UserCreate(
            phone_number=verify_in.phone_number,
            email=verify_in.email
        ))
    elif not user.email:
        # Update email if existing user doesn't have one
        user.email = verify_in.email
        db.commit()
    
    return {"user": user}
