from services.ehr_service import EHRService
from services.tools.Itool import ITool


class ehr_patient(ITool):
    ehr:EHRService

    def __init__(self, ehr:EHRService):
        self.ehr = ehr
        self.name = "ehr_patient"
        self.description = "gets patients general information"

    def run(self, input):
        return self.ehr.get_patients(input["patients"])