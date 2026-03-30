from ehr_ai_core.error.app_error import AppError

from .vector_entry import VectorEntry
from concurrent.futures import ThreadPoolExecutor
from ollama import Client
import os

class Embedder:
    ___model = ""

    def __init__(self, model="bge-m3"):
        self.___model = model
        self.client = Client(
            host=os.getenv("OLLAMA_URL", "http://ehr_ollama:11434")
        )

    def embed(self, text: str):
        try:
            response = self.client.embeddings(
                model=self.___model,
                prompt=text
            )
            return response["embedding"]

        except Exception as e:
            raise AppError(f"Embedding failed: {e.args}", 500)

    def embed_chunks(self, chunks: list[dict], toembed: list[str]) -> list[VectorEntry]:
        embeddings = self.embed_batch([t.lower() for t in toembed])

        return [
            VectorEntry(embeddings[i], chunks[i])
            for i in range(len(chunks))
        ]
    
    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        with ThreadPoolExecutor(max_workers=3) as executor:
            return list(executor.map(self.embed, texts))