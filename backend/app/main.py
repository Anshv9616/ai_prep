from fastapi import FastAPI,Depends,HTTPException,Header
# from fastapi.security import OAuth2PasswordBearer
from app.db.database import engine,Base
from app.models import user,resume
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth
from jose import jwt,JWTError
from app.routers import resume
from app.core.deps import get_current_user
from app.models import chunks
from app.routers import interview
from contextlib import asynccontextmanager


app = FastAPI()
ml_models={}
origins = [
    "http://localhost:3000", 
    "https://ai-prep-murex.vercel.app" # React frontend
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(resume.router)
app.include_router(interview.router)

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "API is running"}








@app.get("/protected")
def protected(user:str=Depends(get_current_user)):
    return {"message":f"Hello{user}"}