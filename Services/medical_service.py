from AIAgent import EHRAgent
from .rag_service import RagService

class MedicalService:
    '''
    Handles the entire process of ingestion, retrieving and dynamically responses
    '''

    rag:RagService
    agent: EHRAgent

    def __init__(self, rag: RagService, agent:EHRAgent):
        self.rag = rag
        self.agent = agent

    def answer(self, filepath:str , question:str) -> str:
        self.rag.ingestion(filepath)
        relevant_chunks = self.rag.search(question)
        answer = self.agent.Predict(question, relevant_chunks)
        return answer