# Example: Medication Query

## Patient

[P003](../data/ehr_P003.json)

## User Query
"What medications is the patient currently taking?"

## Retrieved Context (excerpt)
- Medication list extracted from EHR
- Enriched with section hint: "medications / medicación actual"

## LLM Response (qwen3:4b via Ollama)
> Based on the medical history record, the patient is currently taking **Levodixina** (75 mcg) once daily. This information is documented in the patient's medical history.
> *Note: The appointment note from October 28, 2024, confirms the patient's thyroid function is within normal range and asymptomatic, but does not list additional medications.*.


## Notes
- Response generated using retrieved EHR context only
- No external medical knowledge was injected
