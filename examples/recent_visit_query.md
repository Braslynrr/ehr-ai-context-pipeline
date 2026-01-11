# Example: recent visit Query

## Patient

[P002](../data/ehr_P002.json)

## User Query
"When was the patient’s last visit, and what was the reason?"

## Retrieved Context (excerpt)
- Recent visits list extracted from EHR
- Enriched with section hint: "visita reciente / recent visit"

## LLM Response (qwen3:4b via Ollama)
> Based on the patient's electronic health record, the last visit was on **November 2, 2024**, with Dr. Ramírez for **respiratory control** (as documented in the appointment record). 
> This information is derived directly from the most recent appointment entry in the provided context..


## Notes
- Response generated using retrieved EHR context only
- No external medical knowledge was injected
