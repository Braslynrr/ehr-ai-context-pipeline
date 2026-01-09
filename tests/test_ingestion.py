import json
import pytest
import copy
from ehr_ai_core.ingestion import load_ehr

EHR_DATA = {
        "patient_id": "P001",
        "demographics": {"name": "Test"},
        "medical_history": {
            "chronic_conditions": [],
            "allergies": ["test"],
            "current_medications": []},
        "recent_visits": [{"date": "2024-08-20"}],
        "lab_results": [{"date": "2024-10-10"}]}


def remove_section(dict:dict, name:str) -> dict:
    del dict[name]
    return dict

def test_load_ehr_success(tmp_path):
    

    file_path = tmp_path / "ehr.json"
    file_path.write_text(json.dumps(EHR_DATA), encoding="utf-8")

    result = load_ehr(str(file_path))

    assert result["patient_id"] == "P001"
    assert result["demographics"]["name"] == "Test"
    assert result["medical_history"]["allergies"][0] == "test"
    assert result["recent_visits"][0]["date"] == "2024-08-20"
    assert result["lab_results"][0]["date"] == "2024-10-10"

def test_load_ehr_missing_sections(tmp_path):
    sections = ["patient_id", "demographics" ,"medical_history", "recent_visits", "lab_results"]

    for section in sections:
        new_ehr = remove_section(copy.deepcopy(EHR_DATA), section)

        file_path = tmp_path / "ehr.json"
        file_path.write_text(json.dumps(new_ehr), encoding="utf-8")
        with pytest.raises(ValueError):
            load_ehr(str(file_path))

def test_load_ehr_is_normalizing_dates(tmp_path):
    new_ehr = copy.deepcopy(EHR_DATA)

    new_ehr["recent_visits"][0]["date"] = "10-10-2024"
    new_ehr["lab_results"][0]["date"] = "20-08-2024"

    file_path = tmp_path / "ehr.json"
    file_path.write_text(json.dumps(new_ehr), encoding="utf-8")

    result = load_ehr(str(file_path))

    assert result["recent_visits"][0]["date"] == "2024-10-10"
    assert result["lab_results"][0]["date"] == "2024-08-20"