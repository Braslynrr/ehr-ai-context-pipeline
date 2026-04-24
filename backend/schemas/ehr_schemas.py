from pydantic import BaseModel

class QueryRequest(BaseModel):
    query: str
    patientId: str | None = None
    action_id:str | None = None