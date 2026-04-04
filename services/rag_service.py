import numpy as np

from ehr_ai_core.context.context_builder import join_object
from ehr_ai_core.ingestion import load_ehr
from ehr_ai_core.ingestion.ehr_loader import _normalizing_text
from ehr_ai_core.retrieval import Embedder, enrich_text_from_list
from ehr_ai_core.chunkers import ehr_json_chunkifier
from ehr_ai_core.retrieval.IVector_db import IVector
from sentence_transformers import CrossEncoder

# This service intentionally separates retrieval from generation
# to keep the system modular and testable.
class RagService:
    """
        Handles EHR ingestion, embedding, and retrieval using an in-memory vector store.
    """
    __vectordb:IVector
    __embedder: Embedder
    __reranker:CrossEncoder

    def __init__(self, db:IVector, embedder:Embedder, reranker=None):
        self.__vectordb = db
        self.__embedder = embedder
        self.__reranker = reranker or CrossEncoder(
            'cross-encoder/mmarco-mMiniLMv2-L12-H384-v1'
        )

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
        self.__vectordb.add(embedded_chunks)
    
    def normalize(arr):
        arr = np.array(arr)
        return (arr - arr.min()) / (arr.max() - arr.min() + 1e-8)

    def search(self, query: str, patientId: str | None = None):

        normalized_query = _normalizing_text(query)

        embedded_question = self.__embedder.embed(normalized_query)

        chunks_count = self.__vectordb.chunks_count(patient_id=patientId)

        k = min(30, chunks_count)
        chunks = self.__vectordb.search(embedded_question, k=k, patient_id=patientId)

        pairs = [[query, join_object(doc['content'])] for doc in chunks]

        if(len(pairs) > 0):

            scores = self.__reranker.predict(pairs)

            ranked_indices = np.argsort(-scores)

            reranked_docs = [chunks[i] for i in ranked_indices]
            reranked_scores = [scores[i] for i in ranked_indices]

            for doc, score in zip(reranked_docs, reranked_scores):
                doc['reranker_score'] = score

            # Normalize scores
            sim_scores = np.array([doc["similarity"] for doc in reranked_docs])
            rerank_scores = np.array(reranked_scores)

            sim_scores = (sim_scores - sim_scores.min()) / (sim_scores.max() - sim_scores.min() + 1e-8)
            rerank_scores = (rerank_scores - rerank_scores.min()) / (rerank_scores.max() - rerank_scores.min() + 1e-8)

            for i, doc in enumerate(reranked_docs):
                doc["final_score"] = 0.5 * sim_scores[i] + 0.5 * rerank_scores[i]

            reranked_docs.sort(key=lambda doc: doc["final_score"], reverse=True)

            topk = max(1, min(5, int(chunks_count*0.33)))

            return reranked_docs[:topk]
        
        return []
    
    def get_patients(self, id_list:list[str]|None= None):
        return self.__vectordb.get_patients(id_list=id_list)
    
    def chunks_count(self, patient_id: str|None = None):
        return self.__vectordb.chunks_count(patient_id=patient_id)