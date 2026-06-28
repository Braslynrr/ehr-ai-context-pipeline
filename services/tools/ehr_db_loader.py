from services.rag_service import RagService
from services.tools.Itool import ITool


class ehr_db_loader(ITool):
    rag:RagService

    def __init__(self, rag:RagService):
        self.rag = rag
        self.name = "ehr_db_loader"
        self.description = ""

    def run(self, input):
        chunks = self.rag.get_patient_chunks(input["patientId"])
        demograph_info = self.rag.get_patients([input["patientId"]]).pop()

        user_demograph = {"type": "demographics",
         "content": { 
            "name": demograph_info.get('name', "unknown"),
            "age": demograph_info.get('age', 0),
            "gender": demograph_info.get('gender', "?"),
            "blood_type": demograph_info.get('blood_type', "?")
            },
         "source": f"Patient EHR - {input['patientId']}"
        }
        
        chunks.append(user_demograph)

        input["ehr_json"] = chunks
        return chunks