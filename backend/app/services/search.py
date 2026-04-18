from sqlalchemy.orm import Session
from app.models.chunks import Chunk
from app.models.resume import Resume
import cohere
import os
from dotenv import load_dotenv
load_dotenv()

co = cohere.Client(os.getenv("COHERE_API_KEY"))

def search_chunks(topic: str, db: Session, user_id: int):
    refined_query = f"focus on {topic}: technical details, tools used, and challenges"

    response = co.embed(
        texts=[refined_query],
        model="embed-english-light-v3.0",
        input_type="search_query"
    )
    query_embedding = response.embeddings[0]

    result = db.query(Chunk)\
        .join(Resume)\
        .filter(Resume.user_id == user_id)\
        .order_by(Chunk.embedding.cosine_distance(query_embedding))\
        .limit(5)\
        .all()

    return result