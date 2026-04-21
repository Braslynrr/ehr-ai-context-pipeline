from ehr_ai_core.retrieval.vector_entry import VectorEntry
from abc import ABC,abstractmethod

class IVector(ABC):
    @abstractmethod
    def add(self, entry: VectorEntry):
        pass
    @abstractmethod
    def add(self, entries: list[VectorEntry]):
        pass
    @abstractmethod
    def clean(self):
        pass
    @abstractmethod
    def search(self, query_embedding, k=2, patient_id: str | None = None) -> list[dict]:
        pass
    @abstractmethod
    def get_patients(self, id_list:list[str] | None = None)-> list[dict]:
        pass
    @abstractmethod
    def chunks_count(self, patient_id: str| None = None):
        pass
    @abstractmethod
    def add_patient(self, patient:dict):
        pass
    def patient_chunks(self, patient:str) -> list:
        pass