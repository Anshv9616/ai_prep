import json
import redis
import hashlib
from app.models.interview import InterViewQuestion
from app.services.evaluate import get_ai_feedback
import os
from dotenv import load_dotenv
load_dotenv()

redis_client = redis.from_url(
    os.getenv("REDIS_URL", "redis://localhost:6379"),
    decode_responses=True
)

def get_question_cached(question_id, session_id, user_id, db):
    cache_key = f"question:{user_id}:{session_id}:{question_id}"
    cached = redis_client.get(cache_key)
    if cached:
        data = json.loads(cached)
        return db.query(InterViewQuestion).filter(
            InterViewQuestion.id == data["id"]
        ).first()
    
    
    question = db.query(InterViewQuestion).filter(
        InterViewQuestion.id == question_id,
        InterViewQuestion.session_id == session_id,
        InterViewQuestion.user_id == user_id
    ).first()
    
    if question:
        redis_client.set(cache_key, json.dumps({"id": question.id}), ex=3600)
    
    return question

def get_ai_feedback_cached(question_text: str, user_answer: str):
   
    content_hash = hashlib.md5(
        f"{question_text}:{user_answer}".encode()
    ).hexdigest()
    
    cache_key = f"feedback:{content_hash}"
    
    cached = redis_client.get(cache_key)
    if cached:
        return json.loads(cached)
    
    
    evaluation = get_ai_feedback(question_text, user_answer)
    
    
    redis_client.setex(cache_key, 86400, json.dumps(evaluation))
    
    return evaluation