from datetime import date
from typing import Optional
from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.hotel import Hotel
from app.models.room_type import RoomType
from app.schemas.room_type import RoomTypeCreate, RoomTypeUpdate
from app.services.rate_adjustment_service import (
    compute_effective_rate,
    ensure_non_negative_rate,
    get_next_adjustment,
)


def get_room_type_or_404(db: Session, room_type_id: int) -> RoomType:
    room_type = db.query(RoomType).filter(RoomType.id == room_type_id).first()
    if not room_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Room type not found"
        )
    return room_type


def list_room_types_for_hotel(db: Session, hotel: Hotel, as_of: Optional[date] = None):
    as_of = as_of or date.today()
    room_types = (
        db.query(RoomType)
        .filter(RoomType.hotel_id == hotel.id)
        .order_by(RoomType.created_at.desc())
        .all()
    )
    result = []
    for rt in room_types:
        effective = compute_effective_rate(db, rt, as_of)
        latest = effective["latest_adjustment"]
        upcoming = get_next_adjustment(db, rt, as_of)
        result.append(
            {
                "id": rt.id,
                "hotel_id": rt.hotel_id,
                "name": rt.name,
                "description": rt.description,
                "base_rate": rt.base_rate,
                "created_at": rt.created_at,
                "updated_at": rt.updated_at,
                "current_adjustment": effective["adjustment_amount"],
                "current_adjustment_effective_date": latest.effective_date if latest else None,
                "current_effective_rate": effective["effective_rate"],
                "next_adjustment": upcoming.adjustment_amount if upcoming else None,
                "next_adjustment_effective_date": upcoming.effective_date if upcoming else None,
            }
        )
    return result


def create_room_type(db: Session, hotel: Hotel, payload: RoomTypeCreate) -> RoomType:
    room_type = RoomType(hotel_id=hotel.id, **payload.dict())
    db.add(room_type)
    db.commit()
    db.refresh(room_type)
    return room_type


def update_room_type(db: Session, room_type_id: int, payload: RoomTypeUpdate) -> RoomType:
    room_type = get_room_type_or_404(db, room_type_id)
    data = payload.dict(exclude_unset=True)
    if "base_rate" in data:
        new_base_rate = data["base_rate"]
        for adj in room_type.rate_adjustments:
            ensure_non_negative_rate(new_base_rate, adj.adjustment_amount)
    for field, value in payload.dict(exclude_unset=True).items():
        setattr(room_type, field, value)
    db.commit()
    db.refresh(room_type)
    return room_type


def delete_room_type(db: Session, room_type_id: int) -> None:
    room_type = get_room_type_or_404(db, room_type_id)
    db.delete(room_type)
    db.commit()
