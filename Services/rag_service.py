from ingestion import load_ehr
from retrieval import InMemoryVectorStore, Embedder, enrich_text_from_list
from chunkers import ehr_json_chunkifier

# This service intentionally separates retrieval from generation
# to keep the system modular and testable.
class RagService:
    """
        Handles EHR ingestion, embedding, and retrieval using an in-memory vector store.
    """
    # Using in-memory vector store for simplicity and transparency.
    __vectodb:InMemoryVectorStore
    __embedder: Embedder

    def __init__(self):
        self.__vectodb = InMemoryVectorStore()
        self.__embedder= Embedder()
        
    def ingestion(self, filepath:str):
        """
        Loads EHR files, chunks the data, generates embeddings, and stores them in memory.
        """
        # cleaning db
        self.__vectodb.clean()
        # loading ehr
        file = load_ehr(filepath)
        # chunking ehr
        chunks = ehr_json_chunkifier(file)
        self.__index_chunks(chunks)

    def __index_chunks(self, chunks:list):
        # semeantic enrichment
        enriched_text = enrich_text_from_list(chunks)
        # embedding texts
        embedded_chunks = self.__embedder.embed_chunks(chunks, enriched_text)
        # adding embedding to the DB
        self.__vectodb.add(embedded_chunks)
        

    def search(self, question:str):
        embedded_question = self.__embedder.embed(question)
        return self.__vectodb.search(embedded_question)