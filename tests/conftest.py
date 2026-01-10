# tests/conftest.py
import pytest

@pytest.fixture
def ehr_data_normalized():
    return {
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

@pytest.fixture
def ehr_minimal_data():
    return {
        "patient_id": "P001",
        "demographics": {"name": "Test"},
        "medical_history": {
            "chronic_conditions": [],
            "allergies": ["test"],
            "current_medications": []},
        "recent_visits": [{"date": "2024-08-20"}],
        "lab_results": [{"date": "2024-10-10"}]}
