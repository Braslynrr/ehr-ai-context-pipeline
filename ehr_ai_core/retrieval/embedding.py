from .vector_entry import VectorEntry
from ollama import Client
import os

class Embedder:
    ___model = ""

    def __init__(self, model="nomic-embed-text"):
        self.___model = model
        self.client = Client(
            host=os.getenv("OLLAMA_URL", "http://ehr_ollama:11434")
        )

    def embed(self, text: str):
        return self.client.embeddings(
            model=self.___model,
            prompt=text
        )["embedding"]

    def embed_chunks(self, chunks: list[dict], toembed: list[str]) -> list[VectorEntry]:

        embedded_chunks = []
        for i in range(len(chunks)):

            embed_chunk = VectorEntry(
                self.embed(toembed[i].lower()),
                chunks[i]
            )

            embedded_chunks.append(embed_chunk)

        return embedded_chunks