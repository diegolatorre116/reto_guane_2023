from typing import Any
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app import schemas
from app.core.auth.auth import authenticate_user
from app.core.security.token import create_access_token
from app.config import settings


security_router = APIRouter()


@security_router.post("/", response_model=schemas.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    user = await authenticate_user(
        form_data.username,
        form_data.password
    )
    if not user:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Incorrect username or password" 
        )
    access_token_expires = timedelta(
        minutes=int(settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta= access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
