
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response

from backend.configuration.configuration import Config
from backend.schemas.auth_schemas import LoginRequest
from backend.utils.utils import create_token, verify_token, get_config

router = APIRouter(prefix="/api/auth", tags=["Auth"])

@router.post("/login", summary="Logs in a doctor adding access tokens by cockies")
def login(data: LoginRequest, response:Response, config: Annotated[Config, Depends(get_config)]):
    doctor_name = data.doctor

    if not doctor_name:
        raise HTTPException(status_code=400, detail="Doctor name required")

    token = create_token(doctor_name, config)

    response.set_cookie(
    key="access_token",
    value=token,
    httponly=True,
    secure=True,
    samesite=config.same_site)

    return {"message": "Login successful"}

@router.post("/logout", summary="Logs out a doctor removing credentials")
def logout(response:Response, payload:dict = Depends(verify_token)):
    response.delete_cookie("access_token")
    return {"message": "Logged out"}

@router.get("/me", summary="get authentication status")
def isAuthenticated(payload:dict = Depends(verify_token)):
    return payload
