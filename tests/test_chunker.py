from ehr_ai_core.chunkers import ehr_json_chunkifier


def test_ehr_json_chunkifier_success(ehr_data_normalized):
    chunks = ehr_json_chunkifier(ehr_data_normalized)
    assert len(chunks) == 6

def test_chunk_types_present(ehr_data_normalized):
    chunks = ehr_json_chunkifier(ehr_data_normalized)
    types = {c["type"] for c in chunks}

    assert "recent_visit" in types
    assert "lab_result" in types
    assert "demographics" in types
    assert "chronic_conditions" in types
    assert "allergies" in types
    assert "current_medications" in types


def test_chunks_have_required_fields(ehr_data_normalized):
    chunks = ehr_json_chunkifier(ehr_data_normalized)

    for chunk in chunks:
        assert "type" in chunk
        assert "content" in chunk
        assert "source" in chunk

def test_chunk_content_is_string_or_dict(ehr_data_normalized):
    chunks = ehr_json_chunkifier(ehr_data_normalized)

    for chunk in chunks:
        assert isinstance(chunk["content"], (str, dict, list))


def test_recent_visit_chunk_contains_reason(ehr_data_normalized):
    chunks = ehr_json_chunkifier(ehr_data_normalized)

    visit_chunk = next(c for c in chunks if c["type"] == "recent_visit")
    assert "Reason" in visit_chunk["content"]