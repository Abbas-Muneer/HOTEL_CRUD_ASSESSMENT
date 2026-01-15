from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.schemas.auth import LoginRequest, Token
from app.services.auth import authenticate_user

router = APIRouter()


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # OAuth2PasswordRequestForm uses fields "username" and "password"
    token = authenticate_user(db, form_data.username, form_data.password)
    return {"access_token": token, "token_type": "bearer"}
