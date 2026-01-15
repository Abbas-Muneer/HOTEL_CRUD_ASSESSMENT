from datetime import date as date_cls

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, get_db
from app.schemas.room_type import (
    EffectiveRateResponse,
    RoomTypeCreate,
    RoomTypeRead,
    RoomTypeUpdate,
)
from app.schemas.hotel import RoomTypeEffective
from app.services import hotel_service, room_type_service, rate_adjustment_service

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.post("/hotels/{hotel_id}/room-types", response_model=RoomTypeRead, status_code=201)
def create_room_type(hotel_id: int, payload: RoomTypeCreate, db: Session = Depends(get_db)):
    hotel = hotel_service.get_hotel_or_404(db, hotel_id)
    return room_type_service.create_room_type(db, hotel, payload)


@router.get("/hotels/{hotel_id}/room-types", response_model=list[RoomTypeEffective])
def list_room_types(hotel_id: int, db: Session = Depends(get_db)):
    hotel = hotel_service.get_hotel_or_404(db, hotel_id)
    items = room_type_service.list_room_types_for_hotel(db, hotel)
    return items


@router.get("/room-types/{room_type_id}", response_model=RoomTypeRead)
def get_room_type(room_type_id: int, db: Session = Depends(get_db)):
    room_type = room_type_service.get_room_type_or_404(db, room_type_id)
    return room_type


@router.put("/room-types/{room_type_id}", response_model=RoomTypeRead)
def update_room_type(
    room_type_id: int, payload: RoomTypeUpdate, db: Session = Depends(get_db)
):
    return room_type_service.update_room_type(db, room_type_id, payload)


@router.delete("/room-types/{room_type_id}", status_code=204)
def delete_room_type(room_type_id: int, db: Session = Depends(get_db)):
    room_type_service.delete_room_type(db, room_type_id)
    return None


@router.get("/room-types/{room_type_id}/effective-rate", response_model=EffectiveRateResponse)
def get_effective_rate(
    room_type_id: int,
    date: date_cls = Query(default_factory=date_cls.today),
    db: Session = Depends(get_db),
):
    room_type = room_type_service.get_room_type_or_404(db, room_type_id)
    computation = rate_adjustment_service.compute_effective_rate(db, room_type, date)
    latest = computation["latest_adjustment"]
    return EffectiveRateResponse(
        room_type_id=room_type.id,
        date=date,
        base_rate=room_type.base_rate,
        adjustment_amount=computation["adjustment_amount"],
        effective_date=latest.effective_date if latest else None,
        adjustment_id=latest.id if latest else None,
        effective_rate=computation["effective_rate"],
    )
