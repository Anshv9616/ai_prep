
def chunk_text(text: str, chunk_size=400, overlap=100):
    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size

        if end < text_length:
            while end < text_length and text[end] != " ":
                end += 1

        chunk = text[start:end].strip()
        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks      
