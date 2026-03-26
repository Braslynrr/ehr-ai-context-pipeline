from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from backend.schemas.ehr_schemas import QueryRequest
from backend.utils.utils import get_medical_service, verify_token
from services.ehr_service import EHRService

router = APIRouter(prefix="/api/ehr", tags=["ehr"])

@router.get("/patients", summary="gets all patients")
def get_patients(medical_service:EHRService = Depends(get_medical_service) ,payload:dict = Depends(verify_token)):
    return medical_service.get_Patients()


@router.post("/ask/stream", summary="")
def resolve_query(data: QueryRequest, medical_service:EHRService = Depends(get_medical_service), payload:dict = Depends(verify_token)):

    def generator():
        for chunk in medical_service.stream_answer_clinical_question(data.query):
            yield chunk

    return StreamingResponse(generator(), media_type="text/event-stream")