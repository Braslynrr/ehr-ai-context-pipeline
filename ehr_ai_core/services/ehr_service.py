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

    def answer_clinical_question(self, filepath:str , question:str) -> str:
        if self.lastfile != filepath:
            self.rag.ingestion(filepath)
            self.lastfile = filepath

        # Retriever step
        relevant_chunks = self.rag.search(question)

        context = context_builder(relevant_chunks)
        
        answer = self.agent.Predict(question, context)
        return answer