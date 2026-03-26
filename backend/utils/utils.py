from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, HTTPException, Request
from jose import jwt, JWTError

from backend.configuration.configuration import Config
from services.ehr_service import EHRService


def get_medical_service(request: Request) -> EHRService:
    return request.app.state.medical_service

def get_config(request: Request) -> Config:
    return request.app.state.config

def create_token(doctor: str, config:Config):
    payload = {
        "doctor": doctor,
        "exp": datetime.now(timezone.utc) + timedelta(hours=8)
    }
    return jwt.encode(payload, config.JWT_SECRET_KEY, algorithm=config.JWT_ALGORITHM)

def verify_token(request: Request, config: Annotated[Config, Depends(get_config)]):
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(status_code=401, detail="login required")
    try:
        payload = jwt.decode(token, config.JWT_SECRET_KEY, algorithms=[config.JWT_ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    