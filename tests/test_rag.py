import json
from services import RagService
from .test_chunker import EHR_DATA_NORMALIZED

def test_rag_search(mocker):
    
    fake_embedder = mocker.Mock()
    fake_embedder.embed_chunks.return_value = [0.216534]

    rag = RagService()
    rag._RagService__embedder = fake_embedder

    result = rag.search("glucose")

    assert result is not None

def test_rag_ingestion(tmp_path):

    rag = RagService()

    file_path = tmp_path / "ehr.json"
    file_path.write_text(json.dumps(EHR_DATA_NORMALIZED), encoding="utf-8")

    rag.ingestion(str(file_path))

    assert len(rag.__vectodb.entries) > 0