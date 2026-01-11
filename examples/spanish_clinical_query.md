# Example: Clinical Query in Spanish

This example demonstrates that the pipeline supports multilingual
EHR content and user queries without any language-specific logic.

## Paciente

[P001](../data/ehr_P001.json)

## Consulta del usuario

"¿Cómo ha evolucionado su glucosa?"


## Contexto Recuperado (extractos)

- Recuperó resultados del laboratorio y una visita reciente del paciente
- Enriquecido con las secciones: "Resultados de laboratorio / laboratory results" y "última visita / recent visit"
- La palabra glucosa jugó un papel importante en la recuperación.


## Respuesta del LLM (qwen3:4b via Ollama)

> La glucosa ha evolucionado de manera estable en los últimos días. Según los registros clínicos: - El **10 de octubre de 2024**, en un panel metabólico, el valor de glucosa fue de **128 mg/dL**. - El **15 de octubre de 2024**, en una consulta rutinaria con Dra. Martínez, la glucosa en ayunas también fue de **128 mg/dL**. 
> Por lo tanto, no ha habido variación significativa en los últimos 5 días. *Referencia: Datos obtenidos de la consulta del 15/10/2024 y el panel metabólico del 10/10/2024.*.

## Notes
- La respuesta se generó usando unicamente el contexto recuperado del EHR
- No hubo inyección de conocimiento medico externo
- The same ingestion, chunking, and retrieval pipeline is used regardless of language
