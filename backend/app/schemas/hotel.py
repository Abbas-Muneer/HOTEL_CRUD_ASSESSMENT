from datetime import datetime, date
from typing import Optional, List
from decimal import Decimal

from pydantic import BaseModel, Field, validator


class HotelBase(BaseModel):
    name: str = Field(..., min_length=1)
    address: Optional[str] = None
    city: Optional[str] = None
    status: Optional[str] = "active"


class HotelCreate(HotelBase):
    pass


class HotelUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1)
    address: Optional[str] = None
    city: Optional[str] = None
    status: Optional[str] = None


class HotelRead(HotelBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class RoomTypeEffective(BaseModel):
    id: int
    hotel_id: int
    name: str
    description: Optional[str] = None
    base_rate: Decimal
    current_adjustment: Decimal
    current_adjustment_effective_date: Optional[date]
    current_effective_rate: Decimal
    next_adjustment: Optional[Decimal] = None
    next_adjustment_effective_date: Optional[date] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
        json_encoders = {Decimal: lambda v: float(v)}


class HotelWithRoomTypes(HotelRead):
    room_types: List[RoomTypeEffective]

    class Config:
        orm_mode = True
        json_encoders = {Decimal: lambda v: float(v)}
