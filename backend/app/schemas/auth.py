from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    username: str = Field(..., example="admin@hotel.local")
    password: str = Field(..., example="Admin@123")


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
