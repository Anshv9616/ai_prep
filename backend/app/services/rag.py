


# from transformers import pipeline

# # client=genai.Client(api_key="AIzaSyA9eu7X7M5P9eg5-zaJ0j1nH2V8CI1xHY8")

# generator=pipeline("text-generation",model="gpt2")


# def generate_answer(query: str, chunks: list[str]):
#     def clean_text(text):
#         text = text.replace("\n", " ")
#         text = text.replace("|", " ")
#         return text.strip()

#     clean_chunks = [clean_text(c) for c in chunks[:3]]
#     context = " ".join(clean_chunks)

#     prompt = f"""
# You are a resume assistant.

# Answer ONLY using the context.
# Give a short clear answer.

# Context:
# {context}

# Question:
# {query}

# Answer:
# """

#     result = generator(
#         prompt,
#         max_new_tokens=80,
#         do_sample=False
#     )

#     output = result[0]["generated_text"]

#     return output.split("Answer:")[-1].strip()





from groq import Groq
import json
client = Groq(api_key="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")


 # your client

def generate_answer(query: str, chunks: list[str]):
    context = "\n\n---\n\n".join([f"[SECTION {i+1}] {c.strip()}" for i, c in enumerate(chunks)])

    system_prompt = """You are Ansh Verma's personal Resume Interview Coach (very helpful & honest).

Rules:
- For factual questions → Answer directly from resume. If not explicit → say "Not explicitly mentioned" and mention closest evidence.
- For "generate", "rate", "suggest", "improve" questions → Be creative but grounded in resume. Always give score/reason + 2-3 bullet points.
- ALWAYS return valid JSON only.

JSON format:
{
  "answer": "Full clear answer here (include score/explanation if needed)",
  "sources": ["short relevant snippet 1", "short relevant snippet 2"],
  "confidence": 92,
  "confidence_label": "HIGH"          // only use HIGH / MEDIUM / LOW
}
"""

    try:
        chat = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Resume Context:\n{context}\n\nUser Question: {query}"}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.2,
            max_tokens=500,
            response_format={"type": "json_object"}
        )

        return json.loads(chat.choices[0].message.content)

    except:
        return {
            "answer": "Error generating response",
            "sources": [],
            "confidence": 0,
            "confidence_label": "LOW"
        }