import numpy as np

from ehr_ai_core.retrieval.IVector_db import IVector
from .vector_entry import VectorEntry

def _cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

class InMemoryVectorStore(IVector):
    def __init__(self):
        self.entries: list[VectorEntry] = []

    def add(self, entry: VectorEntry):
        self.entries.append(entry)
    
    def add(self, entry: list[VectorEntry]):
        self.entries.extend(entry)

    def clean(self):
        self.entries = []

    def search(self, query_embedding, k=2, patient_id: str | None = None) -> dict:
        scored = [
            (_cosine_similarity(query_embedding, e.embedding), e)
            for e in self.entries
        ]
        scored.sort(key=lambda x: x[0], reverse=True)
        return [e.payload for _, e in scored[:k]]
    
    def get_patients(self, id:str|None = None):
        patients = None
        
        if id:
            patients =filter(lambda x: x.payload["patient_id"] == id, self.entries)

        patients = map(lambda x:x.payload["demographics"] ,self.entries)
        
        return list(patients)