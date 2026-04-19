from fastapi import APIRouter,UploadFile,File,Depends,HTTPException
from app.services.chunker import chunk_text
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
import shutil

from PyPDF2 import PdfReader
from app.db.database import SessionLocal
from app.models.resume import Resume
from app.core.deps import get_current_user
from app.services.embedding import get_embedding
from app.models.chunks import Chunk
from app.services.search import search_chunks
from app.services.generate_interview import generate_interview
from app.models.interview import InterViewQuestion
from app.services.rag import generate_answer
from app.models.interview import InterViewQuestion
from app.services.evaluate import get_ai_feedback
from groq import Groq
import asyncio
from fastapi import BackgroundTasks
import uuid
import redis
from app.services.cache import get_question_cached,get_ai_feedback_cached
from dotenv import load_dotenv
import os
load_dotenv()

redis_client = redis.from_url(
    os.getenv("REDIS_URL", "redis://localhost:6379"),
    decode_responses=True
)

router=APIRouter(prefix="/interview",tags=["interview"])





def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()





@router.get("/generate")
def generate(topic:str="general",db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    
    search_query=f"{topic} and technical implementation"
    res = search_chunks(search_query, db, user_id=current_user.id)
    session_id = str(uuid.uuid4())
   
    if not res:
        raise HTTPException(
            status_code=404, 
            detail="No resume chunks found. Please upload a resume first."
        )

    
    chunks = [r.content for r in res]
    
    resume = db.query(Resume).filter(Resume.user_id == current_user.id).first()
    questions_data = generate_interview(chunks,topic=topic)
    for q_text in questions_data["questions"]:
     new_q = InterViewQuestion(
        user_id=current_user.id,
        resume_id=resume.id,
        topic=topic,
        session_id=session_id,
        question_text=q_text
     )
     db.add(new_q)

    db.commit()
    
    return {
        "user_id": current_user.id,
        "session_id": session_id,
        "questions": questions_data
    }

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@router.post("/evaluate-audio/{session_id}/{question_id}")
async def evaluate_and_save_audio_answer(
    question_id: int,
    session_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    
    db_question = get_question_cached(question_id, session_id, user.id, db)
    if not db_question:
        raise HTTPException(status_code=404, detail="Question not found in this session")

    temp_path = f"temp_{user.id}_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        
        loop = asyncio.get_event_loop()
        transcription_result = await loop.run_in_executor(
            None,
            lambda: client.audio.transcriptions.create(
                file=(temp_path, open(temp_path, "rb").read()),
                model="whisper-large-v3-turbo",
                response_format="text"
            )
        )
        user_text_answer = transcription_result

        
        evaluation = get_ai_feedback_cached(db_question.question_text, user_text_answer)

        # invalidate question cache after answer is saved
        cache_key = f"question:{user.id}:{session_id}:{question_id}"
        redis_client.delete(cache_key)

        db_question.user_answer = user_text_answer
        db_question.ai_feedback = evaluation["feedback"]
        db_question.score = evaluation["score"]
        db_question.created_at = func.now()
        db.commit()
        db.refresh(db_question)

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

    return {
        "message": "Audio processed and record updated",
        "transcription": user_text_answer,
        "score": db_question.score,
        "feedback": db_question.ai_feedback
    }

@router.get("/stats")
def get_user_stats(db: Session = Depends(get_db), user=Depends(get_current_user)):
    stats = db.query(
        InterViewQuestion.topic,
        func.avg(InterViewQuestion.score).label("average_score"),
        func.count(InterViewQuestion.id).label("total_questions")
    ).filter(InterViewQuestion.user_id == user.id).group_by(InterViewQuestion.topic).all()

    
    return [
        {
            "topic": row.topic,
            "average_score": round(float(row.average_score), 2) if row.average_score else 0,
            "total_questions": row.total_questions
        }
        for row in stats
    ]

@router.get("/session-report/{session_id}")
def get_session_report(
    session_id: str, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    results = db.query(InterViewQuestion).filter(
        InterViewQuestion.session_id == session_id,
        InterViewQuestion.user_id == current_user.id
    ).all()

    if not results:
        raise HTTPException(status_code=404, detail="Session not found")

    
   
    topic = results[0].topic if results else "Unknown"

    
    total_questions = len(results)
    answered_count = len([q for q in results if q.user_answer is not None])
    
    
    status = "Completed" if answered_count == total_questions else "In Progress"

    total_score = sum([q.score for q in results if q.score is not None])
    avg_score = total_score / answered_count if answered_count > 0 else 0
    
    return {
        "session_id": session_id,
        "topic": topic,
        "status": status, 
        "progress": f"{answered_count}/{total_questions}", 
        "average_score": round(avg_score, 2),
        "total_questions": total_questions,
        "answered_questions": answered_count,
        "details": results 
    }


@router.get("/history")
def get_interview_history(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    
    
    history = db.query(
        InterViewQuestion.session_id,
        InterViewQuestion.topic,
        func.max(InterViewQuestion.created_at).label("date"),
        func.avg(InterViewQuestion.score).label("avg_score"),
        func.count(InterViewQuestion.id).label("total_q"),
        func.count(InterViewQuestion.user_answer).label("answered_q")
    ).filter(InterViewQuestion.user_id == current_user.id)\
     .group_by(InterViewQuestion.session_id, InterViewQuestion.topic)\
     .order_by(func.max(InterViewQuestion.created_at).desc()).all()

    
    return [
        {
            "session_id": row.session_id,
            "topic": row.topic,
            "date": row.date,
            "avg_score": round(float(row.avg_score), 2) if row.avg_score else 0,
            "is_completed": row.total_q == row.answered_q, # True if all answered
            "progress": f"{row.answered_q}/{row.total_q}"
        } for row in history
    ]