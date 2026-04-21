from services.rag_service import RagService
from services.tools.Itool import ITool


class ehr_json_ingestion(ITool):
    rag:RagService

    def __init__(self, rag:RagService):
        self.rag = rag
        self.name = "ehr_json_ingestion"
        self.description = ""

    def run(self, input):
        self.rag.json_ingestion(chunks=input["chunks"], patientId=input["patientId"])