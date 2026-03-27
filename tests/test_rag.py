import json
from ehr_ai_core.retrieval.embedding import Embedder
from ehr_ai_core.retrieval.memory_vector_db import InMemoryVectorStore
from services import RagService
from unittest.mock import patch

def test_rag_search(mocker):
    
    fake_embedder = mocker.Mock()
    fake_embedder.embed.return_value = [0.216534]

    db = InMemoryVectorStore()
    rag = RagService(db, fake_embedder)

    result = rag.search("glucose")

    assert result == []

@patch("ehr_ai_core.retrieval.embedding.Client.embeddings")
def test_rag_ingestion(mock_embeddings, tmp_path, ehr_data_normalized):

    mock_embeddings.return_value = {
        "embedding": [0.1] * 768
    }

    embbeder = Embedder()
    db = InMemoryVectorStore()

    rag = RagService(db, embbeder)

    file_path = tmp_path / "ehr.json"
    file_path.write_text(json.dumps(ehr_data_normalized), encoding="utf-8")

    rag.ingestion(str(file_path))

    assert len(rag._RagService__vectodb.entries) > 0