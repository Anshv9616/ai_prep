from fastapi import APIRouter,UploadFile,File,Depends,HTTPException,Form
from app.services.chunker import chunk_text
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
import shutil
import uuid

import os
from PyPDF2 import PdfReader
from app.db.database import SessionLocal
from app.models.resume import Resume
from app.core.deps import get_current_user
from app.services.embedding import get_embedding,get_embeddings_batch
from app.models.chunks import Chunk
from app.services.search import search_chunks
from app.services.generate_interview import generate_interview
from app.models.interview import InterViewQuestion
from app.services.rag import generate_answer
from app.models.interview import InterViewQuestion
from app.services.evaluate import get_ai_feedback,match_resume_jd,generate_cover_letter,generate_linkedin_bio
from fastapi import BackgroundTasks
from groq import Groq
from app.core.deps import get_resume_text
from app.core.cloudinary import upload_resume
router=APIRouter(prefix="/resume",tags=["resume"])

UPLOAD_DIR="uploads"
os.makedirs(UPLOAD_DIR,exist_ok=True)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()



@router.post("/upload")
def upload_resume_route(
    file: UploadFile = File(...),
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    
    existing_resume = db.query(Resume).filter(Resume.user_id == user.id).first()
    if existing_resume:
        db.query(Chunk).filter(Chunk.resume_id == existing_resume.id).delete()
        
        if existing_resume.file_path and not existing_resume.file_path.startswith("http"):
         if os.path.exists(existing_resume.file_path):
          os.remove(existing_resume.file_path)
        db.delete(existing_resume)
        db.commit()

    
    temp_path = f"temp_{user.id}_{uuid.uuid4()}.pdf"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        
        reader = PdfReader(temp_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""

        
        cloudinary_url = upload_resume(temp_path, user.id)

        
        resume = Resume(
            user_id=user.id,
            file_path=cloudinary_url,  
            content=text
        )
        db.add(resume)
        db.commit()
        db.refresh(resume)

        # Chunk and embed
        chunks = chunk_text(text)
        embeddings = get_embeddings_batch(chunks)
       
        db.bulk_save_objects([
            Chunk(resume_id=resume.id, content=ch, embedding=emb)
            for ch, emb in zip(chunks, embeddings)
        ])
        db.commit()

    finally:
        
        if os.path.exists(temp_path):
            os.remove(temp_path)

    return {
        "message": "Resume uploaded successfully",
        "file_url": cloudinary_url,
        "total_chunks": len(chunks)
    }

@router.get("/my")
def get_my_resume(
     user:str=Depends(get_current_user),
     db:Session=Depends(get_db)
):
    resume = db.query(Resume).filter(Resume.user_id == user.id).first()

    if not resume:
        return {"message":"No resume Found"}
    return {
        "file_path": resume.file_path,
        "content": resume.content
    }


@router.get("/search")
def search(query:str,db:Session=Depends(get_db)):
    result=search_chunks(query,db)

    return{
         "results":[r.content for r in result]
    }


@router.get("/ask")
def ask(query: str, db: Session = Depends(get_db)):
    results = search_chunks(query, db)

    chunks = [r.content for r in results]
    chunks = chunks[:3]
    answer = generate_answer(query, chunks)

    return {
        "answer": answer,
        "chunks_used": chunks
    }

@router.post("/match-resume")
def match_resume_to_job(
     job_description:str=Form(...),
     db:Session=Depends(get_db),
     user:User=Depends(get_current_user)
):
    resume_text=get_resume_text(user.id,db)

    if not resume_text:
        raise HTTPException(status_code=404,detail="No resume found")
    
    result=match_resume_jd(resume_text,job_description)
    return result


@router.post("/cover-letter")
def get_cover_letter(
      job_description:str=Form(...),
      db:Session=Depends(get_db),
      user:User=Depends(get_current_user)
):
    resume_text=get_resume_text(user.id,db)

    if not resume_text:
         raise HTTPException(status_code=404,detail="No resume found")
    result=generate_cover_letter(resume_text,job_description)
    return result


@router.get("/linkedin-bio")
def generate_linkedin_bio_route(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    resume_text = get_resume_text(user.id, db)

    if not resume_text:
        raise HTTPException(status_code=404, detail="No resume found. Please upload your resume first.")

    result = generate_linkedin_bio(resume_text)
    return result






