from Services import RagService, MedicalService
from AIAgent import EHRAgent
from Configuration import Config
from API import create_app


config:Config = Config()
rag = RagService()

agent = EHRAgent(config.llm)
medical_service = MedicalService(rag, agent)

app = create_app(medical_service, config)
app.run(debug=True)