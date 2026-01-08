SEMANTIC_HINTS = {
    "current_medications": {
        "es": "medicación actual del paciente, fármacos en uso",
        "en": "current medications, drugs patient is taking"
    },
    "allergies": {
        "es": "alergias conocidas del paciente",
        "en": "known allergies"
    },
    "lab_result": {
        "es": "resultados de laboratorio, análisis clínicos",
        "en": "laboratory results"
    },
    "demographics": {
        "es": "informacion demografica del paciente",
        "en": "patient demographic information"
    },
    "chronic_conditions": {
        "es": "condiciones cronicas",
        "en": "chronic conditions"
    },
    "recent_visit": {
        "es": "visita reciente",
        "en": "recent visit"
    },
}

KEYS = ["content", "date", "source" , "type"]

def get_chunk_type(chunk: dict) -> str | None:
    return chunk.get("type") or chunk.get("section")

def build_embedding_text(chunk: dict) -> str:
    chunk_type = get_chunk_type(chunk)
    hint = SEMANTIC_HINTS.get(chunk_type, {})

    semantic_text = "\n".join([
        hint.get("es", ""),
        hint.get("en", "")
    ]).strip()

    relevantcontent = "" 
    for c in chunk:
        if c in KEYS:
            relevantcontent+= f"{c}: {chunk[c]}\n"

    return f"""
{semantic_text}
{relevantcontent}
""".strip()

def build_embedding_text_from_list(chunks:list[dict]) -> list[str]:
    result = []
    for chunk in chunks:
        result.append(build_embedding_text(chunk))
    return result