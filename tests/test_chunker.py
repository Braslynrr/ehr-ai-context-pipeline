from chunkers import ehr_json_chunkifier

EHR_DATA_NORMALIZED = {
    "patient_id": "P001",

    "demographics": {
        "name": "Test",
        "age": "0",
        "gender": "Male",
        "blood_type": "A+"
    },

    "medical_history": {
        "chronic_conditions": ["test"],
        "allergies": ["test"],
        "current_medications": [{"name": "test", "dose": "0mg", "frequency": "0x/día"}]
    },

    "recent_visits": [
        {
            "date": "2024-08-20",
            "reason": "test",
            "notes": "test",
            "doctor": "test"
        }
    ],

    "lab_results": [
        {
            "date": "2024-10-10",
            "test": "Unknown test",
            "results": {
                "test": "0mg"
            }
        }
    ]
}


def test_ehr_json_chunkifier_success():
    chunks = ehr_json_chunkifier(EHR_DATA_NORMALIZED)
    assert len(chunks) == 6

def test_chunk_types_present():
    chunks = ehr_json_chunkifier(EHR_DATA_NORMALIZED)
    types = {c["type"] for c in chunks}

    assert "recent_visit" in types
    assert "lab_result" in types
    assert "demographics" in types
    assert "chronic_conditions" in types
    assert "allergies" in types
    assert "current_medications" in types


def test_chunks_have_required_fields():
    chunks = ehr_json_chunkifier(EHR_DATA_NORMALIZED)

    for chunk in chunks:
        assert "type" in chunk
        assert "content" in chunk
        assert "source" in chunk

def test_chunk_content_is_string_or_dict():
    chunks = ehr_json_chunkifier(EHR_DATA_NORMALIZED)

    for chunk in chunks:
        assert isinstance(chunk["content"], (str, dict, list))


def test_recent_visit_chunk_contains_reason():
    chunks = ehr_json_chunkifier(EHR_DATA_NORMALIZED)

    visit_chunk = next(c for c in chunks if c["type"] == "recent_visit")
    assert "Reason" in visit_chunk["content"]