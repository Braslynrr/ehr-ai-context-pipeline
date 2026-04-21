from ehr_ai_core.context import context_builder, join_object
from ehr_ai_core.redis.redis import RedisManager
from .rag_service import RagService

class EHRService:
    '''
    Handles the entire process of ingestion, retrieving and dynamically responses
    '''
    lastfile = ""
    rag:RagService
    redis: RedisManager

    def __init__(self, rag: RagService, redis:RedisManager):
        self.rag = rag
        self.redis = redis
    
    def create_stream_id(self, query:str, doctor:str, patientId:str | None = None):
        streamId = self.redis.save_data({"query":query, "doctor": doctor, "patientId":patientId})
        return streamId
    
    def get_stream_id(self, id:str):
        return self.redis.get_by_id(id)
    
    def get_patients(self, patients:list[str] | None= None):
        return self.rag.get_patients(patients)

    def get_chunks(self, query:str, patientId:str):
        relevant_chunks = self.rag.search(query, patientId)
        return relevant_chunks