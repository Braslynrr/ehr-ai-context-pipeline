import numpy as np
from .vector_entry import VectorEntry

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

class InMemoryVectorStore:
    def __init__(self):
        self.entries: list[VectorEntry] = []

    def add(self, entry: VectorEntry):
        self.entries.append(entry)
    
    def add(self, entry: list[VectorEntry]):
        self.entries.extend(entry)

    def search(self, query_embedding, k=3):
        scored = [
            (cosine_similarity(query_embedding, e.embedding), e)
            for e in self.entries
        ]
        scored.sort(key=lambda x: x[0], reverse=True)
        return [e.payload for _, e in scored[:k]]