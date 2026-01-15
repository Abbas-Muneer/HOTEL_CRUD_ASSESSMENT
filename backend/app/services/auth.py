from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import verify_password, create_access_token
from app.models.user import User


def authenticate_user(db: Session, username: str, password: str) -> str:
    user = (
        db.query(User)
        .filter((User.username == username) | (User.email == username))
        .first()
    )
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    token = create_access_token(subject=user.username)
    return token
