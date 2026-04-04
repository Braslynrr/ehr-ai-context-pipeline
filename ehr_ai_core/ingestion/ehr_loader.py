import json
from datetime import datetime
import unicodedata

REQUIRED_SECTIONS = ["patient_id", "demographics" ,"medical_history", "recent_visits", "lab_results"]

def load_ehr(path:str, enconding:str = "utf-8") -> dict:
    file = open(path, 'r', encoding=enconding)
    jsonfile = json.load(file)
    _validate_structure(jsonfile)
    _normalize_ehr(jsonfile)
    jsonfile = _normalize_any(jsonfile)
    return jsonfile

def _validate_structure(ehr:dict):
    missing_sections = []
    for section in REQUIRED_SECTIONS:
        if section not in ehr:
            missing_sections.append(section)
    if len(missing_sections) > 0:
        raise ValueError(f"The ehr needs the following sections to be acceptable: [{', '.join(missing_sections)}]")
    

def _normalize_any(data):
    if isinstance(data, dict):
        return {
            _normalizing_text(k): _normalize_any(v)
            for k, v in data.items()
        }
    elif isinstance(data, list):
        return [_normalize_any(x) for x in data]
    elif isinstance(data, str):
        return _normalizing_text(data)
    else:
        return data
    
    

def _normalizing_text(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", text)
    no_accents = "".join(c for c in normalized if not unicodedata.combining(c))
    return no_accents.lower()


def _normalize_ehr(ehr:dict):
    
    ehr["recent_visits"] = ehr.get("recent_visits", [])
    for visit in ehr["recent_visits"]:
        visit.setdefault("reason", "Unknown")
        visit.setdefault("notes", "")
        visit.setdefault("doctor", "Unknown")
        visit["date"] = _normalize_date(visit["date"])

    ehr["lab_results"] = ehr.get("lab_results", [])
    for lab in ehr["lab_results"]:
        lab.setdefault("test", "Unknown test")
        lab.setdefault("results", {})
        lab["date"] = _normalize_date(lab["date"])


_SUPPORTED_DATE_FORMATS = (
    "%d-%m-%Y",  # 10-12-2024
    "%Y-%m-%d",  # 2024-12-10
    "%m-%d-%Y",  # 12-10-2024
    "%d-%Y-%m"   # 10-2024-12
)

def _normalize_date(date_str: str) -> str:
    for fmt in _SUPPORTED_DATE_FORMATS:
        try:
            return datetime.strptime(date_str, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue

    raise ValueError(f"Unsupported date format: {date_str}")
