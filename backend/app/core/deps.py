from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.models.user import User
from app.db.database import SessionLocal
from app.models.resume import Resume
from app.models.chunks import Chunk
import os
from dotenv import load_dotenv
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        

        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        user = db.query(User).filter(User.email == email).first()

        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        return user   

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    

def get_resume_text(user_id: int, db: Session=Depends(get_db)):
    resume = db.query(Resume).filter(Resume.user_id == user_id).first()
    if not resume:
        return None
    chunks = db.query(Chunk).filter(Chunk.resume_id == resume.id).all()
    return " ".join(chunk.content for chunk in chunks)