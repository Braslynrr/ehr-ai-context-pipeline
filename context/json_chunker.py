import os
from .vector_entry import VectorEntry
from .embedding import embed
from .context_builder import context_builder

def ehr_chunkifier(ehr:dict) -> list:
    chunks = []
    chunks.append(
            {
             "type":"demographics",   
             "content": ehr.get("demographics",[]), 
             "source": f"Patient EHR - {ehr.get("patient_id",[])}"
            })
    
    medical_history = ehr.get("medical_history",[])
    for med in medical_history:
        chunks.append(
            {
                "type": med,
                "content": medical_history[med],
                "source": "medical_history"
            }
        )

    recent_visits = ehr.get("recent_visits", [])
    for visit in recent_visits:
        chunks.append(
            {
                "type":"recent_visit",
                "content" : f"Reason: {visit["reason"]} {os.linesep}Notes: {visit["notes"]}",
                "date": visit["date"],
                "doctor": visit["doctor"],
                "source": f"Appointment ({visit["date"]}) with {visit["doctor"]}"
            }
        )


    lab_results = ehr.get("lab_results")

    for lab in lab_results:
        chunks.append(
            {
                "type":"lab_result",
                "content" : {"test": lab["test"] , "results": lab["results"] },
                "date": visit["date"],
                "source": f"Laboratory result on {visit["date"]}"
            }
        )

    return chunks
    

def embed_chunks(chunks:list[dict], toembed:list[str]):


    embedded_chunks = []
    for i in range(len(chunks)):

        embed_chunk = VectorEntry(
            embed(toembed[i].lower()),
            chunks[i]
        )

        embedded_chunks.append(embed_chunk)

    return embedded_chunks