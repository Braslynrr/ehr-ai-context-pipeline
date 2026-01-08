from ollama import embeddings

def embed(text: str):
    return embeddings(
        model="nomic-embed-text",
        prompt=text
    )["embedding"]