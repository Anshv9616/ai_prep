import os
import cohere
from dotenv import load_dotenv
load_dotenv()

co = cohere.Client(os.getenv("COHERE_API_KEY"))

def get_embedding(text: str) -> list:
    response = co.embed(
        texts=[text],
        model="embed-english-light-v3.0",
        input_type="search_document"
    )
    return response.embeddings[0]

def get_embeddings_batch(texts: list[str]) -> list:
    response = co.embed(
        texts=texts,
        model="embed-english-light-v3.0",
        input_type="search_document"
    )
    return response.embeddings