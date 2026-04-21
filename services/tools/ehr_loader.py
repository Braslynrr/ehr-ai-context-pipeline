from ehr_ai_core.ingestion.ehr_loader import load_json_ehr
from services.tools.Itool import ITool


class ehr_loader(ITool):

    def __init__(self):
        super().__init__()


    def run(self, input):
        fixed_ehr = load_json_ehr(input["patient_ehr"])
        input["fixed_ehr"] = fixed_ehr