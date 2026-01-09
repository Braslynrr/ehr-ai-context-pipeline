import json
from ehr_ai_core.services import RagService

def test_rag_search(mocker):
    
    fake_embedder = mocker.Mock()
    fake_embedder.embed_chunks.return_value = [0.216534]

    rag = RagService()
    rag._RagService__embedder = fake_embedder

    result = rag.search("glucose")

    assert result is not None

def test_rag_ingestion(tmp_path, ehr_data_normalized):

    rag = RagService()

    file_path = tmp_path / "ehr.json"
    file_path.write_text(json.dumps(ehr_data_normalized), encoding="utf-8")

    rag.ingestion(str(file_path))

    assert len(rag._RagService__vectodb.entries) > 0