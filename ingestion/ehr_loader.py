import json
from datetime import datetime

REQUIRED_SECTIONS = ["patient_id", "demographics" ,"medical_history", "recent_visits", "lab_results"]

def load_ehr(path:str, enconding:str = "utf-8") -> dict:
    file = open(path, 'r', encoding=enconding)
    jsonfile = json.load(file)
    _validate_structure(jsonfile)
    _normalize_ehr(jsonfile)
    return jsonfile

def _validate_structure(ehr:dict):
    missing_sections = []
    for section in REQUIRED_SECTIONS:
        if section not in ehr:
            missing_sections.append(section)
    if len(missing_sections) > 0:
        raise ValueError(f"The ehr needs the following sections to be acceptable :[{str.join(missing_sections)}]")
    

def _normalize_ehr(ehr:dict):
    for visit in ehr.get("recent_visits", []):
        visit["date"] = _normalize_date(visit["date"])

    for lab in ehr.get("lab_results", []):
        lab["date"] = _normalize_date(lab["date"])

def _normalize_date(date_str: str) -> str:
    return datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y-%m-%d")