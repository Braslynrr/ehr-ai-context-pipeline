SEMANTIC_HINTS = {
    "current_medications": {
        "es": "medicacion farmacos medicinas",
        "en": "medications drugs medicine"
    },
    "allergies": {
        "es": "alergias",
        "en": "allergies"
    },
    "lab_result": {
        "es": "resultados de laboratorio, analisis clinicos",
        "en": "laboratory results"
    },
    "demographics": {
        "es": "informacion demografica edad nombre sangre pacient genero general",
        "en": "patient demographic information age name blood gender general"
    },
    "chronic_conditions": {
        "es": "condiciones cronicas, padecimientos , enfermedades",
        "en": "chronic conditions, diseases"
    },
    "recent_visit": {
        "es": "visita reciente",
        "en": "recent visit"
    },
}

KEYS = ["content", "date", "source" , "type"]

def get_chunk_type(chunk: dict) -> str | None:
    return chunk.get("type") or chunk.get("section")

def build_enriched_text(chunk: dict) -> str:
    chunk_type = get_chunk_type(chunk)
    hint = SEMANTIC_HINTS.get(chunk_type, {})

    semantic_text = "\n".join([
        hint.get("es", ""),
        hint.get("en", "")
    ]).strip()

    relevantcontent = "" 
    for c in chunk:
        if c in KEYS:
            relevantcontent+= f"{c}: {__join_object(chunk[c])}\n"

    return f"""
{semantic_text}
{relevantcontent}
""".strip()

def enrich_text_from_list(chunks:list[dict]) -> list[str]:
    result = []
    for chunk in chunks:
        result.append(build_enriched_text(chunk))
    return result

def __join_object(obj):
    if isinstance(obj,dict):
        content = "\n"
        for key,val in obj.items():
            val_content = __join_object(val)
            content += f"{key}: {val_content}\n"
        return content
    elif isinstance(obj, list):
        return ", ".join(__join_object(item) for item in obj)
    else:
        return str(obj)
