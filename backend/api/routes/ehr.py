import json

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from backend.schemas.ehr_schemas import QueryRequest
from backend.utils.utils import get_agent, get_medical_service, verify_token, pending_action
from ehr_ai_core.error.app_error import AppError
from services.agent import EHRAgent
from services.ehr_service import EHRService

router = APIRouter(prefix="/api/ehr", tags=["ehr"])

@router.get("/patients", summary="gets all patients")
def get_patients(medical_service:EHRService = Depends(get_medical_service) ,payload:dict = Depends(verify_token)):
    return medical_service.get_patients()


@router.post("/ask", summary="schedule action according the given query")
def resolve_query(data: QueryRequest, medical_service:EHRService = Depends(get_medical_service), payload:dict = Depends(verify_token)):

    if not data.query:
        raise AppError("Missing query", 400)
    
    return medical_service.create_stream_id(query = data.query, patientId = data.patientId, doctor = payload["doctor"])

    

@router.get("/stream/{id}", summary="perform streaming accion")
def perform_stream_action(id:str, medical_service:EHRService = Depends(get_medical_service), agent:EHRAgent = Depends(get_agent), payload:dict = Depends(verify_token)):

    if not id:
        raise AppError("Missing streamId", 400)

    def generator():
        try:
            data = medical_service.get_stream_id(id)
            intent = agent.classify(data["query"])
            for chunk in agent.perform_intent(data = data | intent | {"doctor": payload["doctor"]}): yield f"data: {json.dumps(chunk)}\n\n"
        except AppError as e:
            yield f"event: error\ndata: {e.message}\n\n"

        except Exception as e:
            yield f"event: error\ndata: Internal server error\n\n"
        finally:
            yield f"data: {json.dumps({'chunk':'[DONE]'})}\n\n"

    return StreamingResponse(generator(), media_type="text/event-stream")