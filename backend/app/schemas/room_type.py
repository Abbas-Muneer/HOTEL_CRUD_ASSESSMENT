from datetime import datetime, date
from decimal import Decimal
from typing import Optional, List

from pydantic import BaseModel, Field, validator


class RoomTypeBase(BaseModel):
    name: str = Field(..., min_length=1)
    description: Optional[str] = None
    base_rate: Decimal = Field(..., ge=0)

    @validator("base_rate")
    def validate_base_rate(cls, v: Decimal) -> Decimal:
        if v < 0:
            raise ValueError("base_rate must be non-negative")
        return v


class RoomTypeCreate(RoomTypeBase):
    pass


class RoomTypeUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    base_rate: Optional[Decimal] = Field(None, ge=0)


class RoomTypeRead(RoomTypeBase):
    id: int
    hotel_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
        json_encoders = {Decimal: lambda v: float(v)}


class EffectiveRateResponse(BaseModel):
    room_type_id: int
    date: date
    base_rate: Decimal
    adjustment_amount: Decimal
    effective_date: Optional[date]
    effective_rate: Decimal
    adjustment_id: Optional[int]

    class Config:
        json_encoders = {Decimal: lambda v: float(v)}
