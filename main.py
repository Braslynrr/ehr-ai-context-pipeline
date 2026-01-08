from ingestion import load_ehr
from context import context_builder, ehr_chunkifier ,SimpleRetriever, embed_chunks , embed, InMemoryVectorStore, build_embedding_text_from_list
from Configuration import Config
from AIAgent import EHRAgent

if __name__ == "__main__":
    question = "¿Puedes mostrarme la informacion personal y vital del paciente?"
    question = question.lower()
    config = Config()
    agent = EHRAgent(config.llm)
    vectorDB = InMemoryVectorStore()

    ehr = load_ehr("data/ehr.json")
    chunks = ehr_chunkifier(ehr)
    texts_to_embed = build_embedding_text_from_list(chunks)
    embedded_chunks = embed_chunks(chunks, texts_to_embed)

    vectorDB.add(embedded_chunks)

    #retriever = SimpleRetriever(chunks)
    #relevantchunks = retriever.RetrieveChunks("¿Cuál es la medicación actual del paciente?")
    
    embedded_question = embed(question)
    relevant_chunks = vectorDB.search(embedded_question, k = 2)
    
    context = context_builder(relevant_chunks)


    print(agent.Predict(question, context))