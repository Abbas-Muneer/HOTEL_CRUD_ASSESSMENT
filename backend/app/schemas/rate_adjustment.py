from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field, validator


class RateAdjustmentBase(BaseModel):
    effective_date: date
    adjustment_amount: Decimal
    reason: str = Field(..., min_length=1)

    @validator("reason")
    def validate_reason(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("reason must not be empty")
        return v


class RateAdjustmentCreate(RateAdjustmentBase):
    pass


class RateAdjustmentRead(RateAdjustmentBase):
    id: int
    room_type_id: int
    created_at: datetime

    class Config:
        orm_mode = True
        json_encoders = {Decimal: lambda v: float(v)}
