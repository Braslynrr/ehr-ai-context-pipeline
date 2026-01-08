from .vector_entry import VectorEntry
from ollama import embeddings

class Embedder:
    ___model = ""

    def __init__(self, model="nomic-embed-text"):
        self.___model=model

    def embed(self, text: str):
        return embeddings(
            model=self.___model,
            prompt=text
        )["embedding"]

    def embed_chunks(self, chunks:list[dict], toembed:list[str]):


        embedded_chunks = []
        for i in range(len(chunks)):

            embed_chunk = VectorEntry(
                self.embed(toembed[i].lower()),
                chunks[i]
            )

            embedded_chunks.append(embed_chunk)

        return embedded_chunks