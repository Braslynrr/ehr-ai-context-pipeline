from pydantic import BaseModel

class QueryRequest(BaseModel):
    query: str
    patientId: str | None = None