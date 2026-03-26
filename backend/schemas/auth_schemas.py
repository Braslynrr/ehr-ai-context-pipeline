from pydantic import BaseModel

class LoginRequest(BaseModel):
    doctor: str