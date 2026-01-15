from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserRead(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
