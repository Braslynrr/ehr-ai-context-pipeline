from ehr_ai_core.aiagent import EHRAgent
from ehr_ai_core.context import context_builder
from ehr_ai_core.redis.redis import RedisManager
from .rag_service import RagService

class EHRService:
    '''
    Handles the entire process of ingestion, retrieving and dynamically responses
    '''
    lastfile = ""
    rag:RagService
    agent: EHRAgent
    redis: RedisManager

    def __init__(self, rag: RagService, agent:EHRAgent):
        self.rag = rag
        self.agent = agent
        self.redis = RedisManager()

    def answer_clinical_question(self, question:str) -> str:
        relevant_chunks = self.rag.search(question)

        context = context_builder(relevant_chunks)
        
        answer =  self.agent.Predict(question, context) 
        return answer
    
    def get_stream_id(self, question:str, patientId:str | None = None):
        streamId = self.redis.save_data({"question":question, "patientId":patientId})
        return streamId

    def stream_answer_clinical_question(self, streamId:str, doctor:str):
        data = self.redis.get_by_id(streamId)
        context = f"[Query owner: {doctor}]\n"

        question = data["question"]
        patientId = data["patientId"]

        if patientId:
            patient = self.rag.get_patient(patientId)
            context += f"Patient: {patient.get('name', 'unkwnown')}\n"
        else:
            context = "[General Query]"

        relevant_chunks = self.rag.search(question, patientId)
        context += context_builder(relevant_chunks)

        for chunk in self.agent.Streaming_Prediction(question, context):
            yield {"chunk": chunk}


    def get_Patients(self):
        patients = self.rag.get_patients()
        return patients