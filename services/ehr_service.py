from ehr_ai_core.aiagent import EHRAgent
from ehr_ai_core.context import context_builder
from .rag_service import RagService

class EHRService:
    '''
    Handles the entire process of ingestion, retrieving and dynamically responses
    '''
    lastfile = ""
    rag:RagService
    agent: EHRAgent

    def __init__(self, rag: RagService, agent:EHRAgent):
        self.rag = rag
        self.agent = agent

    def answer_clinical_question(self, question:str) -> str:
        relevant_chunks = self.rag.search(question)

        context = context_builder(relevant_chunks)
        
        answer =  self.agent.Predict(question, context) 
        return answer
    

    def stream_answer_clinical_question(self, question:str, patientId:str | None = None):
        relevant_chunks = self.rag.search(question, patientId)
        context = context_builder(relevant_chunks)

        for chunk in self.agent.Streaming_Prediction(question, context):
            yield chunk


    def get_Patients(self):
        patients = self.rag.get_patients()
        return patients