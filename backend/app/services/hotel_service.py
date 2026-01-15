from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.hotel import Hotel
from app.schemas.hotel import HotelCreate, HotelUpdate


def get_hotel_or_404(db: Session, hotel_id: int) -> Hotel:
    hotel = db.query(Hotel).filter(Hotel.id == hotel_id).first()
    if not hotel:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hotel not found")
    return hotel


def list_hotels(db: Session) -> list[Hotel]:
    return db.query(Hotel).order_by(Hotel.created_at.desc()).all()


def create_hotel(db: Session, data: HotelCreate) -> Hotel:
    hotel = Hotel(**data.dict())
    db.add(hotel)
    db.commit()
    db.refresh(hotel)
    return hotel


def update_hotel(db: Session, hotel_id: int, data: HotelUpdate) -> Hotel:
    hotel = get_hotel_or_404(db, hotel_id)
    for field, value in data.dict(exclude_unset=True).items():
        setattr(hotel, field, value)
    db.commit()
    db.refresh(hotel)
    return hotel


def delete_hotel(db: Session, hotel_id: int) -> None:
    hotel = get_hotel_or_404(db, hotel_id)
    db.delete(hotel)
    db.commit()
