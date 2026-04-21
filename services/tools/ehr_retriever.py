from services.ehr_service import EHRService
from services.tools.Itool import ITool


class ehr_retriever(ITool):
    ehr:EHRService

    def __init__(self, ehr:EHRService):
        self.ehr = ehr
        self.name = "ehr_retriever"
        self.description = "retrieves chunks from DB"

    def run(self, input):
        return self.ehr.get_chunks(input["query"], input["patientId"])