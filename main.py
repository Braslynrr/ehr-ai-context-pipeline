from ingestion import load_ehr
from context import context_builder, ehr_chunkifier ,SimpleRetriever
from Configuration import Config
from AIAgent import EHRAgent

if __name__ == "__main__":
    
    config = Config()
    agent = EHRAgent(config.llm)

    ehr = load_ehr("data/ehr.json")
    chunks = ehr_chunkifier(ehr)
    retriever = SimpleRetriever(chunks)
    relevantchunks = retriever.RetrieveChunks("¿Cuál es la medicación actual del paciente?")
    context = context_builder(relevantchunks)


    print(agent.Predict("¿Cuál es la medicación actual del paciente?", context))