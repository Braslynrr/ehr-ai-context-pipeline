from ehr_ai_core.ingestion import load_ehr
from ehr_ai_core.retrieval import Embedder, enrich_text_from_list
from ehr_ai_core.chunkers import ehr_json_chunkifier
from ehr_ai_core.retrieval.IVector_db import IVector

# This service intentionally separates retrieval from generation
# to keep the system modular and testable.
class RagService:
    """
        Handles EHR ingestion, embedding, and retrieval using an in-memory vector store.
    """
    __vectodb:IVector
    __embedder: Embedder

    def __init__(self, db:IVector, embbeder:Embedder):
        self.__vectodb = db
        self.__embedder = embbeder
        
    def ingestion(self, filepath:str):
        """
        Loads EHR files, chunks the data, generates embeddings, and stores them in memory.
        """
        # loading ehr
        file = load_ehr(filepath)
        # chunking ehr
        patient_id = file["patient_id"]
        chunks = ehr_json_chunkifier(file)

        for i in range(len(chunks)):
            chunks[i]["patient_id"] = patient_id
            chunks[i]["chunk_id"] = f"{patient_id}-{i}"

        self.__index_chunks(chunks)

    def __index_chunks(self, chunks:list):
        # semeantic enrichment
        enriched_text = enrich_text_from_list(chunks)
        # embedding texts
        embedded_chunks = self.__embedder.embed_chunks(chunks, enriched_text)

        # adding embedding to the DB
        self.__vectodb.add(embedded_chunks)
        

    def search(self, question:str, patientId:str | None = None):
        embedded_question = self.__embedder.embed(question)
        return self.__vectodb.search(embedded_question, patient_id=patientId)
    
    def get_patients(self):
        return self.__vectodb.get_patients()