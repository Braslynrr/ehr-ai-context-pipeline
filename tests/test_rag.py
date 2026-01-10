import json
from ehr_ai_core.services import RagService
from unittest.mock import patch

def test_rag_search(mocker):
    
    fake_embedder = mocker.Mock()
    fake_embedder.embed_chunks.return_value = [0.216534]

    rag = RagService()
    rag._RagService__embedder = fake_embedder

    result = rag.search("glucose")

    assert result is not None

@patch("ehr_ai_core.retrieval.embedding.embeddings")
def test_rag_ingestion(mock_embeddings, tmp_path, ehr_data_normalized):
    mock_embeddings.return_value = {
        "embedding": [0.1] * 768
    }

    rag = RagService()

    file_path = tmp_path / "ehr.json"
    file_path.write_text(json.dumps(ehr_data_normalized), encoding="utf-8")

    rag.ingestion(str(file_path))

    assert len(rag._RagService__vectodb.entries) > 0