from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, get_db
from app.schemas.hotel import HotelCreate, HotelRead, HotelUpdate, HotelWithRoomTypes
from app.services import hotel_service, room_type_service

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.get("", response_model=list[HotelRead])
def list_hotels(db: Session = Depends(get_db)):
    return hotel_service.list_hotels(db)


@router.post("", response_model=HotelRead, status_code=201)
def create_hotel(payload: HotelCreate, db: Session = Depends(get_db)):
    return hotel_service.create_hotel(db, payload)


@router.get("/{hotel_id}", response_model=HotelWithRoomTypes)
def get_hotel(hotel_id: int, db: Session = Depends(get_db)):
    hotel = hotel_service.get_hotel_or_404(db, hotel_id)
    room_types = room_type_service.list_room_types_for_hotel(db, hotel)
    return {**HotelRead.from_orm(hotel).dict(), "room_types": room_types}


@router.put("/{hotel_id}", response_model=HotelRead)
def update_hotel(hotel_id: int, payload: HotelUpdate, db: Session = Depends(get_db)):
    return hotel_service.update_hotel(db, hotel_id, payload)


@router.delete("/{hotel_id}", status_code=204)
def delete_hotel(hotel_id: int, db: Session = Depends(get_db)):
    hotel_service.delete_hotel(db, hotel_id)
    return None
